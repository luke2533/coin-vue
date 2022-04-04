# import http.client
# # import csv
# # To store any data from api request
# import json
# # JSON is used to store data


# class Crypto:

#     def crypto_top_100(self):
#         conn = http.client.HTTPSConnection("api.coincap.io")
#         payload = ''
#         headers = {}
#         conn.request("GET", "/v2/assets", payload, headers)
#         res = conn.getresponse()
#         data = res.read()
#         # print(data.decode("utf-8"))

#         coindata = json.loads(data)
#         print(coindata)
#         print("CoinCap working")
#         return coindata

# # CoinCap API Python - http.client Docs
# # https://docs.coincap.io/

import requests
import json

class Crypto:

    def crypto_top_100(self):
        url = "http://api.coincap.io/v2/assets"

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        json_data = json.loads(response.text.encode("utf8"))
        # print(response.text)
        # print(json_data)

        coin_data = json_data["data"]
        print(coin_data)
        return coin_data