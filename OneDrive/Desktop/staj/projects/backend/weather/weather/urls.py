from django.contrib import admin
from django.urls import path, include
from weeklyweather.api import urls as api_urls
from user import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('user/', include(urls)),
]