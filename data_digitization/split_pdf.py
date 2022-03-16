import os
from PyPDF2 import PdfFileReader, PdfFileWriter

input_folder = 'd:/WorkDocs/Documents/ocr/sample_input'
file = 'split_test.pdf'
output_folder = 'd:/WorkDocs/Documents/ocr/sample_output'

test_file = PdfFileReader(os.path.join(input_folder, file))

page_range = test_file.getNumPages()

for i in range(page_range-1):
    page = test_file.getPage(i)
    output_file = 'split_pdf_' + str(i) + '.pdf'
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(page)
    with open(os.path.join(output_folder, output_file), 'wb') as out:
        pdf_writer.write(out)
