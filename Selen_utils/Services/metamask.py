import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from Selen_utils.statuses import Statuses
from Selen_utils.Services.selenium_part import Selen


class Metamask(Selen):
    metamask_url: str

    def restart_metamask(self):
        for i in range(10):
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.switch_to.new_window('tab')
                break
            except:
                print(traceback.format_exc())
        self.get_new(
            f'{self.metamask_url}home.html#onboarding/welcome')

    def connect_metamask_to_site(self, xpath=False, get=None):
        cur = self.driver.current_window_handle
        counts = len(self.driver.window_handles)
        if xpath:
            self.wait_click(xpath)
        if get:
            self.get_new(get)
        self.wait.until(EC.number_of_windows_to_be(counts+1))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_click(
            '//button[@class="button btn--rounded btn-primary"]')  # next
        self.wait_click(
            '//button[@data-testid="page-container-footer-next"]')  # connect
        self.wait.until(EC.number_of_windows_to_be(counts))
        self.driver.switch_to.window(cur)
        

    def sign_message_metamask(self, xpath=None):
        cur = self.driver.current_window_handle
        counts = len(self.driver.window_handles)
        if xpath:
            self.wait_click(xpath)
        self.wait.until(EC.number_of_windows_to_be(counts+1))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_click(
            '//button[@data-testid="request-signature__sign"]')  # sign
        self.wait.until(EC.number_of_windows_to_be(counts))
        self.driver.switch_to.window(cur)
        return Statuses.success

    def login_metamask(self, seed_phrase: str):
        while True:
            ans = self.wait_many_elements([
                '//span[@id="critical-error-button"]', '//button[@data-testid="onboarding-import-wallet"]'])
            if ans == 2:
                self.wait_click(
                    '//button[@data-testid="onboarding-import-wallet"]')
                break
            else:
                try:
                    self.wait_click('//span[@id="critical-error-button"]')
                    sleep(2)
                except:
                    continue
                self.restart_metamask()
        self.wait_click('//button[@data-testid="metametrics-i-agree"]')

        seed_new = seed_phrase.split(' ')
        self.wait_and_return_elem(
            '//input[@data-testid="import-srp__srp-word-0"]')
        for i in range(12):
            self.driver.find_element(
                By.XPATH, f'//input[@data-testid="import-srp__srp-word-{i}"]').send_keys(f'{seed_new[i]}')
        self.wait_click('//button[@data-testid="import-srp-confirm"]')
        self.wait_send(
            '//input[@data-testid="create-password-new"]', 'InFiNiTi2022')
        self.wait_send(
            '//input[@data-testid="create-password-confirm"]', 'InFiNiTi2022')
        self.wait_click('//input[@data-testid="create-password-terms"]')
        self.wait_click('//button[@data-testid="create-password-import"]')
        # всё выполнено
        self.wait_click('//button[@data-testid="onboarding-complete-done"]')
        sleep(2)
        self.get_new(
            f'{self.metamask_url}home.html#onboarding/unlock')
        self.wait_send(
            '//input[@data-testid="unlock-password"]', 'InFiNiTi2022')
        self.wait_click('//button[@data-testid="unlock-submit"]')
        self.wait_click(
            '//button[@data-testid="onboarding-complete-done"]')  # ПОнятно!
        self.wait_click('//button[@data-testid="pin-extension-next"]')  # Далее
        sleep(1)
        self.wait_click(
            '//button[@data-testid="pin-extension-done"]')  # Выполнено
        self.wait_click('//li[@data-testid="home__activity-tab"]')
        sleep(1)
        return Statuses.success
