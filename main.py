import requests
import datetime as dt
import os
import pickle


file_path = 'my_variable.pkl'
if os.path.exists(file_path):
    with open(file_path, 'rb') as file:
        env = pickle.load(file)

APP_ENDPOINT='https://trackapi.nutritionix.com/v2/natural/exercise'

HEADERS={
    'x-app-id':env['APP_ID'],
    'x-app-key':env['APP_KEY']
}

exercise = input('Write which exercise you did: ')

PARAMS={
    'query':exercise,
    'weight_kg':83,
    'height_cm':197,
    'age':31
}

res = requests.post(url=APP_ENDPOINT,json=PARAMS,headers=HEADERS)
res_exercises = res.json()['exercises']
exercises = [(exercise['name'],exercise['duration_min'],exercise['nf_calories']) for exercise in res_exercises]
print(exercises)

SHEET_ENDPOINT='https://api.sheety.co/ccf8a95a505e1ee7fc5c0d8cb2e59a73/workoutSheet/arkusz1'
SHEET_HEADERS={
    'Authorization':env['SHEET_TOKEN']
}

date=dt.datetime.today().strftime('%d/%m/%Y')
time=dt.datetime.today().strftime('%H:%M:%S')

for exercise in exercises:
    body = {
        'arkusz1':{
            'date':date,
            'time':time,
            'exercise':exercise[0],
            'duration':exercise[1],
            'calories':exercise[2]
        }
    }
    req = requests.post(url=SHEET_ENDPOINT,json=body,headers=SHEET_HEADERS)