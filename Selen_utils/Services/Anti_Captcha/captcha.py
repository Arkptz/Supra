import json
import logging as log
from typing import Callable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import traceback
from Selen_utils.Services.selenium_part import Selen
from Selen_utils.statuses import Statuses
from .errors import AntiCapthaError, AntiCapthaNotVisible


class Captcha(Selen):
    captcha_xpath = '//a[@class="status" and contains(.,"Solving is")]'

    def activate_anti_captcha(self, ):
        self.get_new('https://httpbin.org/ip')
        for i in range(3):
            try:
                message = {
                    # всегда указывается именно этот получатель API сообщения
                    'receiver': 'antiCaptchaPlugin',
                    # тип запроса, например setOptions
                    'type': 'setOptions',
                    # мерджим с дополнительными данными
                    'options': {'antiCaptchaApiKey': 'e36b5b6d9bfc7b4ca2bba2e6c5fd0e38'}
                }
                # выполняем JS код на странице
                # а именно отправляем сообщение стандартным методом window.postMessage
                self.driver.execute_script("""
                return window.postMessage({});
                """.format(json.dumps(message)))
                return Statuses.success
            except Exception as e:
                log.error(
                    f'{self.data} -- ошибка при активации антикапчи -- {traceback.format_exc}')
        return None

    def solve_captcha(self, attempts: int = 3, reload_func: Callable | None = None):
        reload_func = reload_func if reload_func else self.driver.refresh
        for i in range(attempts):
            try:
                self._captcha_check()
            except AntiCapthaNotVisible:
                reload_func()
            except AntiCapthaError:
                reload_func()

    def _captcha_check(self) -> str:
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(lambda x: x.find_element(
                By.XPATH, '//a[@class="status" and contains(.,"Solving is")]'))
            log.info('Капчу увидел')
        except Exception as e:
            raise AntiCapthaNotVisible
        while True:
            try:
                self.driver.find_element(
                    By.XPATH, '//a[@class="status" and contains(.,"Solving is")]')
            except:
                break
        try:
            WebDriverWait(self.driver, 5).until(lambda x: x.find_element(
                By.XPATH, '//a[@class="status" and .="Solved"]'))
            log.info('Капчу решил')
        except Exception as e:
            raise AntiCapthaError
        return True
