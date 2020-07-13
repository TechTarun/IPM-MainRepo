# Final Ok From my side
import imaplib
import email
import mailparser
import extract_key as ek
import re
import web_speech2text as s2t
import web_text2speech as t2s
import name_extractor as n
import create_email

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def single_email_search(username, password, criteria):
    """This function will search for a particular mail as per the defined criteria"""
    attach_list = list()
    mail_list = list()
    FROM_EMAIL = username
    FROM_PWD = password
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')
    type, data = mail.search(None, *criteria)
    # search and return uids instead
    i = len(data[0].split())  # data[0] is a space separate string
    if (i == 0):  # if there are no mails found, i==0
        return ("No mails!!")
    latest_email_uid = data[0].split()[-1]  # unique ids wrt label selected
    result, email_data = mail.fetch(latest_email_uid, '(RFC822)')
    # fetch the email body (RFC822) for the given ID
    raw_email = email_data[0][1]
    # continue inside the same for loop as above
    raw_email_string = raw_email.decode('utf-8')
    email = mailparser.parse_from_string(raw_email_string)
    attach = email.attachments
    if (len(attach) > 0):
        for i in range(len(attach)):
            attach_list.append(attach[i]['filename'])
    content = "Email from " + email.from_[0][1] + " dated " + str(
        email.date) + " on the subject " + email.subject + " is " + remove_html_tags(str(email.text_html))
    mail_list.append([content, attach_list])
    return (mail_list)
    mail.close()
    mail.logout()


def all_email_search(username, password, criteria):
    attach_list = list()
    mail_list = list()
    """This function will return all the mails satisfying the defined criteria"""
    FROM_EMAIL = username
    FROM_PWD = password
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')
    type, data = mail.search(None, *criteria)
    # search and return uids instead
    i = len(data[0].split())  # data[0] is a space separate string
    if (i == 0):
        print("No mails!!")
        t2s.say("No mails!!")
        return
    else:
        print("Total number of mails are",i)
    t2s.say("Total number of mails are " + str(i))
    t2s.say("want to see all the mails")
    choice = s2t.listen()
    print(choice)
    if ('yes' in choice or 'yups' in choice or 'ok' in choice or 'yaa' in choice or 'sure' in choice):
        for a in range(i):
            latest_email_uid = data[0].split()[a]  # unique ids wrt label selected
            result, email_data = mail.fetch(latest_email_uid, '(RFC822)')
            # fetch the email body (RFC822) for the given ID
            raw_email = email_data[0][1]
            # continue inside the same for loop as above
            raw_email_string = raw_email.decode('utf-8')
            email = mailparser.parse_from_string(raw_email_string)
            attach = email.attachments
            if (len(attach) > 0):
                for i in range(len(attach)):
                    attach_list.append(attach[i]['filename'])
            print("Email from " + email.from_[0][1] + " dated " + str(
                email.date) + " on the subject " + email.subject + " is " + remove_html_tags(str(email.text_html)))
            content = "Email from " + email.from_[0][1] + " dated " + str(
                email.date) + " on the subject " + email.subject + " is " + remove_html_tags(str(email.text_html))
            print("------------------------------")
            t2s.say("Email from " + email.from_[0][1] + " dated " + str(
                email.date) + " on the subject " + email.subject + " is " + remove_html_tags(str(email.text_html)))
            mail_list.append([content, attach_list])
        return (mail_list)
    else:
        main(choice, criteria)
    mail.close()
    mail.logout()


def single_mail(username, password, text, criteria):
    """This function decides the criteria for searching a particular mail"""
    if ('from' in text or 'of' in text):
        sender = n.get_sender(text.title())
        if (sender == None):
            print("Im in if")
            response = "Sender not recognized!!"
            print(response)
            t2s.say(response)
            return
        else:
            print("I am in else")
            criteria.extend(['From', sender[0], 'From', sender[1]])
            print(criteria)
    if ('subject' in text):
        sub_pos = text.find("subject") + 8
        sub_text = text[sub_pos:]
        print(sub_text)
        subject = ek.extract(sub_text)[0]
        criteria.extend(['Subject', subject])
    response = single_email_search(username, password, criteria)
    t2s.say(response)
    return (response)


def all_mails(username, password, text, criteria):
    """This function decides the criteria for searching all the mails"""
    if ('from' in text or 'of' in text):
        sender = n.get_sender(text.title())
        if (sender == None):
            response = "Sender not recognized!!"
            print(response)
            t2s.say(response)
            return
        else:
            criteria.extend(['From', sender[0], 'From', sender[1]])
    if ('subject' in text):
        sub_pos = text.find("subject") + 8
        sub_text = text[sub_pos:]
        print(sub_text)
        subject = ek.extract(sub_text)[0]
        criteria.extend(['Subject', subject])
    print(criteria)
    mail = all_email_search(username, password, criteria)
    return (mail)


# -----main-------
def main(text, criteria):
    username = "testitonpython@gmail.com"
    password = 'test_password'
    if('send' in text):
        t2s.say("Enter message")
        content = s2t.listen()
        create_email.send_mail(content)
        mail = "done!!"
    elif ('mails' in text or 'emails' in text or 'all' in text):
        mail = all_mails(username, password, text, criteria)
    elif ('mail' in text or 'email' in text):
        mail = single_mail(username, password, text, criteria)
    else:
        t2s.say("define the query properly!!")
    return mail
