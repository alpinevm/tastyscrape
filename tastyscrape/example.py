import asyncio
import calendar
import logging
from os import environ
from datetime import date, timedelta
from decimal import Decimal

from tastyscrape.models import option_chain, underlying
from tastyscrape.models.option import Option, OptionType
from tastyscrape.models.order import (Order, OrderDetails, OrderPriceEffect, OrderType)
from tastyscrape.models.session import TastyAPISession
from tastyscrape.models.trading_account import TradingAccount
from tastyscrape.models.underlying import UnderlyingType
from tastyscrape.streamer import DataStreamer
from tastyscrape.tastyscrape_api import tasty_session

LOGGER = logging.getLogger(__name__)


async def main_loop(session: TastyAPISession, streamer: DataStreamer):

    sub_values = {
        "Quote": ["SPY"]
    }
    # Get an options chain
    undl = underlying.Underlying('SPY')

    chain = await option_chain.get_option_chain(session, undl)
    LOGGER.info('Chain strikes: %s', chain.get_all_strikes())

    await streamer.add_data_sub(sub_values)

    async for item in streamer.listen():
        LOGGER.info('Received item: %s' % item.data)

def main():
    tasty_client = tasty_session.create_new_session(environ.get("TW_USER"), environ.get("TW_PASSWORD"))
    streamer = DataStreamer(tasty_client)

    LOGGER.info('Streamer token: %s' % streamer.get_streamer_token())
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main_loop(tasty_client, streamer))
    except Exception:
        LOGGER.exception('Exception in main loop')
    finally:
        # find all futures/tasks still running and wait for them to finish
        pending_tasks = [
            task for task in asyncio.Task.all_tasks() if not task.done()
        ]
        loop.run_until_complete(asyncio.gather(*pending_tasks))
        loop.close()


if __name__ == '__main__':
    main()
