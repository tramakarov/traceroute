import urllib.request
from urllib.error import URLError, HTTPError
import re
import subprocess
import sys
import traceback

as_regex = re.compile(r'"origin": "(\d+?)",')
ip_regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
table = '{number}\t{ip}\t\t{asn}'


def get_as_number_by_ip(ip):
    """Находит номер атономной системы по IP с помощью RIPEstat"""
    link = ('https://stat.ripe.net/data/routing-status/data.json?resource=' +
            '{}'.format(ip))

    try:
        with urllib.request.urlopen(link) as page:
            result = as_regex.findall(page.read().decode())[0]
            return 'AS{}'.format(result)
    except IndexError:
        return None
    except (URLError, HTTPError) as err:
        return str(err)


def get_route(address):
    tracert = subprocess.Popen(['tracert', address],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    get_as = False
    number = 1

    for line in iter(tracert.stdout.readline, ""):
        line = line.decode(encoding='cp866')
        # print(' line: ', line)
        if line.find('Не удается разрешить системное имя узла') != -1:
            print(line)
            break
        elif line.find('Трассировка маршрута') != -1:
            print(line, end='')
            end = ip_regex.findall(line)[0]
        elif line.find('с максимальным числом прыжков') != -1:
            print(line)
            print(table.format(number='№', ip='IP            ', asn='AS'))
            get_as = True

        try:
            ip = ip_regex.findall(line)[0]
        except IndexError:
            continue

        if get_as:
            asn_number = get_as_number_by_ip(ip)
            if asn_number is None:
                asn_number = '--'

            str_ip = ip + (' '*(15 - len(ip))) if len(ip) < 15 else ip
            print(table.format(number=number, ip=str_ip, asn=asn_number))
            number += 1
            if ip == end:
                print('Трассировка завершена.')
                break


def print_help():
    print('help')


if __name__ == '__main__':
    arg = sys.argv[1]
    get_route(arg) if arg != '-h' else print_help()