"""
Example use case of static greek set for options;
Notice top-level absence of asyncio
"""
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.streamer import DataStreamer
from tastyscrape.bases.underlying import Underlying
from tastyscrape.bases.underlying import UnderlyingType
from tastyscrape.static.options.greek import chain_greeks, option_greeks
from tastyscrape.bases.option import Option, OptionType
from tastyscrape.static.util.options.search import get_all_expirations, parse_chain, split_chain

from dotenv import load_dotenv
import os
from datetime import date
from decimal import Decimal
def main():
    load_dotenv()
    #Authenticate with TastyWorks
    tasty_client = TastyAPISession(os.getenv("TW_USER"), os.getenv("TW_PASS"))
    streamer = DataStreamer(tasty_client)
    print(f'Streaming Token: {streamer.get_streamer_token()}')

    #Specify what chain we want
    SPY = Underlying("SPY", UnderlyingType.EQUITY) #SPY ETF
    expire = get_all_expirations(tasty_client, SPY)[0]

    #Get greeks for the entire chain
    spy_chain = chain_greeks(tasty_client,streamer,SPY,expire)

    #Parse Chain: Insert a new dictionary key with an Option Object for each item in List
    #Split Chain: Split up the chain into puts and calls; get the calls
    spy_chain_obj = split_chain(parse_chain(spy_chain, UnderlyingType.EQUITY))["calls"]

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

    #Get greeks of list, note that validation that these options exist will have to be done beforehand, else program will hang
    this_quote = option_greeks(streamer,[qqq_call, f_put])



if __name__ == '__main__':
    main()
