from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('index', index, name='index'),
    path('about', about, name='about'),
    path('main', main, name='main'),
    path('models', models, name='models'),
    path('model', model, name='models'),
]