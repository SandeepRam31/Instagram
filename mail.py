import smtplib
import os
from email.message import EmailMessage
import imghdr
import glob
from datetime import date
import shutil
import time
import email
import traceback 
import imaplib

ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "pyproject101" + ORG_EMAIL 
FROM_PWD = "sandeepram" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

def send(SUBJECT, SEND = 'pyproject101@gmail.com', body='', attachments = True):
    
    EMAIL_ADDRESS = 'pyproject101@gmail.com'
    EMAIL_PASSWORD = 'sandeepram'

    msg =EmailMessage()
    msg['Subject'] = SUBJECT
    msg['To'] = SEND
    msg['From'] = EMAIL_ADDRESS
    msg.set_content(body)

    if attachments:

        PATH = os.path.join(os.getcwd(), 'pdf_files', os.listdir(os.path.join(os.getcwd(), 'pdf_files'))[0])

        with open(PATH, 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='pdf', filename=PATH)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        try:
            shutil.rmtree(os.path.join(os.getcwd(), 'pdf_files'))
            os.mkdir(os.path.join(os.getcwd(), 'pdf_files'))
        except:
            print('UNABLE TO REMOVE PDF DIRECTORY')
    else:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def read_email_from_gmail(sender, subject):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    # email_subject = msg['subject']
                    # email_from = msg['from']
                    if subject in msg['subject'] and sender in msg['from']:
                        # print('From : ' + email_from + '\n')
                        # print('Subject : ' + email_subject + '\n')
                        return get_body(msg).decode('utf-8')

    except Exception as e:
        print(e)

# Accepting and processing replys
# Adding multiple images as attachments
