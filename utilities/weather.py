import requests
from datetime import datetime, timedelta


DATE_FORMAT = '%Y-%m-%d'


class WeatherAPI:
    def __init__(self, token):
        self.token = token
        self.url = 'https://api.weatherapi.com/v1/'

    def forecast_afternoon_today(self):
        url = f'{self.url}forecast.json'
        params = {'key': self.token, 'q': 'Hanoi', 'days': '1', 'hour': '17', 'lang': 'vi', 'aqi': 'yes'}
        req = requests.get(url=url, params=params)
        res = req.json()
        data = {'today': {}, 'forecast_5pm': {}}
        forecast_days = res['forecast']['forecastday']
        today = datetime.today()
        for forecast in forecast_days:
            date = datetime.strptime(forecast['date'], DATE_FORMAT)
            if today.date() == date.date():
                data['today'] = {
                    'temp': forecast['day']['avgtemp_c'],
                    'humidity': forecast['day']['avghumidity'],
                    'chance_of_rain': forecast['day']['daily_chance_of_rain'],
                    'uv': forecast['day']['uv'],
                    'description': forecast['day']['condition']['text']
                }
                data['forecast_5pm'] = {
                    'temp': forecast['hour'][0]['temp_c'],
                    'feelslike': forecast['hour'][0]['feelslike_c'],
                    'humidity': forecast['hour'][0]['humidity'],
                    'chance_of_rain': forecast['hour'][0]['chance_of_rain'],
                    'uv': forecast['hour'][0]['uv'],
                    'description': forecast['hour'][0]['condition']['text']
                }
            else:
                continue
        return data

    def forecast_morning_tomorrow(self):
        url = f'{self.url}forecast.json'
        params = {'key': self.token, 'q': 'Hanoi', 'days': '2', 'hour': '7', 'lang': 'vi', 'aqi': 'yes'}
        req = requests.get(url=url, params=params)
        res = req.json()
        data = {'today': {}, 'forecast_7am': {}, 'forecast_day': {}}
        forecast_days = res['forecast']['forecastday']
        for forecast in forecast_days:
            date = datetime.strptime(forecast['date'], DATE_FORMAT)
            today = datetime.today()
            if today.date() == date.date():
                data['today'] = {
                    'temp': forecast['day']['avgtemp_c'],
                    'humidity': forecast['day']['avghumidity'],
                    'chance_of_rain': forecast['day']['daily_chance_of_rain'],
                    'uv': forecast['day']['uv'],
                    'description': forecast['day']['condition']['text']
                }
            elif today.date() + timedelta(days=1) == date.date():
                data['forecast_7am'] = {
                    'temp': forecast['hour'][0]['temp_c'],
                    'feelslike': forecast['hour'][0]['feelslike_c'],
                    'humidity': forecast['hour'][0]['humidity'],
                    'chance_of_rain': forecast['hour'][0]['chance_of_rain'],
                    'uv': forecast['hour'][0]['uv'],
                    'description': forecast['hour'][0]['condition']['text']
                }
                data['forecast_day'] = {
                    'temp': forecast['day']['avgtemp_c'],
                    'humidity': forecast['day']['avghumidity'],
                    'chance_of_rain': forecast['day']['daily_chance_of_rain'],
                    'uv': forecast['day']['uv'],
                    'description': forecast['day']['condition']['text']
                }
            else:
                continue
        return data
