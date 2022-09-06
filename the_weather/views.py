from django.shortcuts import render
import requests
from .models import City
from the_weather.templates.weather.forms import CityForm
import math

# Create your views here.
def index(req):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6a90eda12e2d1507afef5e3a63ff7e6d'
    cities = City.objects.all()

    if req.method == 'POST':
        form = CityForm(req.POST)
        form.save()

    form = CityForm()

    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        # This will request the API data and convert the JSON to Python data types
        weather_info = {
            'city': city,
            'temperature': math.ceil(city_weather['main']['temp']),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'hi': math.ceil(city_weather['main']['temp_max']),
            'lo': math.ceil(city_weather['main']['temp_min']),
            # 'windspeed': city_weather['wind']['speed']
        }

        weather_data.append(weather_info)

    context = {'weather_data': weather_data, 'form': form}

    return render(req, 'weather/index.html', context)
