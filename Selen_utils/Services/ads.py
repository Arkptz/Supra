import requests
from multiprocessing.synchronize import Lock
import multiprocessing as mp
from dataclasses import dataclass
from time import sleep
import logging as log
import traceback
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from ADS_BROWSER_SDK.ads import AdsApi
from ADS_BROWSER_SDK.errors import AdsError
from ADS_BROWSER_SDK.configs import UserProxyConfig, FingepringConfig
from Selen_utils.proxy import Proxy_Class

@dataclass
class AdsWithSelen(AdsApi):
    ads_id: str| None = None
    proxy: Proxy_Class | None = None

    def start_browser(self, fc: dict | None = None, upc: dict | None = None) -> webdriver.Chrome:
        q = self.query_group()
        lst_groups = [i['group_name'] for i in q]
        if not 'Sel___' in lst_groups:
            self.create_group('Sel___')
            q = self.query_group()
        for i in q:
            if i['group_name'] == 'Sel___':
                group_id = i['group_id']
        if not fc:
            fc = FingepringConfig(location='ask', canvas=1, webgl_image=1, webgl=1,
                                  audio=1, scan_port_type=1, media_devices=1, client_rects=1, device_name_switch=1,
                                  webrtc='proxy', speech_switch=1, mac_address_config={"model": "1", "address": ""}).dict(exclude_none=True)
        if self.proxy:
            pr = self.proxy
            if not upc:
                upc = UserProxyConfig(
                    proxy_soft='other', proxy_host=pr.ip, proxy_port=pr.port,
                    proxy_user=pr.login, proxy_password=pr.password, proxy_type='http').dict(exclude_none=True)
        else:
            if not upc:
                upc = UserProxyConfig(proxy_soft='no_proxy').dict()
        self.ads_id = self.create_account(
            group_id=group_id, user_proxy_config=upc, fingerprint_config=fc)['id']
        data = self.open_browser(user_id=self.ads_id)
        chrome_driver = data["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", data["ws"]["selenium"])
        driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        return driver

    def close_and_delete_browser(self) -> None:
        self.close_browser(user_id=self.ads_id)
        sleep(7)
        self.delete_account(user_ids=[self.ads_id])
