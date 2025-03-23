import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from analysis import load_data, get_stats

DB_PATH = 'data/data.db'

# 🔥 Diccionario de traducciones
translations = {
    'es': {
        'title': "📈 Crypto Dashboard - Tomas Vales",
        'select_currency': "Selecciona la moneda:",
        'start_date': "Fecha de inicio:",
        'end_date': "Fecha de fin:",
        'view_in': "¿En qué moneda querés ver los precios?",
        'load_data': "Cargar datos",
        'kpi_title': "📌 KPIs del período seleccionado",
        'stats_title': "📊 Estadísticas Detalladas",
        'prices_in': "💰 Precios en",
        'download_csv': "📥 Descargar CSV",
        'graph_title': "📈 Evolución del precio en",
        'warning': "No hay datos disponibles para ese filtro."
    },
    'en': {
        'title': "📈 Crypto Dashboard - Tomas Vales",
        'select_currency': "Select currency:",
        'start_date': "Start Date:",
        'end_date': "End Date:",
        'view_in': "In which currency do you want to see the prices?",
        'load_data': "Load Data",
        'kpi_title': "📌 KPIs of the selected period",
        'stats_title': "📊 Detailed Statistics",
        'prices_in': "💰 Prices in",
        'download_csv': "📥 Download CSV",
        'graph_title': "📈 Price Evolution in",
        'warning': "No data available for this filter."
    }
}

# 🌐 Selector de idioma
lang = st.selectbox("🌐 Language / Idioma", ["Español", "English"])
lang_key = 'es' if lang == "Español" else 'en'
t = translations[lang_key]

# Título
st.title(t['title'])

# Conectamos a la base
conn = sqlite3.connect(DB_PATH)
monedas = pd.read_sql_query("SELECT DISTINCT moneda FROM crypto_precios", conn)
conn.close()

# Selector de moneda
moneda = st.selectbox(t['select_currency'], monedas['moneda'].tolist())

# Fechas
fecha_inicio = st.date_input(t['start_date'], pd.to_datetime("2025-03-01"))
fecha_fin = st.date_input(t['end_date'], pd.to_datetime("2025-03-31"))

# Moneda de visualización
unidad = st.selectbox(t['view_in'], ("USD", "ARS", "EUR"))

# Tasas de cambio manuales
dolar_a_pesos = 1000   # 1 USD = 1000 ARS (ajustable)
dolar_a_euros = 0.92   # 1 USD = 0.92 EUR (ajustable)

# Botón cargar datos
if st.button(t['load_data']):
    df = load_data(moneda, start_date=str(
        fecha_inicio), end_date=str(fecha_fin))

    if not df.empty:
        st.success(f"Datos cargados para **{moneda}**")
        df['fecha'] = pd.to_datetime(df['fecha'])

        st.write(
            f"Fechas disponibles: {df['fecha'].min().date()} -> {df['fecha'].max().date()}")

        # KPIs
        st.subheader(t['kpi_title'])
        precio_actual = df['precio_dolar'].iloc[-1]
        precio_dia_anterior = df['precio_dolar'].iloc[-2] if len(
            df) > 1 else precio_actual
        variacion_diaria = ((precio_actual - precio_dia_anterior) /
                            precio_dia_anterior) * 100 if precio_dia_anterior else 0
        precio_max = df['precio_dolar'].max()

        col1, col2, col3 = st.columns(3)
        col1.metric("💲 Precio Actual (USD)", f"${precio_actual:.2f}")
        col2.metric("📈 Variación Diaria (%)",
                    f"{variacion_diaria:.2f}%", delta=f"{variacion_diaria:.2f}%")
        col3.metric("🚀 Máximo del período", f"${precio_max:.2f}")

        # Estadísticas
        st.subheader(t['stats_title'])
        precio_min = df['precio_dolar'].min()
        precio_prom = df['precio_dolar'].mean()
        desviacion = df['precio_dolar'].std()
        cantidad_dias = len(df)

        st.write(f"**Precio Promedio:** ${precio_prom:.2f} USD")
        st.write(f"**Precio Mínimo:** ${precio_min:.2f} USD")
        st.write(f"**Desviación Estándar:** {desviacion:.2f}")
        st.write(f"**Cantidad de días analizados:** {cantidad_dias} días")

        # ✅ Conversión con tasas fijas
        if unidad == "USD":
            df['precio_final'] = df['precio_dolar']
        elif unidad == "ARS":
            df['precio_final'] = df['precio_dolar'] * dolar_a_pesos
        elif unidad == "EUR":
            df['precio_final'] = df['precio_dolar'] * dolar_a_euros

        # Tabla de precios
        st.subheader(f"{t['prices_in']} {unidad}")
        st.dataframe(df[['fecha', 'precio_final']].rename(
            columns={'precio_final': f'Precio ({unidad})'}))

        # Descargar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=t['download_csv'],
            data=csv,
            file_name=f'{moneda}_{unidad}.csv',
            mime='text/csv',
        )

        # Gráfico
        st.subheader(f"{t['graph_title']} {unidad}")
        fig, ax = plt.subplots()
        ax.plot(df['fecha'], df['precio_final'], marker='o')
        ax.set_xlabel("Fecha")
        ax.set_ylabel(f"Precio en {unidad}")
        ax.set_title(f"Precio de {moneda} en {unidad}")
        st.pyplot(fig)
    else:
        st.warning(t['warning'])
