from datetime import date
from typing import List
import asyncio

from tastyscrape.bases import option_chain
from tastyscrape.bases.session import TastyAPISession
from tastyscrape.bases.streamer import DataStreamer
from tastyscrape.bases.underlying import Underlying

async def _chain_quote(session: TastyAPISession, streamer: DataStreamer, underlying: Underlying, expiration: date) -> List:
    # Get an options chain
    chain = await option_chain.get_option_chain(session, underlying, expiration)

    # Master list of every option code in the chain
    res = []
    for option in chain.options:
        res.append(option.get_dxfeed_symbol())
    sub_value = {
        "Quote": res
    }
    await streamer.add_data_sub(sub_value)

    #read cometd connection until we hit len(res)

    data = []
    tally = 0
    async for item in streamer.listen():
        data += item.data
        tally += len(item.data)
        if(tally == len(res)):
            break

    return data

def chain_quote(session: TastyAPISession, streamer: DataStreamer, underlying: Underlying, expiration: date) -> List:
    #Create temporary async loop to execute op
    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(_chain_quote(session,streamer,underlying,expiration))
    asyncio.get_event_loop().stop()
    return resp