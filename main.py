import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate

# Lista de monede
coins = ['bitcoin', 'ethereum', 'solana']
vs_currency = 'eur'
days = '365'

# Listă pentru toate DataFrame-urile
all_data = []

for coin_id in coins:
    print(f"🔄 Prelucrez: {coin_id}...")

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days,
        'interval': 'daily'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data['prices']  # listă de [timestamp, price]

        df = pd.DataFrame(prices, columns=['time', f'price ({vs_currency})'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['coin'] = coin_id
        df = df[['coin', 'time', f'price ({vs_currency})']]
        df[f'price ({vs_currency})'] = df[f'price ({vs_currency})'].round(2)

        all_data.append(df)
    else:
        print(f"❌ Eroare la {coin_id}: {response.status_code}")

# Concatenează toate într-un singur DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Salvează ca tabel frumos în TXT
txt_table = tabulate(combined_df, headers="keys",
                     tablefmt="pretty", showindex=False)
with open("all_coins_pretty_table.txt", "w") as f:
    f.write(txt_table)

# Salvează ca CSV pentru analiză
combined_df.to_csv("all_coins_historical_prices.csv", index=False)

print("✅ Datele au fost salvate în all_coins_historical_prices.csv și all_coins_pretty_table.txt")
