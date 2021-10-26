from datetime import date, datetime
from typing import List, Text
from decimal import Decimal
import math

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
    #There is probably a more efficient way to do this with regex but this is more readable and will do for now
    ticker = ""
    expiry = date(year=1970, month=1, day=1)
    strike = Decimal(0)
    option_type = ""
    underlying_type = type

    tickEnd = 0
    tickComp = False
    dateComp = False
    pc = False
    for i in range(len(dxstr)):
        if(i != 0):
            #build ticker:
            if(dxstr[i].isdigit() and not tickComp):
                ticker = dxstr[1:i]
                tickEnd = i
                tickComp = True
            if(tickComp and not dateComp):
                thisCenturyFloor = round(datetime.now().year-49,-2)
                thisYearInt = datetime.now().year-thisCenturyFloor
                yr = int(dxstr[tickEnd:tickEnd+2])+thisCenturyFloor
                month = int(dxstr[tickEnd+2:tickEnd+4])
                day = int(dxstr[tickEnd+4:tickEnd+6])
                if(yr < thisYearInt): #this means that the expiration is 01, 02 with year being 98,99, add 100 years to the base
                    yr += 100
                expiry = date(year=yr,month=month,day=day)
                dateComp = True
            if(dateComp and not pc):
                option_type = dxstr[i]
                if(option_type == "P"):
                    option_type = OptionType.PUT
                else:
                    option_type = OptionType.CALL
                pc = True
            if(pc):
                strike = Decimal(dxstr[i+7:])
                break
    return Option(ticker=ticker,expiry=expiry,strike=strike,option_type=option_type,underlying_type=underlying_type)

def organize_chain_response(chain: List) -> List:
    #create a new strike entry todo
    for resp in chain:
        pass
