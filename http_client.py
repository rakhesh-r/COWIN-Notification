import requests


def get(url, params):
    return requests.get(url, headers=__get_headers(), params=params, timeout=2)


def __get_headers():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
               'Accept-Language' : 'en',
               'Accept-Encoding': 'gzip, deflate, br'}
    return headers

print(get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=269&date=05-06-2021', None))
