import multiprocessing
from seleniumwire import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dataclasses import dataclass
import logging as log
import os
from time import sleep, time
import traceback
import warnings
ua = UserAgent()
warnings.filterwarnings("ignore")
a_z = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-2])


class Selen:
    data:str 
    Lock: multiprocessing.Lock
    driver: webdriver.Chrome = None
    wait: WebDriverWait = None

    def get_new(self, link):
        for num, i in enumerate(range(15)):
            try:
                self.driver.get(link)
                return True
            except Exception as e:
                log.error(
                    f'{self.data} -- get_new ({link}-- {traceback.format_exc()}')
            if num == 14:
                raise Exception


    def click_for_x_y(self, x, y):
        log.debug(f'{self.data} -- click ({x}, {y})')
        actions = ActionChains(self.driver)
        actions.move_by_offset(x, y).click().perform()
        actions.reset_actions()


    def check_frame_and_window(self, frame, frame_elem, window, window_elem, timeout=30) -> int:
        time_start = time()
        while time() - time_start < timeout:
            self.driver.switch_to.window(window)
            try:
                self.driver.switch_to.frame(frame)
                self.driver.find_element(By.XPATH, frame_elem)
                return 1
            except Exception as e:
                pass
            self.driver.switch_to.window(window)
            try:
                self.driver.find_element(By.XPATH, window_elem)
                return 2
            except Exception as e:
                pass
        raise TimeoutError


    def wait_many_elements(self, elems: list[str], timeout =30) -> int:
        lst = []
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.any_of(
            *[EC.visibility_of_element_located((By.XPATH, elem)) for elem in elems]))
        for num, i in enumerate(elems):
            try:
                self.driver.find_element(By.XPATH, i)
                return num+1
            except:
                pass

    def wait_and_return_elem(self, xpath:str, timeout=30, sleeps:int=None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        if sleeps:
            sleep(sleeps)
        return self.driver.find_element(By.XPATH, xpath)

    def wait_click(self, xpath:str, sleeps=None, timeout=30) -> None:
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        if sleeps:
            sleep(sleeps)
        self.driver.find_element(By.XPATH, xpath).click()


    def wait_send(self, xpath:str, keys:str):
        self.wait.until(lambda x: x.find_element(By.XPATH, xpath))
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

