import os
import time
import re
from typing import List, Dict, Any, Callable, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Define path to look for .env file
# It can be in config/.env or project root .env
dotenv_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", ".env"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
]

# Load from first available env path
env_loaded = False
for path in dotenv_paths:
    if os.path.exists(path):
        load_dotenv(path)
        env_loaded = True
        break
if not env_loaded:
    load_dotenv()  # Fallback to default search

def get_api_key() -> str:
    """Retrieves the Gemini API Key from environment variables."""
    return os.environ.get("GEMINI_API_KEY", "")

def get_model_name() -> str:
    """Retrieves the default model name from environment variables."""
    return os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

def configure_gemini() -> bool:
    """
    Configures the google-generativeai library with the API key.
    Returns True if successfully configured, False otherwise.
    """
    api_key = get_api_key()
    if not api_key or api_key == "your_gemini_api_key_here":
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False

def call_gemini_with_retry(
    model: genai.GenerativeModel,
    prompt: str,
    max_retries: int = 5,
    initial_delay: float = 12.0,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
    current_step: int = 0,
    total_steps: int = 1,
    progress_status_prefix: str = ""
) -> str:
    """
    Calls the Gemini API generate_content method, wrapping it with an auto-retry loop
    and backoff mechanism when encountering ResourceExhausted (429) rate limit errors.
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                # Add a brief, safe 2-second sleep between queries to help pace requests
                # under the 5 RPM limit
                time.sleep(2)
                return response.text.strip()
            raise Exception("Received empty response from Gemini API.")
            
        except Exception as e:
            err_msg = str(e)
            is_rate_limit = (
                "429" in err_msg or 
                "quota" in err_msg.lower() or 
                "resourceexhausted" in err_msg.lower() or 
                "limit" in err_msg.lower()
            )
            
            if is_rate_limit and attempt < max_retries - 1:
                # Determine how long we should sleep
                sleep_time = delay
                # Extract specific retry duration if provided in error message
                # Example: "Please retry in 48.949520988s."
                seconds_match = re.search(r'retry in ([\d\.]+)s', err_msg)
                if seconds_match:
                    try:
                        sleep_time = float(seconds_match.group(1)) + 2.0
                    except Exception:
                        pass
                
                # Cap the minimum sleep time to 15 seconds to ensure we clear the RPM window
                sleep_time = max(sleep_time, 15.0)
                
                # Report cooling down to the UI
                if progress_callback:
                    # Keep counting down live so user knows the app is active
                    for remaining in range(int(sleep_time), 0, -5):
                        progress_callback(
                            current_step,
                            total_steps,
                            f"{progress_status_prefix} ⚠️ Rate limit hit! Cooling down for {remaining}s..."
                        )
                        time.sleep(min(remaining, 5))
                else:
                    time.sleep(sleep_time)
                
                # Double the backoff delay for the next attempt
                delay *= 2
            else:
                # If it's a non-rate-limit error or max retries reached, propagate it
                raise e
                
    raise Exception("Max retries reached without a successful API response.")

def verify_api_connection() -> Dict[str, Any]:
    """
    Verifies connection to Gemini API by sending a tiny test prompt.
    Used for Day 4 validation.
    """
    if not configure_gemini():
        return {
            "success": False,
            "error": "Gemini API key is not configured. Please add it to your config/.env file."
        }
    
    try:
        model_name = get_model_name()
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Ping. Reply with 'Pong' only.")
        if response and response.text:
            return {
                "success": True,
                "response": response.text.strip(),
                "model_used": model_name
            }
        else:
            return {
                "success": False,
                "error": "Received empty response from Gemini API."
            }
    except Exception as e:
        try:
            fallback_model = "gemini-1.5-flash"
            model = genai.GenerativeModel(fallback_model)
            response = model.generate_content("Ping. Reply with 'Pong' only.")
            if response and response.text:
                return {
                    "success": True,
                    "response": response.text.strip(),
                    "model_used": fallback_model,
                    "warning": f"Configured model failed. Fell back to {fallback_model}."
                }
        except Exception as fallback_err:
            return {
                "success": False,
                "error": f"API call failed: {str(e)}. Fallback also failed: {str(fallback_err)}"
            }
        
        return {
            "success": False,
            "error": f"Connection failed: {str(e)}"
        }

# Prompt definitions for different output formats
FORMAT_PROMPTS = {
    "Executive Summary": (
        "A highly polished, narrative business summary highlighting core findings, "
        "strategic implications, and key recommendations. Organize with clear headings, "
        "bold text for key metrics, and bulleted takeaways where appropriate."
    ),
    "Action-Items Checklist": (
        "A structured checklist of tasks, milestones, and actionable recommendations. "
        "Use markdown checkbox syntax (e.g., - [ ] Task name) and assign tasks to logical owners "
        "or departments if mentioned. Group items by priority (High, Medium, Low) or project phases."
    ),
    "Q&A Study Guide": (
        "A comprehensive Q&A Study Guide containing key questions and detailed answers derived "
        "directly from the source text. Focus on complex concepts, definitions, core hypotheses, "
        "and data points. Use a Q: and A: format."
    ),
    "Core Timeline": (
        "A detailed chronological timeline listing key events, project phases, historical dates, "
        "and milestones. Format each entry as '**[Date/Time]** - Event details' and ensure chronological order."
    )
}

def generate_map_reduce_summary(
    chunks: List[Dict[str, Any]],
    format_type: str = "Executive Summary",
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> Dict[str, Any]:
    """
    Executes the manual Map-Reduce loop on document chunks.
    
    Args:
        chunks: List of dictionaries representing document chunks.
        format_type: Type of final report (e.g., Executive Summary, Action-Items Checklist).
        progress_callback: Callable function taking (current_step, total_steps, status_text)
                           to report progress to frontend.
                           
    Returns:
        Dictionary containing:
            - "success": (bool)
            - "final_summary": (str)
            - "intermediate_summaries": List[str]
            - "error": (str)
    """
    result = {
        "success": False,
        "final_summary": "",
        "intermediate_summaries": [],
        "error": None
    }
    
    if not chunks:
        result["error"] = "No text chunks provided for summarization."
        return result
        
    if not configure_gemini():
        result["error"] = "Gemini API key is not configured. Please add it to your config/.env file."
        return result

    try:
        model_name = get_model_name()
        if not model_name:
            model_name = "gemini-2.5-flash"
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        result["error"] = f"Failed to initialize model {model_name}: {str(e)}"
        return result

    total_chunks = len(chunks)
    intermediate_summaries = []
    total_steps = total_chunks + 1  # Map steps + 1 Reduce step
    
    # ------------------ MAP PHASE ------------------
    if progress_callback:
        progress_callback(0, total_steps, "Starting Map Phase: Summarizing chunks independently...")
        
    for idx, chunk in enumerate(chunks):
        chunk_idx = idx + 1
        prefix_status = f"Map Phase: Processing chunk {chunk_idx}/{total_chunks} (Pages: {chunk['pages']})"
        
        if progress_callback:
            progress_callback(idx, total_steps, f"{prefix_status}...")
            
        map_prompt = f"""You are an expert technical analyst. Summarize the following document chunk.
Retain all key facts, specific metrics, project names, timelines, and main arguments.
Do not introduce external facts or speculate.

---
{chunk['text']}
---

Intermediate Summary:"""
        
        try:
            summary = call_gemini_with_retry(
                model=model,
                prompt=map_prompt,
                progress_callback=progress_callback,
                current_step=idx,
                total_steps=total_steps,
                progress_status_prefix=prefix_status
            )
            intermediate_summaries.append(summary)
        except Exception as e:
            # Try a quick fallback to gemini-1.5-flash for this chunk if model errors
            try:
                fallback_model = genai.GenerativeModel("gemini-1.5-flash")
                summary = call_gemini_with_retry(
                    model=fallback_model,
                    prompt=map_prompt,
                    progress_callback=progress_callback,
                    current_step=idx,
                    total_steps=total_steps,
                    progress_status_prefix=f"[Fallback Model] {prefix_status}"
                )
                intermediate_summaries.append(summary)
                continue
            except Exception:
                pass
            result["error"] = f"Error during Map phase at chunk {chunk_idx}: {str(e)}"
            return result
            
    result["intermediate_summaries"] = intermediate_summaries
    
    # ------------------ REDUCE PHASE ------------------
    prefix_status = "Reduce Phase: Synthesizing final report"
    if progress_callback:
        progress_callback(total_chunks, total_steps, f"{prefix_status}...")
        
    combined_intermediates = "\n\n---\n\n".join(intermediate_summaries)
    target_format_description = FORMAT_PROMPTS.get(format_type, FORMAT_PROMPTS["Executive Summary"])
    
    reduce_prompt = f"""You are an expert chief editor. Combine the following intermediate summaries of a document into a final, unified report.
You must adhere strictly to the target format: {target_format_description}

Maintain professional tone, logical flow, and ensure all key facts, metrics, and takeaways from the intermediate summaries are preserved.
Do not make up facts, names, or timelines.

---
Intermediate Summaries:
{combined_intermediates}
---

Final Formatted Report:"""

    try:
        final_summary = call_gemini_with_retry(
            model=model,
            prompt=reduce_prompt,
            progress_callback=progress_callback,
            current_step=total_chunks,
            total_steps=total_steps,
            progress_status_prefix=prefix_status
        )
        result["final_summary"] = final_summary
        result["success"] = True
    except Exception as e:
        # Fallback to gemini-1.5-flash
        try:
            fallback_model = genai.GenerativeModel("gemini-1.5-flash")
            final_summary = call_gemini_with_retry(
                model=fallback_model,
                prompt=reduce_prompt,
                progress_callback=progress_callback,
                current_step=total_chunks,
                total_steps=total_steps,
                progress_status_prefix=f"[Fallback Model] {prefix_status}"
            )
            result["final_summary"] = final_summary
            result["success"] = True
            if progress_callback:
                progress_callback(total_steps, total_steps, "Completed with fallback model.")
            return result
        except Exception:
            pass
        result["error"] = f"Error during Reduce phase: {str(e)}"
        result["success"] = False
        
    if progress_callback and result["success"]:
        progress_callback(total_steps, total_steps, "Summarization Completed Successfully!")
        
    return result

if __name__ == "__main__":
    print("Testing Gemini API Connection...")
    conn_result = verify_api_connection()
    if conn_result["success"]:
        print(f"Connection Successful! Model: {conn_result['model_used']}")
        print(f"Response: {conn_result['response']}")
    else:
        print(f"Connection Failed: {conn_result['error']}")
