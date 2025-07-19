from . import config
from .notification_service import send_email
from .ib_client import IBClient
from .scheduler import should_run_today

def main():
    if not should_run_today():
        print("⏰ Not time to run trading logic today.")
        return

    client = IBClient()
    client.connect()

    try:
        # before manipulate
        before_cash = client.get_cash_balance()
        print(f"\n💵 Cash available was: {before_cash:.2f} USD")

        # sell stock
        ok, message, sell_amount = client.sell_stock("SGOV", config.NEED_AMOUMT, before_cash)

        # after manipulate
        after_cash = before_cash - sell_amount
        print(f"\n💵 Cash available is: {after_cash:.2f} USD")
        account_summary = client.print_account_summary()
        print(account_summary)

        # send mail
        subject = "IB Cron Bot Trading Report"
        sellResultText = "Sell stock successfully"
        if not ok:
            sellResultText = "Sell stock failed: " + message
        text_content = sellResultText + f"\nBefore cash: {before_cash:.2f} USD\nAfter cash: {after_cash:.2f} USD\nAccount Summary:\n{account_summary}"
        send_email(subject, text_content)

    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
