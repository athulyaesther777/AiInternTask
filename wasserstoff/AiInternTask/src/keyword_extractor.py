# keyword_extractor.py
from keybert import KeyBERT

def extract_keywords(content):
    """Extracts keywords from the provided text content."""
    model = KeyBERT()
    keywords = model.extract_keywords(content, top_n=5)
    return [kw[0] for kw in keywords]
