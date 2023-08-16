from django.urls import path
from . import views as api_views

app_name = 'weeklyweather'
urlpatterns = [
    path('weather/', api_views.WeatherAPIView.as_view(), name='weather'),
    path('city/', api_views.CityAPIView.as_view(), name='city'),

]
