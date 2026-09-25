"""Genera data/lambert_beer_kmno4.csv: datos simulados de un espectrofotómetro.

Simula la curva de calibración de KMnO₄ a 525 nm (celda de 1.00 cm) con tres
réplicas por estándar y una muestra problema. A absorbancias altas se incluye
el efecto de la luz parásita del instrumento, que curva la respuesta y hace
que la ley de Lambert-Beer solo se cumpla en un intervalo.

Uso (desde la carpeta Curso_Python_FQ):

    python herramientas/generar_datos_lambert_beer.py
"""

import csv
import math
import random
from pathlib import Path

EPSILON = 2450          # L/(mol·cm), absortividad molar "verdadera"
PASO_OPTICO = 1.00      # cm
LUZ_PARASITA = 0.004    # Fracción de luz parásita del instrumento
RUIDO = 0.003           # Desviación estándar de cada lectura
BLANCO = 0.004          # Absorbancia residual de la celda

ESTANDARES = [0.0, 4e-5, 8e-5, 1.2e-4, 1.6e-4, 2.4e-4, 3.2e-4, 4.0e-4, 6.0e-4, 8.0e-4,
              1.0e-3, 1.2e-3]  # mol/L
CONC_PROBLEMA = 2.05e-4  # mol/L


def absorbancia_medida(concentracion, azar):
    verdadera = EPSILON * PASO_OPTICO * concentracion
    transmitancia = (10 ** -verdadera + LUZ_PARASITA) / (1 + LUZ_PARASITA)
    return -math.log10(transmitancia) + BLANCO + azar.gauss(0, RUIDO)


def main():
    azar = random.Random(525)
    filas = []
    for concentracion in ESTANDARES:
        for replica in (1, 2, 3):
            filas.append(["estandar", concentracion, replica,
                          round(absorbancia_medida(concentracion, azar), 3)])
    for replica in (1, 2, 3):
        filas.append(["problema", "", replica,
                      round(absorbancia_medida(CONC_PROBLEMA, azar), 3)])

    ruta = Path(__file__).resolve().parent.parent / "data" / "lambert_beer_kmno4.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["tipo", "concentracion_mol_L", "replica", "absorbancia"])
        escritor.writerows(filas)
    print(f"{ruta.name}: {len(filas)} lecturas")


if __name__ == "__main__":
    main()
