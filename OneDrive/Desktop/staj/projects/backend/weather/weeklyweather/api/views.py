from datetime import date, timedelta
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import CitySerializer, WeatherSerializer
from ..models import City, Weather


class CityAPIView(APIView):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)

    def post(self, request):
        city = request.data.get('city', '')
        suggestions = City.objects.filter(city__startswith=city).values_list('city', flat=True).distinct()
        return Response(suggestions)


class WeatherAPIView(ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    def post(self, request):
        city_id = request.data.get('city')
        if not city_id:
            return Response({'error': 'City ID is required.'}, status=400)

        start_date = request.data.get('start_date') or request.POST.get('start_date')
        end_date = request.data.get('end_date') or request.POST.get('end_date')

        if not start_date or not end_date:
            return Response({'error': 'Start date and end date are required.'}, status=400)

        try:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)

        except ValueError:
            return Response({'error': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}, status=400)

        api_key = 'b3342ef714dc4e12bbe110123232106'

        weather_list = []

        if end_date <= start_date:
            end_date_temp = end_date
            end_date = start_date
            start_date = end_date_temp

        city_instance = City.objects.get(id=city_id)
        city_info = str(city_instance)

        while start_date <= end_date:
            url = f'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city_info}&format=json&date={start_date.strftime("%Y-%m-%d")}'
            response = requests.get(url)
            data = response.json()

            if 'data' in data and 'error' not in data['data']:
                temperature = data['data']['current_condition'][0]['temp_C']
                weather_date = start_date.strftime("%Y-%m-%d")

                existing_weather = Weather.objects.filter(city=city_instance, date=weather_date)

                if existing_weather.exists():
                    existing_weather.first().temperature = temperature
                    existing_weather.first().save()
                else:
                    Weather.objects.create(city=city_instance, date=weather_date, temperature=temperature)

                weather_list.append({
                    'date': weather_date,
                    'temperature': temperature,
                })
            else:
                return Response({'error': 'Hava durumu verisi alınamadı'}, status=400)

            start_date += timedelta(days=1)

        return Response(weather_list, status=200)
