import fitz
import glob
import csv

# Open and read keywords from the file
with open('input_keywords.txt', 'r') as keyword_file:
    keywords = keyword_file.read().split(',')

# Prepare CSV file for writing output
with open('keyword_dataset.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["PDF Name", "Keyword", "Count"])  # Write the header row

    # Process all PDF files in the current directory
    for pdf_file in glob.glob('*.pdf'):
        document = fitz.open(pdf_file)  # Open PDF file
        page_count = document.page_count  # Get total number of pages

        keyword_counts = {}  # Store counts of each keyword in the document

        # Loop through each keyword
        for keyword in map(str.strip, keywords):
            count = 0
            # Loop through each page
            for page_number in range(page_count):
                page = document[page_number]
                # Search for keyword instances = page.search_for(keyword)
                count += len(instances)
            # Add keyword count to the dictionary if found
            if count > 0:
                keyword_counts[keyword] = count

        # Write keyword counts to the CSV file
        if keyword_counts:
            for key, value in keyword_counts.items():
                csvwriter.writerow([pdf_file, key, value])
            print(pdf_file, '->', keyword_counts)
        else:
            # Handle case where no keywords are found
            csvwriter.writerow([pdf_file, "No Keywords Found", 0])
            print(pdf_file, '->', 'Image format OR Keyword not present')
