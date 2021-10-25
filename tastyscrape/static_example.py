"""
Example use case of static set;
Notice top-level absence of asyncio
"""
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.streamer import DataStreamer
from tastyscrape.bases.underlying import Underlying
from tastyscrape.bases.underlying import UnderlyingType
from tastyscrape.static.options.multi import chain_quote
from tastyscrape.static.util.options.search import get_all_expirations, get_all_strikes

def main():
    TW_USER = ""
    TW_PASS = ""
    #Authenticate with TastyWorks
    tasty_client = TastyAPISession(TW_USER, TW_PASS)
    streamer = DataStreamer(tasty_client)
    print(f'Streaming Token: {streamer.get_streamer_token()}')

    #Specify what chain we want
    SPY = Underlying("F", UnderlyingType.EQUITY) #SPY ETF
    expire = get_all_expirations(tasty_client, SPY)[0]
    strikes = get_all_strikes(tasty_client,SPY,expire)

    #Get quote for the entire chain
    spy_chain = chain_quote(tasty_client,streamer,SPY,expire)
    print(spy_chain)



if __name__ == '__main__':
    main()
