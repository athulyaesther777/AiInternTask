# src/summarizer.py
from transformers import pipeline

# Load pre-trained models for summarization and keyword extraction
summarizer = pipeline("summarization")
keyword_extractor = pipeline("ner")


def summarize_pdf(pdf_path):
    # For simplicity, we assume that the content is passed as a string.
    with open(pdf_path, "rb") as f:
        content = f.read().decode(errors='ignore')  # Simplified content loading

    # Adjust the length of the summary based on the document length
    if len(content) < 500:  # Short PDF
        min_length = 30
        max_length = 50
    elif len(content) < 1500:  # Medium PDF
        min_length = 50
        max_length = 100
    else:  # Long PDF
        min_length = 100
        max_length = 300

    summary = summarizer(content, min_length=min_length, max_length=max_length)
    return summary[0]['summary_text']


def extract_keywords(pdf_path):
    # For simplicity, we assume that the content is passed as a string.
    with open(pdf_path, "rb") as f:
        content = f.read().decode(errors='ignore')  # Simplified content loading

    # Extract keywords (non-generic, domain-specific)
    keywords = keyword_extractor(content)
    return [kw['word'] for kw in keywords if kw['score'] > 0.8]
