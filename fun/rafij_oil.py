import yfinance as yf

# Создайте объект Ticker для нефти (например, Brent Crude Oil)
oil_ticker = yf.Ticker("BZ=F")

# Получите информацию о цене на нефть
oil_price = oil_ticker.history(period="1d")["Close"].iloc[0]

print(f"Цена на нефть: ${oil_price:.2f}")
