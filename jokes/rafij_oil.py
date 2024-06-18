import yfinance as yf

oil_ticker = yf.Ticker("BZ=F")
oil_price = oil_ticker.history(period="1d")["Close"].iloc[0]

print(f"Цена на нефть: ${oil_price:.2f}")



# # # spoilers 🤭
