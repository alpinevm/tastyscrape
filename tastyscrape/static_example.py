"""
Example use case of static set;
Notice top-level absence of asyncio
"""
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.streamer import DataStreamer
from tastyscrape.bases.underlying import Underlying
from tastyscrape.bases.underlying import UnderlyingType
from tastyscrape.static.options.multi import chain_quote
from tastyscrape.static.util.options.search import get_all_expirations

def main():
    #Authenticate with TastyWorks
    tasty_client = TastyAPISession("TW_USER","TW_PASS")
    streamer = DataStreamer(tasty_client)
    print(f'Streaming Token: {streamer.get_streamer_token()}')

    #Specify what chain we want
    SPY = Underlying("SPY", UnderlyingType.EQUITY) #SPY ETF
    expire = get_all_expirations(tasty_client, SPY)[0] #Get closest expiry

    #Get quote for the entire chain
    for option in chain_quote(tasty_client,streamer,SPY,expire): print(option)



if __name__ == '__main__':
    main()
