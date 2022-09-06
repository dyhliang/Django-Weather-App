from django.shortcuts import render
import requests
from .models import City


# Create your views here.
def index(req):
    url = 'https://samples.openweathermap.org/data/2.5/forecast?id=524901&appid=6a90eda12e2d1507afef5e3a63ff7e6d'

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        # This will request the API data and convert the JSON to Python data types

        weather_info = {
            'city': city,
            'temperature': city_weather['list'][0]['main']['temp'],
            'description': city_weather['list'][0]['weather'][0]['description'],
            'icon': city_weather['list'][0]['weather'][0]['icon']
        }

        weather_data.append(weather_info)

    context = {'weather': weather_data}

    return render(req, 'weather/index.html', context)
