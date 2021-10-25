from tastyscrape.bases import static_option_chain
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.underlying import Underlying

def get_all_expirations(session: TastyAPISession, underlying: Underlying):
    this_chain = static_option_chain.get_option_chain(session,underlying)
    return this_chain.get_all_expirations()
