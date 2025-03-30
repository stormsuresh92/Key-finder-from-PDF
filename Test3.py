import fitz  # PyMuPDF
import os
import csv

def read_keywords_from_file(keyword_file):
    """Reads keywords from a text file (one per line)."""
    try:
        with open(keyword_file, "r", encoding="utf-8") as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except Exception as e:
        print(f"Error reading keyword file: {e}")
        return []

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file and logs errors."""
    try:
        doc = fitz.open(pdf_path)
        
        # Check if the PDF is password-protected
        if doc.needs_pass:
            print(f"Skipping password-protected file: {pdf_path}")
            return None, "Password Protected"

        text = ""
        for page in doc:
            text += page.get_text("text")  # Extract text from each page
        
        # Skip image-based PDFs (no extracted text)
        if not text.strip():
            print(f"Skipping image-based PDF: {pdf_path}")
            return None, "Image-Based"

        return text, None

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None, str(e)

def find_keywords_in_pdfs(folder_path, keywords):
    """Finds user-defined keywords in multiple PDFs and logs errors."""
    pdf_results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text, error_reason = extract_text_from_pdf(pdf_path)

            if text:  # Process only if text extraction was successful
                found_keywords = {word: text.lower().count(word.lower()) for word in keywords}
                pdf_results.append([filename] + [found_keywords.get(keyword, 0) for keyword in keywords] + [""])  # No error
            else:
                pdf_results.append([filename] + ["" for _ in keywords] + [error_reason])  # Error reason only

    return pdf_results

def save_results_to_csv(results, keywords, output_file):
    """Saves keyword occurrences & errors in a single CSV file."""
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header (Keyword names + Error column)
        header = ["PDF Name"] + keywords + ["Error Reason"]
        writer.writerow(header)

        # Write data rows
        writer.writerows(results)
    
    print(f"\nResults saved to {output_file}")

# Example usage
pdf_folder = "pdfs_folder"  # Replace with your folder path
keyword_file = "keywords.txt"  # Text file with keywords (one per line)
output_csv = "results.csv"

# Read keywords from file
user_keywords = read_keywords_from_file(keyword_file)

if user_keywords:
    # Process PDFs and save results
    results = find_keywords_in_pdfs(pdf_folder, user_keywords)
    save_results_to_csv(results, user_keywords, output_csv)
else:
    print("No keywords found. Please check the keyword file.")
