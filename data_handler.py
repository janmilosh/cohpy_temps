import os
import requests
import json
import pdb

WU_API_KEY = os.environ.get('WU_API_KEY')


def _get_normal_meeting_day(year, month):
    pass

def _get_may_meeting_day(year):
    pass

def _get_december_meeting_day(year):
    pass



def _get_columbus_historical_max_temp(year, month, day):
    url = "http://api.wunderground.com/api/{}/history_{}{}{}/q/OH/Columbus.json".format(WU_API_KEY, year, month, day)
    response = requests.get(url)
    return json.loads(response.content)['history']['dailysummary'][0]['maxtempi']


if __name__ == '__main__':
    print _get_columbus_historical_max_temp('2006', '03', '18')
