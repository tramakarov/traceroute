import urllib.request
from urllib.error import URLError, HTTPError
import re
import subprocess
import sys
import json

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


def get_country_and_provider(ip):
    country, provider = ('--', '--')
    link = ('https://stat.ripe.net/data/whois/data.json?resource=' + ip)

    try:
        with urllib.request.urlopen(link) as page:
            data = json.loads(page.read().decode('utf-8'))['data']
    except (URLError, HTTPError) as err:
        return country, provider

    country, provider = scan_records(data, 'records')

    if '--' in (country, provider):
        scan_results = scan_records(data, 'irr_records')
        country = scan_results[0] if scan_results[0] != '--' else country
        provider = scan_results[1] if scan_results[1] != '--' else provider

    return country, provider


def scan_records(data, records_key):
    country, provider = ('--', '--')
    for record in data[records_key]:
        if country != '--' and provider != '--':
            break
        for item in record:
            if country != '--' and provider != '--':
                break
            if item['key'].lower() == 'country' and country == '--':
                country = item['value']
            if item['key'].lower() == 'descr' and provider == '--':
                provider = item['value']

    return country, provider


def stringify_info(number, ip, as_number, country, provider):
    return (number + ' '*(5-len(number)) + ip + ' '*(18-len(ip)) +
            as_number + ' '*(9 - len(as_number)) +
            country + ' '*(10-len(country)) + provider)


def get_route(address):
    tracert = subprocess.Popen(['tracert', address],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    get_as = False
    number = 1

    for line in iter(tracert.stdout.readline, ""):
        line = line.decode(encoding='cp866')
        if line.find('Не удается разрешить системное имя узла') != -1:
            print(line)
            break
        elif line.find('Трассировка маршрута') != -1:
            print(line, end='')
            end = ip_regex.findall(line)[0]
        elif line.find('с максимальным числом прыжков') != -1:
            print(line)
            print('№' + ' '*4 + 'IP' + ' '*16 + 'AS' + ' '*7 + 'Country   ' +
                  'Provider')
            get_as = True

        try:
            ip = ip_regex.findall(line)[0]
        except IndexError:
            continue

        if get_as:
            asn_number = get_as_number_by_ip(ip)
            country, provider = (get_country_and_provider(ip)
                                 if asn_number is not None else ('--', '--'))
            if asn_number is None:
                asn_number = '--'

            str_ip = ip + (' '*(15 - len(ip))) if len(ip) < 15 else ip
            print(stringify_info(str(number), str_ip, asn_number, country,
                                 provider))
            number += 1
            if ip == end:
                print('Трассировка завершена.')
                break


def print_help():
    with open('help.txt', 'r', encoding='utf-8') as file:
        print(file.read())


if __name__ == '__main__':
    arg = sys.argv[1]
    get_route(arg) if arg not in ['-h', '--help'] else print_help()
