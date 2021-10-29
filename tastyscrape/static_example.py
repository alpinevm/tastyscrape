"""
Example use case of static set;
Notice top-level absence of asyncio
"""
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.streamer import DataStreamer
from tastyscrape.bases.underlying import Underlying
from tastyscrape.bases.underlying import UnderlyingType
from tastyscrape.static.options.multi import chain_quote, option_quote
from tastyscrape.bases.option import Option, OptionType
from tastyscrape.static.util.options.search import get_all_expirations, parse_chain, get_option_from_dxfeed

from datetime import date
from decimal import Decimal

import time
def main():
    TW_USER = ""
    TW_PASS = ""

    #Authenticate with TastyWorks
    tasty_client = TastyAPISession(TW_USER, TW_PASS)
    streamer = DataStreamer(tasty_client)
    print(f'Streaming Token: {streamer.get_streamer_token()}')

    #Specify what chain we want
    SPY = Underlying("SPY", UnderlyingType.EQUITY) #SPY ETF
    expire = get_all_expirations(tasty_client, SPY)[0]

    #Get quote for the entire chain
    spy_chain = chain_quote(tasty_client,streamer,SPY,expire)

    #Parse Chain: Insert a new dictionary key with an Option Object for each item in List
    spy_chain_obj = parse_chain(spy_chain, UnderlyingType.EQUITY)

    #Now define some explicit contracts
    qqq_call = Option(
        ticker="QQQ",
        expiry=date(year=2024,month=1,day=19),
        strike=Decimal(400),
        option_type=OptionType.CALL,
        underlying_type=UnderlyingType.EQUITY,
    )
    f_put = Option(
        ticker="F",
        expiry=date(year=2024, month=1, day=19),
        strike=Decimal(10),
        option_type=OptionType.PUT,
        underlying_type=UnderlyingType.EQUITY,
    )

    #Get quotes of list
    this_quote = option_quote(streamer,[qqq_call, f_put])

    #Get Option object from dxfeed symbol
    this_obj = get_option_from_dxfeed(this_quote[0]["eventSymbol"], UnderlyingType.EQUITY)



if __name__ == '__main__':
    main()
