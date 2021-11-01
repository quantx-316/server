import socket
import json
import sys
from util import send_msg, recv_msg

from user_code import backtest_tick

class Portfolio():
    def __init__(self):
        self.cash = 100000
        self.positions = {}
        self.transactions = []

    def action(self, action, quoteset):
        if action['action'] == 'buy':
            if self.cash < quoteset[action['symbol']]['price_close']:
                #TODO: error message to user
                print('Not enough cash')
                return

            self.cash -= action['num_shares'] * quoteset[action['symbol']]['price_close']

            if action['symbol'] in self.positions.keys():
                self.positions[action['symbol']] += action['num_shares']
                self.transactions.append(action)
            else:
                self.positions[action['symbol']] = action['num_shares']
                self.transactions.append(action)
            
        elif action['action'] == 'sell':
            if action['symbol'] in self.positions.keys():
                if self.positions[action['symbol']] < action['num_shares']:
                    #TODO: error message to user
                    print('Not enough shares')
                    return

                self.cash += action['num_shares'] * quoteset[action['symbol']]['price_close']

                self.positions[action['symbol']] -= action['num_shares']
                self.transactions.append(action)

    def value(self, quoteset):
        value = self.cash
        for symbol in self.positions.keys():
            value += self.positions[symbol] * quoteset[symbol]['price_close']
        return value


def main():    
    # Open a TCP socket and connect to the server process 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = int(sys.argv[1])
        s.connect(('localhost', port))

        # Read the backtest metadata
        backtest_recv = recv_msg(s)
        backtest = json.loads(backtest_recv.decode())

        # Read AAPL quotes 
        aapl_quotes = []
        while True:
            quote_recv = recv_msg(s).decode()
            if quote_recv == 'go':
                break
            quote = json.loads(quote_recv)
            aapl_quotes.append(quote)

        quotesets = [{'AAPL': x} for x in aapl_quotes]

        # Run the backtest
        portfolio = Portfolio()
        quote_history = []

        results = []

        for quoteset in quotesets:
            quote_history.append(quoteset)
            actions = backtest_tick(quoteset, portfolio, quote_history)

            for action in actions:
                portfolio.action(action, quoteset)
        
            results.append({
                'time': str(quoteset['AAPL']['time']),
                'portfolio': {
                    'value': portfolio.value(quoteset),
                    'positions': portfolio.positions.copy(),
                    'cash': portfolio.cash
                }
            })

        payload = {
            'final_value': portfolio.value(quotesets[-1]),
            'roi': (portfolio.value(quotesets[-1]) - portfolio.value(quotesets[0])) / portfolio.value(quotesets[0]),
            'transactions': portfolio.transactions,
            'portfolio_over_time': results,
        }

        send_msg(s, json.dumps(payload).encode())


if __name__ == '__main__':
    main()
