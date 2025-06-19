import sqlite3
import pandas as pd
import openpyxl

# Parámetros para la fórmula de tamaño de muestra
Z = 1.96  # 95% de confianza
p = 0.5   # proporción esperada
e = 0.05  # margen de error

# Función para calcular el tamaño de la muestra
def calcular_tamaño_muestra(N, Z=1.96, p=0.5, e=0.05):
    numerador = N * (Z ** 2) * p * (1 - p)
    denominador = ((e ** 2) * (N - 1)) + ((Z ** 2) * p * (1 - p))
    n = numerador / denominador
    n_redondeado = int(round(n))
    print(f"Se debe muestrear {n_redondeado} árboles para tener una muestra representativa.")
    return n_redondeado

# Conectar con la base de datos SQLite
conn = sqlite3.connect("arboles.db")

# Leer todos los registros de la tabla 'arboles' como un DataFrame
df = pd.read_sql_query("SELECT * FROM arboles", conn)

# Obtener el tamaño total de la población (N)
N = len(df)

# Calcular el tamaño de la muestra
n_muestra = calcular_tamaño_muestra(N)

# Seleccionar aleatoriamente los árboles
muestra = df.sample(n=n_muestra, random_state=42)

# (Opcional) Guardar la muestra seleccionada en un nuevo archivo Excel
muestra.to_excel("muestra_seleccionada.xlsx", index=False)

# Cerrar la conexión a la base de datos
conn.close()