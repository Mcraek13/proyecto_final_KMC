import streamlit as st
import sqlite3
import pandas as pd

# --- Conexión a base de datos ---
conn = sqlite3.connect("arboles.db", check_same_thread=False)
cursor = conn.cursor()

# --- Crear tabla si no existe ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS arboles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie TEXT,
    dap REAL,
    altura REAL,
    parcela TEXT,
    ubicacion TEXT,
    largo_hoja REAL,
    ancho_hoja REAL
)
""")


# --- Encabezado de la app ---
st.set_page_config(page_title="App de Árboles", layout="centered")
st.title("🌳 Registro de Árboles de Campo")
st.markdown("Aplicación de registro forestal en campo. Ingrese los datos por árbol.")

# --- Formulario ---
with st.form("formulario_arbol"):
    id = st.text_input("🌲 id")
    especie = st.text_input("🌲 Especie")
    dap = st.number_input("📏 DAP (cm)", min_value=0.0, step=0.1)
    altura = st.number_input("📐 Altura (m)", min_value=0.0, step=0.1)
    parcela = st.text_input("🗺️ Parcela")
    ubicacion = st.text_input("📍 Ubicación")
    largo_hoja = st.number_input("🍃 Largo de hoja (cm)", min_value=0.0, step=0.1)
    ancho_hoja = st.number_input("🍃 Ancho de hoja (cm)", min_value=0.0, step=0.1)

    enviado = st.form_submit_button("✅ Guardar árbol")

    if enviado:
        cursor.execute("""
            INSERT INTO arboles (
                id, especie, dap, altura, parcela,
                ubicacion, largo_hoja, ancho_hoja
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, especie, dap, altura, parcela,
              ubicacion, largo_hoja, ancho_hoja))
        conn.commit()
        st.success("🌱 Árbol guardado correctamente.")

# --- Mostrar número de árboles guardados ---
cursor.execute("SELECT COUNT(*) FROM arboles")
total = cursor.fetchone()[0]
st.info(f"🌲 Total de árboles registrados: **{total}**")

# --- Exportar a Excel ---
st.markdown("### 📤 Exportar a Excel")

if st.button("📁 Descargar archivo Excel"):
    df = pd.read_sql_query("SELECT * FROM arboles", conn)
    df.to_excel("registro_arboles.xlsx", index=False)
    with open("registro_arboles.xlsx", "rb") as f:
        st.download_button(
            label="⬇️ Descargar Excel",
            data=f,
            file_name="registro_arboles.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- Personalización visual opcional ---
st.markdown("""
---
🧑‍🔬 **Desarrollado por [K. Mc Rae Calvo]**  
📍 Proyecto de muestreo forestal con Python + SQLite + Streamlit  
""")