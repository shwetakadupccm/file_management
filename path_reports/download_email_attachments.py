import imaplib
import os
import email
import pandas as pd
import datetime

# import socket
# socket.getaddrinfo('127.0.0.1', 8080)

user = 'vcanshare@gmail.com'
password = 'Prashanti@123'
host = 'imap.gmail.com'

ag_mail_id = 'info@agdiagnostics.com'
ruby_hall_mail_id = ['labwan@rubyhall.com', 'labreports@rubyhall.com']
jeh_mail_id = ['nutan.jumle@jehangirhospital.com', 'lab@jehangirhospital.com']

mail = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
mail.login(user, password)
mail.select('Inbox')
# mail.messages(date__gt=datetime.date(2021, 10, 1))
x1 = datetime.date(2021, 10, 1)
start_date = x1.strftime('%d-%b-%Y')

type, data = mail.search(None, '(FROM "info@agdiagnostics.com")',
                         '(SENTSINCE ' + '"' + start_date + '"' + ')' )

mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join('D:/Shweta/email/after_specific_date/from_ag_2021_10_01', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print('done')

def download_email_attachment(username, password, download_attach_from = '', year = 2021, month = 10, day = 1,
                              attachments_output_folder_path = ''):

    mail = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
    mail.login(username, password)
    mail.select('Inbox')
    info = []
    start_date = datetime.date(year, month, day).strftime('%d-%b-%Y')
    type, data = mail.search(None, '(FROM ' + '"' + download_attach_from + '"' +')', '(SENTSINCE ' + '"' + start_date + '"' + ')')

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                file_path = os.path.join(attachments_output_folder_path, file_name)
                if not os.path.isfile(file_path):
                    try:
                        fp = open(file_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    except OSError:
                        print('OS-error')
                    subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
                    file_name_subject = [file_name, subject]
                    info.append(file_name_subject)
    df = pd.DataFrame(info, columns=['attchment_name', 'subject'])
    return df

df = download_email_attachment(user, password, download_attach_from = 'labreports@rubyhall.com', year = 2021, month = 12, day = 30,
                attachments_output_folder_path = "D:/Shweta/email/2022_03_03/Ruby_hall/attachments")

#                 subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
#                 print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName,
#                                                                 subject=subject,
#                                                                 uid=latest_email_uid.decode('utf-8')))
## get reprot summary

ag_reports = os.listdir('D:/Shweta/email/attachments_from_ag')
jeh_reports = os.listdir('D:/Shweta/email/attachments_from_jehangir')
ruby_hall_reports = os.listdir('D:/Shweta/email/attachments_from_ruby_hall')

ag_df = pd.DataFrame(ag_reports, columns=['AG_report_names'])
jeh_df = pd.DataFrame(jeh_reports, columns=['jehangir_report_names'])
ruby_df = pd.DataFrame(ruby_hall_reports, columns=['ruby_hall_report_names'])
combined_ag_jeh = ag_df.combine_first(jeh_df)
combined_ag_jeh_ruby = combined_ag_jeh.combine_first(ruby_df)

combined_ag_jeh_ruby.to_excel('D:/Shweta/email/output_df/2021_07_09_reports_summary_all_sk.xlsx',
                              index=False)

