import os
import PyPDF2
import pandas as pd
from gensim.summarization.summarizer import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def summarize_text(text, word_count=100):
    try:
        return summarize(text, word_count=word_count)
    except ValueError:
        return text  # Return original text if summarization fails

def extract_keywords(text, top_n=10):
    stop_words = set(stopwords.words('english'))
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    # Get the top N keywords
    keywords = df.T.nlargest(top_n, 0).index.tolist()
    return keywords

def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    keywords = extract_keywords(text)
    return summary, keywords

def save_results_to_file(filename, summary, keywords, output_dir):
    # Create a dynamic output file name based on the PDF filename
    base_name = os.path.splitext(filename)[0]
    output_file = os.path.join(output_dir, f"{base_name}_results.txt")

    with open(output_file, 'a') as f:
        f.write(f"Document Name: {filename}\n")
        f.write(f"Summary: {summary}\n")
        f.write(f"Keywords: {', '.join(keywords)}\n")
        f.write("\n" + "="*40 + "\n\n")

pdf_directory = r"C:\Users\91730\pythonProject\pdfsummarizer\pythonProject1\src\downloaded_pdfs"
output_directory = r"C:\Users\91730\pythonProject\pdfsummarizer\output_results"

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        summary, keywords = process_pdf(pdf_path)

        # Save the results to a dynamically named output file
        save_results_to_file(filename, summary, keywords, output_directory)

        # Optionally, update MongoDB (if needed)
        # update_pdf_metadata(filename, summary, keywords)  # Uncomment if needed

print("Processing completed and results saved.")
