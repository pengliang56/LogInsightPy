from django.urls import path

from apps.view.search_view import search_json
from apps.view.main_view import main_json

urlpatterns = [
    path('api/log/search/', search_json, name='search_json'),
    path('api/log/main/', main_json, name='main_json'),
]