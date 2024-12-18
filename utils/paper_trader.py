from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest

class PaperTrader:
    def __init__(self, trading_client):
        self.trading_client = trading_client

    def place_market_order(self, symbol, qty, side):
        if not symbol or qty <= 0 or side.lower() not in ["buy", "sell"]:
            raise ValueError("Invalid parameters for market order.")
        
        side_enum = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side_enum,
            time_in_force=TimeInForce.DAY,
            type=OrderType.MARKET
        )

        try:
            order = self.trading_client.submit_order(order_data)
        except Exception as e:
            raise RuntimeError(f"Error placing market order: {e}")

        return order
