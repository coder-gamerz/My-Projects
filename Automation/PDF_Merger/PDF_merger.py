import PyPDF2
import os

merger = PyPDF2.PdfMerger()

for file in os.listdir(r'C:\Users\shrey\OneDrive\Documents\Automation\PDF_Merger\PDFs'):
    if file.endswith(".pdf"):
        merger.append(fr'C:\Users\shrey\OneDrive\Documents\Automation\PDF_Merger\PDFs\{file}')
    merger.write(r"C:\Users\shrey\OneDrive\Documents\Automation\PDF_Merger\Merged_PDFs\combined.pdf")
    
# A simple PDF merger
    
