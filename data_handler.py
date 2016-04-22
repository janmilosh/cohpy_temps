import calendar
import json
import os
import pdb
import requests
import time
from datetime import date

WU_API_KEY = os.environ.get('WU_API_KEY')

class TempData(object):
    def __init__(self):
        self.temp_dict = {}

    def run(self):
        self._write_meeting_dates_to_file()
        self._add_meeting_dates_and_temps_to_dict()
        self._write_dict_to_json_file()

    def _meeting_dates(self):
        months_years = self._meeting_months_and_years()
        meeting_days = []
        for month_year in months_years:
            year = month_year['year']
            month = month_year['month']
            day = self._meeting_day(year, month)
            if day != None:
                meeting_days.append(date(year, month, day))
        return meeting_days

    def _write_meeting_dates_to_file(self):
        meeting_dates = self._meeting_dates()
        with open('meeting_dates.txt', 'wb') as date_file:
            for meeting_date in meeting_dates:
                date_file.write(meeting_date.strftime("%-m/%-d/%Y") + "\n")

    def _add_meeting_dates_and_temps_to_dict(self):
        meeting_dates = self._meeting_dates()
        for meeting_date in meeting_dates:
            formatted_date = meeting_date.strftime("%m-%d-%Y")
            meeting_month =  meeting_date.strftime("%B")
            temp = self._columbus_historical_max_temp(formatted_date)
            print formatted_date, temp
            if not self.temp_dict.get(meeting_month):
                self.temp_dict[meeting_month] = { "temps": [] }
            self.temp_dict[meeting_month]["temps"].append( { "date": formatted_date, "temp": temp } )
            time.sleep(7)

    def _write_dict_to_json_file(self):
        with open('real_data.json', 'w') as outfile:
            json.dump(self.temp_dict, outfile)
        print self.temp_dict

    def _meeting_months_and_years(self):
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

    def _meeting_day(self, year, month):
        if month == 11:
            return None

        mondays = self._mondays_in_month(year, month)
        
        if month == 5:
            return self._may_meeting_day(mondays)
        elif month == 12:
            return self._december_meeting_day(mondays)
        else:
            return self._normal_meeting_day(mondays)

    def _mondays_in_month(self, year, month):
        mondays = []
        month_matrix = calendar.monthcalendar(year, month)
        for week in month_matrix:
            if week[0] > 0:
                mondays.append(week[0])
        return mondays

    def _normal_meeting_day(self, mondays):
        return mondays[-1]

    def _may_meeting_day(self, mondays):
        return mondays[-2]

    def _december_meeting_day(self, mondays):
        if mondays[0] < 3:
            return mondays[1]
        else:
            return mondays[0]

    def _columbus_historical_max_temp(self, formatted_date):
        date_list = formatted_date.split('-')
        year = date_list[2]
        month = date_list[0]
        day = date_list[1]
        url = "http://api.wunderground.com/api/{}/history_{}{}{}/q/OH/Columbus.json".format(WU_API_KEY, year, month, day)
        response = requests.get(url)
        try:
            return json.loads(response.content)['history']['dailysummary'][0]['maxtempi']
        except IndexError:
            return None


if __name__ == '__main__':
    temp_data = TempData()
    temp_data.run()
