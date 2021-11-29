# import ingest
try:
    from secrets import finn_hub_key
except ImportError:
    print('Failed to import "finn_hub_key" from "secrets.py". Aborting fast-forward.')
    exit(1)

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import sleep

import psycopg2
from pgcopy import CopyManager
import finnhub

CONNECTION = "postgres://root:password@timedb:5432/quantx"
symbols = []
# fast forward till the end of the past hour
end_time = datetime.now()
end_time = end_time.replace(second=0, microsecond=0, minute=0, hour=end_time.hour);
end_time -= timedelta(minutes=1)

def main():
    with psycopg2.connect(CONNECTION) as conn:
        with conn.cursor() as curs:
            curs.execute("""select quote.symbol, MAX(time) from 
                        symbol LEFT JOIN quote ON symbol.symbol = quote.symbol
                        GROUP BY quote.symbol
                        ;""")
            symbol_time = curs.fetchall()
    
    # convert list of tuple to list of list:
    symbol_time = [list(tup) for tup in symbol_time]
    for entry in symbol_time:
        if entry[1] is None:
            # by default, retrieve one month of data
            entry[1] = datetime.now() - timedelta(days=30)
        else:
            entry[1] += timedelta(minutes=1) # start grabbing data from 1 min after the last data point
    if not symbol_time:
        raise RuntimeWarning("No Symbols were retrieved from db!")
    
    for entry in symbol_time:
        start_time = entry[1]
    current_time = start_time
    while current_time < end_time:
        current_time = advance_one_month(current_time, symbol=entry[0])


def advance_one_month(current_start, symbol):
    '''Advance one month per api call because of FinnHub restrictions'''
    current_end = current_start + relativedelta(months=+1, minutes=-1)
    current_end = min(current_end, end_time)
    print(f"Retreiving data from {current_start} to {current_end}")
    responses = get_candles_for_symbol(current_start, current_end, symbol)
    write_db(responses, symbol)
    return current_end + timedelta(minutes = 1)


def write_db(responses, symbol):
    with psycopg2.connect(CONNECTION) as conn:
        cols=['time', 'symbol', 'price_open', 'price_high', 'price_low', 'price_close']
        mgr = CopyManager(conn, 'quote', cols)
        for response in responses:
            if response['s'] != 'ok': # out of market time, etc.
                continue
            datetimes = [datetime.fromtimestamp(x) for x in response['t']]
            data = [list(a) for a in zip(
                datetimes, 
                [symbol]*len(datetimes), 
                response['o'], response['h'], response['l'], response['c'])]
            mgr.copy(data)
        


def get_candles_for_symbol(start: datetime, end: datetime, symbol: str):
    start_time = int(start.timestamp())
    end_time = int(end.timestamp())
    
    responses = []
    finnhub_client = finnhub.Client(api_key=finn_hub_key)

    # make the call

    for _ in range(10):
        try:
            response = finnhub_client.stock_candles(symbol, '1', start_time, end_time)
        except finnhub.FinnhubAPIException as e:
            if  e.status_code == 429: # out of API calls
                sleep(60)
                continue
            else:
                raise e
        break
    else:
        raise RuntimeWarning(f"API Call Failed for symbol {symbol}, start time = {start_time}, end time = {end_time}.")
    #print(response)
    responses.append(response)
    return responses

if __name__ == "__main__":
    main()