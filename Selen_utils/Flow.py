import multiprocessing
from multiprocessing.synchronize import Lock
from typing import Callable
from dataclasses import dataclass
from colorama import Fore
import logging as log
import os
import pandas as pd
from time import sleep, time
import random
import traceback
import warnings
import pathlib
from seleniumwire import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from fake_useragent import UserAgent
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import seleniumwire.undetected_chromedriver as uc
import logging as log
from .proxy import Proxy_Class
from .Services.Anti_Captcha.captcha import Captcha, Selen
from csv_utils import CsvCheck
from Selen_utils.statuses import Statuses
ua = UserAgent()
warnings.filterwarnings("ignore")
a_z = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-2])

LOGGER.setLevel(log.WARNING)
@dataclass
class Flow(Captcha, Selen):
    data: str
    Lock: Lock
    proxy_list: list = None
    delay: str = '0'
    ip: str = None
    csv: CsvCheck = None
    count_accs: int = None
    data_q: multiprocessing.Queue = None
    proxy: Proxy_Class | None = None
    count_make_accs: multiprocessing.Value = None
    excel_file: CsvCheck = None
    ads = False
    driver: webdriver.Chrome = None
    wait: WebDriverWait = None

    def start_driver(self, ads=False, local_url_ads: str = None):
        self.activate_delay()
        log.info('СТарт драйвера')
        if ads:
            from .Services.ads import AdsWithSelen
            self.ads = AdsWithSelen(
                base_url_ads=local_url_ads, lock=self.Lock, proxy=self.proxy)
            self.driver = self.ads.start_browser()
        else:
            options = {}
            if self.proxy:
                options['proxy'] = {'http': f'http://{self.proxy.url_proxy}',
                                    'http': f'https://{self.proxy.url_proxy}', }
            options_c = Options()
            options_c.add_argument(
                '--disable-blink-features=AutomationControlled')
            # options = {'proxy':
            #            {'http': f'http://{self.proxy.url_proxy}',
            #             'http': f'https://{self.proxy.url_proxy}', }}
            options_c.add_argument(f"user-agent={ua.random}")
            options_c.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            # if metamask:
            #     # options_c.add_extension(
            #     #     metamask_path)
            #     metamask_path = str(pathlib.Path(metamask_path).absolute())
            #     # options_c.add_argument(f'--load-extension={metamask_path}')
            #     options_c.add_extension(metamask_path)
            self.driver = webdriver.Chrome(
                options=options_c,  service_log_path='NUL', seleniumwire_options=options)
        self.driver.set_window_size(1700, 1080)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # if metamask:
        #     self.metamask_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/'
        #     window_name = 'metamask'
        #     self.wait.until(EC.number_of_windows_to_be(2))
        #     for i in self.driver.window_handles:
        #         self.driver.switch_to.window(i)
        #         if window_name in self.driver.title.lower():
        #             self.metamask_url = self.driver.current_url.split('/home')[0] + '/'
        #             break

    def activate_delay(self):
        d = self.delay
        if d == '0':
            return ''
        elif '-' in d:
            first, two = map(float, d.split('-'))
            sleep(random.randint(int(round(first*60, 0)), int(round(two*60, 0))))
        else:
            sleep(int(round(float(d)*60, 0)))

    def close_driver(self):
        self.driver.quit()
        if self.ads:
            self.ads.close_and_delete_browser()

    def zapysk(self, list_func: list[Callable]):
        res = Statuses.success
        for i in list_func:
            try:
                i()
            except:
                res = Statuses.error
                log.error(f'{self.data} -- {traceback.format_exc()}')
        if self.count_make_accs:
            self.count_make_accs.value += 1
            txt = f'{self.count_make_accs.value}/{self.count_accs}'
        if res == Statuses.error:
            if self.count_make_accs:
                print(Fore.RED + txt)
                log.info(f'{txt}')
            try:
                self.driver.save_screenshot(
                    f'{homeDir}\\Screenshots_error\\{self.data.string}.png')
            except Exception as e:
                log.error(
                    f'{self.data} -- {traceback.format_exc()}')
        else:
            if self.count_make_accs:
                print(Fore.GREEN + txt)
        self.close_driver()
        if self.proxy:
            self.proxy_list.append(self.proxy)
        _data = {'mail': self.data.mail, 'mail_pass': self.data.pass_mail,
                 'result': f'{res}', 'check':self.data.check}
        self.excel_file.add_string(_data)
        self.csv.add_string({'data': f'{self.data.string}'})
