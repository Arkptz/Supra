import requests
from dataclasses import dataclass
from time import sleep
import logging as log
import traceback


methods = {
    'GET': requests.get,
    'POST': requests.post
}


@dataclass
class DolphinApi:
    base_local: str = 'http://localhost:3001'
    base_url: str = 'https://anty-api.com'
    api_key: str = ''
    sess: requests.Session = requests.Session()

    def request(self, endpoint: str, params: dict | None = None, data: dict | None = None, json: dict | None = None, attempts: int = 5, method: str = 'GET', base: str = True):
        sess = self.sess
        req_info = f'request {method} {self.base_url+endpoint}\n data = {data}\n params = {params}\n'
        for attempt in range(attempts):
            try:
                response = sess.request(
                    url=(self.base_url if base else self.base_local) + endpoint,
                    params=params, data=data, json=json, method=method)
                print(response.text)
                response=response.json()
            except:
                log.error(f'Error with {req_info}-- {traceback.format_exc()}')

            log.info(
                f'Success request to Dolphin {req_info}response = {response}')
            return response

    def sign_in(self, username: str, password: str) -> dict:
        data = self.request(
            '/auth/login', data={'username': username, 'password': password}, method='POST')
        self.set_token(data['token'])
        return data

    def start_browser(self, profile_id: str, automation: int = 1):
        data = self.request(
            f'/v1.0/browser_profiles/{profile_id}/start', params={'automation': automation}, method='GET', base=False)
        print(data)

    def list_browser_profiles(self, limit: int = 50, query: str | None = None, tags: list[str] = [],
                              statuses: list[str] = [], mainWebsites: list[str] = [], users: list[str] = [], page: int = 0):
        data = self.request(
            f'/browser_profiles', params={'limit': limit, 'query': query, 'tags': tags,
                                          'statuses': statuses, 'mainWebsites': mainWebsites, 'users': users, 'page': page}, method='GET',)
        return data

    def set_token(self, token: str):
        self.sess.headers = {'Authorization': f'Bearer {token}'}


a = DolphinApi()

print(a.list_browser_profiles())
a.start_browser('23859316')
