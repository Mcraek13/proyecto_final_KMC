import sqlite3
import tkinter as tk
from tkinter import messagebox


# Función para guardar los datos
def guardar_arbol():
    datos = (
        id.get(),
        especie.get(),
        float(dap.get()),
        float(altura.get()),
        parcela.get(),
        ubicacion.get(),
        float(largo_hoja.get()),
        float(ancho_hoja.get())
    )

    conn = sqlite3.connect("arboles.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO arboles (
            id, especie, dap, altura, parcela, ubicacion, largo_hoja, ancho_hoja
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()

    messagebox.showinfo("✅ Éxito", "Árbol guardado correctamente.")
    limpiar_campos()


def limpiar_campos():
    for campo in [id, especie, dap, altura, parcela, ubicacion, largo_hoja, ancho_hoja]:
        campo.delete(0, tk.END)


# Crear ventana
ventana = tk.Tk()
ventana.title("Ingreso de Árboles")

# Campos
campos = [
    ("id", "id"), ("Especie", "especie"), ("DAP (cm)", "dap"), ("Altura (m)", "altura"),
    ("Parcela", "parcela"),
    ("Ubicación", "ubicacion"), ("Largo hoja (cm)", "largo_hoja"), ("Ancho hoja (cm)", "ancho_hoja")
]

for i, (label, varname) in enumerate(campos):
    tk.Label(ventana, text=label).grid(row=i, column=0, sticky="e")
    globals()[varname] = tk.Entry(ventana)
    globals()[varname].grid(row=i, column=1)

# Botón
tk.Button(ventana, text="Guardar árbol", command=guardar_arbol).grid(row=len(campos), column=0, columnspan=2)

# Ejecutar ventana
ventana.mainloop()
