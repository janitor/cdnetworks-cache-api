# coding: utf-8

import requests
import urlparse


SERVICE_AREA_US_GLOBAL = 'us_global'
SERVICE_AREA_KOREA = 'korea'
SERVICE_AREA_JAPAN = 'japan'
SERVICE_AREA_CHINA = 'china'

API_URL_US_GLOBAL = 'https://openapi.us.cdnetworks.com/purge/rest/'
API_URL_KOREA = 'https://openapi.kr.cdnetworks.com/purge/rest/'
API_URL_JAPAN = 'https://openapi.jp.cdnetworks.com/purge/rest/'
API_URL_CHINA = 'https://openapi.txnetworks.cn/purge/rest/'

API_URLS = {
    SERVICE_AREA_US_GLOBAL: API_URL_US_GLOBAL,
    SERVICE_AREA_KOREA: API_URL_KOREA,
    SERVICE_AREA_JAPAN: API_URL_JAPAN,
    SERVICE_AREA_CHINA: API_URL_CHINA,
}


class CDNetworksAPI:

    def __init__(self, username, password, area=SERVICE_AREA_US_GLOBAL):
        assert(area in API_URLS)

        self.api_url = API_URLS[area]
        self.username = username
        self.password = password

    def _do_method_request(self, method, **params):
        params.update({
            'user': self.username,
            'pass': self.password,
            'output': 'json',
        })
        method_url = urlparse.urljoin(self.api_url, method)
        response = requests.get(method_url, params=params)
        response_json = response.json()

        result_code = response_json['resultCode']
        if result_code != 200:
            raise CDNetworksException(response_json.get('details', ''))

        return response_json

    def get_pads(self):
        response = self._do_method_request('padList')
        result = {
            'pads': [x for x in response['pads']],
        }
        return result

    def do_purge(self, pad, purge_type, path='', mail_to=''):
        response_json = self._do_method_request('doPurge', pad=pad, type=purge_type, mail_to=mail_to, path=path)
        result = {
            'pid': response_json['pid'],
        }
        return result

    def get_purge_status(self, pid):
        response_json = self._do_method_request('status', pid=pid)
        result = {
            'details': response_json['details'],
            'percentComplete': response_json['percentComplete'],
        }
        return result


class CDNetworksException(Exception):
    """
    400: API request could not be completed
    403: Login Failed
    404: API call not properly formed
    500: An unexpected error occurred. Please contact support
    509: Exceeded API rate limit
    """
