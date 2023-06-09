import sqlite3

marcas_modelos = {
    'Ford': ['Focus', 'Mustang', 'Fusion', 'Explorer', 'Fiesta'],
    'Toyota': ['Camry', 'Corolla', 'Prius', 'RAV4', 'Highlander'],
    'Chevrolet': ['Camaro', 'Malibu', 'Silverado', 'Equinox', 'Traverse'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
    'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class'],
    'Volkswagen': ['Jetta', 'Golf', 'Passat', 'Tiguan', 'Atlas'],
    'Audi': ['A4', 'A6', 'Q5', 'Q7', 'TT'],
    'Nissan': ['Altima', 'Maxima', 'Rogue', 'Pathfinder', 'Murano'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
    'Kia': ['Optima', 'Forte', 'Sportage', 'Sorento', 'Soul'],
    'Jeep': ['Wrangler', 'Grand Cherokee', 'Cherokee', 'Compass', 'Renegade'],
    'Volvo': ['S60', 'XC60', 'XC90', 'V60', 'V90'],
    'Subaru': ['Impreza', 'Legacy', 'Outback', 'Forester', 'Crosstrek'],
    'Mazda': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'MX-5 Miata'],
    'Fiat': ['500', '500X', '500L', '124 Spider', 'Tipo'],
    'Land Rover': ['Range Rover', 'Range Rover Sport', 'Discovery', 'Defender', 'Evoque'],
    'Jaguar': ['XE', 'XF', 'F-PACE', 'E-PACE', 'I-PACE'],
    'Porsche': ['911', 'Cayenne', 'Macan', 'Panamera', 'Boxster'],
    'Tesla': ['Model S', 'Model 3', 'Model X', 'Model Y', 'Cybertruck'],
}

# Crear base de datos SQLite3
conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

# Crear tablas en la base de datos
c.execute('''
    CREATE TABLE IF NOT EXISTS marca (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS modelo (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS marca_modelo (
        id INTEGER PRIMARY KEY,
        marca_id INTEGER,
        modelo_id INTEGER,
        equipo BOOLEAN,
        parte BOOLEAN,
        pieza BOOLEAN,
        insumo BOOLEAN,
        FOREIGN KEY (marca_id) REFERENCES marca (id),
        FOREIGN KEY (modelo_id) REFERENCES modelo (id)
    )
''')

# Insertar marcas y modelos en la base de datos
for marca, modelos in marcas_modelos.items():
    # Insertar marca
    c.execute("INSERT OR IGNORE INTO marca (nombre) VALUES (?)", (marca,))
    marca_id = c.lastrowid

    for modelo in modelos:
        # Insertar modelo
        c.execute("INSERT OR IGNORE INTO modelo (nombre) VALUES (?)", (modelo,))
        modelo_id = c.lastrowid

        # Insertar relación marca-modelo
        c.execute("INSERT INTO marca_modelo (marca_id, modelo_id, equipo, parte, pieza, insumo) VALUES (?, ?, 0, 0, 0, 0)",
                  (marca_id, modelo_id))

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y populada exitosamente.")