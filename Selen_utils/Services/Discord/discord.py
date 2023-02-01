from time import sleep
from typing import Callable
import logging as log
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from Selen_utils.statuses import Statuses
from Selen_utils.Services.selenium_part import Selen
from .errors import DiscordInvalidTokenError, DiscordNotDisplayPageError, DiscordNoAuthorizeError



class Discord(Selen):

    def authorize_discord(self, token: str | None, att=1):
        ans = self.wait_many_elements([
            '//input[@name="password"]', '//button[@class="button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeMedium-2bFIHr grow-2sR_-F"]'])
        if ans == 1:
            if not token:
                raise DiscordNoAuthorizeError
            func = '''function login(token) {
                        setInterval(() => {
                            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                        }, 50);
                        setTimeout(() => {
                            location.reload();
                        }, 2500);
                        }
                        '''
            self.driver.execute_script(
                func + f"login('{token}');")
            sleep(10)
            elems = ['//button[@class="button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeMedium-2bFIHr grow-2sR_-F"]',
                     '//section[@class="panels-3wFtMD"]',
                     '//div[contains(.,"You need to verify your account")]',
                     '//input[@name="password"]']
            ans = self.wait_many_elements(elems)
            if ans == 4:
                if att >= 3:
                    return DiscordInvalidTokenError
                self.driver.refresh()
                return self.authorize_discord(att=att+1, token=token)
            elif ans == 3:
                return DiscordInvalidTokenError
            elif ans == 2:
                raise DiscordNotDisplayPageError
            elif ans == 1:
                self.wait_click(
                    '//button[@class="button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeMedium-2bFIHr grow-2sR_-F"]')
                log.debug(
                    f'{self.data} -- прожали авториз (дс)')
                return Statuses.success

    def connect_discord(self, xpath: str | None = None, token: str | None = None):
        cur = self.driver.current_window_handle
        counts = len(self.driver.window_handles)
        if xpath:
            self.wait_click(xpath)
        self.wait.until(EC.number_of_windows_to_be(counts+1))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        while True:
            try:
                ans = self.authorize_discord(token=token)
                self.wait.until(EC.number_of_windows_to_be(counts))
                self.driver.switch_to.window(cur)
                return ans
            except DiscordNotDisplayPageError:
                self.driver.close()
                self.wait.until(EC.number_of_windows_to_be(counts))
                self.driver.switch_to.window(cur)
                continue
