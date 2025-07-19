import math
import traceback
from ib_insync import IB, Contract, Order, Stock
from . import config

class IBClient:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        print(f"Connecting to IB at {config.IB_HOST}:{config.IB_PORT}...")
        self.ib.connect(config.IB_HOST, config.IB_PORT, clientId=config.IB_CLIENT_ID)
        # IMPROTANT: This mean that we use delayed market data
        self.ib.reqMarketDataType(3)
        print("✅ Connected to IB Gateway")
        self.ib.reqAccountSummary()
        self.ib.sleep(1)

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()
            print("Disconnected from IB TWS/Gateway.")

    def print_account_summary(self):
        """
        Print a summary of current account holdings, including market value and PnL.
        """
        summary_output = "\n📊 Account Summary:\n"
        portfolio_items = self.ib.portfolio()

        if not portfolio_items:
            summary_output += "No positions found in portfolio.\n"
            return summary_output

        for item in portfolio_items:
            if item.contract and item.contract.symbol:
                symbol = item.contract.symbol
                market_value = item.marketValue
                position = item.position
                unrealized_pnl = item.unrealizedPNL

                pnl_percentage = 0.0
                if market_value:
                    pnl_percentage = round((unrealized_pnl / market_value) * 100, 2)

                summary_output += (f"- {symbol} (Shares: {position}): "
                                   f"Market Value: ${market_value:,.2f}, "
                                   f"PnL: {pnl_percentage:.2f}%\n")
            else:
                summary_output += "Found a position without a symbol.\n"

        return summary_output


    def get_cash_balance(self):
        summary = self.ib.accountSummary()
        for item in summary:
            if item.tag == "AvailableFunds":
                return float(item.value)
        return 0.0

    def sell_stock(self, symbol, amount, account_cash):
        """
        Sell a specified amount of stock.

        :param symbol: Stock symbol (e.g. SGOV)
        :param amount: Amount to sell (e.g. 5000)
        """
        try:
            if amount <= 0:
                raise ValueError("Amount must be a positive number")
            
            if account_cash - amount < 0:
                # Get current market value and number of shares
                current_price_per_share, num_shares, total_market_value = self.get_stock_info(symbol)

                print(f"You have {total_market_value} in market value and {num_shares} shares of {symbol}")

                # Calculate number of shares to sell
                still_need = amount - account_cash
                shares_to_sell = self.calculate_shares_to_sell(still_need, current_price_per_share)

                # Check if we have enough shares to sell
                self.check_stock_balance(num_shares, shares_to_sell)

                # Create a sell order
                order, contract = self.create_sell_order(symbol, shares_to_sell)

                # Place the order
                self.place_order(order, contract)

                # Log the transaction
                print(f"SOLD {shares_to_sell} shares of {symbol}")

                sell_amount = current_price_per_share * shares_to_sell

                return True, ""
            else:
                print("There is no need to sell stock")
                return False, "You still have enough cash to buy stock, there is no need to sell stock", 0

        except Exception as e:
            # Send an email notification with the error message
            print(f"Error selling {symbol}: {str(e)}\n{traceback.format_exc()}")

            return False, str(e), sell_amount


    def calculate_shares_to_sell(self, amount_to_sell: float, current_share_price: float) -> int:
        """
        Calculate the number of shares to sell based on the sell amount and market value.

        :param amount_to_sell: Amount to sell (e.g. 5000)
        :param current_share_price: Current market value
        :return: Number of shares to sell
        """
        if amount_to_sell <= 0 or current_share_price <= 0:
            raise ValueError("Sell amount and market value must be positive numbers")

        theoretical_shares = amount_to_sell / current_share_price
        shares_to_sell = math.ceil(theoretical_shares)
        return max(shares_to_sell, 0)

    def check_stock_balance(self, num_shares, shares_to_sell):
        """
        Check if we have enough shares to sell.

        :param num_shares: Current number of shares
        :param shares_to_sell: Number of shares to sell
        :raise: ValueError if we don't have enough shares
        """
        if shares_to_sell > num_shares:
            raise ValueError(f"Insufficient stock balance: {num_shares} < {shares_to_sell}")

    def create_sell_order(self, symbol: str, shares_to_sell: int) -> tuple:
        """
        Create a sell order for a specified symbol and number of shares.

        :param symbol: Stock symbol (e.g. SGOV)
        :param shares_to_sell: Number of shares to sell
        :return: Sell order and contract
        """
        contract = Contract(symbol=symbol, exchange="SMART", currency="USD", secType="STK", primaryExchange='ARCA')
        order = Order()
        order.action = "SELL"
        order.totalQuantity = shares_to_sell
        order.orderType = "MKT"
        order.tif = "DAY" 
        return order, contract

    def place_order(self, order: Order, contract: Contract) -> None:
        """
        Place a sell order for the specified contract and order.

        :param order: Sell order
        :param contract: Contract to sell
        """
        # Ensure the contract is fully populated
        self.ib.qualifyContracts(contract)

        # Place the order
        trade = self.ib.placeOrder(contract, order)

        # Wait for the order status to update
        self.ib.sleep(2)

        # Check the order status
        if trade.orderStatus.status == "Filled":
            print(f"Order filled at {trade.orderStatus.avgFillPrice:.2f}")
        elif trade.orderStatus.status in ["PreSubmitted", "Submitted"]:
            print("Order submitted but not yet filled.")
        else:
            print(f"Order failed or rejected: {trade.orderStatus.status}, {trade.orderStatus.whyHeld}")
    
    def get_market_price(self, symbol: str) -> float:
        """
        Get the latest price for the specified stock symbol.
        """
        contract = Contract(symbol=symbol, secType="STK", exchange="SMART", primaryExchange="ARCA", currency="USD")
        self.ib.qualifyContracts(contract)

        self.ib.reqMktData(contract)
        self.ib.sleep(5)
        ticker = self.ib.ticker(contract)

        if ticker.last:
            return ticker.last
        elif ticker.close:
            return ticker.close
        elif ticker.bid and ticker.ask:
            return (ticker.bid + ticker.ask) / 2
        else:
            return float('nan')  # Return NaN if unable to get the price
        
    def get_stock_info(self, symbol: str) -> tuple:
        """
        Get current per-share market price and total number of shares for a specified symbol.

        :param symbol: Stock symbol (e.g. SGOV)
        :return: (current_price_per_share, num_shares, total_market_value)
        """
        share_count = 0
        market_value_total = 0.0

        # Retrieve share count and total market value from ib.portfolio
        portfolio_items = self.ib.portfolio()
        for item in portfolio_items:
            if item.contract.symbol == symbol:
                share_count = item.position
                market_value_total = item.marketValue
                break  # Exit loop once found

        # Retrieve price per share
        price_per_share = self.get_market_price(symbol)
        
        # Handle NaN values
        if math.isnan(price_per_share):
            price_per_share = 0.0  # Or another reasonable default value

        print(f"DEBUG: {symbol} - Price per Share: {price_per_share}, Share Count: {share_count}, Total Market Value: {market_value_total}")
        return price_per_share, share_count, market_value_total
