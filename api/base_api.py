import requests


class BaseApi:
    """Базовый клиент: свой Session и буфер HTTP-логов на каждый тест."""

    def __init__(self, log_buffer):
        self.log_buffer = log_buffer
        self.session = requests.Session()
        self.session.hooks['response'].append(log_buffer.record)

    def request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)
