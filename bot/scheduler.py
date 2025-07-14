from datetime import date

def should_run_today():
    """Determine if the trading logic should run today."""
    # Example: Execute on the first trading day of the month
    current_day = date.today().day
    return current_day == 14