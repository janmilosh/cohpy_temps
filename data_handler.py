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
        # self._write_meeting_dates_to_file()
        # self._add_meeting_dates_and_temps_to_dict()
        self._add_prediction_to_dict()
        self._write_dict_to_json_file()
        print self.temp_dict

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

    def _add_prediction_to_dict(self):
        self.temp_dict = {'February': {'temps': [{'date': '02-22-2010', 'temp': u'40'}, {'date': '02-28-2011', 'temp': u'63'}, {'date': '02-27-2012', 'temp': u'58'}, {'date': '02-25-2013', 'temp': u'46'}, {'date': '02-24-2014', 'temp': u'34'}, {'date': '02-23-2015', 'temp': u'19'}, {'date': '02-29-2016', 'temp': u'57'}]}, 'October': {'temps': [{'date': '10-26-2009', 'temp': u'67'}, {'date': '10-25-2010', 'temp': u'71'}, {'date': '10-31-2011', 'temp': u'52'}, {'date': '10-29-2012', 'temp': u'41'}, {'date': '10-28-2013', 'temp': u'62'}, {'date': '10-27-2014', 'temp': u'79'}, {'date': '10-26-2015', 'temp': u'62'}]}, 'March': {'temps': [{'date': '03-29-2010', 'temp': u'50'}, {'date': '03-28-2011', 'temp': u'42'}, {'date': '03-26-2012', 'temp': u'52'}, {'date': '03-25-2013', 'temp': u'36'}, {'date': '03-31-2014', 'temp': u'65'}, {'date': '03-30-2015', 'temp': u'57'}, {'date': '03-28-2016', 'temp': u'59'}]}, 'August': {'temps': [{'date': '08-30-2010', 'temp': u'93'}, {'date': '08-29-2011', 'temp': u'78'}, {'date': '08-27-2012', 'temp': u'84'}, {'date': '08-26-2013', 'temp': u'90'}, {'date': '08-25-2014', 'temp': u'87'}, {'date': '08-31-2015', 'temp': u'86'}]}, 'September': {'temps': [{'date': '09-28-2009', 'temp': u'65'}, {'date': '09-27-2010', 'temp': u'61'}, {'date': '09-26-2011', 'temp': u'70'}, {'date': '09-24-2012', 'temp': u'68'}, {'date': '09-30-2013', 'temp': u'75'}, {'date': '09-29-2014', 'temp': u'84'}, {'date': '09-28-2015', 'temp': u'82'}]}, 'December': {'temps': [{'date': '12-07-2009', 'temp': u'35'}, {'date': '12-06-2010', 'temp': u'25'}, {'date': '12-05-2011', 'temp': u'53'}, {'date': '12-03-2012', 'temp': u'63'}, {'date': '12-09-2013', 'temp': u'35'}, {'date': '12-08-2014', 'temp': u'45'}, {'date': '12-07-2015', 'temp': u'51'}]}, 'June': {'temps': [{'date': '06-28-2010', 'temp': u'85'}, {'date': '06-27-2011', 'temp': u'83'}, {'date': '06-25-2012', 'temp': u'80'}, {'date': '06-24-2013', 'temp': u'87'}, {'date': '06-30-2014', 'temp': u'87'}, {'date': '06-29-2015', 'temp': u'66'}]}, 'April': {'temps': [{'date': '04-26-2010', 'temp': u'57'}, {'date': '04-25-2011', 'temp': u'74'}, {'date': '04-30-2012', 'temp': u'84'}, {'date': '04-29-2013', 'temp': u'65'}, {'date': '04-28-2014', 'temp': u'59'}, {'date': '04-27-2015', 'temp': u'54'}, {'date': '04-25-2016', 'temp': None}]}, 'May': {'temps': [{'date': '05-24-2010', 'temp': u'83'}, {'date': '05-23-2011', 'temp': u'82'}, {'date': '05-21-2012', 'temp': u'87'}, {'date': '05-20-2013', 'temp': u'86'}, {'date': '05-19-2014', 'temp': u'71'}, {'date': '05-18-2015', 'temp': u'79'}]}, 'January': {'temps': [{'date': '01-25-2010', 'temp': u'49'}, {'date': '01-31-2011', 'temp': u'32'}, {'date': '01-30-2012', 'temp': u'50'}, {'date': '01-28-2013', 'temp': u'51'}, {'date': '01-27-2014', 'temp': u'42'}, {'date': '01-26-2015', 'temp': u'27'}, {'date': '01-25-2016', 'temp': u'46'}]}, 'July': {'temps': [{'date': '07-26-2010', 'temp': u'83'}, {'date': '07-25-2011', 'temp': u'89'}, {'date': '07-30-2012', 'temp': u'90'}, {'date': '07-29-2013', 'temp': u'76'}, {'date': '07-28-2014', 'temp': u'76'}, {'date': '07-27-2015', 'temp': u'87'}]}}
        for month in self.temp_dict:
            for meetups_list in self.temp_dict[month]:
                temp_list = []
                for meetup in self.temp_dict[month][meetups_list]:
                    if meetup['temp']:
                        temp_list.append(int(meetup['temp']))
                predicted_temp = self._calculate_prediction(temp_list)
            self.temp_dict[month]['prediction'] = predicted_temp

    def _calculate_prediction(self, temp_list):
        temp_list.sort()
        del temp_list[0]
        del temp_list[-1]
        average_float = sum(temp_list)*1.0/len(temp_list)
        average_int_to_str = str(int(round(average_float)))
        return average_int_to_str
        
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
        url = "http://api.wunderground.com/api/{}/history_{}{}{}/q/OH/KCMH.json".format(WU_API_KEY, year, month, day)
        print url
        response = requests.get(url)
        try:
            return json.loads(response.content)['history']['dailysummary'][0]['maxtempi']
        except IndexError:
            return None


if __name__ == '__main__':
    temp_data = TempData()
    temp_data.run()
