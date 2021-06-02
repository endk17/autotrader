import config
import sqlite3

connection = sqlite3.connect(config.DB_FILE)
    
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
""")

cursor.execute("""
    DROP TABLE stock
""")

cursor.execute("""
    DROP TABLE strategy
""")

cursor.execute("""
    DROP TABLE stock_strategy
""")

cursor.execute("""
    DROP TABLE stock_price_minute
""")

connection.commit()