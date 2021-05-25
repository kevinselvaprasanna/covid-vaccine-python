import requests
from requests.exceptions import HTTPError
import datetime

from gi.repository import Notify

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
    print(f'HTTP error occurred: {http_err}') 
except Exception as err:
    print(f'Other error occurred: {err}') 
else:
    print('Success!')
    json_response = response.json()
    sessions = json_response['sessions']
    for i in range(len(sessions)):
        if sessions[i]['available_capacity_dose1'] != 0 and sessions[i]["min_age_limit"] == 18:
            name = sessions[i]['name'] 
            print('Vaccine Available at ' + name)
            notification = Notify.Notification.new('Vaccine Available', '✔️ ' + name)
            notification.show()
            available = available + 1
        
    if available == 0:
        print('Nothing available')
        notification = Notify.Notification.new('Nothing available', '❌')
        notification.show()


