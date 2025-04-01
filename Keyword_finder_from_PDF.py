import fitz  # pip install PyMuPDF, then import fitz
import glob
import csv
from tqdm import tqdm

# Open and read keywords from the file
try:
    with open('input_keywords.txt', 'r') as keyword_file:
        keywords = [keyword.strip() for keyword in keyword_file.read().split(',')]
except FileNotFoundError:
    print("Error: 'input_keywords.txt' not found. Please ensure the file exists in the directory.")
    keywords = []

# Initialize the output data structure
output_data = [["PDF Name"] + keywords + ["Reason"]]  # Add headers (keywords + reason)

# Process all PDF files in the current directory
for pdf_file in tqdm(glob.glob('*.pdf')):
    try:
        # Attempt to open the PDF file
        document = fitz.open(pdf_file)
        
        # Check if the PDF is password-protected
        if document.is_encrypted:
            #print(f"Error: '{pdf_file}' is password-protected.")
            output_data.append([pdf_file] + [""] * len(keywords) + ["Password Protected"])
            continue
        
        # Check if the PDF has any text (image-only PDFs will not be handled)
        text_found = any(page.get_text() for page in document)
        if not text_found:
            #print(f"Error: '{pdf_file}' is an image-only PDF. Skipping...")
            output_data.append([pdf_file] + [""] * len(keywords) + ["Image Format"])
            continue
        
        page_count = document.page_count  # Get total number of pages
    except Exception as e:
        #print(f"Error processing file '{pdf_file}': {e}")
        output_data.append([pdf_file] + [""] * len(keywords) + ["Unable to open"])
        continue

    # Initialize keyword counts for the current PDF
    keyword_counts = [pdf_file] + [0] * len(keywords) + [""]  # Last column for Reason

    for keyword_index, keyword in enumerate(keywords):
        try:
            count = 0
            keyword_lower = keyword.lower()  # Handle case-insensitivity
            # Loop through each page
            for page_number in range(page_count):
                page = document[page_number]
                text = page.get_text().lower()
                count += text.count(keyword_lower)
            # Update the count for the keyword
            keyword_counts[keyword_index + 1] = count
        except Exception as e:
            #print(f"Error searching for keyword '{keyword}' in file '{pdf_file}': {e}")
            keyword_counts[keyword_index + 1] = "Error"

    # Append the row for the current PDF file
    if sum(keyword_counts[1:-1]) == 0:  # No keywords found in the entire PDF
        #print(f"No keywords found in '{pdf_file}'.")
        output_data.append(keyword_counts[:-1] + ["No Keywords Found"])  # Add reason
    else:
        output_data.append(keyword_counts)

# Write to the CSV file
try:
    with open('keyword_dataset.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(output_data)  # Write all rows at once
    print(f"Output saved in 'keyword_dataset.csv' in the desired format!")
except Exception as e:
    print(f"Error writing to output file: {e}")
