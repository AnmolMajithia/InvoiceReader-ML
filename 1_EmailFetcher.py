import email
import imaplib
import os

detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')
usr='pleasehackme6548@gmail.com'
pswd='testeraccount123'
imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login(usr, pswd)
if typ != 'OK':
    print('Not able to sign in!')
imapSession.select('"[Gmail]/All Mail"')
typ, data = imapSession.search(None, 'ALL')
if typ != 'OK':
    print('Error searching Inbox.')
for msgId in data[0].split():
    typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
    if typ != 'OK':
        print('Error fetching mail.')
    emailBody = messageParts[0][1].decode('utf-8')
    mail = email.message_from_string(emailBody)
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(detach_dir, 'attachments', fileName)
            if not os.path.isfile(filePath) :
                print(fileName)
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
imapSession.close()
imapSession.logout()
