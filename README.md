# Smart PDF Summarizer

Multi-Format PDF Summarization Studio — a Streamlit dashboard that uses
a Map-Reduce architecture with the Google Gemini API to summarize
long PDF documents into multiple formats (Executive Summary,
Action-Items Checklist, Q&A Study Guide, Core Timeline).

## Status — Day 11 of 15

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
- [x] Day 11: UI polish — polished "Studio" dashboard theme, export
      feature (`app/exporter.py`), page-wise citation chunks
- [ ] Day 12: Performance tuning, caching
- [ ] Day 13: Expanded unit test coverage
- [ ] Day 14: Documentation pass
- [ ] Day 15: Final presentation

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp config/.env.example config/.env   # then add your real GEMINI_API_KEY
```

Get a free Gemini API key at https://aistudio.google.com/apikey

## Running the app

```bash
streamlit run app/main.py
```

Upload a PDF, pick a summary format, and click **Generate Summarization
Report**. Live progress updates show as each chunk is processed; the
final report is saved automatically and viewable in **Saved Archives**.

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
  via `.gitignore`). Never commit that file.
- Scanned/image-only PDFs aren't supported yet — text extraction
  requires a real text layer.
