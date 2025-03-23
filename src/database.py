import sqlite3


def crear_db():
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()

    cursor.execute('''
    
                CREATE TABLE IF NOT EXISTS crypto_precios(
                   
                   id integer primary key autoincrement,
                   moneda TEXT NOT NULL,
                   precio_dolar REAL NOT NULL,
                   fecha TEXT NOT NULL
                   
        
                   )
                   
                   
                   
                   ''')\

    conn.commit()
    conn.close()


if __name__ == '__main__':
    crear_db()
    print('La base de datos fue creada correctamente')
    print("Desarollado por -Tomas Vales.")
