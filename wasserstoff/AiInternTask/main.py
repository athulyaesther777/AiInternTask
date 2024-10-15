import fitz  # PyMuPDF
import os
import time
import psutil  # To measure memory usage
from transformers import T5Tokenizer, T5ForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor
from keyword_extractor import extract_keywords  # Import the keyword extractor
from src.mongodb_handler import insert_mongodb  # Import MongoDB handler functions
from pymongo import MongoClient  # Import MongoClient
from logger import log_info, log_error, log_debug, log_warning, log_exception

# Connect to MongoDB
def connect_to_mongodb(uri="mongodb://localhost:27017/", db_name="your_database_name"):
    """Connect to MongoDB and return the database."""
    client = MongoClient(uri)
    return client[db_name]  # Return the database object


# Function to retrieve and print document structure from MongoDB
def print_mongodb_documents(db, collection_name):
    """Print the structure of documents in the specified MongoDB collection."""
    collection = db[collection_name]
    documents = collection.find()

    for doc in documents:
        print("=" * 50)  # Separator for readability
        print("Document ID:", doc.get('_id'))  # Print the document ID
        print("Document Structure:")
        for key, value in doc.items():  # Iterate over key-value pairs
            print(f"{key}: {value}")


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Load each page
        text += page.get_text("text")  # Extract text from page
    return text


# Function to summarize the extracted text
def summarize_text(text, model, tokenizer, max_input_length=512, max_output_length=150):
    # Tokenize input
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs, max_length=max_output_length, min_length=30, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)

    # Decode summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


# Load pre-trained T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


# Process PDFs in batches to avoid memory overload
def run_parallel_pipeline(folder_path, batch_size=2):
    """Processes PDF files in parallel batches."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    total_files = len(pdf_files)

    log_info(f"Found {total_files} PDF files in {folder_path}.")

    for i in range(0, total_files, batch_size):
        batch = pdf_files[i:i + batch_size]
        log_info(f"Processing batch {i // batch_size + 1}: {batch}")

        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(lambda pdf_name: process_pdf(folder_path, pdf_name), batch)


# Function to process each PDF file
def process_pdf(folder_path, pdf_name):
    """Processes a single PDF, extracts text, generates summary, and stores metadata."""
    pdf_path = os.path.join(folder_path, pdf_name)
    start_time = time.time()  # Track overall processing time

    # Initialize performance metrics
    metrics = {
        "extraction_time": 0,
        "summary_time": 0,
        "keyword_extraction_time": 0,
        "mongodb_insertion_time": 0,
        "memory_usage": 0
    }

    try:
        # Step 1: Extract text from the current PDF
        extraction_start_time = time.time()
        extracted_text = extract_text_from_pdf(pdf_path)
        extraction_duration = time.time() - extraction_start_time  # Calculate duration
        metrics["extraction_time"] = extraction_duration
        log_info(f"Text extraction took: {extraction_duration:.2f} seconds")

        # Optional: Trim the extracted text if it's too long
        extracted_text = extracted_text[:2000]  # Use first 2000 characters for summarization

        # Step 2: Generate different lengths of summaries
        summary_start_time = time.time()
        short_summary = summarize_text(extracted_text, model, tokenizer, max_output_length=50)  # Short summary
        medium_summary = summarize_text(extracted_text, model, tokenizer, max_output_length=100)  # Medium summary
        long_summary = summarize_text(extracted_text, model, tokenizer, max_output_length=200)  # Long summary
        summary_duration = time.time() - summary_start_time  # Calculate duration
        metrics["summary_time"] = summary_duration
        log_info(f"Summary generation took: {summary_duration:.2f} seconds")

        # Step 3: Extract keywords from the extracted text
        keyword_extraction_start_time = time.time()
        keywords = extract_keywords(extracted_text)  # Call the keyword extraction function
        keyword_extraction_duration = time.time() - keyword_extraction_start_time  # Calculate duration
        metrics["keyword_extraction_time"] = keyword_extraction_duration
        log_info(f"Keyword extraction took: {keyword_extraction_duration:.2f} seconds")

        # Step 4: Print structured output
        print("=" * 50)
        print(f"Summaries of {pdf_name}:")
        print("=" * 50)
        print("Short Summary:")
        print(f"'{short_summary}'\n")
        print("Medium Summary:")
        print(f"'{medium_summary}'\n")
        print("Long Summary:")
        print(f"'{long_summary}'\n")
        print("Keywords extracted:")
        print(", ".join(keywords))  # Join keywords with commas
        print("=" * 50)

        # Save the summaries to a structured text file
        summary_file_path = os.path.join(folder_path, f"{pdf_name}_summary.txt")
        with open(summary_file_path, "w") as file:
            file.write(f"Summaries of {pdf_name}:\n")
            file.write("=" * 50 + "\n")
            file.write("Short Summary:\n")
            file.write(f"{short_summary}\n\n")
            file.write("Medium Summary:\n")
            file.write(f"{medium_summary}\n\n")
            file.write("Long Summary:\n")
            file.write(f"{long_summary}\n\n")
            file.write("Keywords extracted:\n")
            file.write(", ".join(keywords) + "\n")

        log_info(f"Summaries saved to {summary_file_path}")

        # Prepare metadata for MongoDB
        metadata = {
            "name": pdf_name,
            "short_summary": short_summary,
            "medium_summary": medium_summary,
            "long_summary": long_summary,
            "keywords": keywords,
            "processed_at": time.time()
        }

        # Insert metadata into MongoDB
        mongodb_insertion_start_time = time.time()
        insert_mongodb(metadata)
        mongodb_insertion_duration = time.time() - mongodb_insertion_start_time  # Calculate duration
        metrics["mongodb_insertion_time"] = mongodb_insertion_duration
        log_info(f"MongoDB insertion took: {mongodb_insertion_duration:.2f} seconds")

    except MemoryError:
        log_error(f"Error processing {pdf_name}: Not enough memory to process this PDF.")
    except EOFError:
        log_error(f"Error processing {pdf_name}: PDF is corrupted or incomplete.")
    except Exception as e:
        log_error(f"Error processing {pdf_name}: {e}")
    finally:
        end_time = time.time()
        metrics["memory_usage"] = psutil.Process().memory_info().rss  # Get current memory usage
        log_info(f"Overall processing time for {pdf_name}: {end_time - start_time:.2f} seconds")

        # Log performance metrics
        log_info(f"Performance metrics for {pdf_name}: {metrics}")

# Main execution
if __name__ == "__main__":
    folder_path = r"C:\Users\91730\pythonProject\pdfsummarizer\pythonProject1\src\downloaded_pdfs"

    # Connect to MongoDB
    db = connect_to_mongodb(db_name="your_database_name")  # Replace with your database name

    if not os.path.exists(folder_path):
        log_error(f"Folder path {folder_path} does not exist.")
    else:
        run_parallel_pipeline(folder_path)

    # Print the MongoDB documents after processing the PDFs
    print_mongodb_documents(db, collection_name="your_collection_name")  # Replace with your collection name
