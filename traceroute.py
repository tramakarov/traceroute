import urllib.request
from urllib.error import URLError, HTTPError
import re

as_regex = re.compile(r'"origin": "(\d+?)",')


def get_as_number_by_ip(ip):
    """Находит номер атономной системы по IP с помощью RIPEstat"""
    link = ('https://stat.ripe.net/data/routing-status/data.json?resource=' +
            '{}'.format(ip))
    try:
        with urllib.request.urlopen(link) as page:
            result = as_regex.findall(page.read().decode())[0]
            return result
    except (URLError, HTTPError, IndexError):
        return None