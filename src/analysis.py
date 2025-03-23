import sqlite3
import pandas as pd

DB_PATH = 'data/data.db'


def load_data(coin, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT moneda, precio_dolar, fecha
        FROM crypto_precios
        WHERE moneda = ?
    """

    params = [coin]

    if start_date:
        query += " AND DATE(fecha) >= ?"
        params.append(start_date)

    if end_date:
        query += " AND DATE(fecha) <= ?"
        params.append(end_date)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_stats(df):
    if df.empty:
        return None

    stats = {
        'Precio Máximo': df['precio_dolar'].max(),
        'Precio Mínimo': df['precio_dolar'].min(),
        'Precio Promedio': df['precio_dolar'].mean()
    }
    return stats


if __name__ == "__main__":
    coin = 'solana'
    data = load_data(coin)

    print("\nFechas disponibles:",
          data['fecha'].min(), "->", data['fecha'].max())
    print(data.head())

    stats = get_stats(data)

    if stats:
        print("\n📊 Estadísticas de", coin)
        for k, v in stats.items():
            print(f"{k}: ${v:.2f}")
    else:
        print("No hay datos disponibles para ese filtro.")
