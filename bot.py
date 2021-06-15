import ccxt
import config
import pandas as pd
pd.set_option('display.max_rows', None)

import schedule
import ta
from ta.volatility import BollingerBands, AverageTrueRange

exchange = ccxt.binance({
    'apikey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY
})

#markets = exchange.load_markets()
bars = exchange.fetch_ohlcv('BNB/USDT',timeframe='15m', limit=300)

df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

def tr(df):
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc']= abs(df['high'] - df['previous_close'])
    df['low-pc']= abs(df['low'] - df['previous_close'])

    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr 


def atr(df, period=14):
    df['tr'] =tr(df)
    the_atr = df['tr'].rolling(period).mean()

    print("calculate average true range")

    
    return the_atr

#df['atr'] = the_atr
#print(df)


def supertrend(df, period=7, multiplier=3):
    hl2 = (df['high'] + df['low']) /2 
    #print("calculating supertrend")
    #basic upperband = ((high + low) / 2) + (multiplier * atr)
    #basic lowerband = ((high + low) / 2) - (multiplier * atr)
    df['atr'] = atr(df, period=period)
    df['basic_upperband'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    df['basic_lowerband'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current-1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['upperband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_previous'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperrband'][current] > df['upperband'][previous]:
                df['lowerband'][current] = df['upperband'][previous]


        #print(current)

    #return df

    
#print(supertrend(df))

#atr(df, period=5)

#print(df)







#print(df)

#for bar in bars:
#    print(bar)

#bb_indicator = BollingerBands(df['close'])

#df['upper_band'] = bb_indicator.bollinger_hband()
#df['lower_band'] = bb_indicator.bollinger_lband()
#df['moving_average'] = bb_indicator.bollinger_mavg()

#print(df)

#atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])

#df['atr'] = atr_indicator.average_true_range()

#print(df)










#balances = exchange.fetch_balance()
#print(balances['total']['USDT'])

#order = exchange.create_market_buy_order('ADA/USDT', 0.01)
#print(order)


# print(ccxt.exchanges) 
# for exchange in ccxt.exchanges:
#     print(exchange) 

#markets = exchange.load_markets()

#exchange = ccxt.binance()
#print(exchange)
#markets = exchange.load_markets()

#ohlc = exchange.fetch_ohlcv('ETH/USDT')

#for candle in ohlc:
#    print(candle)

#for market in markets:
#   print(market)


