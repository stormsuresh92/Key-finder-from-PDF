import fitz
import os
import glob
import re
for files in glob.glob("*.pdf"):
    doc = fitz.open(files)
    print(files)
    print(doc)
    lk=open("input_keywords.txt",'r')
    kl=lk.read()
    page_no=doc.pageCount
    split_ketywords=kl.split('|')
    d={}               
    for keys in split_ketywords:
        c=0
        for pp in range(0,page_no):
            page = doc[pp]
            text = str(keys.strip())
            text_instances = page.searchFor(text)            
            for inst in text_instances:
                print(inst, type(inst))
                # time.sleep(1)
                c+=1
        if c>=1:
            d[str(keys)]=c   
    files=re.sub('Input_pdf','',str(files))
    files=re.sub('^\s*','',str(files))
    files=files.replace('\\','')
    if len(d)>0:
        print(d)
        hg=open("output.txt","a",encoding="utf-8")
        gh=hg.write(str(files.strip())+"|"+str(d)+"\n")
    else:
        print('N/A')
        hg=open("output.txt","a",encoding="utf-8")
        gh=hg.write(str(files.strip())+"|"+"IMAGE OR N/A"+"\n")
        

        
