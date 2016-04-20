import calendar
import json
import os
import pdb
import requests
import time
from datetime import date

WU_API_KEY = os.environ.get('WU_API_KEY')

def meeting_temps():
    iso_dates = _meeting_iso_dates()
    # get everything from database
    for iso_date in iso_dates:
        #do the following if not in database, add to dates and save new date/temp
        print iso_date
        print _columbus_historical_max_temp(iso_date)
        print 
        time.sleep(7)   

def _meeting_iso_dates():
    months_years = _meeting_months_and_years()
    meeting_days = []
    for month_year in months_years:
        year = month_year['year']
        month = month_year['month']
        day = _meeting_day(year, month)
        if day != None:
            meeting_days.append(date(year, month, day).isoformat())
    return meeting_days

def _meeting_months_and_years():
    year = 2009 # first meeting year
    month = 9 # first meeting month
    months_and_years = [{'year': year, 'month': month}]
    while True:
        if month < 12:
            month += 1
        else:
            month = 1
            year += 1
        months_and_years.append({'year': year, 'month':month})
        if year == date.today().year and month == date.today().month:
            return months_and_years

def _meeting_day(year, month):
    if month == 11:
        return None

    mondays = _mondays_in_month(year, month)
    
    if month == 5:
        return _may_meeting_day(mondays)
    elif month == 12:
        return _december_meeting_day(mondays)
    else:
        return _normal_meeting_day(mondays)

def _mondays_in_month(year, month):
    mondays = []
    month_matrix = calendar.monthcalendar(year, month)
    for week in month_matrix:
        if week[0] > 0:
            mondays.append(week[0])
    return mondays

def _normal_meeting_day(mondays):
    return mondays[-1]

def _may_meeting_day(mondays):
    return mondays[-2]

def _december_meeting_day(mondays):
    if mondays[0] < 3:
        return mondays[1]
    else:
        return mondays[0]

def _columbus_historical_max_temp(isodate):
    date_list = isodate.split('-')
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]
    url = "http://api.wunderground.com/api/{}/history_{}{}{}/q/OH/Columbus.json".format(WU_API_KEY, year, month, day)
    response = requests.get(url)
    return json.loads(response.content)['history']['dailysummary'][0]['maxtempi']


if __name__ == '__main__':
    meeting_temps()
