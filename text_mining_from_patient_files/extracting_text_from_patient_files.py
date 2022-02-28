import os
import re
import shutil
import pytesseract as pt
from pdf2image import convert_from_path
from PIL import Image
import cv2

pt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def convert_pdf_to_img_then_txt(patients_files_path, jpg_folder_path):
    pdf_files = os.listdir(patients_files_path)
    for pdf_file in pdf_files:
        if pdf_file.endswith('.pdf'):
            pages = convert_from_path(os.path.join(patients_files_path, pdf_file), 500,
                                      poppler_path = 'C:/Program Files/poppler-0.68.0/bin')
            i = 0
            for index, page in enumerate(pages):
                if i == index:
                    file_name = pdf_file.lower()
                    file_name = re.sub('.pdf', '', file_name)
                    out_jpg = file_name + '_' + str(i) + '.jpg'
                    page.save(os.path.join(jpg_folder_path, out_jpg), 'JPEG')
                    print(out_jpg)
                    img = Image.open(os.path.join(jpg_folder_path, out_jpg))
                    text = pt.image_to_string(img, lang="eng")
                    txt_file_name = re.sub('.pdf', '', out_jpg)
                    txt_file_path = os.path.join(jpg_folder_path, txt_file_name + ".txt")
                    # print(text)
                    file1 = open(txt_file_path, "w")
                    file1.write(text)
                    file1.close()
                i += 1

convert_pdf_to_img_then_txt('D:/Shweta/path_reports/scanned_patient_files_from_server',
                            'D:/Shweta/path_reports/scanned_patient_files_from_server/jpg_txt_files')

def extract_text_from_image(folder_path, txt_file_folder_path):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.jpg'):
            image = cv2.imread(os.path.join(folder_path, file))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
            cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

            repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
            result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=1)

            text = pt.image_to_string(result, lang='eng', config='--psm 3')
            file_name = re.sub('.jpg', '', file)
            new_file_name = file_name + '.txt'
            txt_file_path = os.path.join(txt_file_folder_path, new_file_name)
            file1 = open(txt_file_path, "w")
            file1.write(text)
            file1.close()

extract_text_from_image('D:/Shweta/path_reports/scanned_patient_files_from_server/jpg_txt_files',
                        'D:/Shweta/path_reports/scanned_patient_files_from_server/txt_files_from_img')

##### text mining from file txt #######

def get_report_text_into_list(file_path):
    file = open(file_path, 'rt')
    lines = []
    for line in file:
        line_txt = line.strip(':, \n')
        if line_txt.isdigit():
            lines.append(line_txt)
        else:
            line_txt_cleaned = line_txt.lower()
            lines.append(line_txt_cleaned)
    file.close()
    return lines

def get_unique_value_from_list(list_with_duplicate_values):
    unique_list = []
    for value in list_with_duplicate_values:
        if value not in unique_list:
            unique_list.append(value)
    output_lst = [line for line in unique_list if line]
    return output_lst

def classify_report_by_type(text_lst, cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    text_lst_str = str(text_lst)
    if cytology_keyword in text_lst_str:
        return 'cytology'
    elif histology_keyword in text_lst_str:
        return 'histology'
    elif ihc_keyword in text_lst_str:
        return 'immunohistochemistry'
    elif blood_count_keyword in text_lst_str:
        return 'complete_blood_count'
    elif ki_keyword in text_lst_str:
        return 'ki67'
    elif glucose_keyword in text_lst_str:
        return 'plasma_glucose'
    elif any(x in text_lst_str for x in nutrient_keyword):
        return 'nutrient_report'
    elif liver_keyword in text_lst_str:
        return 'liver_function_test'
    else:
        return 'type_not_found'

def find_and_move_ihc_reports_from_file(txt_folder_path, destination_path, cytology_keyword = 'cytology',
                            histology_keyword = 'histology', ihc_keyword = 'immunohistochemistry',
                            blood_count_keyword = 'blood count', ki_keyword = 'ki 67', glucose_keyword = 'glucose',
                            liver_keyword = 'liver', nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum']):
    txt_files = os.listdir(txt_folder_path)
    for file in txt_files:
        file_path = os.path.join(txt_folder_path, file)
        txt_lst = get_report_text_into_list(file_path)
        txt_lst_unique = get_unique_value_from_list(txt_lst)
        report_type = classify_report_by_type(txt_lst_unique, cytology_keyword, histology_keyword, ihc_keyword,
                             blood_count_keyword, ki_keyword, glucose_keyword, liver_keyword, nutrient_keyword)

        if report_type == 'cytology' or report_type == 'histology' or report_type == 'immunohistochemistry' :
            src_path = os.path.join(txt_folder_path, file)
            dest_path = os.path.join(destination_path, file)
            shutil.copy(src_path, dest_path)

destination_path = 'D:/Shweta/path_reports/scanned_patient_files_from_server/ihc_reports_from_file'
txt_folder_path = 'D:/Shweta/path_reports/scanned_patient_files_from_server/txt_files_from_img'

find_and_move_ihc_reports_from_file(txt_folder_path, destination_path, cytology_keyword = 'cytology', histology_keyword = 'histology',
                            ihc_keyword = 'immunohistochemistry', blood_count_keyword = 'blood count',
                            ki_keyword = 'ki 67', glucose_keyword = 'glucose', liver_keyword = 'liver',
                            nutrient_keyword = ['vitamin', 'calcium', 'phosphorus', 'urea', 'serum'])

