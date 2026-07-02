# Smart PDF Summarizer

Multi-Format PDF Summarization Studio — a Streamlit dashboard that uses
a Map-Reduce architecture with the Google Gemini API to summarize
long PDF documents into multiple formats (Executive Summary,
Action-Items Checklist, Q&A Study Guide, Core Timeline).

## Status — Day 15 of 15 ✅ COMPLETE

- [x] Day 1: Project structure, Git, virtual environment
- [x] Day 2: PDF text parser (`app/parser.py`, PyMuPDF)
- [x] Day 3: Document chunker (`app/chunker.py`) — splits text into
      ~3,000 character blocks without cutting sentences, with overlap
      support to preserve context between chunks
- [x] Day 4: Gemini API connection setup & verification
      (`verify_api_connection()` in `app/summarizer.py`)
- [x] Day 5: Map phase summarizer — summarizes each chunk independently
- [x] Day 6: Reduce phase summarizer — compiles intermediate summaries
      into the final formatted report (4 format templates)
- [x] Day 7: SQLite database logger (`database/db_manager.py`,
      `app/db_helper.py`) — schema + save/read/delete history functions
- [x] Day 8: Streamlit dashboard layout — file uploader, format
      selector, chunk-size/overlap sliders
- [x] Day 9: Live progress bar wired to the Map-Reduce loop
- [x] Day 10: Full pipeline integration (upload → process → save → display)
- [x] Day 11: UI polish — "Studio" dashboard theme, export feature
      (`app/exporter.py`), page-wise citation chunks
- [x] Day 12: Performance tuning — caching, error handling, empty PDF detection
- [x] Day 13: Unit testing — 10/10 pytest tests passing
- [x] Day 14: Project documentation — README, inline comments, Project Report PDF
- [x] Day 15: Presentation slides — final slide deck submitted

---

## Project Structure

```
smart_pdf_summarizer/
│
├── config/
│   └── .env.example          # Template for GEMINI_API_KEY
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py         # SQLite connection logging summaries history
│   └── summaries.db          # Database file (ignored in .gitignore)
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Streamlit application main runner
│   ├── parser.py             # PDF text extraction scripts
│   ├── chunker.py            # Document text splitting pipeline
│   ├── summarizer.py         # Gemini API Map-Reduce coordinator
│   ├── db_helper.py          # SQLite logging helpers
│   └── exporter.py           # Export summaries to .md, .txt, PDF
│
├── tests/
│   └── test_chunker.py       # Unit tests verifying text chunking logic
│
├── requirements.txt
├── .gitignore
├── README.md
└── run.py                    # CLI script launching streamlit
                              # (`streamlit run app/main.py`)
```

---

## How to Run This Project

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

**Option B — Enter directly in the app sidebar:**
Run the app and paste your key into the **"Google Gemini API Key"**
field in the sidebar. No file editing needed.

### 5. Run the app

```bash
python -m streamlit run app/main.py
```

This opens the dashboard at `http://localhost:8501` in your browser.

### 6. Try it out

1. Upload any PDF using the **Upload PDF Document** box in the sidebar
2. Choose a summary format (Executive Summary, Action-Items Checklist,
   Q&A Study Guide, or Core Timeline)
3. Click **Generate Summarization Report**
4. Watch the live progress as the document is chunked and summarized
5. View the final report, plus page-wise citation chunks
6. Check the **Saved Archives** tab to see past summaries

---

## Try Each Piece Individually

```bash
# Day 2: parse a PDF page-by-page
python app/parser.py path/to/file.pdf

# Day 3: parse + chunk a PDF
python app/chunker.py path/to/file.pdf

# Day 4: verify Gemini API connection
python app/summarizer.py

# Day 7: initialize the SQLite database
python database/db_manager.py

# Day 13: run unit tests
pytest tests/test_chunker.py -v
```

---

## Final Deliverables Submitted

| # | Deliverable | Status |
|---|---|---|
| 1 | Source Code | ✅ Complete |
| 2 | GitHub Repository | ✅ github.com/shaikh-azim29/smart-pdf-summarizer |
| 3 | README.md | ✅ Complete |
| 4 | Local Database (`summaries.db`) | ✅ Auto-generated on first run |
| 5 | Project Report PDF | ✅ Submitted |
| 6 | Presentation Slides | ✅ Submitted |
| 7 | Demo Video | ✅ Submitted |

---

## Notes

- Keep your real Gemini API key only in `config/.env` (already excluded
  via `.gitignore`) — **never commit that file.**
- Scanned/image-only PDFs aren't supported yet — text extraction
  requires a real text layer in the PDF.
- `database/summaries.db` is gitignored — it is generated locally on
  first run and submitted separately as a deliverable.
