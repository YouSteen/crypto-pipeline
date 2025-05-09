import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate

# Parametrii
coin_id = 'bitcoin'
vs_currency = 'eur'
days = '365'  # ultimele 365 de zile

# Endpointul CoinGecko
url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
params = {
    'vs_currency': vs_currency,
    'days': days,
    'interval': 'daily'
}

# Cererea GET
response = requests.get(url, params=params)

# Verifică dacă răspunsul e valid
if response.status_code == 200:
data = response.json()
prices = data['prices']  # listă de [timestamp, price]

# Crează DataFrame și convertește timestamp-ul
df = pd.DataFrame(prices, columns=['time', 'price'])
df['time'] = pd.to_datetime(df['time'], unit='ms')

df['coin'] = coin_id

df = df[['coin', 'time', 'price']]

 # Datele salvate in txt pentru o vizualizare mai buna, dar nu pot fi manipulate de aici
 txt_table = tabulate(df, headers="keys",
                       tablefmt="pretty", showindex=False)
  txt_path = f"{coin_id}_pretty_table.txt"
   with open(txt_path, "w") as f:
        f.write(txt_table)

    # Afișează primele rânduri
    print(df.head())

    # Salvează în CSV
    filename = f"{coin_id}_historical_prices.csv"
    df.to_csv(filename, index=False)
    print(f"Datele au fost salvate în {filename}")
else:
    print("Eroare la cerere:", response.status_code)
    print(response.text)
