import nltk
import imaplib, email
import pandas as pd

my_host = input('Host:\t')
my_user = input('Username:\t')
my_pass = input('Password:\t')
imap_obj = imaplib.IMAP4_SSL(host=my_host)
imap_obj.login(user=my_user, password=my_pass)
#%%
dir_list = [d.decode().split(' "/" ')[1] for d in imap_obj.list()[1]]
#%%
from bs4 import BeautifulSoup
msg_df = pd.DataFrame()

msg_list = []
for dir in dir_list[0:2]:
    status, messages = imap_obj.select(dir)

    if status != "OK": exit("Incorrect mail box")


    for i in range(1, int(messages[0])):
        res, msg = imap_obj.fetch(str(i), '(RFC822)')
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():

                        tmp_dict = {}
                        tmp_dict['To'] = msg['To']

                        tmp_dict['Subject'] = email.header.decode_header(msg['Subject'])[0]

                        tmp_dict['From'] = msg['From']
                        try:
                            tmp_dict['Content'] = msg.get_payload(decode=True)
                        except:
                            pass

                        tmp_dict['Labels'] = dir.strip('"')
                        msg_df = msg_df.append(tmp_dict, ignore_index=True)
#%%
imap_obj.logout()

#%%

import html2text

def parse_email_body(self, email):
    """
    Parse the body of the given email message.
    Returns a dictionary containing the plaintext and HTML versions of the body.
    """
    body = {"text": "", "zhtml": ""}
    if email.is_multipart():
        for part in email.get_payload():
            if part.get_content_type() == "text/plain":
                body["text"] = self.remove_special_chars(part.get_payload())
            elif part.get_content_type() == "text/html":
                body["zhtml"] = html2text.html2text(part.get_payload())
    else:
        body["text"] = email.get_payload()
    return body



