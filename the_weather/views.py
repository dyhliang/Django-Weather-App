from django.shortcuts import render
import requests
from .models import City
from the_weather.templates.weather.forms import CityForm

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
            'temperature': city_weather['list'][0]['main']['temp'],
            'description': city_weather['list'][0]['the_weather'][0]['description'],
            'icon': city_weather['list'][0]['the_weather'][0]['icon']
        }

        weather_data.append(weather_info)

    context = {'the_weather': weather_data, 'form': form}

    return render(req, 'the_weather/index.html', context)
