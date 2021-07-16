import PyPDF2
import os
import re

folder_path = 'D:\\Shweta\\path_reports\\2021_12_07_surgery_path_reports_nact_sk'
file_name = '13_18_Sx_01.pdf'

pdfFileObject = open(os.path.join(folder_path, file_name), 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
count = pdfReader.numPages
for i in range(count):
    page = pdfReader.getPage(i)
    print(page.extractText())

EOF_MARKER = b'%%EOF'

with open(os.path.join(folder_path, file_name), 'rb') as f:
    contents = f.read()

# check if EOF is somewhere else in the file
if EOF_MARKER in contents:
    # we can remove the early %%EOF and put it at the end of the file
    contents = contents.replace(EOF_MARKER, b'')
    contents = contents + EOF_MARKER
else:
    # Some files really don't have an EOF marker
    # In this case it helped to manually review the end of the file
    print(contents[-8:]) # see last characters at the end of the file
    # printed b'\n%%EO%E'
    contents = contents[:-6] + EOF_MARKER

# with open(file_name.replace('.pdf', '') + '_fixed.pdf', 'wb') as f:
#     f.write(contents)

##

import pdfrw
import PyPDF4
pdf = os.path.join(folder_path, file_name)
x = pdfrw.PdfReader(pdf)
y = pdfrw.PdfWriter()
y.addpages(x.pages)
y.write(pdf)
pdf = PyPDF4.PdfFileReader(open(pdf, "rb"))

##
# from tika import parser # pip install tika
#
# raw = parser.from_file(os.path.join(folder_path, file_name))
# print(raw['content'])

##
import textract
text = textract.process(os.path.join(folder_path, file_name))

##
import pdftotext

# Load your PDF
with open("lorem_ipsum.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

# If it's password-protected
with open("secure.pdf", "rb") as f:
    pdf = pdftotext.PDF(f, "secret")

# How many pages?
print(len(pdf))

# Iterate over all the pages
for page in pdf:
    print(page)

# Read some individual pages
print(pdf[0])
print(pdf[1])

# Read all the text into one string
print("\n\n".join(pdf))

file_path = os.path.join(folder_path, file_name)
##
import os, subprocess
SCRIPT_DIR = os.path.dirname(os.path.abspath(file_path))
args = ["/usr/local/bin/pdftotext",
        '-enc',
        'UTF-8',
        "{}/my-pdf.pdf".format(SCRIPT_DIR),
        '-']
res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = res.stdout.decode('utf-8')

##
import fitz  # this is pymupdf

with fitz.open("my.pdf") as doc:
    text = ""
    for page in doc:
        text += page.getText()

print(text)

##
# from pdfminer.high_level import extract_text
# text = extract_text(file_path)
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    '''Convert pdf content from a file path to text

    :path the file path
    '''
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()

    with io.StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec,
                           laparams=laparams) as device:
            with open(path, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp,
                                              pagenos,
                                              maxpages=maxpages,
                                              password=password,
                                              caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)

                return retstr.getvalue()

txt = convert_pdf_to_txt(os.path.join(folder_path, file_name))

##

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()


    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)


    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

text = convert_pdf_to_txt(file_path)

string = 'chemotherapy'

text1 = text.replace('\n', '/')
text1 = text.replace(':', '/')
text1 = re.split('/', text1)

for line in text1:
    print(line)
    if string in line:
        print(string)
    else:
        print('not_found')

str1 = 'CLINICAL DETAILS'
for line in text1:
    if str1 in line:
        print(line)
    else:
        print('not_found')