import pandas as pd
import sqlite3

# Ruta del archivo Excel
archivo_excel = "bd igual tabla.xlsx"

# Leer hoja (puedes especificar el nombre con sheet_name="Hoja1")
df = pd.read_excel(archivo_excel)

# Conectar a base de datos SQLite (crea el archivo si no existe)
conn = sqlite3.connect("arboles.db")

# Escribir el DataFrame en una tabla (crea o reemplaza la tabla)
df.to_sql("arboles", conn, if_exists="replace", index=False)

# Confirmar y cerrar
conn.commit()
conn.close()

print("✅ Datos importados correctamente")
