from django.urls import path
from .views import *

urlpatterns = [
    path('search/', searchToken),
    path('trending/', getTrendingTokens),
    path('metadata/<slug:poolAddress>', getTokenMetaData),
    path('metadata/<str:network>/<slug:poolAddress>',
         getTokenMetaDataWithNetwork),
    path('chartdata/', getCandlesForChart),
    path('safe-trip-chart/', getSTFDailyChart),
    path('sponsored/', getSponsoredTokens),

]
