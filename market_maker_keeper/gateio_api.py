#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import urllib
import hmac

import requests


class GateIOApi:
    def __init__(self,api_server: str, api_key: str, secret_key: str, timeout: float):
        assert(isinstance(api_server, str))
        assert(isinstance(api_key, str))
        assert(isinstance(secret_key, str))
        assert(isinstance(timeout, float))

        self.api_server = api_server
        self.api_key = api_key
        self.secret_key = secret_key
        self.timeout = timeout

    def pairs(self):
        return self._http_get("/api2/1/pairs", '')

    def marketinfo(self):
        return self._http_get("/api2/1/marketinfo", '')

    def marketlist(self):
        return self._http_get("/api2/1/marketlist", '')

    def tickers(self):
        return self._http_get("/api2/1/tickers", '')

    def ticker(self, pair: str):
        assert(isinstance(pair, str))
        return self._http_get("/api2/1/ticker", pair)

    def order_book(self, pair: str):
        assert(isinstance(pair, str))
        return self._http_get("/api2/1/orderBook", pair)

    def all_trade_history(self, pair: str):
        assert(isinstance(pair, str))
        return self._http_get("/api2/1/tradeHistory", pair)

    def get_balances(self):
        return self._http_post("/api2/1/private/balances", {})

    def get_orders(self):
        URL = "/api2/1/private/openOrders"
        params = {}
        return self._http_post(URL, params)

    def get_order(self, orderNumber, currencyPair):
        URL = "/api2/1/private/getOrder"
        return self._http_post(URL, params)

    def buy(self, currencyPair, rate, amount):
        URL = "/api2/1/private/buy"
        params = {'currencyPair': currencyPair, 'rate':rate, 'amount':amount}
        return self._http_post(URL, params)

    def sell(self, currencyPair, rate, amount):
        URL = "/api2/1/private/sell"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return self._http_post(URL, params)

    def cancel_order(self, pair: str, order_id: int):
        assert(isinstance(pair, str))
        assert(isinstance(order_id, int))
        return self._http_post("/api2/1/private/cancelOrder", {'orderNumber': order_id, 'currencyPair': pair})

    def cancel_all_orders(self, pair: str):
        assert(isinstance(pair, str))
        return self._http_post("/api2/1/private/cancelAllOrders", {'type': -1, 'currencyPair': pair})

    def get_trade_history(self, pair: str):
        assert(isinstance(pair, str))
        return self._http_post("/api2/1/private/tradeHistory", {'currencyPair': pair})

    def _http_get(self, resource: str, params: str):
        assert(isinstance(resource, str))
        assert(isinstance(params, str))

        return requests.get(url=f"{self.api_server}{resource}/{params}", timeout=self.timeout).json()

    def _create_signature(self, params):
        assert(isinstance(params, dict))

        sign = ''
        for key in (params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        sign = sign[:-1]

        return hmac.new(key=bytes(self.secret_key, encoding='utf8'),
                        msg=bytes(sign, encoding='utf8'),
                        digestmod=hashlib.sha512).hexdigest()

    def _http_post(self, resource: str, params: dict):
        assert(isinstance(resource, str))
        assert(isinstance(params, dict))

        return requests.post(url=f"{self.api_server}{resource}",
                             data=urllib.parse.urlencode(params),
                             headers={"Content-Type": "application/x-www-form-urlencoded",
                                      "KEY": self.api_key,
                                      "SIGN": self._create_signature(params)},
                             timeout=self.timeout).json()