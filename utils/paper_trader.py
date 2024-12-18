from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest

class PaperTrader:
    def __init__(self, trading_client):
        self.trading_client = trading_client

    def place_market_order(self, symbol, qty, side):
        side_enum = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side_enum,
            time_in_force=TimeInForce.DAY,
            type=OrderType.MARKET
        )
        order = self.trading_client.submit_order(order_data)
        return order
