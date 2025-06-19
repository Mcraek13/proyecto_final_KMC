import streamlit as st
import pandas as pd
import sqlite3
from scipy import stats
import numpy as np
import io


# -------------------------
# Conexión a la base de datos
# -------------------------
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect("arboles.db")
    df = pd.read_sql_query("SELECT * FROM arboles", conn)
    conn.close()
    return df

df = cargar_datos()

def interpretar_correlacion(r):
    if r == 1:
        return "Correlación perfecta positiva"
    elif r == -1:
        return "Correlación perfecta negativa"
    elif r >= 0.7:
        return "Correlación fuerte positiva"
    elif r >= 0.4:
        return "Correlación moderada positiva"
    elif r >= 0.1:
        return "Correlación débil positiva"
    elif r <= -0.7:
        return "Correlación fuerte negativa"
    elif r <= -0.4:
        return "Correlación moderada negativa"
    elif r <= -0.1:
        return "Correlación débil negativa"
    else:
        return "Sin correlación"

# -------------------------
# Cálculo del tamaño de muestra
# -------------------------
def calcular_tamaño_muestra(N, Z=1.96, p=0.5, e=0.05):
    numerador = N * (Z ** 2) * p * (1 - p)
    denominador = ((e ** 2) * (N - 1)) + ((Z ** 2) * p * (1 - p))
    n = numerador / denominador
    return int(round(n))

# -------------------------
# Título de la app
# -------------------------
st.title("📊 Análisis Estadístico de Árboles")

# -------------------------
# Mostrar resumen general
# -------------------------
N = len(df)
n_muestra = calcular_tamaño_muestra(N)
st.subheader("1️⃣ Tamaño de muestra representativa")
st.write(f"🌳 Árboles en la base de datos: {N}")
st.write(f"📌 Tamaño de muestra estimado (95% confianza, 5% error): {n_muestra}")

# -------------------------
# Estadísticas descriptivas
# -------------------------
st.subheader("2️⃣ Estadísticas descriptivas")

cols_num = ["altura", "dap", "largo_hoja", "ancho_hoja"]
df_numerico = df[cols_num].dropna()

desc = df_numerico.describe().T
desc["moda"] = df_numerico.mode().iloc[0]
desc["varianza"] = df_numerico.var()
desc = desc[["mean", "50%", "moda", "std", "varianza"]]
desc.columns = ["Media", "Mediana", "Moda", "Desv. Estándar", "Varianza"]

st.dataframe(desc)

# -------------------------
# Correlación entre variables
# -------------------------
st.subheader("3️⃣ Matriz de correlación (Pearson)")

corr_matrix = df_numerico.corr(method="pearson")
st.dataframe(corr_matrix)

# Interpretación de la matriz de correlación
interpretaciones = []
for var1 in corr_matrix.columns:
    for var2 in corr_matrix.columns:
        if var1 != var2:
            r = corr_matrix.loc[var1, var2]
            interpretaciones.append({
                "Variable 1": var1,
                "Variable 2": var2,
                "Coef. Pearson (r)": round(r, 2),
                "Interpretación": interpretar_correlacion(r)
            })

df_interpretacion = pd.DataFrame(interpretaciones)

st.write("📖 Interpretación de correlaciones:")
st.dataframe(df_interpretacion)

# -------------------------
# Prueba de Chi-cuadrado (si hay variables categóricas)
# Prueba t de Student para comparar medias

# Prueba ANOVA para comparar medias entre varias especies
# -------------------------
st.subheader("4️⃣ Prueba ANOVA (más de dos grupos)")

cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
if cat_cols:
    var_cat = st.selectbox("Variable categórica (grupos)", cat_cols, key="anova_cat")
    var_num = st.selectbox("Variable numérica a comparar", cols_num, key="anova_num")

    grupos = df[var_cat].dropna().unique()
    muestras = [df[df[var_cat] == grupo][var_num].dropna() for grupo in grupos]

    if all(len(muestra) > 1 for muestra in muestras) and len(grupos) > 2:
        # Aplicar ANOVA
        f_stat, p_valor = stats.f_oneway(*muestras)

        st.write(f"📊 Comparación de medias de **{var_num}** entre grupos de **{var_cat}**")
        resumen = df.groupby(var_cat)[var_num].agg(['count', 'mean', 'std']).rename(columns={
            "count": "n", "mean": "Media", "std": "Desv. Estándar"
        })
        st.dataframe(resumen)

        st.write(f"🔍 Estadístico F: {f_stat:.4f}")
        st.write(f"🧪 p-valor: {p_valor:.4f}")

        if p_valor < 0.05:
            st.success("✅ Existe una diferencia estadísticamente significativa entre al menos dos de los grupos.")
            st.write("Esto indica que la media de **al menos un grupo** es distinta en comparación con las otras.")
        else:
            st.warning("🟡 No hay evidencia suficiente para afirmar que existen diferencias significativas entre los grupos.")
            st.write("Esto sugiere que las medias de los grupos podrían ser estadísticamente similares.")

    else:
        st.warning("Cada grupo debe tener al menos 2 datos y debe haber más de 2 grupos para aplicar ANOVA.")
else:
    st.info("No hay variables categóricas para aplicar ANOVA.")

# -------------------------
# Mostrar muestra aleatoria
# -------------------------
st.subheader("5️⃣ Muestra aleatoria representativa")
muestra = df.sample(n=n_muestra, random_state=42)
st.dataframe(muestra)

# -------------------------
# Descargar muestra como Excel
# -------------------------
@st.cache_data
def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

st.download_button(
    label="📥 Descargar muestra como Excel",
    data=convertir_excel(muestra),
    file_name="muestra_arboles.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.subheader("📌 Cantidad de árboles por especie")
st.dataframe(df["especie"].value_counts())