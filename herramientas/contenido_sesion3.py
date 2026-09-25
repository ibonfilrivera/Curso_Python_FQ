"""Contenido de la Sesión 3: bibliotecas científicas y análisis de datos."""

from bloques import URL_CRUDA, cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(3, "Bibliotecas científicas y visualización de datos", """
En esta sesión usaremos bibliotecas especializadas de Python para ajustar datos experimentales,
generar gráficas de calidad editorial, analizar las lecturas de un espectrofotómetro y explorar
una base de datos con casi 10 000 compuestos.

**Al terminar podrás:**
- Hacer regresiones y resolver ecuaciones con SciPy.
- Construir gráficas científicas con Matplotlib (ejes, unidades, leyendas y exportación).
- Leer, filtrar, agrupar y resumir datos de laboratorio con Pandas.
- Determinar experimentalmente la ley de Lambert-Beer y su intervalo de validez.
- Representar moléculas y buscar subestructuras con RDKit.
""", carpeta, archivo)
        + instrucciones(3)
        + md("""
## **Importar bibliotecas**

Como vimos con NumPy en la sesión anterior, las bibliotecas se cargan con `import` y es
costumbre darles un alias corto:
""")
        + code("""
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
""")
        + md("""
# **math, SymPy y SciPy**

El módulo `math` incluye funciones y constantes matemáticas básicas.
""")
        + code("""
print(math.sin(math.pi))       # Seno (el resultado es ~0 por redondeo numérico)
print(math.cos(math.pi / 3))   # Coseno
print(math.sqrt(100))          # Raíz cuadrada
print(math.log(math.e))        # Logaritmo natural
print(math.log10(100))         # Logaritmo base 10
print(math.log2(8))            # Logaritmo base 2
""")
        + md("""
**SymPy** hace cálculo **simbólico**: manipula expresiones algebraicas en lugar de números.
""")
        + code("""
import sympy as sp

x = sp.symbols("x")
expresion = x**2 * sp.exp(-x)

print("Derivada:", sp.diff(expresion, x))
print("Integral:", sp.integrate(expresion, x))
""")
        + md("""
**SciPy** reúne métodos numéricos, estadísticos y de optimización para el trabajo científico.
Por ejemplo, con `scipy.stats` podemos analizar una curva de calibración de absorbancia contra
concentración:
""")
        + code("""
from scipy.stats import describe, linregress

concentraciones = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]      # mg/L
absorbancias = [0.012, 0.225, 0.451, 0.645, 0.852, 1.058]

print(describe(absorbancias))                          # Estadística descriptiva

ajuste = linregress(concentraciones, absorbancias)     # Regresión lineal
print(f"Pendiente: {ajuste.slope:.4f} L/mg")
print(f"Ordenada:  {ajuste.intercept:.4f}")
print(f"r²:        {ajuste.rvalue**2:.5f}")
""")
        + md("Con `curve_fit` de `scipy.optimize` podemos ajustar cualquier función, por ejemplo un polinomio de segundo grado:")
        + code("""
from scipy.optimize import curve_fit

def cuadratica(x, a, b, c):
    return a * x**2 + b * x + c

parametros, covarianza = curve_fit(cuadratica, concentraciones, absorbancias)
a, b, c = parametros
print(f"A = {a:.2e}·c² + {b:.4f}·c + {c:.4f}")
""")
        + md("""
`scipy.optimize` también resuelve ecuaciones numéricamente (`fsolve`) y busca mínimos de
funciones (`minimize`):
""")
        + code("""
from scipy.optimize import fsolve, minimize

def polinomio(x):
    return (x + 2)**2 - 4

raiz = fsolve(polinomio, x0=-3)       # Busca una raíz cerca de x = -3
print(f"Raíz: x = {raiz[0]:.4f}")

minimo = minimize(polinomio, x0=3)    # Busca un mínimo empezando en x = 3
print(f"Mínimo en x = {minimo.x[0]:.4f}, f(x) = {minimo.fun:.4f}")
""")
        + md(r"""
### **Ejercicio 1: Orden de reacción**

Se midió la concentración de un reactivo A a lo largo del tiempo. Las ecuaciones integradas de
velocidad son:

| Orden | Ecuación | Se grafica contra $t$ |
| :-: | :-: | :-: |
| 0 | $[A] = -kt + [A]_0$ | $[A]$ |
| 1 | $\ln[A] = -kt + \ln[A]_0$ | $\ln[A]$ |
| 2 | $\frac{1}{[A]} = kt + \frac{1}{[A]_0}$ | $\frac{1}{[A]}$ |

Haz las tres regresiones lineales con `linregress`, compara sus $r^2$ y guarda:
- `mejor_orden`: el orden (0, 1 o 2) que mejor describe los datos.
- `k`: la constante de velocidad (positiva) para ese orden.
""")
        + code("""
tiempo = [0, 10, 20, 30, 40, 50]                      # min
conc = [1.000, 0.607, 0.368, 0.223, 0.135, 0.082]     # mol/L
""")
        + ejercicio("ej1", """
ln_conc = [math.log(c) for c in conc]      # Lista por comprensión: aplica log a cada valor
inv_conc = ____

orden_0 = linregress(tiempo, conc)
orden_1 = ____
orden_2 = ____

print(f"r² orden 0: {orden_0.rvalue**2:.5f}")

mejor_orden = ____
k = ____
""")
        + md("""
# **Matplotlib**

Matplotlib es la biblioteca de visualización más usada en ciencia. Aunque tiene varias formas
de uso, recomendamos la interfaz **orientada a objetos**:

```python
fig, ax = plt.subplots()      # fig: la figura completa; ax: los ejes donde se dibuja
ax.plot(x, y)                 # Dibujar
ax.set_xlabel("...")          # Personalizar
plt.show()                    # Mostrar
```

Una gráfica científica de calidad siempre tiene: **ejes etiquetados con unidades**, una
**leyenda** si hay más de una serie, y un tamaño de letra legible.

📎 Referencias: [hojas de referencia rápida](https://matplotlib.org/cheatsheets/) y
[galería de ejemplos](https://matplotlib.org/stable/gallery/index.html).
""")
        + md(r"""
### **Gráfica de líneas: decaimiento radiactivo**

Retomemos el carbono-14 de la sesión anterior, ahora con $m(t) = m_0 \left(\frac{1}{2}\right)^{t/t_{1/2}}$.
Con NumPy generamos 200 tiempos de una sola vez con `np.linspace`.
""")
        + code("""
t_vida_media = 5730                              # años
t = np.linspace(0, 5 * t_vida_media, 200)        # 200 tiempos entre 0 y 5 vidas medias
masa = 1.0 * 0.5**(t / t_vida_media)             # g

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(t, masa, color="tab:blue", linewidth=2, label="¹⁴C")
ax.axhline(0.5, color="gray", linestyle="--", label="Mitad de la masa inicial")
ax.set_xlabel("Tiempo (años)")
ax.set_ylabel("Masa (g)")
ax.set_title("Decaimiento radiactivo del carbono-14")
ax.legend()
ax.grid(alpha=0.3)
plt.show()
""")
        + md("""
### **Varias gráficas en una figura**

`plt.subplots(filas, columnas)` crea una cuadrícula de ejes. Veamos los datos cinéticos del
Ejercicio 1 con las tres transformaciones: la que se vea como una recta indica el orden de reacción.
""")
        + code("""
tiempo_arr = np.array(tiempo)
conc_arr = np.array(conc)

transformaciones = [
    (conc_arr, "[A] (mol/L)", "Orden 0"),
    (np.log(conc_arr), "ln [A]", "Orden 1"),
    (1 / conc_arr, "1/[A] (L/mol)", "Orden 2"),
]

fig, ejes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, (y, etiqueta, titulo) in zip(ejes, transformaciones):
    ajuste_orden = linregress(tiempo_arr, y)
    ax.plot(tiempo_arr, y, "o", label="Datos")
    ax.plot(tiempo_arr, ajuste_orden.slope * tiempo_arr + ajuste_orden.intercept, "--",
            label=f"r² = {ajuste_orden.rvalue**2:.4f}")
    ax.set_xlabel("t (min)")
    ax.set_ylabel(etiqueta)
    ax.set_title(titulo)
    ax.legend()

fig.tight_layout()     # Evita que se encimen las etiquetas
plt.show()
""")
        + md("""
### **Guardar una figura**

Para un reporte o una tesis, exporta con alta resolución (300 ppp) o en formato vectorial (PDF,
SVG). En Colab, el archivo aparece en el panel de archivos 📁 de la izquierda.

```python
fig.savefig("cinetica.png", dpi=300, bbox_inches="tight")
fig.savefig("cinetica.pdf", bbox_inches="tight")
```
""")
        + md("""
### **Ejercicio 2: Curva de calibración**

Con los datos de `concentraciones` y `absorbancias` de la sección de SciPy:

1. Crea la figura `fig_calibracion` con los puntos experimentales (`ax.scatter`) y la recta del
   ajuste lineal (`ax.plot`).
2. Etiqueta ambos ejes con sus unidades y agrega una leyenda.
3. Una muestra problema tiene una absorbancia de 0.500. Calcula su concentración con la recta
   de calibración y guárdala en `conc_problema`.

> Aquí *suponemos* que la absorbancia es proporcional a la concentración. En el Ejercicio 3
> comprobaremos esa suposición con datos de un espectrofotómetro.
""")
        + ejercicio("ej2", """
ajuste = linregress(concentraciones, absorbancias)
x = np.array(concentraciones)

fig_calibracion, ax = plt.subplots(figsize=(6, 4))
ax.scatter(____, ____, label="Datos experimentales")
ax.plot(x, ____, color="tab:red", label="Ajuste lineal")
ax.set_xlabel(____)
ax.set_ylabel(____)
ax.legend()
plt.show()

conc_problema = ____
print(f"Concentración de la muestra problema: {conc_problema} mg/L")
""")
        + md("""
# **Pandas: datos del laboratorio**

Pandas es la biblioteca más usada para analizar datos tabulares. Su estructura principal es el
**DataFrame**, una tabla con filas y columnas con nombre, parecida a una hoja de cálculo. La
mayoría de los instrumentos (espectrofotómetros, potenciómetros, cromatógrafos) exportan sus
lecturas como CSV o Excel, y Pandas las lee con `pd.read_csv()` o `pd.read_excel()`.

Empezaremos con las lecturas de un espectrofotómetro: disoluciones estándar de KMnO₄ medidas
**por triplicado** a 525 nm en una celda de 1.00 cm, más una muestra problema. Los datos son
simulados, pero reproducen el comportamiento de un instrumento real.
""")
        + code(f"""
from pathlib import Path

def leer_datos(archivo):
    \"\"\"Lee un CSV de la carpeta data/: la copia local si existe o la de GitHub (en Colab).\"\"\"
    ruta_local = Path("../data") / archivo
    return pd.read_csv(ruta_local if ruta_local.exists() else f"{URL_CRUDA}/data/{{archivo}}")

datos_lb = leer_datos("lambert_beer_kmno4.csv")

print(f"{{datos_lb.shape[0]}} lecturas, columnas: {{list(datos_lb.columns)}}")
datos_lb.head(6)
""")
        + md("""
Una columna se selecciona por su nombre, y las filas se **filtran** escribiendo una condición
entre corchetes. Varias condiciones se combinan con `&` (y) o `|` (o), cada una entre paréntesis:
""")
        + code("""
print("Absorbancia máxima:", datos_lb["absorbancia"].max())

# Solo las lecturas de la muestra problema
datos_lb[datos_lb["tipo"] == "problema"]
""")
        + md("""
Para resumir datos por grupos usamos `groupby`, el equivalente a una *tabla dinámica* de Excel:
se agrupan las filas que comparten un valor y se aplica una función a cada grupo.
""")
        + code("""
# ¿Cuántas lecturas hay de cada tipo, y cuál es su absorbancia promedio?
datos_lb.groupby("tipo")["absorbancia"].agg(["count", "mean"])
""")
        + md(r"""
### **Ejercicio 3: Determinación de la ley de Lambert-Beer**

La ley de Lambert-Beer relaciona la absorbancia con la concentración:

$$A = \varepsilon\, b\, c$$

donde $\varepsilon$ es la absortividad molar (L·mol⁻¹·cm⁻¹), $b$ el paso óptico (cm) y $c$ la
concentración (mol/L). Con las lecturas de `datos_lb` vamos a comprobar si se cumple, en qué
intervalo, y a usarla para cuantificar la muestra problema.

**3a. Promedio de réplicas.** Filtra los estándares (`tipo == "estandar"`) y agrúpalos por
concentración para obtener el DataFrame `resumen`, con las columnas `promedio` y `desviacion`
(desviación estándar) de la absorbancia.
""")
        + ejercicio("ej3a", """
estandares = datos_lb[____]
resumen = estandares.groupby(____)["absorbancia"].agg(promedio="mean", desviacion="std")
resumen
""")
        + md("""
**3b. Absortividad molar.** Los espectrofotómetros pierden linealidad a absorbancias altas (por
la luz parásita, entre otras causas), así que la ley solo se cumple en un intervalo.

1. Ajusta una recta con **todos** los estándares y guarda su r² en `r2_todos`.
2. Ajusta otra solo con los estándares cuya absorbancia promedio sea **≤ 1.0** (DataFrame
   `lineal`, ajuste `ajuste_lb`) y guarda su r² en `r2_lineal`.
3. Calcula la absortividad molar `epsilon` a partir de la pendiente (b = 1.00 cm).
4. Grafica en `fig_lb` los promedios con barras de error y la recta del intervalo lineal.
""")
        + ejercicio("ej3b", """
b = 1.00   # cm, paso óptico

ajuste_todos = linregress(resumen.index, resumen["promedio"])
r2_todos = ____

lineal = resumen[____]
ajuste_lb = ____
r2_lineal = ____
epsilon = ____

fig_lb, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(resumen.index * 1e3, resumen["promedio"], yerr=resumen["desviacion"],
            fmt="o", capsize=3, label="Estándares (promedio ± s)")
c = np.linspace(0, lineal.index.max(), 50)
ax.plot(c * 1e3, ____, color="tab:red", label="Ajuste lineal (A ≤ 1)")
ax.set_xlabel("Concentración de KMnO₄ (mmol/L)")
ax.set_ylabel(____)
ax.legend()
plt.show()

print(f"r² con todos los puntos: {r2_todos}")
print(f"r² en el intervalo lineal: {r2_lineal}")
print(f"ε = {epsilon} L/(mol·cm)")
""")
        + md("""
**3c. Muestra problema.** Promedia las tres lecturas de la muestra problema, calcula su
concentración con `ajuste_lb` (`conc_problema_lb`, en mol/L) y guarda en `dentro_intervalo` si
esa concentración queda dentro del intervalo de los estándares lineales (`True` o `False`).

> 🤔 **Para reflexionar:** si otra muestra diera A = 1.8, ¿por qué convendría diluirla antes de
> medirla, en lugar de extrapolar la recta?
""")
        + ejercicio("ej3c", """
problema = datos_lb[datos_lb["tipo"] == "problema"]
a_problema = ____

conc_problema_lb = ____
dentro_intervalo = ____

print(f"A = {a_problema} → c = {conc_problema_lb} mol/L")
print(f"¿Dentro del intervalo calibrado? {dentro_intervalo}")
""")
        + md("""
## **Bases de datos grandes: AqSolDB**

Las mismas herramientas sirven para tablas mucho más grandes. Usaremos **AqSolDB**, una base de
datos curada con la solubilidad acuosa de 9 982 compuestos
([Sorkun *et al.*, *Scientific Data* **6**, 143 (2019)](https://doi.org/10.1038/s41597-019-0151-1)).
Algunas de sus columnas son:

| Columna | Significado |
| :--- | :--- |
| `Name`, `SMILES` | Nombre y estructura del compuesto |
| `Solubility` | log S, con S la solubilidad en mol/L |
| `MolWt` | Masa molar (g/mol) |
| `MolLogP` | Coeficiente de partición octanol/agua (log P) |
| `NumHDonors`, `NumHAcceptors` | Donadores y aceptores de puentes de hidrógeno |
| `TPSA` | Área superficial polar (Å²) |
""")
        + code("""
df = leer_datos("curated_solubility.csv")

print(f"La tabla tiene {df.shape[0]} filas y {df.shape[1]} columnas")
df.head()
""")
        + md("Hagamos un análisis preliminar. `describe()` resume las columnas numéricas:")
        + code("""
df[["Solubility", "MolWt", "MolLogP", "NumHDonors", "NumHAcceptors"]].describe()
""")
        + code("""
# Compuestos con masa molar menor a 50 g/mol
df[df["MolWt"] < 50][["Name", "MolWt", "Solubility"]]
""")
        + code("""
# Los 5 compuestos más solubles
df.sort_values("Solubility", ascending=False)[["Name", "Solubility"]].head()
""")
        + md("Pandas se integra con Matplotlib. Por ejemplo, un histograma de la solubilidad:")
        + code("""
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["Solubility"], bins=50, color="tab:green", edgecolor="white")
ax.set_xlabel("log S (S en mol/L)")
ax.set_ylabel("Número de compuestos")
ax.set_title("Distribución de la solubilidad acuosa en AqSolDB")
plt.show()
""")
        + md("""
### **Ejercicio 4: Regla de los 5 de Lipinski**

En el diseño de fármacos, la regla de Lipinski estima si un compuesto podría ser activo por vía
oral. Un buen candidato cumple **todas** estas condiciones:

- Masa molar ≤ 500 g/mol.
- log P ≤ 5.
- Donadores de puentes de hidrógeno ≤ 5.
- Aceptores de puentes de hidrógeno ≤ 10.

Guarda en `lipinski` las filas de `df` que cumplen la regla y en `porcentaje_lipinski` el
porcentaje de compuestos que la cumplen.
""")
        + ejercicio("ej4", """
lipinski = df[(df["MolWt"] <= 500)
              & (____)
              & (____)
              & (____)]

porcentaje_lipinski = ____
print(f"{len(lipinski)} compuestos ({porcentaje_lipinski} %) cumplen la regla de Lipinski")
""")
        + md("""
### **Ejercicio 5 (integrador): lipofilicidad y solubilidad**

¿Los compuestos más lipofílicos son menos solubles en agua?

1. Crea la figura `fig_logp` con un diagrama de dispersión de `MolLogP` (eje x) contra
   `Solubility` (eje y), con ambos ejes etiquetados.
2. Calcula el coeficiente de correlación de Pearson entre ambas columnas y guárdalo en `r_logp`.
3. Interpreta: ¿qué signo tiene la correlación y qué significa químicamente?
""")
        + ejercicio("ej5", """
r_logp = ____

fig_logp, ax = plt.subplots(figsize=(6, 4))
ax.scatter(____, ____, s=5, alpha=0.3)
____
____
plt.show()
print(f"r = {r_logp}")
""")
        + md("""
# **RDKit: química computacional**

RDKit es una biblioteca de quimioinformática: interpreta estructuras moleculares (por ejemplo,
en notación **SMILES**), las dibuja y calcula propiedades. Como no viene instalada en Colab, la
instalamos primero.
""")
        + code("""
try:
    import rdkit
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "rdkit"], check=True)

from rdkit import Chem, RDLogger
from rdkit.Chem import Draw

RDLogger.DisableLog("rdApp.*")   # Oculta advertencias de estructuras problemáticas
""")
        + code("""
aspirina = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
aspirina
""")
        + md("Convertimos todos los SMILES de la tabla en objetos de RDKit (tarda unos segundos):")
        + code("""
df["Mols"] = df["SMILES"].apply(Chem.MolFromSmiles)

no_validas = df["Mols"].isna().sum()
print(f"Moléculas que RDKit no pudo interpretar: {no_validas}")

Draw.MolsToGridImage(df["Mols"][:8].tolist(), molsPerRow=4, subImgSize=(200, 200),
                     legends=[nombre[:25] for nombre in df["Name"][:8]])
""")
        + md("""
### **Ejercicio 6: Búsqueda de subestructuras**

Con un patrón **SMARTS** podemos buscar fragmentos dentro de las moléculas. El anillo bencénico
aromático se escribe `"c1ccccc1"`.

1. Completa la función `tiene_benceno(mol)`, que devuelva `True` si la molécula contiene un
   anillo bencénico (y `False` si `mol` es `None`).
2. Aplícala para crear la columna `df["tiene_benceno"]`.
3. Guarda en `n_benceno` cuántos compuestos contienen benceno.
""")
        + ejercicio("ej6", """
patron_benceno = Chem.MolFromSmarts("c1ccccc1")

def tiene_benceno(mol):
    if mol is None:
        return False
    return ____

df["tiene_benceno"] = ____
n_benceno = ____
print(f"{n_benceno} compuestos contienen un anillo bencénico")
""")
        + md("""
## **Resumen de la sesión**

| Biblioteca | Para qué sirve | Funciones clave |
| :--- | :--- | :--- |
| `math` | Funciones matemáticas básicas | `math.log`, `math.sqrt`, `math.pi` |
| SymPy | Cálculo simbólico | `sp.symbols`, `sp.diff`, `sp.integrate` |
| SciPy | Estadística, ajustes y ecuaciones | `linregress`, `curve_fit`, `fsolve` |
| Matplotlib | Gráficas | `plt.subplots`, `ax.plot`, `ax.scatter`, `ax.errorbar`, `fig.savefig` |
| Pandas | Datos tabulares | `pd.read_csv`, `df[condición]`, `groupby().agg()`, `describe` |
| RDKit | Quimioinformática | `Chem.MolFromSmiles`, `HasSubstructMatch` |

**Para seguir aprendiendo:**
- [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas) y [Data Visualization](https://www.kaggle.com/learn/data-visualization).
- [Tutorial de introducción de RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html).
""")
        + cierre()
    )
