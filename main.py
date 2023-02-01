from Selen_utils import Proxy_Class, Captcha, Flow, Statuses
from csv_utils import Execute, CsvCheck
from data_class import data_cl
import config as cf
import multiprocessing
import logging as log
import imaplib
import queue
from seleniumwire import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementClickInterceptedException
from dataclasses import dataclass
from threading import Thread
import asyncio
import traceback
import os
from uuid6 import uuid8
import pandas as pd
from time import sleep, time
from imap import Imap
import random
import warnings
ua = UserAgent()
warnings.filterwarnings("ignore")
a_z = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])

datas = cf.datas
csv = cf.csv
excel_file = CsvCheck(name_file=rf'{homeDir}\\result.xlsx', colums_check=[
                          'mail', 'mail_pass','check' 'result'], type_file='excel')

class Supra(Flow):
    data: data_cl

    def restart_driver(self):
        log.info(f'{self.data} -- restart_driver')
        if self.driver:
            self.close_driver()
        # metamask_path = f'{homeDir}\\files\\metamask.crx'#f'{homeDir}\\files\\nkbihfbeogaeaoehlefnkodbefgpgknn\\10.24.1_0'
        self.start_driver(
            ads=True, local_url_ads=cf.url_ads)

    def go(self,):
        if self.proxy:
            if self.proxy.proxy_link:
                self.proxy.change_ip()
        log.info(f'Старт потока {self.data}')
        self.restart_driver()
        if not self.data.check:
            self.get_new('https://supraoracles.com/blastoff?ref=07a2f-93415')
            self.wait_click('//div[contains(@class, "[#294D7A]")]')
            self.wait_click(
                '//div[@class="bg-primary transation cursor-pointer rounded p-3 duration-150 ease-in-out hover:bg-opacity-80 sm:px-5"]')
            self.wait_send(
                '//input[@class="input cc5fc8d49 ce4208c50"]', self.data.mail)
            self.wait_send(
                '//input[@class="input cc5fc8d49 c9ad7de0b"]', self.data.pass_mail)
            imap = Imap(self.data.mail, self.data.pass_mail)
            imap.update_message_count()
            self.wait_click('//button[@type="submit"]')
            self.wait_and_return_elem(
                '//h4[@class="max-w-[33rem] text-lg font-bold leading-6 md:text-[1.375rem] md:leading-7"]', timeout=90)
            imap.wait_new_letter()
            link = imap.supra_pars()
            self.get_new(link)
            self.wait_and_return_elem('//h2[.="Welcome to the crew!"]')
            sleep(2)
            self.get_new('https://supraoracles.com/blastoff')
            self.wait_click('//div[contains(@class, "[#294D7A]")]')
            self.wait_click('''//a[.="Let's Go"]''')
            self.wait_click('//button[.="Enter Now"]', timeout=60)
            sleep(2)
            self.get_new('https://supraoracles.com/blastoff')
            self.wait_click('//div[contains(@class, "[#294D7A]")]')
            #self.wait_click('//button[.="Continue"]')
            self.wait_click('''//a[.="Let's Go"]''')
            self.wait_click('//button[contains(@class,"whitespace-nowrap font-bold text-white md:text-lg")]')#copy_link
            self.wait_click('//button[.="Continue"]')
            #self.get_new('https://supraoracles.com/blastoff/ru/learn')
            self.wait_click('//a[.="Start Mission"]')
            self.wait_click('//button[.="Start Mission"]', timeout=90)
            self.wait_click('//p[contains(.,"All of the above.")]')
            self.wait_and_return_elem('//div[.="Completed"]')
            self.get_new('https://supraoracles.com/blastoff')
            self.wait_click('//div[contains(@class, "[#294D7A]")]')
            self.wait_click('''//a[.="Let's Go"]''')
            self.wait_click('//button[contains(.,"Continue")]')
            self.wait_and_return_elem('//h6[.="Well done!"]')
            self.wait_click('//button[.="Continue"]')
            self.wait_click('//a[.="Start KYC"]')
            self.wait_click('//button[contains(.,"Start KYC")]')
            self.wait_click('//button[.="Accept"]')
            self.wait_click('//button[@data-onfido-qa="welcome-next-btn"]',timeout=60)
            self.wait_click('//input[@aria-describedby="country-search__assistiveHint"]')
            self.wait_click('//li[contains(.,"Indonesia")]')
            self.wait_click('//button[@data-onfido-qa="national_identity_card"]')
            self.wait_click('//button[@class="ods-button -action--primary onfido-sdk-ui-Theme-button-centered onfido-sdk-ui-Theme-button-lg onfido-sdk-ui-Uploader-crossDeviceButton"]')
            self.wait_click('//button[@data-onfido-qa="cross-device-continue-btn"]')
            self.wait_click('//a[@data-onfido-qa="cross-device-copy_link-link-option"]')
            elem = self.wait_and_return_elem('//span[@class="onfido-sdk-ui-crossDevice-CrossDeviceLink-linkText"]')
            url = elem.text
            from Tg_bot.bot import send_data
            asyncio.run(send_data(self.data, url))
            #self.wait_click('//button[.="Continue"]')
            return Statuses.success
        else:
            self.get_new('https://supraoracles.com/blastoff')
            self.wait_click('//button[.="Sign In"]')
            self.wait_send(
                '//input[@id="username"]', self.data.mail)
            self.wait_send(
                '//input[@id="password"]', self.data.pass_mail)
            self.wait_click('//button[@type="submit"]')
            self.wait_click('//div[contains(@class, "[#294D7A]")]')
            elem = self.wait_and_return_elem('//div[@class="bg-midnight flex items-center justify-evenly rounded-lg p-2 lg:space-x-10 lg:px-10 lg:py-0"]')
            name_file = f'{homeDir}/screen_kyc/{uuid8()}.png'
            elem.screenshot(name_file)
            from Tg_bot.bot import send_screen
            asyncio.run(send_screen(name_file, self.data))
            return Statuses.success

    def start(self,):
        self.zapysk([self.go])


def launch():
    m = multiprocessing.Manager()
    counter = multiprocessing.Value('i', 0)
    global proxy_list
    proxy_list = m.list()
    excel_file.check_file()
    data_q = datas.get_queue()
    
    with open(f'{homeDir}\\txt\\proxy.txt') as file:
        for i in file.read().split('\n'):
            prox = Proxy_Class(i)
            proxy_list.append(prox)
    with open(f'{homeDir}\\stop.txt', 'w') as file:
        pass
    global Lock
    Lock = multiprocessing.Lock()
    print(f'Кол-во данных - {datas.count_args}')
    threads_count = int(
        input(f"Сколько потоков требуется (Прокси указано - {len(proxy_list)})? - "))
    delay = input('Задержка(либо 1-2, либо 0) - ')
    flow = 0
    while True:
        while (not data_q.empty()):
            while len(multiprocessing.active_children())-1 >= threads_count:
                sleep(1)
            for i in range(threads_count-len(multiprocessing.active_children())+1):
                if (not data_q.empty()) and len(proxy_list) > 0:
                    with open(f'{homeDir}\\stop.txt', 'r') as file:
                        if 'true' in file.read():
                            continue
                    data = data_q.get()
                    proxx = random.choice(proxy_list)
                    # proxx.change_ip()
                    proxy_list.remove(proxx)
                    t = multiprocessing.Process(
                        target=Supra(data=data, proxy=proxx, data_q=data_q, Lock=Lock, proxy_list=proxy_list,
                                    delay=delay, csv=csv, count_accs=datas.count_args,
                                    count_make_accs=counter, excel_file=excel_file).start)
                    t.start()
                    flow += 1
        while len(multiprocessing.active_children()) != 1:
            sleep(1)
        break

if __name__ == '__main__':
    launch()

