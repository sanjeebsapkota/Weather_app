from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    # Default city if not provided in POST request
    city = request.POST.get('city', 'indore')

    # OpenWeatherMap API setup
    # weather_api_key = 'AIzaSyBmu41JL750tq2o5AbE0S3Ss7b7vqlZ4Dw'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=3fe75560837a04d7f8b571a1a3403332'

    weather_params = {'units': 'metric'}

    # Google Custom Search API setup
    search_engine_id = 'd5488189bf4944710'
    api_key = 'AIzaSyBmu41JL750tq2o5AbE0S3Ss7b7vqlZ4Dw'
    query = city + '1920x1080'
    start = 1
    search_type = 'image'
    image_url = ''

    try:
        # Fetch image URL using Google Custom Search API
        city_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"
        data = requests.get(city_url).json()
        
        # Check if search returned any items
        if 'items' in data:
            search_items = data['items']
            if len(search_items) > 1:
                image_url = search_items[1]['link']
        
        # Fetch weather data using OpenWeatherMap API
        weather_response = requests.get(weather_url, params=weather_params).json()
        
        # Extract required weather information
        description = weather_response['weather'][0]['description']
        icon = weather_response['weather'][0]['icon']
        temp = weather_response['main']['temp']
        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        # Handle KeyError which occurs if expected keys are not found in API response
        exception_occurred = True
        messages.error(request, 'Weather data is not available for the entered city.')
        default_description = 'Clear sky'
        default_icon = '01d'
        default_temp = 25
        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': default_description,
            'icon': default_icon,
            'temp': default_temp,
            'day': day,
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })
