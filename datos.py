import sqlite3

# Conecta con la base de datos que ya tienes (usa el mismo nombre que tu archivo .db)
conn = sqlite3.connect("arboles.db")
cursor = conn.cursor()

# Crear tabla de árboles si no existe
sql = ("""
CREATE TABLE IF NOT EXISTS arboles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie TEXT,
    dap REAL,
    altura REAL,
    parcela TEXT
);
""")
cursor.execute(sql)
conn.commit()
conn.close()

print("Tabla creada correctamente.")

conn = sqlite3.connect("arboles.db")
cursor = conn.cursor()

# Agregar las columnas
try:
    cursor.execute("ALTER TABLE arboles ADD COLUMN ubicacion TEXT;")
    cursor.execute("ALTER TABLE arboles ADD COLUMN largo_hoja REAL;")
    cursor.execute("ALTER TABLE arboles ADD COLUMN ancho_hoja REAL;")
    conn.commit()
    print("✅ Columnas agregadas correctamente.")
except Exception as e:
    print("⚠️ Error:", e)

conn.close()
