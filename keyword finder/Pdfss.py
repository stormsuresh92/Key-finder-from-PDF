import fitz
import glob
import csv

try:
    # Open and read keywords from the file
    with open('input_keywords.txt', 'r') as keyword_file:
        keywords = [keyword.strip() for keyword in keyword_file.read().split(',')]
except FileNotFoundError:
    print("Error: 'input_keywords.txt' not found. Please ensure the file exists in the directory.")
    keywords = []  # Initialize with empty list to prevent further errors

# Initialize the output data structure
output_data = [["PDF Name"] + keywords]  # Add headers (keywords)

# Process all PDF files in the current directory
for pdf_file in glob.glob('*.pdf'):
    try:
        document = fitz.open(pdf_file)  # Open PDF file
        page_count = document.page_count  # Get total number of pages
    except Exception as e:
        print(f"Error processing file '{pdf_file}': {e}")
        output_data.append([pdf_file] + ["Error"] * len(keywords))
        continue

    # Initialize keyword counts for the current PDF
    keyword_counts = [pdf_file] + [0] * len(keywords)

    for keyword_index, keyword in enumerate(keywords):
        try:
            count = 0
            # Loop through each page
            for page_number in range(page_count):
                page = document[page_number]
                # Search for the keyword on the page
                instances = page.search_for(keyword)
                count += len(instances)
            # Update the count for the keyword
            keyword_counts[keyword_index + 1] = count
        except Exception as e:
            print(f"Error searching for keyword '{keyword}' in file '{pdf_file}': {e}")
            keyword_counts[keyword_index + 1] = "Error"

    # Append the row for the current PDF file
    output_data.append(keyword_counts)

try:
    # Write to a CSV file
    with open('keyword_dataset.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(output_data)  # Write all rows at once
    print("Output saved in 'keyword_dataset.csv' in the desired format!")
except Exception as e:
    print(f"Error writing to output file: {e}")
