from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import logging
from process_pdf import process_pdf  # Assuming process_pdf logic is separated into its own module

def run_parallel_pipeline(folder_path, batch_size=2):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    total_files = len(pdf_files)
    start_time = time.time()  # Start timer for performance metrics

    for i in range(0, total_files, batch_size):
        batch = pdf_files[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = {executor.submit(process_pdf, pdf): pdf for pdf in batch}
            for future in as_completed(futures):
                pdf = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Failed to process {pdf}: {e}")

    # Performance metric
    end_time = time.time()
    logging.info(f"Total time for processing {total_files} PDFs: {end_time - start_time:.2f} seconds")
