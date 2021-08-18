import requests
from . import queries
from os import environ

def queryStringinValue(value):
    # input in string or contract address
    # output out an array of contract addresses - 25 limit
    var = {
        "name" : value,
    }
    res = requests.post(environ["BITQUERY_URL"],
                            json={'query': queries.searchQuery, 'variables' : var},
                            headers=queries.headers)
    return res

def queryAddressesForPairs(addresses):
    # input in an array of contract addresses
    # output out an array of pairs in order of trades.
    var = {
        "arr" : addresses,
    }
    res = requests.post(environ["BITQUERY_URL"],
                        json={'query': queries.poolSearchQuery, 'variables' : var},
                        headers=queries.headers)
    
    return res

def getBaseQuoteFromPairAddress(pairAddress):
    var = {
        "pool" : pairAddress,
    }
    res = requests.post(environ["BITQUERY_URL"],
                        json={'query': queries.baseQuoteAddressQuery, 'variables' : var},
                        headers=queries.headers)
    
    return res


def getMetaVolumeLQTrades(baseAddress, quoteAddress, pairAddress, since):
    var = {
        "base" : baseAddress,
        "quote" : quoteAddress,
        "pair" : pairAddress,
        "since" : since,
        "balance" : [
            baseAddress,
            quoteAddress,
        ]
    }
    res = requests.post(environ["BITQUERY_URL"],
                        json={'query': queries.metaDataQuery, 'variables' : var},
                        headers=queries.headers)
        
    return res