from PIL import Image
import pytesseract as pt
import os
import numpy as np
import cv2

def main():
    # path for the folder for getting the raw images
    path = "D:\\WorkDocs\\Documents\\Prashanti_Docs\\Digitised_files\\123_10\\test_image_text"

    # path for the folder for getting the output
    tempPath = "D:\\WorkDocs\\Documents\\Prashanti_Docs\\Digitised_files\\123_10\\test_image_text\\text_output"

    # iterating the images inside the folder
    for imageName in os.listdir(path):
        inputPath = os.path.join(path, imageName)
        img = Image.open(inputPath)

        # applying ocr using pytesseract for python
        text = pt.image_to_string(img, lang="eng")
        # not sure what convert('L') does - make image Grayscale
        img = Image.open(imageName).convert('L')
        ret, img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
        # img = Image.fromarray(img.astype(np.uint8))
        text = pt.image_to_string(img, lang='eng')
        # threshold image to
        # for removing the .jpg from the imagePath
        imagePath = imagePath[0:-4]

        fullTempPath = os.path.join(tempPath, 'time_' + imageName + ".txt")
        print(text)

        # saving the  text for every image in a separate .txt file
        file1 = open(fullTempPath, "w")
        file1.write(text)
        file1.close()
# see for tips
# https://stackoverflow.com/questions/53797130/empty-string-with-tesseract

if __name__ == '__main__':
    main()

