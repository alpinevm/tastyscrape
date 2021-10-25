"""
OptionChain class and functions built around requests instead of aiohttp;
For use with "static" methods
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Dict

import requests

from tastyscrape.bases.option import Option, OptionType
from tastyscrape.bases.underlying import Underlying, UnderlyingType


class OptionChain(object):
    def __init__(self, options):
        self.options = options

    def _get_filter_strategy(self, key, unique=True):
        values = [getattr(option, key) for option in self.options]
        if not any(values):
            raise Exception(f'No values found for specified key: {key}')

        values = list(set(values)) if unique else list(values)
        return sorted(values)


    def get_all_strikes(self):
        return self._get_filter_strategy('strike')

    def get_all_expirations(self):
        return self._get_filter_strategy('expiry')



def get_option_chain(session, underlying: Underlying, expiration: date = None) -> OptionChain:
    data = _get_tasty_option_chain_data(session, underlying)
    res = []

    for exp in data['expirations']:
        exp_date = datetime.strptime(exp['expiration-date'], '%Y-%m-%d').date()

        if expiration and expiration != exp_date:
            continue

        for strike in exp['strikes']:
            strike_val = Decimal(strike['strike-price'])
            for option_types in OptionType:
                new_option = Option(
                    ticker=underlying.ticker,
                    expiry=exp_date,
                    strike=strike_val,
                    option_type=option_types,
                    underlying_type=UnderlyingType.EQUITY
                )
                res.append(new_option)
    return OptionChain(res)


def _get_tasty_option_chain_data(session, underlying) -> Dict:
    with requests.request(
            'GET',
            f'{session.API_url}/option-chains/{underlying.ticker}/nested',
            headers=session.get_request_headers()) as response:

        if response.status_code != 200:
            raise Exception(f'Could not find option chain for symbol {underlying.ticker}')
        resp = response.json()

        # NOTE: Have not seen an example with more than 1 item. No idea what that would be.
        return resp['data']['items'][0]
