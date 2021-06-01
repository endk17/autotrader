from main import strategy
from db import config
import sqlite3
from datetime import date, datetime, timedelta, tzinfo
from timezone import is_dst

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame


connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id FROM strategy WHERE name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    SELECT symbol, name
    FROM stock
    JOIN stock_strategy on stock_strategy.stock_id = stock.id
    WHERE stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]
print(symbols)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL, api_version='v2')

current_date = '2021-05-28'
if is_dst():
    # current_date = datetime.today().isoformat()
    start_minute_bar = f"{current_date}T09:30:00-05:00"
    end_minute_bar = f"{current_date}T09:45:00-05:00"
else:
    # current_date = datetime.today().isoformat()
    start_minute_bar = f"{current_date}T09:30:00-04:00"
    end_minute_bar = f"{current_date}T09:45:00-04:00"


orders = api.list_orders(status='all', limit=500, after=f"{current_date}T09:30:00-05:00)")
existing_order_symbols = [order.symbol for order in orders if orders.status != 'canceled']

# print(
#     start_minute_bar,
#     end_minute_bar,
# )

for symbol in symbols:

    # minute_bars = api.get_barset(symbol, 'minute', start=start_minute_bar, end=end_minute_bar).df
    # minute_bars = api.get_bars(symbol, TimeFrame.Minute, start_minute_bar, end_minute_bar).df
    minute_bars = api.get_bars(symbol, TimeFrame.Minute, current_date, current_date).df
    print(symbol)

    opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bars = minute_bars.loc[opening_range_mask]
    print(opening_range_bars)

    if not minute_bars.empty:
        opening_range_low = opening_range_bars['low'].min()
        opening_range_high = opening_range_bars['high'].max()
        opening_range = opening_range_high - opening_range_low
        # print(
        #     opening_range_low,
        #     opening_range_high,
        #     opening_range 
        # )

        after_opening_range_mask = minute_bars.index >= end_minute_bar
        after_opening_range_bars = minute_bars.loc[after_opening_range_mask]
        # print(
        #     after_opening_range_bars
        # )

        after_opening_range_breakdown = after_opening_range_bars[after_opening_range_bars['close'] > opening_range_low]

        if not after_opening_range_breakdown.empty:
            if symbol not in existing_order_symbols:
                limit_price = after_opening_range_breakdown.iloc[0]['close']
                
                message = f"selling short {symbol} at {limit_price}, closed_below {opening_range_low} at {after_opening_range_breakdown.iloc[0]['close']}"
                # messages.append(message)

                print(message)

                try:
                    # submit order
                    api.submit_order(
                        symbol='symbol',
                        side='sell',
                        type='limit',
                        qty='100',
                        time_in_force='day',
                        order_class='bracket',
                        take_profit=dict(
                            limit_price=limit_price - opening_range,
                        ),
                        stop_loss=dict(
                            stop_price=limit_price + opening_range,
                            limit_price=limit_price,
                        )
                    )
                except Exception as e:
                    print(f"could not submit order {e}")
            else:
                print(f"Sell order for {symbol} exists, skipping place order!!")