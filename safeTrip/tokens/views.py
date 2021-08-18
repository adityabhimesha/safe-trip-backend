import json
from django.http import HttpResponse
from .models import Tokens
from . import controllers
import arrow

error = {
    "error" : "There Has Been A Error, Please Try Again!"
}

def searchToken(request):

    value = request.GET['value']
    if not value.startswith('0x'):
        value = value.upper()

    res = controllers.queryStringinValue(value)
    if res.status_code != 200:
        return HttpResponse(json.dumps(error), content_type="application/json")
    
    res = res.json()
    addresses = []
    for i in res['data']['search']:
        addresses.append(i['subject']['address'])

    result = controllers.queryAddressesForPairs(addresses)
    if result.status_code != 200:
        return HttpResponse(json.dumps(error), content_type="application/json")
    
    result = result.json()
    objs = []
    for pool in result['data']['ethereum']['dexTrades']:
        new_pool = Tokens(
            pk=pool['smartContract']['address']['address'],
            pair_base_address=pool['baseCurrency']['address'],
            pair_quote_address=pool['quoteCurrency']['address'],
            pair_base_name=pool['baseCurrency']['symbol'],
            pair_quote_name=pool['quoteCurrency']['symbol']
        )
        objs.append(new_pool)

    #could get really risky!
    try:
        if len(objs) != 0:
            Tokens.objects.bulk_create(objs, len(objs),ignore_conflicts=True)
    except:
        print("Creation of objects from search results has failed!")
        pass
    return HttpResponse(json.dumps(result), content_type="application/json")


def getTrendingTokens(request):

    topTokens = Tokens.objects.all().order_by('-views')
    

    return HttpResponse(json.dumps(topTokens), content_type="application/json")


#main call when requesting for pool address
def getTokenMetaData(request,poolAddress):

    if not poolAddress.startswith('0x'):
        payload = {
            "error":"Address Requested Must Start with 0x"
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")
    
    token = Tokens.objects.filter(pk=poolAddress)
    if len(token) != 0:
        token[0].views = token[0].views + 1
        token[0].save()
        token = token[0]

    else:
        #run pool search and add to DB
        result = controllers.getBaseQuoteFromPairAddress(poolAddress)
        if result.status_code != 200:
            error = {
                "error" : "There Has Been A Error While Fetching Data"
            }
            return HttpResponse(json.dumps(error), content_type="application/json")
        
        result = result.json()
        result = result['data']['ethereum']['dexTrades']
        if len(result) == 0:
            payload = {
                "error":"Could Not Find The Pair Requested"
            }
            return HttpResponse(json.dumps(payload), content_type="application/json")

        token = Tokens(
            pair_address=result[0]['smartContract']['address']['address'],
            pair_base_name=result[0]['baseCurrency']['symbol'],
            pair_quote_name=result[0]['quoteCurrency']['symbol'],
            pair_base_address=result[0]['baseCurrency']['address'],
            pair_quote_address=result[0]['quoteCurrency']['address'],
        )
        token.save()


    ar = arrow.utcnow()
    ar = ar.shift(days=-10)

    result = controllers.getMetaVolumeLQTrades(
        token.pair_base_address,
        token.pair_quote_address,
        token.pair_address,
        ar.format('YYYY-MM-DDTHH:mm:ss')
        )

    if result.status_code != 200:
        error = {
            "status":"There has been an Error!",
            
        }
        return HttpResponse(json.dumps(error), content_type="application/json",status=500) 
    
    result = result.json()

    payload = {
        "tokens":{
            "pair_address" : token.pair_address,
            "pair_base_name" : token.pair_base_name,
            "pair_quote_name" : token.pair_quote_name,
            "pair_base_address" : token.pair_base_address,
            "pair_quote_address" : token.pair_quote_address,
        },
        "details" : result['data']['ethereum']['details'],
        "dailyVolume" : result['data']['ethereum']['dailyVolume'],
        "liquidity" : result['data']['ethereum']['liquidity'],
        "trades" : result['data']['ethereum']['trades'],
    }


    return HttpResponse(json.dumps(payload), content_type="application/json")
    

def getCandlesForChart(request):
    ar = arrow.utcnow()
    ar = ar.shift(days=-10)

    #2021-08-11T12:17:19.352690+00:00
    return HttpResponse(ar.format('YYYY-MM-DD'), content_type="application/json")



#https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/0xe9e7cea3dedca5984780bafc599bd69add087d56
