from datetime import date, datetime
from typing import List, Text, Dict
from decimal import Decimal
import math
import re

from tastyscrape.bases import static_option_chain
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.underlying import Underlying
from tastyscrape.bases.underlying import UnderlyingType
from tastyscrape.bases.option import Option
from tastyscrape.bases.option import OptionType

def get_all_expirations(session: TastyAPISession, underlying: Underlying) -> List:
    this_chain = static_option_chain.get_option_chain(session,underlying)
    return this_chain.get_all_expirations()

def get_all_strikes(session: TastyAPISession, underlying: Underlying, expiration: date) -> List:
    this_chain = static_option_chain.get_option_chain(session,underlying,expiration)
    return this_chain.get_all_strikes()

def get_option_from_dxfeed(dxstr: Text, type: UnderlyingType) -> Option:
    parsed = re.compile("(\.)([A-Z.]+)(\d{2})(\d{2})(\d{2})([CP])([\d.]+)").match(dxstr)


    thisCenturyFloor = round(datetime.now().year-49,-2)
    thisYearInt = datetime.now().year-thisCenturyFloor
    yr = parsed[3]+round(datetime.now().year-49,-2) < datetime.now().year-round(datetime.now().year-49,-2)
    if(yr < thisYearInt): #this means that the expiration is 01, 02 with year being 98,99, add 100 years to the base
        yr += 100

    return Option(ticker=parsed[2], expiry=date(year=yr,month=parsed[4],day=parsed[5]), strike=strike, option_type=option_type, underlying_type=type)

def parse_chain(resp_chain: List[[Dict]]) -> List[List[Dict]]:
    #adds dictionaries for every
    parser = re.compile("(\.)([A-Z.]+)(\d{2})(\d{2})(\d{2})([CP])([\d.]+)")
    ichain = []
    for option in resp_chain:
        parsed_symbol = parser.match(option["eventSymbol"])
        option["ticker"] =
