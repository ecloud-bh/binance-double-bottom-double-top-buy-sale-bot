import time
from binance.client import Client
from binance.exceptions import BinanceAPIException

# eCloud Tech. Muhammet P.

# API anahtarlarınızı buraya girin
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# Binance istemcisini başlatın
client = Client(api_key, api_secret)

# İşlem yapmak istediğiniz sembol ve zaman aralığını seçin
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_15MINUTE

# İkili dip ve ikili tepe formasyonları için minimum derinlik ve eşik değerlerini belirleyin
min_depth = 0.01
threshold = 0.1

# İkili dip formasyonunu kontrol eden işlev
def is_double_bottom(prices, min_depth, threshold):
    price_diff = prices[-1] - min(prices[:-1])
    depth = price_diff / min(prices[:-1])
    if depth > min_depth and depth < threshold:
        return True
    return False

# İkili tepe formasyonunu kontrol eden işlev
def is_double_top(prices, min_depth, threshold):
    price_diff = max(prices[:-1]) - prices[-1]
    depth = price_diff / max(prices[:-1])
    if depth > min_depth and depth < threshold:
        return True
    return False

# Botun ana döngüsü
while True:
    try:
        # Fiyat verilerini alın
        candles = client.get_klines(symbol=symbol, interval=interval, limit=10)
        prices = [float(candle[4]) for candle in candles]

        # İkili dip formasyonu varsa alım yap
        if is_double_bottom(prices, min_depth, threshold):
            print("Buying")
            # Alım emrini burada gerçekleştirin
            with open("transactions.txt", "a") as f:
                f.write(f"BUY {symbol} at {prices[-1]} - Double Bottom\n")
        # İkili tepe formasyonu varsa satış yap
        elif is_double_top(prices, min_depth, threshold):
            print("Selling")
            # Satış emrini burada gerçekleştirin
            with open("transactions.txt", "a") as f:
                f.write(f"SELL {symbol} at {prices[-1]} - Double Top\n")

        # 60 saniye bekleyin ve ardından döngüyü tekrarlayın
        time.sleep(60)

    except BinanceAPIException as e:
        print(f"Binance API error: {e}")
        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
