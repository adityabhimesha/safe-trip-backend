from django.urls import path
from .views import *

urlpatterns = [
    path('search/', searchToken),
    path('trending/', getTrendingTokens),
    path('metadata/<slug:poolAddress>', getTokenMetaData),
    path('chartdata/', getCandlesForChart),

]
