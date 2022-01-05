import pandas as pd
import tabula
import os
import pytesseract as pt
import cv2
import itertools
from PIL import Image

pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pdf_folder_path = "D:/Shweta/email/fish_reports/from_vandana's_email"
folder_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files'
output_path = 'D:/Shweta/path_reports/Histopath_reports_from_server/Biopsy/bx_img_txt_files/img_df'
file_name = '2100121523.pdf'
img_name = '06_20_bx_1.jpg'

table_df = tabula.read_pdf(os.path.join(pdf_folder_path, file_name), pages = 'all', encoding="utf-8")
df = pd.DataFrame(table_df)

i = 0
for table in table_df:
    table.to_excel('output'+str(i)+'.xlsx',index=False)
    print(i)
    i=i+1
# tabula.convert_into(os.path.join(pdf_folder_path, file_name), os.path.join(pdf_folder_path, "output.csv"),
#                     output_format="csv", pages='all')

# tables = camelot.read_pdf(os.path.join(pdf_folder_path, file_name), pages='all')
##

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

ImagetoXls(folder_path, output_path)

##
img = cv2.imread(os.path.join(folder_path, img_name))
d = pt.image_to_data(img, output_type=pt.Output.DICT)

n_boxes = len(d['level'])

for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

cv2.imshow('img', img)
cv2.waitKey(0)


######
def find_tables(image):
    BLUR_KERNEL_SIZE = (17, 17)
    STD_DEV_X_DIRECTION = 0
    STD_DEV_Y_DIRECTION = 0
    blurred = cv2.GaussianBlur(image, BLUR_KERNEL_SIZE, STD_DEV_X_DIRECTION, STD_DEV_Y_DIRECTION)
    MAX_COLOR_VAL = 255
    BLOCK_SIZE = 15
    SUBTRACT_FROM_MEAN = -2

    img_bin = cv2.adaptiveThreshold(
        ~blurred,
        MAX_COLOR_VAL,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        BLOCK_SIZE,
        SUBTRACT_FROM_MEAN,
    )
    vertical = horizontal = img_bin.copy()
    SCALE = 5
    image_width, image_height = horizontal.shape
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image_width / SCALE), 1))
    horizontally_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_kernel)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(image_height / SCALE)))
    vertically_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)

    horizontally_dilated = cv2.dilate(horizontally_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1)))
    vertically_dilated = cv2.dilate(vertically_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60)))

    mask = horizontally_dilated + vertically_dilated
    contours, heirarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
    )

    MIN_TABLE_AREA = 1e5
    contours = [c for c in contours if cv2.contourArea(c) > MIN_TABLE_AREA]
    perimeter_lengths = [cv2.arcLength(c, True) for c in contours]
    epsilons = [0.1 * p for p in perimeter_lengths]
    approx_polys = [cv2.approxPolyDP(c, e, True) for c, e in zip(contours, epsilons)]
    bounding_rects = [cv2.boundingRect(a) for a in approx_polys]

    # The link where a lot of this code was borrowed from recommends an
    # additional step to check the number of "joints" inside this bounding rectangle.
    # A table should have a lot of intersections. We might have a rectangular image
    # here though which would only have 4 intersections, 1 at each corner.
    # Leaving that step as a future TODO if it is ever necessary.
    images = [image[y:y + h, x:x + w] for x, y, w, h in bounding_rects]
    return images

def main(folder_path):
    files = os.listdir(folder_path)
    results = []
    for f in files:
        directory, filename = os.path.split(f)
        image = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        tables = find_tables(image)
        files = []
        filename_sans_extension = os.path.splitext(filename)[0]
        if tables:
            os.makedirs(os.path.join(directory, filename_sans_extension), exist_ok=True)
        for i, table in enumerate(tables):
            table_filename = "table-{:03d}.png".format(i)
            table_filepath = os.path.join(
                directory, filename_sans_extension, table_filename
            )
            files.append(table_filepath)
            cv2.imwrite(table_filepath, table)
        if tables:
            results.append((f, files))
    # Results is [[<input image>, [<images of detected tables>]]]
    return results
