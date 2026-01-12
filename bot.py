from binance import Client
from binance.exceptions import BinanceAPIException
from logger import setup_logger
from config import API_KEY, API_SECRET

logger = setup_logger()

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"

        logger.info("Connected to Binance Futures Testnet")

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            logger.info(f"Market order response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Market order error: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )
            logger.info(f"Limit order response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Limit order error: {e}")
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce="GTC"
            )
            logger.info(f"Stop-Limit order response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Stop-Limit order error: {e}")
            return None


if __name__ == "__main__":
    bot = BasicBot(API_KEY, API_SECRET)

    print("\n===== BINANCE FUTURES TESTNET TRADING BOT =====")

    symbol = input("Enter Symbol (example BTCUSDT): ").upper()
    side = input("Enter Side (BUY / SELL): ").upper()
    order_type = input("Order Type (MARKET / LIMIT / STOP): ").upper()
    quantity = float(input("Enter Quantity: "))

    if order_type == "MARKET":
        result = bot.place_market_order(symbol, side, quantity)

    elif order_type == "LIMIT":
        price = input("Enter Limit Price: ")
        result = bot.place_limit_order(symbol, side, quantity, price)

    elif order_type == "STOP":
        stop_price = input("Enter Stop Price: ")
        limit_price = input("Enter Limit Price: ")
        result = bot.place_stop_limit_order(
            symbol, side, quantity, stop_price, limit_price
        )

    else:
        print("Invalid order type")
        result = None

    if result:
        print("\nOrder placed successfully")
        print("Order ID:", result["orderId"])
        print("Status:", result["status"])
    else:
        print("\nOrder failed. Check logs.")
