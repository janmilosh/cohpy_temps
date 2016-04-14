import calendar
import json
import os
import pdb
import requests


WU_API_KEY = os.environ.get('WU_API_KEY')

def _get_meeting_day(year, month):
    if month == 11:
        return None

    mondays = _mondays_in_month(year, month)
    
    if month == 5:
        return _get_may_meeting_day(mondays)
    elif month == 12:
        return _get_december_meeting_day(mondays)
    else:
        return _get_normal_meeting_day(mondays)

def _get_normal_meeting_day(mondays):
    return mondays[-1]

def _get_may_meeting_day(mondays):
    return mondays[-2]

def _get_december_meeting_day(mondays):
    if mondays[0] < 3:
        return mondays[1]
    else:
        return mondays[0]

def _mondays_in_month(year, month):
    mondays = []
    month_matrix = calendar.monthcalendar(year, month)
    for week in month_matrix:
        if week[0] > 0:
            mondays.append(week[0])
    return mondays


def _get_columbus_historical_max_temp(year, month, day):
    url = "http://api.wunderground.com/api/{}/history_{}{}{}/q/OH/Columbus.json".format(WU_API_KEY, year, month, day)
    response = requests.get(url)
    return json.loads(response.content)['history']['dailysummary'][0]['maxtempi']


if __name__ == '__main__':
    print _get_meeting_day(2016, 12)
    # print _get_columbus_historical_max_temp('2006', '03', '18')
