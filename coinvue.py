# CoinCap API Python - http.client Docs
# https://docs.coincap.io/

import requests
import json


class Crypto:

    def crypto_top_50(self):
        url = "http://api.coincap.io/v2/assets?limit=50"

        payload = {}
        headers = {}

        response = requests.request(
            "GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text.encode("utf8"))

        coin_data = json_data["data"]
        return coin_data

        # Calls upon the api to fetch token data
