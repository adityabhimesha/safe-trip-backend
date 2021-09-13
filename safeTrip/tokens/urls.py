from django.urls import path
from .views import *

urlpatterns = [
    path('search/', searchToken),
    path('search/<str:network>/', searchTokenWithNetwork),
    path('trending/', getTrendingTokens),
    path('trending/<str:network>/', getTrendingTokensWithNetwork),
    path('metadata/<slug:poolAddress>', getTokenMetaData),
    path('metadata/<str:network>/<slug:poolAddress>', getTokenMetaDataWithNetwork),
    path('chartdata/', getCandlesForChart),
    path('chartdata/<str:network>/',
         getCandlesForChartWithNetwork),
    path('safe-trip-chart/', getSTFDailyChart),
    path('sponsored/', getSponsoredTokens),
    path('sponsored/<str:network>/', getSponsoredTokensWithNetwork),
]
