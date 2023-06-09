import sqlite3
prop = [
  "Potencia",
  "Cilindraje",
  "Eficiencia",
  "Número de cilindros",
  "Combustible",
  "Configuración",
  "Tipo",
  "Número de velocidades",
  "Modo de tracción",
  "Diámetro del tubo",
  "Material",
  "Número de salidas",
  "Sistema de control de emisiones",
  "Tipo",
  "Amortiguadores",
  "Resortes",
  "Barra estabilizadora",
  "Tipo",
  "Tamaño del disco",
  "Material de las pastillas",
  "Sistema de asistencia",
  "Tipo",
  "Radio de giro",
  "Sensibilidad",
  "Ajustes",
  "Voltaje",
  "Capacidad de la batería",
  "Potencia del alternador",
  "Sistemas auxiliares",
  "Tipo de construcción",
  "Número de puertas",
  "Peso",
  "Aerodinámica",
  "Capacidad de carga",
  "Número de asientos",
  "Tapicería",
  "Espacio interior",
  "Sistema de infoentretenimiento",
  "Conectividad",
  "Seguridad",
  "Tamaño",
  "Índice de carga",
  "Índice de velocidad",
  "Tipo de neumático"
]

categorias_piezas = {
    'Piston': ['Material', 'Tamaño'],
    'Válvula': ['Tipo'],
    'Embrague': ['Tipo','Diámetro'],
    'Caja de cambios': ['Embrague','Tipo','Diametro'],
    'Tubo de escape': ['Diámetro','Material'],
    'Amortiguador': ['Tipo','Recorrido','Lado'],
    'Disco de freno': ['Diámetro'],
    'Tanque de combustible': ['Capacidad', 'Material'],
    'Filtro de combustible': ['Tipo', 'Eficiencia de filtración'],
    'Radiador': ['Capacidad', 'Material'],
    'Bateria': ['Capacidad', 'Voltaje'],
    'Alternador': ['Potencia', 'Voltaje'],
    'Capó': ['Material', 'Peso'],
}

# Lista de categorías de partes y sus propiedades
categorias_partes = {
    'Motor': ['Potencia', 'Cilindraje', 'Eficiencia','Numero de cilindros','Combustible'],
    'Transmisión': ['Tipo', 'Número de velocidades'],
    'Sistema de escape': ['Diámetro del tubo', 'Número de salidas'],
    'Suspensión': ['Tipo', 'Amortiguadores','Resortes'],
    'Sistema de frenos': ['Tipo', 'Material de las pastillas'],
    'Sistema de dirección': ['Tipo', 'Radio de giro', 'Sensibilidad'],
    'Sistema eléctrico': ['Voltaje', 'Capacidad de la batería', 'Potencia del alternador'],
    'Carrocería': ['Tipo de construcción', 'Número de puertas'],
    'Interior': ['Número de asientos', 'Tapicería', 'Seguridad'],
  }

categorias_equipos = {
    'Deportivos': ['Color', 'Puertas'],
    'Clasicos': ['Color'],
    '4x4': ['Ancho','Alto','Tipo'],
    'Omnibus': ['Embrague','Tipo','Diametro'],
    'Camiones': ['Diámetro','Material'],
    'Tractores': ['Tipo','Recorrido','Lado'],

}

# Crear base de datos SQLite3
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS propiedad (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_pieza (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_parte (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_equipo (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_pieza_propiedad (
        id INTEGER PRIMARY KEY,
        categoriapieza_id INTEGER,
        propiedad_id INTEGER,
        FOREIGN KEY (categoriapieza_id) REFERENCES categoria_pieza (id),
        FOREIGN KEY (propiedad_id) REFERENCES propiedad (id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_parte_propiedad (
        id INTEGER PRIMARY KEY,
        categoriaparte_id INTEGER,
        propiedad_id INTEGER,
        FOREIGN KEY (categoriaparte_id) REFERENCES categoria_parte (id),
        FOREIGN KEY (propiedad_id) REFERENCES propiedad (id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS categoria_equipo_propiedad (
        id INTEGER PRIMARY KEY,
        categoriaequipo_id INTEGER,
        propiedad_id INTEGER,
        FOREIGN KEY (categoriaequipo_id) REFERENCES categoria_equipo (id),
        FOREIGN KEY (propiedad_id) REFERENCES propiedad (id)
    )
''')

# Insertar propiedades en la base de datos
for categoria, propiedades in categorias_piezas.items():
    # Primero, inserte la categoría en la tabla 'categoria_pieza'
    c.execute("INSERT OR IGNORE INTO categoria_pieza (nombre) VALUES (?)", (categoria,))
    categoriapieza_id = c.lastrowid

    # Luego, inserte cada propiedad y su relación con la categoría en la tabla 'categoria_pieza_propiedad'
    for propiedad in propiedades:
        c.execute("INSERT OR IGNORE INTO propiedad (nombre) VALUES (?)", (propiedad,))
        propiedad_id = c.lastrowid

        # Compruebe si la relación entre la categoría y la propiedad ya existe en la tabla
        c.execute("SELECT id FROM categoria_pieza_propiedad WHERE categoriapieza_id = ? AND propiedad_id = ?", (categoriapieza_id, propiedad_id))
        resultado = c.fetchone()
        if resultado is None:
            # Si es una nueva relación, insértela en la tabla 'categoria_pieza_propiedad'
            c.execute("INSERT INTO categoria_pieza_propiedad (categoriapieza_id, propiedad_id) VALUES (?, ?)", (categoriapieza_id, propiedad_id))

for categoria, propiedades in categorias_partes.items():
    # Primero, inserte la categoría en la tabla 'categoria_pieza'
    c.execute("INSERT OR IGNORE INTO categoria_parte (nombre) VALUES (?)", (categoria,))
    categoriaparte_id = c.lastrowid

    # Luego, inserte cada propiedad y su relación con la categoría en la tabla 'categoria_pieza_propiedad'
    for propiedad in propiedades:
        c.execute("INSERT OR IGNORE INTO propiedad (nombre) VALUES (?)", (propiedad,))
        propiedad_id = c.lastrowid

        # Compruebe si la relación entre la categoría y la propiedad ya existe en la tabla
        c.execute("SELECT id FROM categoria_parte_propiedad WHERE categoriaparte_id = ? AND propiedad_id = ?", (categoriaparte_id, propiedad_id))
        resultado = c.fetchone()
        if resultado is None:
            # Si es una nueva relación, insértela en la tabla 'categoria_pieza_propiedad'
            c.execute("INSERT INTO categoria_parte_propiedad (categoriaparte_id, propiedad_id) VALUES (?, ?)", (categoriaparte_id, propiedad_id))

for categoria, propiedades in categorias_equipos.items():
    # Primero, inserte la categoría en la tabla 'categoria_pieza'
    c.execute("INSERT OR IGNORE INTO categoria_equipo (nombre) VALUES (?)", (categoria,))
    categoriaequipo_id = c.lastrowid

    # Luego, inserte cada propiedad y su relación con la categoría en la tabla 'categoria_equipo_propiedad'
    for propiedad in propiedades:
        c.execute("INSERT OR IGNORE INTO propiedad (nombre) VALUES (?)", (propiedad,))
        propiedad_id = c.lastrowid

        # Compruebe si la relación entre la categoría y la propiedad ya existe en la tabla
        c.execute("SELECT id FROM categoria_equipo_propiedad WHERE categoriaequipo_id = ? AND propiedad_id = ?", (categoriaequipo_id, propiedad_id))
        resultado = c.fetchone()
        if resultado is None:
            # Si es una nueva relación, insértela en la tabla 'categoria_equipo_propiedad'
            c.execute("INSERT INTO categoria_equipo_propiedad (categoriaequipo_id, propiedad_id) VALUES (?, ?)", (categoriaequipo_id, propiedad_id))

conn.commit()
conn.close()

print("Base de datos creada y populada exitosamente.")