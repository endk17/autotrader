from db import config
import tulipy
from helpers import calc_qty
from timezone import is_dst
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

# symbols = ['AMC', 'SPY', 'DIA']

# for symbols in symbols:
#     api.submit_order()

#     quote = api.get_last_quote(symbol)

#     api.submit_order(
#         symbol=symbol,
#         side='buy',
#         type='market',
#         qty=calc_qty(quote.bidprice),
#         time_in_force='day',
#         order_class='bracket',
#         take_profit=dict(
#             limit_price=limit_price + opening_range,
#         ),
#         stop_loss=dict(
#             stop_price=limit_price - opening_range,
#             limit_price=limit_price,
#         )
#     )

# orders = api.list_orders()
# positions = api.list_positions()

# api.submit_order(
#     symbol='AMC',
#     side='sell',
#     qty=200,
#     time_in_force='day',
#     type='trailing_stop',
#     trail_price='0.2'
# )

# api.submit_order(
#     symbol='AMC',
#     side='sell',
#     qty=200,
#     time_in_force='day',
#     type='trailing_stop',
#     trail_percent='2'
# )

# Use Average True Range for Stop loss based on daily price action
daily_bars = api.get_bars('TSLA', TimeFrame.Day, '2021-05-01', '2021-06-01').df
print(daily_bars)

atr = tulipy.atr(daily_bars.high.values, daily_bars.low.values, daily_bars.close.values, 14)
print(atr)