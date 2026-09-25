"""Ejercicios de la Sesión 3: SciPy, NumPy, Matplotlib, Pandas y RDKit."""

import math

from .nucleo import (Incorrecto, Pendiente, Sesion, ____, _tiene_espacios, comparar_numero,
                     obtener, obtener_funcion, probar_funcion)

sesion = Sesion("Sesión 3")
progreso = sesion.progreso

TIEMPO = [0, 10, 20, 30, 40, 50]
CONCENTRACION = [1.000, 0.607, 0.368, 0.223, 0.135, 0.082]
CONC_CALIBRACION = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
ABS_CALIBRACION = [0.012, 0.225, 0.451, 0.645, 0.852, 1.058]


def _regresion(x, y):
    """Pendiente, ordenada y r² por mínimos cuadrados (sin depender de SciPy)."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    pendiente = sxy / sxx
    return pendiente, my - pendiente * mx, sxy ** 2 / (sxx * syy)


def _cerca_arreglo(obtenido, esperado):
    import numpy as np
    obtenido = np.asarray(obtenido, dtype=float)
    return obtenido.shape == np.shape(esperado) and np.allclose(obtenido, esperado, atol=1e-6)


# --- Ejercicio 1: cinética ---------------------------------------------------

def _ej1(ns):
    orden = obtener(ns, "mejor_orden")
    if orden != 1:
        raise Incorrecto(f"`mejor_orden` vale {orden!r}. Compara los valores de r² "
                         "(`rvalue**2`) de las tres regresiones: el mejor ajuste es el "
                         "más cercano a 1.")
    pendiente, _, _ = _regresion(TIEMPO, [math.log(c) for c in CONCENTRACION])
    k = obtener(ns, "k")
    if isinstance(k, (int, float)) and k < 0:
        raise Incorrecto("La constante de velocidad es positiva: k = −pendiente.")
    comparar_numero("k", k, -pendiente, rel=5e-3)
    return f"La reacción es de primer orden con k ≈ {-pendiente:.4f} min⁻¹."


ej1 = sesion.agregar(
    "ej1", "Orden de reacción", _ej1,
    pista="Para cada orden, grafica la variable transformada ([A], ln[A] o 1/[A]) contra "
          "t con `linregress`. El atributo `rvalue` es r; elévalo al cuadrado.",
    solucion="""
ln_conc = [math.log(c) for c in conc]
inv_conc = [1 / c for c in conc]

ajustes = {
    0: linregress(tiempo, conc),
    1: linregress(tiempo, ln_conc),
    2: linregress(tiempo, inv_conc),
}
for orden, ajuste in ajustes.items():
    print(f"Orden {orden}: r² = {ajuste.rvalue**2:.5f}")

mejor_orden = max(ajustes, key=lambda o: ajustes[o].rvalue**2)
k = -ajustes[1].slope
print(f"Mejor ajuste: orden {mejor_orden}, k = {k:.4f} min⁻¹")
""")


# --- Ejercicio 2: matriz de rotación ------------------------------------------

def _ej2(ns):
    funcion = obtener_funcion(ns, "rotar_vector")
    r = math.sqrt(2)
    casos = [
        (([1, 0], 90), {}, [0.0, 1.0]),
        (([0, 1], 90), {}, [-1.0, 0.0]),
        (([2, 0], 180), {}, [-2.0, 0.0]),
        (([1, 1], 45), {}, [0.0, r]),
        (([3, 4], 0), {}, [3.0, 4.0]),
    ]
    probar_funcion("rotar_vector", funcion, casos, comparar=_cerca_arreglo)


ej2 = sesion.agregar(
    "ej2", "Rotación de un vector", _ej2,
    pista="El ángulo llega en grados: conviértelo con `np.radians()`. El producto "
          "matriz-vector se escribe `R @ v`.",
    solucion="""
def rotar_vector(vector, angulo_grados):
    theta = np.radians(angulo_grados)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return R @ np.asarray(vector, dtype=float)

print(rotar_vector([0, 1], 90))
""")


# --- Ejercicio 3: regla de Cramer ---------------------------------------------

def _ej3(ns):
    funcion = obtener_funcion(ns, "resolver_cramer_2x2")
    import numpy as np
    casos = [
        ((np.array([[3, 2], [4, -1]]), np.array([12, 5])), {}, [2.0, 3.0]),
        ((np.array([[1, 1], [1, -1]]), np.array([0.5, 0.1])), {}, [0.3, 0.2]),
        ((np.array([[2.0, 1.0], [1.0, 3.0]]), np.array([3.0, 5.0])), {}, [0.8, 1.4]),
    ]
    try:
        probar_funcion("resolver_cramer_2x2", funcion, casos, comparar=_cerca_arreglo)
    except Incorrecto as e:
        if "0.5" in str(e):
            raise Incorrecto(str(e) + " Si la matriz es de enteros, `copy()` conserva el "
                             "tipo `int` y los decimales de `b` se truncan: usa "
                             "`np.array(A, dtype=float)`.") from None
        raise


ej3 = sesion.agregar(
    "ej3", "Regla de Cramer", _ej3,
    pista="Construye Aₓ sustituyendo la primera columna de A por b (`Ax[:, 0] = b`) y A_y "
          "sustituyendo la segunda. Trabaja con `dtype=float` para no perder decimales.",
    solucion="""
def resolver_cramer_2x2(A, b):
    A = np.array(A, dtype=float)
    delta = np.linalg.det(A)

    A_x = A.copy()
    A_x[:, 0] = b
    A_y = A.copy()
    A_y[:, 1] = b

    return np.array([np.linalg.det(A_x), np.linalg.det(A_y)]) / delta

A = np.array([[3, 2], [4, -1]])
b = np.array([12, 5])
print(resolver_cramer_2x2(A, b), np.linalg.solve(A, b))
""")


# --- Ejercicio 4: curva de calibración ----------------------------------------

def _ejes_de(ns, nombre):
    from matplotlib.figure import Figure
    figura = obtener(ns, nombre)
    if not isinstance(figura, Figure):
        raise Incorrecto(f"`{nombre}` debe ser una figura de Matplotlib; créala con "
                         f"`{nombre}, ax = plt.subplots()`.")
    if not figura.axes:
        raise Incorrecto(f"`{nombre}` no tiene ejes. ¿Dibujaste sobre otra figura?")
    ax = figura.axes[0]
    if not ax.get_xlabel().strip() or not ax.get_ylabel().strip():
        raise Incorrecto("Toda gráfica científica necesita etiquetas en ambos ejes, "
                         "con unidades: usa `ax.set_xlabel()` y `ax.set_ylabel()`.")
    return ax


def _puntos_graficados(ax):
    """Número de puntos dibujados como marcadores (scatter o plot con 'o')."""
    puntos = [len(c.get_offsets()) for c in ax.collections]
    puntos += [len(linea.get_xdata()) for linea in ax.get_lines()
               if linea.get_linestyle() in ("None", "", " ")
               and linea.get_marker() not in ("None", "", None)]
    return puntos


def _ej4(ns):
    conc_problema = obtener(ns, "conc_problema")
    ax = _ejes_de(ns, "fig_calibracion")
    if len(CONC_CALIBRACION) not in _puntos_graficados(ax):
        raise Incorrecto("No encuentro los 6 puntos experimentales. Dibújalos con "
                         "`ax.scatter()` o con `ax.plot(x, y, 'o')`.")
    rectas = [linea for linea in ax.get_lines()
              if linea.get_linestyle() not in ("None", "", " ")]
    if not rectas:
        raise Incorrecto("Falta la recta del ajuste lineal: dibújala con `ax.plot()`.")
    if ax.get_legend() is None:
        raise Incorrecto("Agrega una leyenda con `ax.legend()` para distinguir datos y ajuste.")
    pendiente, ordenada, _ = _regresion(CONC_CALIBRACION, ABS_CALIBRACION)
    comparar_numero("conc_problema", conc_problema,
                    (0.500 - ordenada) / pendiente, rel=5e-3)


ej4 = sesion.agregar(
    "ej4", "Curva de calibración", _ej4,
    pista="Obtén `pendiente` y `ordenada` con `linregress`. La recta es "
          "`pendiente * x + ordenada`; para la muestra problema despeja x = (A − b) / m.",
    solucion="""
ajuste = linregress(concentraciones, absorbancias)
x = np.array(concentraciones)

fig_calibracion, ax = plt.subplots(figsize=(6, 4))
ax.scatter(concentraciones, absorbancias, color="tab:blue", label="Datos experimentales")
ax.plot(x, ajuste.slope * x + ajuste.intercept, color="tab:red",
        label=f"A = {ajuste.slope:.4f}·c + {ajuste.intercept:.4f} (r² = {ajuste.rvalue**2:.4f})")
ax.set_xlabel("Concentración (mg/L)")
ax.set_ylabel("Absorbancia")
ax.set_title("Curva de calibración")
ax.legend()
plt.show()

conc_problema = (0.500 - ajuste.intercept) / ajuste.slope
print(f"Concentración de la muestra problema: {conc_problema:.2f} mg/L")
""")


# --- Ejercicio 5: regla de Lipinski --------------------------------------------

def _ej5(ns):
    df = obtener(ns, "df")
    lipinski = obtener(ns, "lipinski")
    esperado = df[(df["MolWt"] <= 500) & (df["MolLogP"] <= 5)
                  & (df["NumHDonors"] <= 5) & (df["NumHAcceptors"] <= 10)]
    if not hasattr(lipinski, "index"):
        raise Incorrecto("`lipinski` debe ser un DataFrame filtrado a partir de `df`.")
    if len(lipinski) != len(esperado) or not lipinski.index.equals(esperado.index):
        raise Incorrecto(f"`lipinski` tiene {len(lipinski)} filas, pero {len(esperado)} "
                         "moléculas cumplen la regla. Revisa que uses `<=` y que los "
                         "límites de donadores (5) y aceptores (10) no estén intercambiados.")
    comparar_numero("porcentaje_lipinski", obtener(ns, "porcentaje_lipinski"),
                    100 * len(esperado) / len(df), rel=5e-3)
    return f"{len(esperado)} de {len(df)} moléculas ({100 * len(esperado) / len(df):.1f} %) cumplen la regla."


ej5 = sesion.agregar(
    "ej5", "Regla de los 5 de Lipinski", _ej5,
    pista="Combina las cuatro condiciones con `&` y encierra cada una entre paréntesis: "
          '`df[(df["MolWt"] <= 500) & (...)]`.',
    solucion="""
lipinski = df[(df["MolWt"] <= 500)
              & (df["MolLogP"] <= 5)
              & (df["NumHDonors"] <= 5)
              & (df["NumHAcceptors"] <= 10)]

porcentaje_lipinski = 100 * len(lipinski) / len(df)
print(f"{len(lipinski)} moléculas ({porcentaje_lipinski:.1f} %) cumplen la regla de Lipinski")
""")


# --- Ejercicio 6: integrador ---------------------------------------------------

def _ej6(ns):
    df = obtener(ns, "df")
    r_logp = obtener(ns, "r_logp")
    ax = _ejes_de(ns, "fig_logp")
    if len(df) not in _puntos_graficados(ax):
        raise Incorrecto("La gráfica debe mostrar un punto por molécula del DataFrame: "
                         '`ax.scatter(df["MolLogP"], df["Solubility"])`.')
    comparar_numero("r_logp", r_logp,
                    df["MolLogP"].corr(df["Solubility"]), rel=1e-3)


ej6 = sesion.agregar(
    "ej6", "LogP contra solubilidad", _ej6,
    pista='El coeficiente de Pearson entre dos columnas se obtiene con '
          '`df["MolLogP"].corr(df["Solubility"])`. Usa `alpha=0.3` para ver mejor los puntos.',
    solucion="""
r_logp = df["MolLogP"].corr(df["Solubility"])

fig_logp, ax = plt.subplots(figsize=(6, 4))
ax.scatter(df["MolLogP"], df["Solubility"], s=5, alpha=0.3)
ax.set_xlabel("logP (octanol/agua)")
ax.set_ylabel("log S (mol/L)")
ax.set_title(f"Solubilidad acuosa contra lipofilicidad (r = {r_logp:.2f})")
plt.show()
""")


# --- Ejercicio 7: RDKit ----------------------------------------------------------

def _ej7(ns):
    df = obtener(ns, "df")
    if _tiene_espacios(obtener_funcion(ns, "tiene_benceno")):
        raise Pendiente("Completa la función `tiene_benceno`: sustituye los `____`.")
    n = obtener(ns, "n_benceno")
    if "tiene_benceno" not in df.columns:
        raise Incorrecto('Agrega la columna `df["tiene_benceno"]` aplicando tu función a '
                         'la columna `"Mols"`.')
    comparar_numero("n_benceno", n, int((df["tiene_benceno"] == True).sum()))  # noqa: E712
    from rdkit import Chem
    benceno = Chem.MolFromSmarts("c1ccccc1")
    muestra = df.sample(min(200, len(df)), random_state=0)
    for mol, marcado in zip(muestra["Mols"], muestra["tiene_benceno"]):
        esperado = None if mol is None else mol.HasSubstructMatch(benceno)
        if esperado is not None and bool(marcado) != esperado:
            raise Incorrecto("Algunas moléculas están mal clasificadas en "
                             '`df["tiene_benceno"]`. Usa `HasSubstructMatch` con el '
                             'patrón SMARTS aromático "c1ccccc1".')


ej7 = sesion.agregar(
    "ej7", "Búsqueda de subestructuras", _ej7,
    pista="Crea el patrón una sola vez con `Chem.MolFromSmarts(\"c1ccccc1\")` y, dentro de "
          "la función, devuelve `mol.HasSubstructMatch(patron)` (o `False` si `mol` es `None`).",
    solucion="""
patron_benceno = Chem.MolFromSmarts("c1ccccc1")

def tiene_benceno(mol):
    if mol is None:          # SMILES que RDKit no pudo interpretar
        return False
    return mol.HasSubstructMatch(patron_benceno)

df["tiene_benceno"] = df["Mols"].apply(tiene_benceno)
n_benceno = int(df["tiene_benceno"].sum())
print(f"{n_benceno} de {len(df)} moléculas contienen un anillo bencénico")
""")


__all__ = ["____", "progreso"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
