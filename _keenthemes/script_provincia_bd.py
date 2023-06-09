import sqlite3

provincias = {
    'Pinar del Rio',
    'Mayabeque',
    'Artemisa',
    'La Habana',
    'Matanzas',
    'Villa Clara',
    'Camaguey',
    'Santi Spiritu',
    'Cienfuego',
    'Granma',
    'Ciego de Avila',
    'Holguin',
    'Isla de la Juventud',
    'Santiago de Cuba',
    'Guantanamo',

}

# Crear base de datos SQLite3
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS provincia (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

for p in provincias:
    c.execute("INSERT OR IGNORE INTO provincia (nombre) VALUES (?)", (p,))
    p_id = c.lastrowid


conn.commit()
conn.close()

print("Base de datos creada y populada exitosamente.")