from django.shortcuts import render, redirect
import requests
from .models import City
from the_weather.templates.weather.forms import CityForm
import math


def index(req):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6a90eda12e2d1507afef5e3a63ff7e6d'
    cities = City.objects.all()

    error_msg = ""
    message = ""
    message_class = ""

    if req.method == 'POST':
        form = CityForm(req.POST)

        # To prevent duplicate cities
        if form.is_valid():
            new_city = form.cleaned_data['name']
            cities_count = City.objects.filter(name=new_city).count()

            if cities_count == 0:
                city_weather = requests.get(url.format(new_city)).json()
                # Validates the city entered - 200(valid)
                if city_weather['cod'] == 200:
                    form.save()
                else:
                    error_msg = "City not found - try again."
            else:
                error_msg = "City is already displayed - try again."

        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message = 'City added!'
            message_class = 'is-success'

    form = CityForm()

    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        # This will request the API data and convert the JSON to Python data types
        weather_info = {
            'city': city,
            'temperature': math.ceil(city_weather['main']['temp']),
            'description': city_weather['weather'][0]['description'].capitalize(),
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'hi': math.ceil(city_weather['main']['temp_max']),
            'lo': math.ceil(city_weather['main']['temp_min']),
            # 'windspeed': city_weather['wind']['speed']
        }

        weather_data.append(weather_info)

    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class}

    return render(req, 'weather/index.html', context)

def delete_city(req, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
