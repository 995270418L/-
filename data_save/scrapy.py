import requests


class StockCrapy:

    def init(self):
        pass

    def request_html_get(self, url, format='UTF-8'):
        r = requests.get(url)
        if r.status_code == 200:
            r.encoding = format
            return r.text

    def request_json_get(self, url, format='UTF-8'):
        r = requests.get(url)
        if r.status_code == 200:
            r.encoding = format
            return r.json
