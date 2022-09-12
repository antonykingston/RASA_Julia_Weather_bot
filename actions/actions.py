# **************************************************************************************
# WARNING: This is a static file, useful as a starting point. You may want to change it.
# **************************************************************************************

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import ActionExecutionRejection
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
import requests
import json

from rasa_sdk.events import SlotSet


import datetime as dt
from time import timezone



'''
Create your own API key from weather-api
https://openweathermap.org/

'''


api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #add your api key here

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?appid="

def kelvin_to_c_f(kelvin):
    celsius = kelvin - 273.5
    fahrenheit = celsius * (9/5) +32
    return celsius , fahrenheit

class MyCustomAction(Action):

    def name(self) -> Text:
        return "action_weather_forcast"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['entities'][0]['value'])
        ent = tracker.latest_message['entities'][0]['value']


        API_KEY = api_key
        CITY = ent

        url = BASE_URL + API_KEY + "&q=" + CITY

        print(f"________________________ \n\n {url} \n________________________" )

        response = requests.get(url).json()
        
        temp_kelvin = response['main']['temp']
        temp_celsius , temp_fahrenheit = kelvin_to_c_f(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius , feels_like_fahrenheit = kelvin_to_c_f(feels_like_kelvin)
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])


        print(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
        print(f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
        print(f"humidity in {CITY}: {humidity}%")
        print(f"General Weather in {CITY}: {description}")
        print(f"Sun rises in {CITY} at {sunrise_time} local time.")
        print(f"Sun sets in {CITY} at {sunset_time} local time.")

        dispatcher.utter_message(text=f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
        dispatcher.utter_message(text=f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
        dispatcher.utter_message(text=f"humidity in {CITY}: {humidity}%")
        dispatcher.utter_message(text=f"General Weather in {CITY}: {description}")
        dispatcher.utter_message(text=f"Sun rises in {CITY} at {sunrise_time} local time.")
        dispatcher.utter_message(text=f"Sun sets in {CITY} at {sunset_time} local time.")


        
        return
