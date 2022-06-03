import fitz
import os
import glob

for pdf_files in glob.glob('*.pdf'):
	document = fitz.open(pdf_files)
	document_page_number = document.pageCount
	keyword_file = open ('input_keywords.txt', 'r')
	keywords = keyword_file.read()
	keyword_sep = keywords.split(',')
	k = {}
	for keywords in keyword_sep:
		c=0
		for page in range(0, document_page_number):
			content = document[page]
			keyword = keywords.strip()
			keys = content.search_for(keywords)
			for key in keys:
				c+=1
		if c>=1:
			k[keywords]=c
	if len(k)>0:
		print(pdf_files, '->', k)
		output = open('keyword dataset.tsv', 'a')
		output.write(pdf_files + '\t' + str(k) + '\n')
	else:
		print(pdf_files, '->', k)
		output = open('keyword dataset.tsv', 'a')
		output.write(pdf_files + '\t' + 'Image format OR Keyword not present' + '\n')

		


