exports.searchFirstQuery = `
query($name: String!){
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
}`

exports.searchSecondQuery =
`
query($arr: [String!]){
    ethereum(network: bsc) {
        dexTrades(
            options: {limit: 25, desc: "count"}
            baseCurrency: {in : $arr}
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

`
