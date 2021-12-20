import requests
import gzip

from scripts.common.exceptions import NotFoundError


class HttpDriver:
    @staticmethod
    def format_url(raw_url: str, file_name: ''):
        prefix = 'ftp://'
        return f'https://{raw_url[len(prefix):]}/{file_name}'

    @staticmethod
    def get_contents(url: str):
        r = requests.get(url)
        if r.status_code == 404:
            raise NotFoundError
        return r.text

    @staticmethod
    # downloads url over http and unzips it via gzip
    def download_gz(url: str):
        r = requests.get(url, stream=True)
        if r.status_code == 404:
            raise NotFoundError
        contents = gzip.GzipFile(fileobj=r.raw).read().decode('utf-8')
        return contents
