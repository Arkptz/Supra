from dataclasses import dataclass
from loguru import logger
import sys
import base64


@dataclass
class data_cl:
    string:str
    mail:str=None
    pass_mail:str=None
    check:bool = False
    def __init__(self, string:str) -> None:
        self.string = string
        spl_string = string.split(':')
        ln = len(spl_string)
        if ln == 2 :
            self.mail, self.pass_mail = spl_string
        else:
            print(f'Ошибка ввода данных: {string}')
            sys.exit()


