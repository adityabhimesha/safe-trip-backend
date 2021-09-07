from os import environ
headers = {
    'X-API-KEY': environ["BITQUERY_API_KEY"],
    'Content-Type': 'application/json',
}

searchQuery = """
    query($name:String!) {
        search(string: $name, network: bsc) {
          subject {
            __typename
            ... on Address {
              address
              annotation
            }
            ... on Currency {
              symbol
              name
              address
              tokenType
              decimals
            }
            ... on SmartContract {
              address
              annotation
              contractType
              protocol
            }
          }
          network {
            network
          }
        }
      }
"""

poolSearchQuery = """
    query ($arr: [String!]) {
  ethereum(network: bsc) {
    dexTrades(
      options: {limit: 25, desc: "count"}
      baseCurrency: {in: $arr}
      exchangeName: {in: ["Pancake", "Pancake v2"]}
    ) {
      smartContract {
        address {
          address
        }
      }
      count
      exchange {
        name
      }
      baseCurrency {
        address
        symbol
      }
      quoteCurrency {
        address
        symbol
      }
    }
  }
}
 
"""

poolSearchQueryMultiNetwork = """
query ($arr: [String!], $network:EthereumNetwork, $exchangearr: [String!]) {
  ethereum(network: $network) {
    dexTrades(
      options: {limit: 25, desc: "count"}
      baseCurrency: {in: $arr}
      exchangeName: {in: $exchangearr}
    ) {
      smartContract {
        address {
          address
        }
      }
      count
      exchange {
        name
      }
      baseCurrency {
        address
        symbol
      }
      quoteCurrency {
        address
        symbol
      }
    }
  }
}
"""

baseQuoteAddressQuery = """
query($pool:String){
  ethereum(network: bsc) {
    dexTrades(
      options: {limit: 25, desc: "count"}
      exchangeName: {in: ["Pancake", "Pancake v2"]}
      smartContractAddress: {is: $pool}
    ) {
      smartContract {
        address {
          address
        }
      }
      count
      exchange {
        name
      }
      baseCurrency {
        address
        symbol
      }
      quoteCurrency {
        address
        symbol
      }
    }
  }
}

"""


metaDataQuery = """

query($base:String, $quote:String, $pair:String, $balance:[String!], $since:ISO8601DateTime){
  ethereum(network: bsc) {
    details: address(address: {is: $quote}) {
      address
      smartContract {
        attributes {
          name
          value
        }
        currency {
          symbol
          name
          decimals
          tokenType
        }
      }
    }
    dailyVolume: dexTrades(
      baseCurrency: {is: $base}
      quoteCurrency: {is: $quote}
      exchangeName: {in: ["Pancake", "Pancake v2"]}
      time: {since: $since}
    ) {
      timeInterval {
        day(count: 1)
      }
      tradeAmount(in: USD)
      quotePrice
    }
		liquidity: address(address: {is: $pair}) {
      address
      balances(currency: {in: $balance}) {
        currency {
          symbol
          address
        }
        value
      }
    }
    trades:dexTrades(
      options: {limit: 500, desc: ["block.timestamp.time"]}
      exchangeName: {in: ["Pancake", "Pancake v2"]}
      baseCurrency: {is: $base}
      quoteCurrency: {is: $quote}
      date: {since: "2021-08-08"}
    ) {
      block {
        height
        timestamp {
          time(format: "%Y-%m-%d %H:%M:%S")
        }
      }
      buyAmount
      buyCurrency {
        address
        symbol
      }
      sellAmount
      sellCurrency {
        address
        symbol
      }
      transaction {
        hash
      }
      side
      taker {
        address
      }
      maker{
        address
      }
      tradeAmount(in: USD)
      price
    }
  }
}


"""

ohlcQuery = """

query($base:String,$quote:String,$time:Int,$since:ISO8601DateTime, $till:ISO8601DateTime){
  ethereum(network: bsc) {
    dexTrades(
      options: {asc: "timeInterval.minute"}
      date: {till:$till, since: $since}
      exchangeName: {in:["Pancake", "Pancake v2"]}
      baseCurrency: {is: $base}
      quoteCurrency: {is: $quote}
    ) {
      timeInterval {
        minute(count: $time, format: "%Y-%m-%dT%H:%M:%SZ")
      }
      volume: quoteAmount
      high: quotePrice(calculate: maximum)
      low: quotePrice(calculate: minimum)
      open: minimum(of: block, get: quote_price)
      close: maximum(of: block, get: quote_price)
    }
  }
}

"""


# Pancake Trade Volume for different currency pairs

# {
#   ethereum(network: bsc) {
#     dexTrades(
#       options: {desc: "tradeAmount"}
#       exchangeName: {is: "Pancake"}
#       date: {since: "2020-09-12", till: "2020-12-12"}
#     ) {
#       buyCurrency {
#         address
#         symbol
#       }
#       sellCurrency {
#         address
#         symbol
#       }
#       trades: count
#       tradeAmount(in: USD)
#     }
#   }
# }
