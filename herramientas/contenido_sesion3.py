"""Contenido de la Sesión 3: bibliotecas científicas y análisis de datos."""

from bloques import URL_CRUDA, cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(3, "Bibliotecas científicas y visualización de datos", """
En esta sesión usaremos bibliotecas especializadas de Python para hacer cálculos numéricos,
ajustar datos experimentales, generar gráficas de calidad editorial y explorar una base de datos
con casi 10 000 compuestos.

**Al terminar podrás:**
- Hacer regresiones y resolver ecuaciones con SciPy.
- Operar con vectores y matrices usando NumPy.
- Construir gráficas científicas con Matplotlib (ejes, unidades, leyendas y exportación).
- Leer, filtrar y resumir datos tabulares con Pandas.
- Representar moléculas y buscar subestructuras con RDKit.
""", carpeta, archivo)
        + instrucciones(3)
        + md("""
## **Importar bibliotecas**

Una **biblioteca** (o *librería*) es un conjunto de funciones que alguien más escribió y que
podemos reutilizar. Se cargan con `import`, y es costumbre darles un alias corto:
""")
        + code("""
import math
import time

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
# **NumPy**

Las listas de Python son flexibles, pero lentas para cálculos numéricos. NumPy ofrece los
**arreglos** (`np.array`), que permiten operar con todos los elementos a la vez y son mucho más
rápidos. Comparemos el tiempo para elevar al cuadrado un millón de números:
""")
        + code("""
lista = list(range(1_000_000))
arreglo = np.array(lista)

inicio = time.perf_counter()
cuadrados_lista = [valor**2 for valor in lista]
tiempo_lista = time.perf_counter() - inicio

inicio = time.perf_counter()
cuadrados_arreglo = arreglo**2          # Operación vectorizada: sin ciclo explícito
tiempo_arreglo = time.perf_counter() - inicio

print(f"Con lista:   {tiempo_lista * 1000:.1f} ms")
print(f"Con arreglo: {tiempo_arreglo * 1000:.1f} ms  ({tiempo_lista / tiempo_arreglo:.0f} veces más rápido)")
""")
        + md("Los arreglos representan vectores y matrices, y permiten las operaciones del álgebra lineal:")
        + code("""
matriz_A = np.array([[1, 2],
                     [3, 4]])
matriz_B = np.array([[5, 6],
                     [7, 8]])

# Producto elemento a elemento (NO es el producto de matrices)
print("A * B =\\n", matriz_A * matriz_B)

# Producto matricial (filas por columnas)
print("A @ B =\\n", matriz_A @ matriz_B)

# Transpuesta
print("Aᵀ =\\n", matriz_A.T)
""")
        + md("""
Al igual que las listas, los arreglos se indexan; además podemos extraer filas o columnas
completas con **rebanadas** (*slicing*): `arr[fila, columna]`, donde `:` significa "todas".
""")
        + code("""
arr = np.arange(9).reshape(3, 3)    # Números del 0 al 8 acomodados en una matriz 3×3
print(arr, "forma:", arr.shape)

print("Primera fila:", arr[0])
print("Elemento (0, 1):", arr[0, 1])
print("Primera columna:", arr[:, 0])

arr[0, :] = [10, 20, 30]            # Reemplazamos la primera fila
print(arr)
""")
        + md("El módulo `np.linalg` contiene las funciones más comunes de álgebra lineal:")
        + code("""
print("Determinante de A:", np.linalg.det(matriz_A))

valores_propios, vectores_propios = np.linalg.eig(matriz_A)
print("Valores propios:", valores_propios)
print("Vectores propios (columnas):\\n", vectores_propios)
""")
        + code("""
# Resolver el sistema   2x +  y +  z = 10
#                        x -  y + 2z =  5
#                       3x + 2y -  z =  7
coeficientes = np.array([[2,  1,  1],
                         [1, -1,  2],
                         [3,  2, -1]])
resultados = np.array([10, 5, 7])

solucion = np.linalg.solve(coeficientes, resultados)
print("x, y, z =", solucion)
""")
        + md(r"""
### **Ejercicio 2: Matriz de rotación**

Para rotar un vector en $\mathbb{R}^2$ un ángulo $\theta$ se multiplica por la matriz de rotación:

$$R(\theta) = \begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{pmatrix}$$

Escribe la función `rotar_vector(vector, angulo_grados)` que devuelva el vector rotado.
""")
        + ejercicio("ej2", """
def rotar_vector(vector, angulo_grados):
    theta = ____
    R = ____
    return ____

print(rotar_vector([1, 0], 90))   # Debe dar aproximadamente [0, 1]
""")
        + md(r"""
### **Ejercicio 3: Regla de Cramer**

Para un sistema de $2 \times 2$

$$\begin{aligned}
ax + by &= e \\
cx + dy &= f
\end{aligned}$$

la regla de Cramer da $x = \frac{\Delta_x}{\Delta}$ y $y = \frac{\Delta_y}{\Delta}$, con

$$\Delta = \begin{vmatrix} a & b \\ c & d \end{vmatrix}, \quad
\Delta_x = \begin{vmatrix} e & b \\ f & d \end{vmatrix}, \quad
\Delta_y = \begin{vmatrix} a & e \\ c & f \end{vmatrix}$$

Escribe `resolver_cramer_2x2(A, b)` que devuelva un arreglo `[x, y]`, y compara tu resultado
con `np.linalg.solve`.
""")
        + ejercicio("ej3", """
def resolver_cramer_2x2(A, b):
    A = np.array(A, dtype=float)
    delta = ____

    A_x = A.copy()
    A_x[:, 0] = b
    A_y = ____
    ____

    return ____

A = np.array([[3, 2], [4, -1]])
b = np.array([12, 5])
print(resolver_cramer_2x2(A, b), np.linalg.solve(A, b))
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
### **Ejercicio 4: Curva de calibración**

Con los datos de `concentraciones` y `absorbancias` de la sección de SciPy:

1. Crea la figura `fig_calibracion` con los puntos experimentales (`ax.scatter`) y la recta del
   ajuste lineal (`ax.plot`).
2. Etiqueta ambos ejes con sus unidades y agrega una leyenda.
3. Una muestra problema tiene una absorbancia de 0.500. Calcula su concentración con la recta
   de calibración y guárdala en `conc_problema`.
""")
        + ejercicio("ej4", """
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
# **Pandas**

Pandas es la biblioteca más usada para analizar datos tabulares: lee archivos (CSV, Excel,
etc.), filtra, agrupa y grafica. Su estructura principal es el **DataFrame**, una tabla con
filas y columnas con nombre, similar a una hoja de cálculo.

Usaremos **AqSolDB**, una base de datos curada con la solubilidad acuosa de 9 982 compuestos
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
        + code(f"""
from pathlib import Path

RUTA_LOCAL = Path("../data/curated_solubility.csv")
URL_DATOS = "{URL_CRUDA}/data/curated_solubility.csv"

# Usa la copia local si existe; si no (por ejemplo, en Colab), descarga el archivo
df = pd.read_csv(RUTA_LOCAL if RUTA_LOCAL.exists() else URL_DATOS)

print(f"La tabla tiene {{df.shape[0]}} filas y {{df.shape[1]}} columnas")
df.head()
""")
        + md("Hagamos un análisis preliminar. `describe()` resume las columnas numéricas:")
        + code("""
df[["Solubility", "MolWt", "MolLogP", "NumHDonors", "NumHAcceptors"]].describe()
""")
        + md("""
Para **filtrar** filas escribimos una condición entre corchetes. Varias condiciones se combinan
con `&` (y) o `|` (o), y cada una va entre paréntesis:
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
### **Ejercicio 5: Regla de los 5 de Lipinski**

En el diseño de fármacos, la regla de Lipinski estima si un compuesto podría ser activo por vía
oral. Un buen candidato cumple **todas** estas condiciones:

- Masa molar ≤ 500 g/mol.
- log P ≤ 5.
- Donadores de puentes de hidrógeno ≤ 5.
- Aceptores de puentes de hidrógeno ≤ 10.

Guarda en `lipinski` las filas de `df` que cumplen la regla y en `porcentaje_lipinski` el
porcentaje de compuestos que la cumplen.
""")
        + ejercicio("ej5", """
lipinski = df[(df["MolWt"] <= 500)
              & (____)
              & (____)
              & (____)]

porcentaje_lipinski = ____
print(f"{len(lipinski)} compuestos ({porcentaje_lipinski} %) cumplen la regla de Lipinski")
""")
        + md("""
### **Ejercicio 6 (integrador): lipofilicidad y solubilidad**

¿Los compuestos más lipofílicos son menos solubles en agua?

1. Crea la figura `fig_logp` con un diagrama de dispersión de `MolLogP` (eje x) contra
   `Solubility` (eje y), con ambos ejes etiquetados.
2. Calcula el coeficiente de correlación de Pearson entre ambas columnas y guárdalo en `r_logp`.
3. Interpreta: ¿qué signo tiene la correlación y qué significa químicamente?
""")
        + ejercicio("ej6", """
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
### **Ejercicio 7: Búsqueda de subestructuras**

Con un patrón **SMARTS** podemos buscar fragmentos dentro de las moléculas. El anillo bencénico
aromático se escribe `"c1ccccc1"`.

1. Completa la función `tiene_benceno(mol)`, que devuelva `True` si la molécula contiene un
   anillo bencénico (y `False` si `mol` es `None`).
2. Aplícala para crear la columna `df["tiene_benceno"]`.
3. Guarda en `n_benceno` cuántos compuestos contienen benceno.
""")
        + ejercicio("ej7", """
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
| NumPy | Arreglos y álgebra lineal | `np.array`, `@`, `np.linalg.solve` |
| Matplotlib | Gráficas | `plt.subplots`, `ax.plot`, `ax.scatter`, `fig.savefig` |
| Pandas | Datos tabulares | `pd.read_csv`, `df.describe`, `df[condición]` |
| RDKit | Quimioinformática | `Chem.MolFromSmiles`, `HasSubstructMatch` |

**Para seguir aprendiendo:**
- [Kaggle Learn: Pandas](https://www.kaggle.com/learn/pandas) y [Data Visualization](https://www.kaggle.com/learn/data-visualization).
- [Tutorial de introducción de RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html).
""")
        + cierre()
    )
