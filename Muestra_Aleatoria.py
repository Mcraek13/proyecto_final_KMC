# programa que pueda calcular la muestra representativa que se debe muestrear
# formula para calcular la muestra conociendo la población n= N x Z2 x p x (1−p) / (e2 x (N−1)) + (Z2 x p x (1−p))

import pandas as pd
import openpyxl

nivel_confianza = 0.95  # 95%
Z = 1.96  # valor z para 95%
p = 0.5   # proporción esperada
e = 0.05  # error permitido (5%)

def calcular_tamaño_muestra(N, Z=1.96, p=0.5, e=0.05):
    numerador = N * (Z ** 2) * p * (1 - p)
    denominador = ((e ** 2) * (N - 1)) + ((Z ** 2) * p * (1 - p))
    n = numerador / denominador
        print(f"Se debe muestrear {n} árboles para tener una muestra representativa en la parcela.")
    return int(round(n))



df = pd.read_excel("Proyecto_final.xlsx")
#detallar que columna necesito para hacer este calculo
N = len(df)

#escoger aleatoriamente los arboles

muestra = df.sample(n=n_muestra, random_state=42)
muestra.to_excel("muestra_seleccionada.xlsx", index=False)
