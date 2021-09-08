import json
from django.http import HttpResponse
from .models import Tokens
from .models import PancakeTokens
from .models import UniswapTokens
from .models import MaticTokens
from . import controllers
import datetime

error = {
    "error": "There Has Been A Error, Please Try Again!"
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

    quotes = ["BUSD", "WBNB", "USDT"]
    result = result.json()
    if(len(result) >= 5):
        result = result[:5]
    objs = []
    for pool in result['data']['ethereum']['dexTrades']:
        if pool['baseCurrency']['symbol'] in quotes:
            new_pool = Tokens(
                pk=pool['smartContract']['address']['address'],
                pair_base_address=pool['quoteCurrency']['address'],
                pair_quote_address=pool['baseCurrency']['address'],
                pair_base_name=pool['quoteCurrency']['symbol'],
                pair_quote_name=pool['baseCurrency']['symbol'])

        else:
            new_pool = Tokens(
                pk=pool['smartContract']['address']['address'],
                pair_base_address=pool['baseCurrency']['address'],
                pair_quote_address=pool['quoteCurrency']['address'],
                pair_base_name=pool['baseCurrency']['symbol'],
                pair_quote_name=pool['quoteCurrency']['symbol'])
        objs.append(new_pool)

    # could get really risky!
    try:
        if len(objs) != 0:
            Tokens.objects.bulk_create(objs, len(objs), ignore_conflicts=True)
    except:
        print("Creation of objects from search results has failed!")
        pass
    return HttpResponse(json.dumps(result), content_type="application/json")


def searchTokenWithNetwork(request, network):

    value = request.GET['value']
    if not value.startswith('0x'):
        value = value.upper()

    res = controllers.queryStringinValueWithNetwork(value, network)
    if res.status_code != 200:
        return HttpResponse(json.dumps(error), content_type="application/json")

    res = res.json()
    addresses = []
    for i in res['data']['search']:
        addresses.append(i['subject']['address'])	

    result = controllers.queryAddressesForPairsWithNetwork(addresses, network)
    if result.status_code != 200:
        return HttpResponse(json.dumps(error), content_type="application/json")

    quotes = ["BUSD", "WBNB", "USDT"]
    result = result.json()
    if(len(result) >= 5):
        result = result[:5]
    objs = []
    for pool in result['data']['ethereum']['dexTrades']:
        if pool['baseCurrency']['symbol'] in quotes:
            if network == 'bsc':
                new_pool = PancakeTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['quoteCurrency']['address'],
                    pair_quote_address=pool['baseCurrency']['address'],
                    pair_base_name=pool['quoteCurrency']['symbol'],
                    pair_quote_name=pool['baseCurrency']['symbol'])
            elif network == 'ethereum':
                new_pool = UniswapTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['quoteCurrency']['address'],
                    pair_quote_address=pool['baseCurrency']['address'],
                    pair_base_name=pool['quoteCurrency']['symbol'],
                    pair_quote_name=pool['baseCurrency']['symbol'])
            else:
                new_pool = MaticTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['quoteCurrency']['address'],
                    pair_quote_address=pool['baseCurrency']['address'],
                    pair_base_name=pool['quoteCurrency']['symbol'],
                    pair_quote_name=pool['baseCurrency']['symbol'])
        else:
            if network == 'bsc':
                new_pool = PancakeTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['baseCurrency']['address'],
                    pair_quote_address=pool['quoteCurrency']['address'],
                    pair_base_name=pool['baseCurrency']['symbol'],
                    pair_quote_name=pool['quoteCurrency']['symbol'])
            elif network == 'ethereum':
                new_pool = UniswapTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['baseCurrency']['address'],
                    pair_quote_address=pool['quoteCurrency']['address'],
                    pair_base_name=pool['baseCurrency']['symbol'],
                    pair_quote_name=pool['quoteCurrency']['symbol'])
            else:
                new_pool = MaticTokens(
                    pk=pool['smartContract']['address']['address'],
                    pair_base_address=pool['baseCurrency']['address'],
                    pair_quote_address=pool['quoteCurrency']['address'],
                    pair_base_name=pool['baseCurrency']['symbol'],
                    pair_quote_name=pool['quoteCurrency']['symbol'])
        objs.append(new_pool)

    # could get really risky!
    try:
					if len(objs) != 0:
						if network == 'bsc':
								PancakeTokens.objects.bulk_create(objs, len(objs), ignore_conflicts=True)
						elif network == 'ethereum':
								UniswapTokens.objects.bulk_create(objs, len(objs), ignore_conflicts=True)
						else:
								MaticTokens.objects.bulk_create(objs, len(objs), ignore_conflicts=True)
    except:
        print("Creation of objects from search results has failed!")
        pass
    return HttpResponse(json.dumps(result), content_type="application/json")


def getTrendingTokens(request):

    topTokens = Tokens.objects.all().order_by('-views')[:10]
    payload = []
    for token in topTokens:
        res = {}
        res["pair_address"] = token.pair_address
        res["pair_base_name"] = token.pair_base_name
        res["pair_quote_name"] = token.pair_quote_name
        res["views"] = token.views

        payload.append(res)

    return HttpResponse(json.dumps(payload), content_type="application/json")


def getTrendingTokensWithNetwork(request, network):
	payload = []

	if network == 'bsc':
		topTokens = PancakeTokens.objects.all().order_by('-views')[:10]
	elif network == 'ethereum':
		topTokens = UniswapTokens.objects.all().order_by('-views')[:10]
	else:
		topTokens = MaticTokens.objects.all().order_by('-views')[:10]
	
	for token in topTokens:
		res = {}
		res["pair_address"] = token.pair_address
		res["pair_base_name"] = token.pair_base_name
		res["pair_quote_name"] = token.pair_quote_name
		res["views"] = token.views
		
		payload.append(res)
		
	return HttpResponse(json.dumps(payload), content_type="application/json")


def getSponsoredTokens(request):

    topTokens = Tokens.objects.filter(is_sponsored=True)
    payload = []
    for token in topTokens:
        res = {}
        res["pair_address"] = token.pair_address
        res["pair_base_name"] = token.pair_base_name
        res["pair_quote_name"] = token.pair_quote_name
        res["details"] = token.sponsored_details

        payload.append(res)

    return HttpResponse(json.dumps(payload), content_type="application/json")


def getSponsoredTokensWithNetwork(request, network):
	payload = []

	if network == 'bsc':
		topTokens = PancakeTokens.objects.filter(is_sponsored=True)
	elif network == 'ethereum':
		topTokens = UniswapTokens.objects.filter(is_sponsored=True)
	else:
		topTokens = MaticTokens.objects.filter(is_sponsored=True)
	
	for token in topTokens:
		res = {}
		res["pair_address"] = token.pair_address
		res["pair_base_name"] = token.pair_base_name
		res["pair_quote_name"] = token.pair_quote_name
		res["details"] = token.sponsored_details
		payload.append(res)
	
	return HttpResponse(json.dumps(payload), content_type="application/json")


# main call when requesting for pool address
def getTokenMetaData(request, poolAddress):

    if not poolAddress.startswith('0x'):
        payload = {
            "error": "Address Requested Must Start with 0x"
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")

    token = Tokens.objects.filter(pk=poolAddress)
    if len(token) != 0:
        token[0].views = token[0].views + 1
        token[0].save()
        token = token[0]

    else:
        # run pool search and add to DB
        result = controllers.getBaseQuoteFromPairAddress(poolAddress)
        if result.status_code != 200:
            error = {
                "error": "There Has Been A Error While Fetching Data"
            }
            return HttpResponse(json.dumps(error), content_type="application/json")

        result = result.json()
        result = result['data']['ethereum']['dexTrades']
        if len(result) == 0:
            payload = {
                "error": "Could Not Find The Pair Requested"
            }
            return HttpResponse(json.dumps(payload), content_type="application/json")

        quotes = ["BUSD", "WBNB", "USDT"]
        if(result[0]['baseCurrency']['symbol'] in quotes):
            token = Tokens(
                pair_address=result[0]['smartContract']['address']['address'],
                pair_base_name=result[0]['quoteCurrency']['symbol'],
                pair_quote_name=result[0]['baseCurrency']['symbol'],
                pair_base_address=result[0]['quoteCurrency']['address'],
                pair_quote_address=result[0]['baseCurrency']['address'],
            )
        else:
            token = Tokens(
                pair_address=result[0]['smartContract']['address']['address'],
                pair_base_name=result[0]['baseCurrency']['symbol'],
                pair_quote_name=result[0]['quoteCurrency']['symbol'],
                pair_base_address=result[0]['baseCurrency']['address'],
                pair_quote_address=result[0]['quoteCurrency']['address'],
            )
        token.save()

    ar = datetime.datetime.utcnow()
    temp = datetime.datetime(ar.year, ar.month, ar.day)
    start = temp - datetime.timedelta(days=8)
    end = datetime.datetime.utcnow()
    print(end)

    result = controllers.getMetaVolumeLQTrades(
        token.pair_quote_address,
        token.pair_base_address,
        token.pair_address,
        start.strftime('%Y%m%dT%H%M%S'),
    )

    if result.status_code != 200:
        error = {
            "status": "There has been an Error!",
        }
        return HttpResponse(json.dumps(error), content_type="application/json", status=500)

    result = result.json()

    payload = {
        "tokens": {
            "pair_address": token.pair_address,
            "pair_base_name": token.pair_base_name,
            "pair_quote_name": token.pair_quote_name,
            "pair_base_address": token.pair_base_address,
            "pair_quote_address": token.pair_quote_address,
        },
        "details": result['data']['ethereum']['details'],
        "dailyVolume": result['data']['ethereum']['dailyVolume'],
        "liquidity": result['data']['ethereum']['liquidity'],
        "trades": result['data']['ethereum']['trades'],
    }

    return HttpResponse(json.dumps(payload), content_type="application/json")


# main call when requesting for pool address with network
def getTokenMetaDataWithNetwork(request, network, poolAddress):

    if not poolAddress.startswith('0x'):
        payload = {
            "error": "Address Requested Must Start with 0x"
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")

    token = Tokens.objects.filter(pk=poolAddress)
    if len(token) != 0:
        token[0].views = token[0].views + 1
        token[0].save()
        token = token[0]

    else:
        if network == "bsc":
            exchangeArr = ["Pancake", "Pancake v2"]
        elif network == "ethereum":
            exchangeArr = ["Uniswap", "Uniswap v2"]
        elif network == "matic":
            exchangeArr = ["QuickSwap", "QuickSwap v2"]
        else:
            exchangeArr = []

        # run pool search and add to DB
        result = controllers.queryAddressesForPairsWithNetwork(
            poolAddress, network, exchangeArr)
        if result.status_code != 200:
            error = {
                "error": "There Has Been A Error While Fetching Data"
            }
            return HttpResponse(json.dumps(error), content_type="application/json")

        result = result.json()
        result = result['data']['ethereum']['dexTrades']
        if len(result) == 0:
            payload = {
                "error": "Could Not Find The Pair Requested"
            }
            return HttpResponse(json.dumps(payload), content_type="application/json")

        quotes = ["BUSD", "WBNB", "USDT"]
        if(result[0]['baseCurrency']['symbol'] in quotes):
            token = Tokens(
                pair_address=result[0]['smartContract']['address']['address'],
                pair_base_name=result[0]['quoteCurrency']['symbol'],
                pair_quote_name=result[0]['baseCurrency']['symbol'],
                pair_base_address=result[0]['quoteCurrency']['address'],
                pair_quote_address=result[0]['baseCurrency']['address'],
            )
        else:
            token = Tokens(
                pair_address=result[0]['smartContract']['address']['address'],
                pair_base_name=result[0]['baseCurrency']['symbol'],
                pair_quote_name=result[0]['quoteCurrency']['symbol'],
                pair_base_address=result[0]['baseCurrency']['address'],
                pair_quote_address=result[0]['quoteCurrency']['address'],
            )
        token.save()

    ar = datetime.datetime.utcnow()
    temp = datetime.datetime(ar.year, ar.month, ar.day)
    start = temp - datetime.timedelta(days=8)
    end = datetime.datetime.utcnow()
    print(end)

    result = controllers.getMetaVolumeLQTrades(
        token.pair_quote_address,
        token.pair_base_address,
        token.pair_address,
        start.strftime('%Y%m%dT%H%M%S'),
    )

    if result.status_code != 200:
        error = {
            "status": "There has been an Error!",
        }
        return HttpResponse(json.dumps(error), content_type="application/json", status=500)

    result = result.json()

    payload = {
        "tokens": {
            "pair_address": token.pair_address,
            "pair_base_name": token.pair_base_name,
            "pair_quote_name": token.pair_quote_name,
            "pair_base_address": token.pair_base_address,
            "pair_quote_address": token.pair_quote_address,
        },
        "details": result['data']['ethereum']['details'],
        "dailyVolume": result['data']['ethereum']['dailyVolume'],
        "liquidity": result['data']['ethereum']['liquidity'],
        "trades": result['data']['ethereum']['trades'],
    }

    return HttpResponse(json.dumps(payload), content_type="application/json")


def getSTFDailyChart(request):
    base = "0xe3916a4dc3c952c78348379a62d66869d9b59942"
    quote = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
    since = datetime.datetime.utcnow() - datetime.timedelta(days=15)
    till = datetime.datetime.utcnow()
    resolution = "1440"
    result = controllers.getOHLCData(
        base,
        quote,
        since.strftime('%Y%m%dT%H%M%S'),
        till.strftime('%Y%m%dT%H%M%S'),
        int(resolution)
    )
    if result.status_code != 200:
        error = {
            "status": "There has been an Error!",

        }
        return HttpResponse(json.dumps(error), content_type="application/json", status=500)

    result = result.json()
    payload = {
        "data": result['data']['ethereum']['dexTrades'],
    }
    return HttpResponse(json.dumps(payload), content_type="application/json")

# chart data for other charts


def getCandlesForChart(request):
    base = request.GET['base']
    quote = request.GET['quote']
    till = datetime.datetime.fromtimestamp(int(request.GET['till']))
    resolution = request.GET['resolution']

    if resolution == '1D':
        resolution = "1440"
    elif resolution == '1W':
        resolution = "10080"

    count = (int(request.GET['count'])) * (int(resolution))
    since = till - datetime.timedelta(minutes=count)

    print(since, till, count)
    result = controllers.getOHLCData(
        base,
        quote,
        since.strftime('%Y%m%dT%H%M%SZ'),
        till.strftime('%Y%m%dT%H%M%SZ'),
        int(resolution)
    )
    if result.status_code != 200:
        error = {
            "status": "There has been an Error!",

        }
        return HttpResponse(json.dumps(error), content_type="application/json", status=500)

    res = []
    result = result.json()
    for ohlc in result['data']['ethereum']['dexTrades']:
        obj = {}
        datetime1 = datetime.datetime.strptime(
            ohlc['timeInterval']['minute'], "%Y-%m-%dT%H:%M:%SZ")
        if datetime1 > since and datetime1 < till:
            obj['time'] = int(datetime1.timestamp())
            obj['open'] = ohlc['open']
            obj['high'] = ohlc['high']
            obj['low'] = ohlc['low']
            obj['close'] = ohlc['close']
            obj['volume'] = ohlc['volume']
            res.append(obj)

    payload = {
        "data": res,
    }
    print(len(payload["data"]))
    return HttpResponse(json.dumps(payload), content_type="application/json")


def getCandlesForChartWithNetwork(request, network):
    base = request.GET['base']
    quote = request.GET['quote']
    till = datetime.datetime.fromtimestamp(int(request.GET['till']))
    resolution = request.GET['resolution']

    if resolution == '1D':
        resolution = "1440"
    elif resolution == '1W':
        resolution = "10080"

    count = (int(request.GET['count'])) * (int(resolution))
    since = till - datetime.timedelta(minutes=count)

    print(since, till, count)
    result = controllers.getOHLCDataWithNetwork(
        base,
        quote,
        since.strftime('%Y%m%dT%H%M%SZ'),
        till.strftime('%Y%m%dT%H%M%SZ'),
        int(resolution),
        network
    )
    if result.status_code != 200:
        error = {
            "status": "There has been an Error!",

        }
        return HttpResponse(json.dumps(error), content_type="application/json", status=500)

    res = []
    result = result.json()
    for ohlc in result['data']['ethereum']['dexTrades']:
        obj = {}
        datetime1 = datetime.datetime.strptime(
            ohlc['timeInterval']['minute'], "%Y-%m-%dT%H:%M:%SZ")
        if datetime1 > since and datetime1 < till:
            obj['time'] = int(datetime1.timestamp())
            obj['open'] = ohlc['open']
            obj['high'] = ohlc['high']
            obj['low'] = ohlc['low']
            obj['close'] = ohlc['close']
            obj['volume'] = ohlc['volume']
            res.append(obj)

    payload = {
        "data": res,
    }
    print(len(payload["data"]))
    return HttpResponse(json.dumps(payload), content_type="application/json")


# https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/0xe9e7cea3dedca5984780bafc599bd69add087d56
