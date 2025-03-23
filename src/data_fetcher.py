import requests
import sqlite3
from datetime import datetime

DB_PATH = 'data/data.db'


def fetch_cryto_data(coin_id, days='7'):
    """
    Esto es un Fetch usando la API de CoinGecko con precios historicos de los ultimos dias.
    """

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    parametros = {

        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }

    response = requests.get(url, params=parametros)
    if response.status_code == 200:
        data = response.json()
        return data['prices']
    else:
        print("Error en la peticion de datos.", response.status_code)
        return []


def insertar_precios_en_db(coin_name, prices):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for price_point in prices:
        timestamp, price = price_point
        date = datetime.utcfromtimestamp(
            timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''

                INSERT INTO crypto_precios(moneda, precio_dolar, fecha)
                VALUES(?,?,?)

                ''', (coin_name, price, date))

    conn.commit()
    conn.close()

    print(
        f"Datos de {coin_name} insertados correctamente en la base de datos.")


if __name__ == "__main__":

    coin_id = 'solana'
    prices = fetch_cryto_data(coin_id, days='30')
    if prices:
        insertar_precios_en_db(coin_id, prices)
