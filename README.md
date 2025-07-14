# IB Cronjob Trading Bot 🐍📈

使用 Interactive Brokers + Python + ib_insync 建立的自動化定期交易機器人。

## 🔧 功能
- 連線到 IB Gateway (支援 Paper Trading)
- 查詢帳戶現金餘額與部位
- 預留模組化交易邏輯（定期賣出 / 買入）

## 📦 安裝步驟

```bash
git clone https://github.com/yourname/ib-cron-bot.git
cd ib-cron-bot/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt