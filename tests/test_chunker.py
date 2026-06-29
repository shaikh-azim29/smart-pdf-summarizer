import sys
import os

# Add project root to python path for testing
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.chunker import chunk_document

def test_chunk_document_basic():
    """Test that a simple, small document produces exactly one chunk with correct metadata."""
    pages = {
        1: "This is page one text. It is very simple and short."
    }
    chunks = chunk_document(pages, max_chars=1000, overlap=0)
    
    assert len(chunks) == 1
    assert chunks[0]["index"] == 1
    assert chunks[0]["pages"] == [1]
    assert chunks[0]["text"] == "This is page one text. It is very simple and short."
    assert chunks[0]["char_count"] == len(pages[1])

def test_chunk_document_multiple_pages():
    """Test that chunks correctly track multiple pages."""
    pages = {
        1: "This is page one text which is short.",
        2: "This is page two text which is also short."
    }
    # Set max_chars low enough to force multiple chunks or see page mappings
    chunks = chunk_document(pages, max_chars=40, overlap=0)
    
    assert len(chunks) >= 2
    # Check that pages are represented
    pages_seen = set()
    for chunk in chunks:
        for p in chunk["pages"]:
            pages_seen.add(p)
    assert 1 in pages_seen
    assert 2 in pages_seen

def test_chunk_document_size_boundary():
    """Test that no chunk exceeds the maximum character threshold."""
    # Create text with several paragraphs
    paragraphs = ["Paragraph number one is here.", "Paragraph number two is here.", "Paragraph number three is here."]
    pages = {
        1: "\n\n".join(paragraphs)
    }
    
    # Force splitting by choosing max_chars smaller than the total text but larger than single paragraph
    max_chars = 60
    chunks = chunk_document(pages, max_chars=max_chars, overlap=0)
    
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk["char_count"] <= max_chars
        assert len(chunk["text"]) <= max_chars

def test_chunk_document_overlap_handling():
    """Test that overlap is correctly added to subsequent chunks."""
    pages = {
        1: "This is the first sentence. This is the second sentence. This is the third sentence."
    }
    
    # Split text into chunks
    chunks = chunk_document(pages, max_chars=50, overlap=25)
    
    assert len(chunks) >= 2
    # The second chunk should carry over some text from the first chunk
    # e.g., parts of the first or second sentence should appear in chunk 2
    chunk1_text = chunks[0]["text"]
    chunk2_text = chunks[1]["text"]
    
    # Verify that some words from chunk 1's end overlap into chunk 2
    words_chunk1 = chunk1_text.split()
    last_few_words = " ".join(words_chunk1[-3:])
    
    # We check if overlap candidate exists in some form
    overlap_found = False
    for word in words_chunk1[-3:]:
        if word in chunk2_text:
            overlap_found = True
            break
    assert overlap_found, f"Expected overlap between '{chunk1_text}' and '{chunk2_text}'"

def test_chunk_document_empty_input():
    """Test that empty or whitespace-only inputs return empty chunk lists."""
    pages = {
        1: "",
        2: "   "
    }
    chunks = chunk_document(pages, max_chars=1000)
    assert len(chunks) == 0
