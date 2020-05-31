# traceroute

Версия 1

Автор: Макаров Егор, КН-202

### Описание

Обертка над консольным `tracert`

Для каждого IP-адреса выводит номер автономной системы, к которой этот адрес относится, страну и провайдера

### Пример запуска

```python
>python traceroute.py yandex.com
Трассировка маршрута к yandex.com [77.88.55.77]
с максимальным числом прыжков 30:

№    IP                AS       Country   Provider
1    192.168.0.1       --       --        --
2    10.143.255.254    --       --        --
3    85.235.63.46      AS25086  RU        Ural Telephone Company, Ekaterinburg
4    212.188.18.130    AS8359   RU        MTS / former ZAO MTU-Intel's p2p Network
5    212.188.29.249    AS8359   RU        MTS / former ZAO MTU-Intel's p2p Network
6    195.34.50.222     AS8359   RU        MTS PJSC
7    195.34.50.206     AS8359   RU        MTS PJSC
8    195.34.50.73      AS8359   RU        MTS PJSC
9    212.188.33.199    AS8359   RU        MTS's p2p Network
10   213.180.213.249   AS13238  RU        Yandex enterprise network
11   10.2.1.2          --       --        --
12   77.88.55.77       AS13238  RU        Yandex enterprise network
Трассировка завершена.
```

### Как работать с программой

`-h` — вызов справки

`<адрес-сайта>`, `<ip-адрес>` — запуск траcсировщика