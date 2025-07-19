# Stock Trading Bot

A simple stock trading bot using IB API.

## Features

* Sell stocks using IB API
* Automatic trading based on predefined rules

## Installation
1. Download IB TWS/Gateway
https://www.interactivebrokers.com/en/trading/ibgateway-latest.php

2. Clone and setup project
```bash
git clone https://github.com/pig6485/IB-Trade-Job.git
cd IB-Trade-Job/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a new file named `.env` and add your MAILGUN credentials:
MAILGUN_API_KEY=xxx
MAILGUN_DOMAIN=xxx
MAILGUN_RECIPIENT=xxx

4. Run app
```bash
python -m bot.main
```