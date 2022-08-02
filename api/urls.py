from django.urls import path
from .views import *

urlpatterns = [
    path('getModelsByDatasetID', getModelsByDatasetID, name='getModelsByDatasetID'),
    path('model', getModel, name='getModel'),
    path('searchGsSentences', search, name='searchGsSentences'),
    path('wrongPairs', getWrongTranslationPairs, name='wrongPairs'),
    path('findPair', findPair, name='findPair'),


]