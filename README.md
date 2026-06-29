# Smart PDF Summarizer

Multi-Format PDF Summarization Studio — a Streamlit dashboard that uses
a Map-Reduce architecture with the Google Gemini API to summarize
long PDF documents into multiple formats (Executive Summary,
Action-Items Checklist, Q&A Study Guide, Core Timeline).

## Status — Day 11 of 15

- [x] Day 1: Project structure, Git, virtual environment
- [x] Day 2: PDF text parser (`app/parser.py`, PyMuPDF)
- [x] Day 3: Document chunker (`app/chunker.py`)
- [x] Day 4: Gemini API connection setup & verification
- [x] Day 5: Map phase summarizer
- [x] Day 6: Reduce phase summarizer (4 format templates)
- [x] Day 7: SQLite database logger
- [x] Day 8: Streamlit dashboard layout
- [x] Day 9: Live progress bar wired to the Map-Reduce loop
- [x] Day 10: Full pipeline integration (upload → process → save → display)
- [x] Day 11: UI polish — "Studio" dashboard theme, export feature
      (`app/exporter.py`), page-wise citation chunks
- [ ] Day 12: Performance tuning, caching
- [ ] Day 13: Expanded unit test coverage
- [ ] Day 14: Documentation pass
- [ ] Day 15: Final presentation

## How to run this project

### 1. Clone the repository

```bash
git clone https://github.com/shaikh-azim29/smart-pdf-summarizer.git
cd smart-pdf-summarizer
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key

Get a **free** API key from https://aistudio.google.com/apikey

You can provide the key in **either** of two ways:

**Option A — `.env` file (recommended for repeated use):**
```bash
cp config/.env.example config/.env
```
Then open `config/.env` and replace the placeholder with your real key:
```
GEMINI_API_KEY=your_real_key_here
```

**Option B — Enter it directly in the app sidebar:**
Just run the app (next step) and paste your key into the
**"Google Gemini API Key"** field in the sidebar. No file editing needed —
useful for quickly testing without setting up `.env`.

### 5. Run the app

```bash
streamlit run app/main.py
```

This opens the dashboard at `http://localhost:8501` in your browser.

### 6. Try it out

1. Upload any PDF using the **Upload PDF Document** box in the sidebar.
2. Choose a summary format (Executive Summary, Action-Items Checklist,
   Q&A Study Guide, or Core Timeline).
3. Click **Generate Summarization Report**.
4. Watch the live progress as the document is chunked and summarized.
5. View the final report, plus page-wise citation chunks.
6. Check the **Saved Archives** tab to see past summaries (stored in
   `database/summaries.db`).

## Try each piece individually

```bash
# Day 2: parse a PDF page-by-page
python app/parser.py path/to/file.pdf

# Day 3: parse + chunk a PDF
python app/chunker.py path/to/file.pdf

# Day 4: verify Gemini API connection
python app/summarizer.py

# Day 7: initialize the SQLite database
python database/db_manager.py

# Run chunker unit tests
pytest tests/test_chunker.py -v
```

## Notes

- Keep your real Gemini API key only in `config/.env` (already excluded
  via `.gitignore`) — **never commit that file.**
- Scanned/image-only PDFs aren't supported yet — text extraction
  requires a real text layer in the PDF.
