# importing required modules
# https://bobcares.com/blog/how-to-install-opencv-on-ubuntu-20-04/
import pandas as pd
import numpy as np
import itertools
import subprocess
import cv2
import argparse
from pdf2image import convert_from_path
import sys
import pytesseract as pt
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

# creating a pdf file object
path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy'
# path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/'
pdfname = '110_18_FNAC_Bx_IHC.pdf'
pdfFile = os.path.join(path, pdfname)
pdfFileObj = open(pdfFile, mode='r+b')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
PyPDF2.PdfFileWriter()
# printing number of pages in pdf file
print(pdfReader.numPages)
pdfReader.getObject()
pdfReader.getPageMode()
# creating a page object
pageObj = pdfReader.getPage(0)

# extracting text from page
print(pageObj.extractText())
pdfReader.getFields()
# closing the pdf file object
pdfFileObj.close()


# https://realpython.com/pdf-python/

# rotate_pages.py

def rotate_pages(pdfFile):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(path)
    # Rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # Rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # Add a page in normal orientation
    pdf_writer.addPage(pdf_reader.getPage(2))

    with open('rotate_pages.pdf', 'wb') as fh:
        pdf_writer.write(fh)


if __name__ == '__main__':
    path = 'Jupyter_Notebook_An_Introduction.pdf'
    rotate_pages(path)


def rotate_pages(pdfFile):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(path)
    # Rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # Rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # Add a page in normal orientation
    pdf_writer.addPage(pdf_reader.getPage(2))

    with open('rotate_pages.pdf', 'wb') as fh:
        pdf_writer.write(fh)


if __name__ == '__main__':
    path = 'Jupyter_Notebook_An_Introduction.pdf'
    rotate_pages(path)

# pdf Merge

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))
        fullTempPath = os.path.join(tempPath, 'time_' + imageName + ".txt")
    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
    paths = ['document1.pdf', 'document2.pdf']
    merge_pdfs(paths, output='merged.pdf')


# read rotate, write
path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/'
pdfName = '2020_02_06_Reports_from_Golwilkarrotate.PDF'
pdfFile = os.path.join(path, pdfName)
# this works!!!


def read_rotate_write(path, pdfName):
    pdfFile = os.path.join(path, pdfName)
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(pdfFile)
    pages = pdf_reader.numPages
    for page in range(0, pages):
        page_rot = pdf_reader.getPage(page).rotateCounterClockwise(90)
        pdf_writer.addPage(page_rot)
        writePath = os.path.join(
            path, (pdfName[1:-4] + '_rotate_' + str(page) + '.jpeg'))
        with open(writePath, 'wb') as out:
            pdf_writer.write(out)

# scanned pdf is an image. Has to be read as such.
folder_path = 'D:\\Shweta\\path_reports\\Histopath_reports_from_server\\Biopsy'
file_name = '110_18_FNAC_Bx_IHC.pdf'

# write each image to different file.
path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/'
pdfName = '020_02_06_Reports_from_Golwilkarrotate.pdf'
pdfFile = os.path.join(folder_path, file_name)
# this works!!!
inputpdf = PdfFileReader(open(pdfFile, "rb"))
for i in range(inputpdf.numPages):
    outputName = pdfFile[0:-4] + '_' + str(i) + '.jpg'
    output = Image.Image.convert()
    output.addPage(inputpdf.getPage(i))
    with open(outputName, "wb") as outputStream:
        output.write(outputStream)

# read each image and store as df that is print to excel.

# Python program to extract text from all the images in a folder
# storing the text in corresponding files in a different folder

def main():
    # path for the folder for getting the raw images
    path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page'
    # path for the folder for getting the output
    tempPath = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/textFiles'
    for imageName in os.listdir(path):
        inputPath = os.path.join(path, imageName)
        img = Image.open(inputPath)
        # applying ocr using pytesseract for python
        text = pt.image_to_string(img, lang="eng")
        # for removing the .jpg from the imagePath
        imageName = imageName[0:-4]
        fullTempPath = os.path.join(tempPath, imageName + ".txt")
        print(text)
        # saving the  text for every image in a separate .txt file
        file1 = open(fullTempPath, "w")
        file1.write(text)
        file1.close()
# does not recognize pdf as a image.


def pdftoImage():
    path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page'
    # path for the folder for getting the output
    tempPath = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/textFiles'
    for imageName in os.listdir(path):
        imagePath = os.path.join(path, imageName)
        print(imagePath)
        pages = convert_from_path(imagePath, 500)
        outJpg = imageName[0:-4]+'.jpg'
        for page in pages:
            page.save(outJpg, 'JPEG')
        print(outJpg)
        img = Image.open(os.path.join(path, outJpg))
        text = pt.image_to_string(img, lang="eng")
        imageName = imageName[0:-4]
        fullTempPath = os.path.join(tempPath, imageName + ".txt")
        print(text)
        # saving the  text for every image in a separate .txt file
        file1 = open(fullTempPath, "w")
        file1.write(text)
        file1.close()


# did not created jpg file. downloaded poppler and re-installed pdf2image
# (https://stackoverflow.com/questions/46184239/extract-a-page-from-a-pdf-as-a-jpeg)
# convert to jpg

pdf_dir = r"D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page"
os.chdir(pdf_dir)

pdftoppm_path = r"C:\Program Files (x86)\poppler\bin\pdftoppm.exe"

for pdf_file in os.listdir(pdf_dir):
    print(pdf_file)
    if pdf_file.endswith(".pdf"):
        outjpg = os.path.join(pdf_dir, pdf_file[0:-4])
        subprocess.Popen(
            '"{!s}" -jpeg {!s} {!s}'.format(pdftoppm_path, pdf_file, outjpg))
#        subprocess.Popen('"%s" -jpeg %s out' % (pdftoppm_path, pdf_file))


def ImagetoText():
    path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/imageFiles'
    # path for the folder for getting the output
    tempPath = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/textFiles'
    for imageName in os.listdir(path):
        print(imageName)
        if imageName.endswith('.jpg'):
            imagePath = os.path.join(path, imageName)
            img = Image.open(imagePath)
            text = pt.image_to_string(img, lang="eng")
            txtName = imageName[0:-4]
            fullTempPath = os.path.join(tempPath, txtName + ".txt")
            print(text)
            # saving the  text for every image in a separate .txt file
            file1 = open(fullTempPath, "w")
            file1.write(text)
            file1.close()


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def readOneCol(txtfile, startline, fileLength):
    print(txtfile)
    f = open(txtfile, "r")
    text = []
    endline = False
    for line in range(startline, fileLength):
        f1 = f.readline(1)
        if f1 != '\n':
            text = text + [f1]
        else:
            endline = line
    return text, endline


path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/cleanedimageRotated'
output_path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/CleanRotatedExcel'


def ImagetoXls(path, output_path):
    for imageName in os.listdir(path):
        print(imageName)
        if imageName.endswith('.jpg'):
            inputPath = os.path.join(path, imageName)
            output = os.path.join(output_path, imageName[0:-4] + '.xlsx')
            img = Image.open(inputPath)
            # applying ocr using pytesseract for python
            text = pt.image_to_data(img, output_type='data.frame')
            text = text.dropna()
            lines = text[['line_num']].drop_duplicates()
            #line = 1
            #df = text.loc[text['line_num'] == line]
            #block_nums = df[['block_num']].drop_duplicates().values.tolist()
            #block_nums = list(itertools.chain.from_iterable(block_nums))
            #df_dat = pd.DataFrame(columns=block_nums)
            #df_all = df_dat
            df_all = pd.DataFrame()
            for line in range(0, lines.shape[0]+1):
                df = text.loc[text['line_num'] == line]
                block_nums = df[['block_num']
                                ].drop_duplicates().values.tolist()
                block_nums = list(itertools.chain.from_iterable(block_nums))
                df_dat = pd.DataFrame(columns=block_nums)
                print('line ', line)
                for block in block_nums:
                    dat = df.loc[df['block_num'] == block]
                    dat = dat[['text']].values.tolist()
                    block_data = list(itertools.chain.from_iterable(dat))
                    block_data = ["|".join(block_data)]
                    df_dat[block] = block_data
                df_all = df_all.append(df_dat)
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df_all.to_excel(writer, index=False, na_rep='N/A')
                writer.save()
                writer.close()

# some text is being missed possibly due to skew

# https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/


path = "D:\WorkDocs\Documents\Prashanti_Docs\Golwilkar_lab_reports\printed_report_list\single_page\imageFiles\Reports_from_Golwilkarrotate_1-1.jpg"

path = os.path.join(path)
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", '--path')
#ap.parse_args("-i", "--path")
#args = vars(ap.parse_args())
# load the image from disk
#image = cv2.imread(args["path"])
path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/imageFiles'
output_path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/cleanedimageRotated'


def ImageCleanunSkew(path, output_path):
    for imageName in os.listdir(path):
        print(imageName)
        if imageName.endswith('.jpg'):
            if '_06_' in imageName:
                newName = imageName.split('06_')[1]
            else:
                newName = imageName
            if '0' in newName:
                newName = newName.replace('0', 'o')
            print(newName)
            inputPath = os.path.join(path, imageName)
            newPath = os.path.join(path, newName)
            os.rename(inputPath, newPath)
            output = os.path.join(output_path, newName)
            image = cv2.imread(newPath)
            # remove small black line on sides of image
            # left side
            white = (255, 255, 255)
            x2 = 50
            y2 = image.shape[0]
            x1 = 0
            y1 = 0
            left_rectangle = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            image = cv2.fillConvexPoly(
                image, np.array(left_rectangle, 'int32'), white)
            x1 = image.shape[1]
            x2 = x1 - 50
            y2 = image.shape[0]
            y1 = 0
            right_rectangle = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
            image = cv2.fillConvexPoly(
                image, np.array(right_rectangle, 'int32'), white)
            # convert the image to grayscale and flip the foreground
            # and background to ensure foreground is now "white" and
            # the background is "black"
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bitwise_not(gray)
            # threshold the image, setting all foreground pixels to
            # 255 and all background pixels to 0
            thresh = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # grab the (x, y) coordinates of all pixel values that
            # are greater than zero, then use these coordinates to
            # compute a rotated bounding box that contains all
            # coordinates
            coords = np.column_stack(np.where(thresh > 0))
            angle = cv2.minAreaRect(coords)[-1]
            # the `cv2.minAreaRect` function returns values in the
            # range [-90, 0); as the rectangle rotates clockwise the
            # returned angle trends to 0 -- in this special case we
            # need to add 90 degrees to the angle
            if angle < -45:
                angle = -(90 + angle)
            # otherwise, just take the inverse of the angle to make
            # it positive
            else:
                angle = -angle
            # rotate the image to deskew it
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
            gray = cv2.bitwise_not(gray)
            # threshold the image, setting all foreground pixels to
            # 255 and all background pixels to 0
          #  (thresh, bwimage) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            (thresh, blackAndWhiteImage) = cv2.threshold(
                grayImage, 127, 255, cv2.THRESH_BINARY)
            cv2.imwrite(output, blackAndWhiteImage)
        print(output, ' created')


path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/imageFiles'
output_path = 'D:/WorkDocs/Documents/Prashanti_Docs/Golwilkar_lab_reports/printed_report_list/single_page/imageRotated'
newName = imageName.split('06_')[1]
if '0' in newName:
    newName = newName.replace('0', 'o')
print(newName)
inputPath = os.path.join(path, imageName)
newPath = os.path.join(path, newName)
os.rename(inputPath, newPath)
output = os.path.join(output_path, newName)
image = cv2.imread(newPath)
# convert the image to grayscale and flip the foreground
# and background to ensure foreground is now "white" and
# the background is "black"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
if angle < -45:
    angle = -(90 + angle)
# otherwise, just take the inverse of the angle to make
# it positive
else:
    angle = -angle
# rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(
    image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite(output, rotated)
print(output, ' created')
x1, y1 = coords[0]
x2, y2 = coords[1]


rect = cv2.rectangle(image, x1, y2, 150)
#x2 = coords[1][0]
x2 = 50
y2 = image.shape[1]
x1 = 0
y1 = 0
rectangle = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
cv2.fillConvexPoly(image, np.array(rectangle, 'int32'), (0, 0, 0))
cv2.fillPoly(image, (0, 0), (100, 1754), (255, 255, 255))
y2_ = image.shape

cv2.are

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

rotated = cv2.warpAffine(
    image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
