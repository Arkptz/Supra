from csv import excel
import imaplib
import email
from time import time
from bs4 import BeautifulSoup as bs
from email.message import Message


class Imap:
    host: str = 'imap.rambler.ru'
    message_count: int = 0
    msg:Message = ''

    def __init__(self, login, password, host='imap.rambler.ru') -> None:
        self.host = host
        self.connect = imaplib.IMAP4_SSL('imap.rambler.ru')
        self.connect.login(login, password)
        self.connect.list()

    def update_message_count(self) -> int:
        status, messages = self.connect.select("inbox")
        self.message_count = int(messages[0])
        return self.message_count

    def wait_new_letter(self, timeout = 60) -> Message:
        start_time = time()
        message_count = self.message_count
        while message_count == self.message_count:
            if time() - start_time > 60:
                raise
            self.update_message_count()
        res, msg = self.connect.fetch(str(self.message_count), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                self.msg = msg
                return msg

    def supra_pars(self) -> str:
        msg = self.msg.as_string()
        page = bs(msg, 'lxml')
        link = page.find_all('a')[1]
        
        return link.text.replace('=\n','').replace('3D', '')
