import imaplib
import time
from fake_useragent import UserAgent
import requests

#code = input("Ref code: ")

ua = UserAgent()


def read_mails():
    """ Чтение почт с текстовика"""
    address_pass = {}
    with open("mails.txt", "r") as file:
        mails = file.readlines()

    for i in mails:
        mail_date = i.split(":")
        address_pass[mail_date[0]] = mail_date[1]

    return address_pass


def get_code_from_rambler(login, password):
    ''' Отвечает за вход на почту и поиск кода для регистрации на сайте'''
    mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    mail.login(login, password)
    mail.list()
    mail.select("inbox")
    result, data = mail.search (None, "ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    latest_email_id
    result, data = mail.fetch(latest_email_id,'(RFC822)')
    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    mail = raw_email.decode('UTF-8')
    el = mail.find("Your verification code")
    els = []
    for k in range (24,30):
        t = el+k
        els.append (mail[t])
    code = ""
    return code.join(els)


def enter_wallet(token):
    '''пока-что не используется'''
    headers = {
        'Authorization': 'Bearer ' + token,
        'Connection': 'keep-alive',
        'User-Agent': ua.random,
    }

    json_data = {
        'wallet': '0x9281244dc7fF5f1e212FD5a67A04f48ab37f94A3',
    }

    response = requests.patch('https://api.step.app/v1/user/me', headers=headers, json=json_data).text
    return response


def main():
    mails = read_mails()

    for mail, password in mails.items():
        session = requests.Session()
        reg_mail = requests.get(f"https://api.step.app/v1/auth/otp-code?email={mail}")  # отправка кода на почту
        time.sleep(5)
        code = get_code_from_rambler(login=mail, password=password)   # получение кода с почты
        time.sleep(5)
        token = requests.get(f"https://api.step.app/v1/auth/token?email={mail}&code={code}").json()["access"]["token"]  # подтверждение почты и токен для подтверждения кошелька

        '''
        
        тут должен быть код, для использования реф. кода
        
        '''


print(get_code_from_rambler("shcherbakova.ailin.1962@lenta.ru", "zJZFNmxKg4"))