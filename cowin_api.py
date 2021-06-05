import http_client

SERVER = 'https://cdn-api.co-vin.in/api'
STATE_KARNATAKA = '16'
DISTRICT_DK = '269'
CALENDAR_BY_DISTRICT = '/v2/appointment/sessions/public/calendarByDistrict'
CALENDAR_BY_DISTRICT_PARAMS = lambda district_id, date: {'district_id': district_id, 'date': date}


def get_calendar_data_by_district_id(district_id, date):
    url = SERVER + CALENDAR_BY_DISTRICT
    r = http_client.get(url, CALENDAR_BY_DISTRICT_PARAMS(district_id, date))
    if not r.ok:
        raise Exception("Failed to call " + url)
    response = r.json()
    return response

#print(get_calendar_data_by_district_id('269', '05-06-2021'))