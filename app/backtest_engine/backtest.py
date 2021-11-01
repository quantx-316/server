import json 
import socket 
import os
import random

from subprocess import Popen, DEVNULL
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm.session import Session

from app.schemas.backtests import Backtest
from app.schemas.quotes import Quote 
from app.utils.constants import IntervalName

from app.routers.quotes import get_single_quote 

from .util import send_msg, recv_msg, DateTimeEncoder

def get_timestamps_in_range(start: datetime, end: datetime, interval: IntervalName):
    """
    Returns a list of datetime objects representing start times for candles 
    with the given candle interval, from start to end.
    """
    print("start: " + str(start))
    print("end: " + str(end))

    if interval == IntervalName.minute:
        return [start + timedelta(minutes=i) for i in range(0, (end - start).seconds // 60)]
    elif interval == IntervalName.fiveMinute:
        return [start + timedelta(minutes=5*i) for i in range(0, (end - start).seconds // 300)]
    elif interval == IntervalName.fifteenMinute:
        return [start + timedelta(minutes=15*i) for i in range(0, (end - start).seconds // 900)]
    elif interval == IntervalName.thirtyMinute:
        return [start + timedelta(minutes=30*i) for i in range(0, (end - start).seconds // 1800)]
    elif interval == IntervalName.hour:
        return [start + timedelta(hours=i) for i in range(0, (end - start).seconds // 3600)]
    elif interval == IntervalName.day:
        return [start + timedelta(days=i) for i in range(0, (end - start).days)]
    elif interval == IntervalName.week:
        return [start + timedelta(weeks=i) for i in range(0, (end - start).days // 7)]
    else:
        raise ValueError("Invalid interval name.")


def run_backtest(backtest: Backtest, db: Session) -> str:
    candles: List[datetime] = get_timestamps_in_range(backtest.test_start, backtest.test_end, backtest.test_interval)

    # Get quotes for each candle
    quotes: List[Quote] = []
    for candle in candles:
        quote = get_single_quote('AAPL', backtest.test_interval, candle, db)
        quotes.append(quote)

    # Set up execution directory 
    dir_name = "_backtest_exec_" + str(backtest.id)
    dir_path = os.path.join(os.getcwd(), 'app', 'backtest_engine', dir_name)
    os.mkdir(dir_path)
    
    # Copy host layer program and util file to directory
    os.system(f'cp /main/app/backtest_engine/host_layer.py {dir_path}/')
    os.system(f'cp /main/app/backtest_engine/util.py {dir_path}/')
    
    # Write user code to directory
    with open(f'{dir_path}/user_code.py', 'w') as f:
        f.write(backtest.code_snapshot)

    # Start the host layer subprocess
    with open(f'{dir_path}/out.txt', 'w') as out_file:
        # Pick a port 
        port = random.randint(10000, 60000)

        host_layer_process = Popen(
            ['python3', f'{dir_path}/host_layer.py', str(port)], 
            cwd=dir_path, 
            stdout=out_file, 
            stderr=out_file
        )

        # Open a socket and listen for connection from host layer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                # Connected. Send backtest information and then quotes 
                payload = {
                    'id': backtest.id,
                    'interval': backtest.test_interval,
                    'test_start': str(backtest.test_start),
                    'test_end': str(backtest.test_end)
                }

                send_msg(conn, json.dumps(payload).encode())

                for quote in quotes:
                    quote_msg = {
                        'symbol': quote.symbol,
                        'time': str(quote.candle),
                        'price_open': quote.price_open,
                        'price_high': quote.price_high,
                        'price_low': quote.price_low,
                        'price_close': quote.price_close
                    }
                    send_msg(conn, json.dumps(quote_msg).encode())
                
                send_msg(conn, 'go'.encode())
                
                # Blocking call, wait to receive a message
                recv = recv_msg(conn)
                recv_parsed = json.loads(recv.decode())

                print(recv_parsed)

                # return json.dumps(recv_parsed, indent=4, default=str)
                return recv
