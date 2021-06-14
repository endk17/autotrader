# AutoTrader

This is a [python](https://flask.palletsprojects.com/en/2.0.x/) based web application which interacts with [Alpaca Markets Terading API](https://alpaca.markets/)


## Packages / Requirements

The primary components of this application are:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Unicorn](https://www.uvicorn.org/)
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)

For a more detailed list please see the [requirements text file](./requirements.txt)


## Strategy(s)

1. Opening Range Breakout (15 Minute Candle)

2. Opening Range Breakdown (15 Minute Candle)

__The definition used to explain these strategies was taking from [Warrior Trading](https://www.warriortrading.com/opening-range-breakout/) as this definition was then used  as a premise to devise the codified solution__