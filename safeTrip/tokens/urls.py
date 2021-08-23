from django.urls import path
from .views import *

urlpatterns = [

    path('', status),
    path('search/', searchToken),
    path('trending/', getTrendingTokens),
    path('metadata/<slug:poolAddress>', getTokenMetaData),
    path('chartdata/', getCandlesForChart),
    path('safe-trip-chart/', getSTFDailyChart),
    path('sponsored/', getSponsoredTokens),

]
