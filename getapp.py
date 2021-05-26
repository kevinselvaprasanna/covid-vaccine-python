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


url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'
pincode = '600091'
day_ahead = 1


today = datetime.date.today()
day = today + datetime.timedelta(days=day_ahead)
available = 0

headers = {'Accept':'application/json','Accept-Language': 'hi_IN','User-Agent':'PostmanRuntime/7.28.0'}
params = {'pincode': pincode, 'date':day.strftime("%d-%m-%Y")}

Notify.init("Covid-Vaccine Notifier")

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
    for i in range(len(sessions)):
        if sessions[i]['available_capacity_dose1'] != 0 and sessions[i]["min_age_limit"] == 18:
            name = sessions[i]['name'] 
            print('Vaccine')
            notification = Notify.Notification.new('Vaccine Available', '✔️ ' + name)
            notification.show()
            available = available + 1
            playsound('alarm.mp3')
        
    if available == 0:
        print('NO')
        notification = Notify.Notification.new('Nothing available', '❌').show()


