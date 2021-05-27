#!/usr/bin/env python
import requests
from requests.exceptions import HTTPError
import datetime
from playsound import playsound

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

def mynotify(text):
    Notify.Notification.new(text).show()


url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'
pincodes = {'600091','600061','600096','600042'}


today = datetime.date.today()
day0 = today + datetime.timedelta(days=1)
day1 = today + datetime.timedelta(days=2)
days = [day0, day1]
available = 0

headers = {'Accept':'application/json','Accept-Language': 'hi_IN','User-Agent':'PostmanRuntime/7.28.0'}

Notify.init("Covid-Vaccine Notifier")


for day in days:
    params = {'district_id': 571, 'date':day.strftime("%d-%m-%Y")}
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
        )
        response.raise_for_status()
    except HTTPError as http_err:
        mynotify(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        mynotify(f'Other error occurred: {err}') 
    else:
        json_response = response.json()
        sessions = json_response['sessions']
        for session in sessions:
            if session['available_capacity_dose1'] != 0 and session["min_age_limit"] == 18 and session["pincode"] in pincodes:
                name = session['name'] 
                print('Vaccine')
                Notify.Notification.new('Vaccine Available', '✔️ ' + name).show()
                available += 1
            
if available == 0:
    print('NO')
    Notify.Notification.new('Nothing available', '❌').show()
else:
    playsound('alarm.mp3')



