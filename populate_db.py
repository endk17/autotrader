import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')
cursor = connection.cursor()

api = tradeapi.REST('PKFOVYBEBA53NX5FC6SO', 'KIrS9PuvzzzWIGigVKFRQ3TVkaTV9xIQTU7kh9Gm', base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
assets = api.list_assets()

for asset in assets:

    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)


connection.commit()