from django.urls import path
from .views import *

urlpatterns = [
    path('search/', searchToken),
    path('search/<str:network>', searchTokenWithNetwork),
    path('trending/', getTrendingTokens),
    path('metadata/<slug:poolAddress>', getTokenMetaData),
    path('metadata/<str:network>/<slug:poolAddress>',
         getTokenMetaDataWithNetwork),
    path('chartdata/', getCandlesForChart),
    path('chartdata/<str:network>/<slug:pairAddress>', getCandlesForChartWithNetwork),
    path('safe-trip-chart/', getSTFDailyChart),
    path('sponsored/', getSponsoredTokens),

]
