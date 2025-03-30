import fitz
import glob
import os
import csv
import logging
import re

# Configure logging
logging.basicConfig(filename="pdf_keyword_extraction.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure 'static' directory exists for saving the output
output_dir = "static"
os.makedirs(output_dir, exist_ok=True)

# Define output file path in the 'static' directory
output_path = os.path.join(output_dir, "keyword_dataset.csv")

# Open and read keywords from the file
try:
    with open('input_keywords.txt', 'r', encoding="utf-8") as keyword_file:
        keywords = [keyword.strip().lower() for keyword in keyword_file.read().split(',') if keyword.strip()]
    if not keywords:
        raise ValueError("Keyword file is empty.")
except FileNotFoundError:
    logging.error("Error: 'input_keywords.txt' not found.")
    print("Error: 'input_keywords.txt' not found.")
    keywords = []
except ValueError as ve:
    logging.error(f"Error: {ve}")
    print(f"Error: {ve}")
    keywords = []

# Initialize output data with headers
output_data = [["PDF Name"] + keywords]

# Process all PDF files in the current directory
pdf_files = glob.glob('*.pdf')

if not pdf_files:
    print("No PDF files found in the directory.")
    logging.info("No PDF files found.")

for pdf_file in pdf_files:
    try:
        print(f"Processing: {pdf_file}")
        document = fitz.open(pdf_file)

        if document.is_encrypted:
            logging.warning(f"Skipping '{pdf_file}': Password protected.")
            print(f"Skipping '{pdf_file}': Password protected.")
            output_data.append([pdf_file] + ["Password Protected"] * len(keywords))
            continue

        text_found = any(page.get_text() for page in document)
        if not text_found:
            logging.warning(f"Skipping '{pdf_file}': Image-only PDF detected.")
            print(f"Skipping '{pdf_file}': Image-only PDF detected.")
            output_data.append([pdf_file] + ["Image Only"] * len(keywords))
            continue

        page_count = document.page_count
    except Exception as e:
        logging.error(f"Error processing '{pdf_file}': {e}")
        print(f"Error processing '{pdf_file}': {e}")
        output_data.append([pdf_file] + ["Error"] * len(keywords))
        continue

    # Initialize keyword counts for the current PDF
    keyword_counts = [pdf_file] + [0] * len(keywords)

    for keyword_index, keyword in enumerate(keywords):
        try:
            count = 0
            keyword_regex = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)

            for page in document:
                text = page.get_text("text")
                count += len(list(keyword_regex.finditer(text)))

            keyword_counts[keyword_index + 1] = count
        except Exception as e:
            logging.error(f"Error searching for '{keyword}' in '{pdf_file}': {e}")
            keyword_counts[keyword_index + 1] = "Error"

    if sum(keyword_counts[1:]) == 0:
        logging.info(f"No keywords found in '{pdf_file}'.")
        print(f"No keywords found in '{pdf_file}'.")
        output_data.append([pdf_file] + ["No Keywords Found"] * len(keywords))
    else:
        output_data.append(keyword_counts)

# Write to CSV file
try:
    with open(output_path, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(output_data)
    print(f"✅ Output saved in '{output_path}'")
    logging.info(f"Output saved in '{output_path}'")
except Exception as e:
    logging.error(f"Error writing to output file: {e}")
    print(f"Error writing to output file: {e}")
