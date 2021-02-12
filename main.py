import requests
from datetime import datetime
import os

GENDER = "female"
WEIGHT_KG = 70
HEIGHT_CM = 175
AGE = 29

NU_API_KEY = os.environ["NU_API_KEY"]
NU_APP_ID = os.environ["NU_APP_ID"]
SH_TOKEN = os.environ["SH_TOKEN"]
SH_ENDPOINT = os.environ["SH_ENDPOINT"]

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

exercise_headers = {
    "x-app-id": NU_APP_ID,
    "x-app-key": NU_API_KEY,
}

exercise_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=EXERCISE_ENDPOINT, json=exercise_parameters, headers=exercise_headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheet_headers = {
    "Authorization": f"Bearer {SH_TOKEN}"
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": round(exercise["duration_min"]),
            "calories": round(exercise["nf_calories"])
        }
    }

    sheet_response = requests.post(url=SH_ENDPOINT, json=sheet_inputs, headers=sheet_headers)
    print(sheet_response.text)
