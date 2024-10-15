import fitz  # PyMuPDF
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration


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

# Directory containing the PDF files
pdf_directory = r"C:\Users\91730\pythonProject\pdfsummarizer\pythonProject1\src\downloaded_pdfs"

# Iterate through all files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):  # Process only PDF files
        pdf_path = os.path.join(pdf_directory, filename)

        # Step 1: Extract text from the current PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Optional: Trim the extracted text if it's too long
        extracted_text = extracted_text[:2000]  # Use first 2000 characters for summarization

        # Step 2: Summarize the extracted text
        summary = summarize_text(extracted_text, model, tokenizer)

        # Step 3: Print or save the summary
        print(f"Summary of {filename}:")
        print(summary)

        # Save the summary to a text file
        summary_file_path = os.path.join(pdf_directory, f"{filename}_summary.txt")
        with open(summary_file_path, "w") as file:
            file.write(summary)

        print(f"Summary saved to {summary_file_path}\n")
