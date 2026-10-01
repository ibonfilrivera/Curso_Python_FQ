"""Ejercicios de la Sesión 3: SciPy, Matplotlib, Pandas, RDKit y el proyecto final."""

import math

import os

from .nucleo import (Incorrecto, Pendiente, Sesion, ____, _PorCompletar, _tiene_espacios,
                     comparar_numero, obtener, obtener_funcion)

sesion = Sesion("Sesión 3", "S3")
progreso = sesion.progreso
iniciar_registro = sesion.iniciar_registro

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
    comparar_numero("k", k, -pendiente, rel=5e-3, unidades="1/min")
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
mejor_orden = 0
for orden, ajuste in ajustes.items():
    print(f"Orden {orden}: r² = {ajuste.rvalue**2:.5f}")
    if ajuste.rvalue**2 > ajustes[mejor_orden].rvalue**2:
        mejor_orden = orden
k = -ajustes[1].slope
print(f"Mejor ajuste: orden {mejor_orden}, k = {k:.4f} min⁻¹")
""")


# --- Ejercicio 2: curva de calibración ----------------------------------------

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


def _ej2(ns):
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
                    (0.500 - ordenada) / pendiente, rel=5e-3, unidades="mg/L")


ej2 = sesion.agregar(
    "ej2", "Curva de calibración", _ej2,
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


# --- Ejercicio 3: ley de Lambert-Beer -----------------------------------------------

LIMITE_LINEAL = 1.0     # Absorbancia máxima del intervalo lineal
PASO_OPTICO = 1.00      # cm


def _estandares_lb(ns):
    datos = obtener(ns, "datos_lb")
    estandares = datos[datos["tipo"] == "estandar"]
    return datos, estandares.groupby("concentracion_mol_L")["absorbancia"].agg(
        promedio="mean", desviacion="std")


def _ajuste_lb(resumen):
    lineal = resumen[resumen["promedio"] <= LIMITE_LINEAL]
    return _regresion(list(lineal.index), list(lineal["promedio"]))


def _ej3a(ns):
    resumen = obtener(ns, "resumen")
    _, esperado = _estandares_lb(ns)
    if not hasattr(resumen, "columns"):
        raise Incorrecto("`resumen` debe ser un DataFrame creado con `groupby(...).agg(...)`.")
    faltan = {"promedio", "desviacion"} - set(resumen.columns)
    if faltan:
        raise Incorrecto(f"A `resumen` le faltan las columnas {sorted(faltan)}. Usa "
                         '`.agg(promedio="mean", desviacion="std")`.')
    if len(resumen) != len(esperado):
        raise Incorrecto(f"`resumen` tiene {len(resumen)} filas, pero hay {len(esperado)} "
                         "estándares distintos. ¿Filtraste solo las filas con "
                         '`tipo == "estandar"` y agrupaste por concentración?')
    import numpy as np
    if not np.allclose(resumen.index.astype(float), esperado.index, rtol=1e-9, atol=0):
        raise Incorrecto("El índice de `resumen` debe ser la concentración: agrupa por "
                         '`"concentracion_mol_L"`.')
    for columna in ("promedio", "desviacion"):
        if not np.allclose(resumen[columna], esperado[columna], atol=1e-9):
            raise Incorrecto(f"Los valores de la columna `{columna}` no coinciden con los "
                             "esperados. Revisa la función de agregación.")
    return f"{len(esperado)} estándares, cada uno con 3 réplicas."


ej3a = sesion.agregar(
    "ej3a", "Lambert-Beer: promedio de réplicas", _ej3a,
    pista='Primero filtra: `datos_lb[datos_lb["tipo"] == "estandar"]`. Después agrupa con '
          '`.groupby("concentracion_mol_L")["absorbancia"]` y resume con '
          '`.agg(promedio="mean", desviacion="std")`.',
    solucion="""
estandares = datos_lb[datos_lb["tipo"] == "estandar"]
resumen = estandares.groupby("concentracion_mol_L")["absorbancia"].agg(
    promedio="mean", desviacion="std")
resumen
""")


def _ej3b(ns):
    epsilon = obtener(ns, "epsilon")
    r2_lineal = obtener(ns, "r2_lineal")
    r2_todos = obtener(ns, "r2_todos")
    ax = _ejes_de(ns, "fig_lb")
    _, resumen = _estandares_lb(ns)
    todos = _regresion(list(resumen.index), list(resumen["promedio"]))
    pendiente, _, r2 = _ajuste_lb(resumen)
    comparar_numero("r2_todos", r2_todos, todos[2], rel=1e-4)
    comparar_numero("epsilon", epsilon, pendiente / PASO_OPTICO, rel=2e-3, unidades="L/(mol*cm)")
    comparar_numero("r2_lineal", r2_lineal, r2, rel=1e-4)
    if ax.get_legend() is None:
        raise Incorrecto("Agrega una leyenda con `ax.legend()` para distinguir los estándares "
                         "del ajuste.")
    return (f"ε ≈ {pendiente / PASO_OPTICO:.0f} L·mol⁻¹·cm⁻¹. Con todos los puntos, r² baja a "
            f"{todos[2]:.4f}: por encima de A ≈ 1 la respuesta deja de ser lineal.")


ej3b = sesion.agregar(
    "ej3b", "Lambert-Beer: absortividad molar", _ej3b,
    pista="Filtra `resumen` con `resumen[\"promedio\"] <= 1.0` y ajusta con `linregress` "
          "usando `lineal.index` como x. Como A = ε·b·c, la pendiente es ε·b; con b = 1.00 cm, "
          "ε = pendiente / b.",
    solucion="""
b = 1.00   # cm

ajuste_todos = linregress(resumen.index, resumen["promedio"])
r2_todos = ajuste_todos.rvalue**2

lineal = resumen[resumen["promedio"] <= 1.0]
ajuste_lb = linregress(lineal.index, lineal["promedio"])
r2_lineal = ajuste_lb.rvalue**2
epsilon = ajuste_lb.slope / b

fig_lb, ax = plt.subplots(figsize=(6, 4))
ax.errorbar(resumen.index * 1e3, resumen["promedio"], yerr=resumen["desviacion"],
            fmt="o", capsize=3, label="Estándares (promedio ± s)")
c = np.linspace(0, lineal.index.max(), 50)
ax.plot(c * 1e3, ajuste_lb.slope * c + ajuste_lb.intercept, color="tab:red",
        label=f"Ajuste en A ≤ 1: ε = {epsilon:.0f} L/(mol·cm)")
c_extra = np.linspace(lineal.index.max(), resumen.index.max(), 20)
ax.plot(c_extra * 1e3, ajuste_lb.slope * c_extra + ajuste_lb.intercept, color="tab:red",
        linestyle="--", alpha=0.5, label="Extrapolación de la recta")
ax.axhline(1.0, color="gray", linestyle=":", label="Límite del intervalo lineal")
ax.set_xlabel("Concentración de KMnO₄ (mmol/L)")
ax.set_ylabel("Absorbancia a 525 nm")
ax.legend()
plt.show()

print(f"Todos los puntos: r² = {r2_todos:.4f}")
print(f"Intervalo lineal: r² = {r2_lineal:.5f}, ε = {epsilon:.0f} L/(mol·cm)")
""")


def _ej3c(ns):
    datos, resumen = _estandares_lb(ns)
    conc = obtener(ns, "conc_problema_lb")
    pendiente, ordenada, _ = _ajuste_lb(resumen)
    a_problema = datos[datos["tipo"] == "problema"]["absorbancia"].mean()
    esperado = (a_problema - ordenada) / pendiente
    comparar_numero("conc_problema_lb", conc, esperado, rel=5e-3, unidades="mol/L")
    dentro = obtener(ns, "dentro_intervalo")
    lineal = resumen[resumen["promedio"] <= LIMITE_LINEAL]
    esperado_dentro = bool(lineal.index.min() <= esperado <= lineal.index.max())
    if type(dentro).__name__ not in ("bool", "bool_"):
        raise Incorrecto("`dentro_intervalo` debe ser `True` o `False`, resultado de una comparación.")
    if bool(dentro) != esperado_dentro:
        raise Incorrecto("`dentro_intervalo` no es correcto: compara la concentración con la "
                         "menor y la mayor de los estándares del intervalo lineal.")
    return (f"c = {esperado:.3e} mol/L; la muestra está dentro del intervalo calibrado, "
            "así que el resultado es confiable.")


ej3c = sesion.agregar(
    "ej3c", "Lambert-Beer: muestra problema", _ej3c,
    pista="Promedia las tres lecturas de la muestra problema y despeja c = (A − ordenada) / "
          "pendiente usando `ajuste_lb`. Para `dentro_intervalo`, compara c con "
          "`lineal.index.min()` y `lineal.index.max()`.",
    solucion="""
problema = datos_lb[datos_lb["tipo"] == "problema"]
a_problema = problema["absorbancia"].mean()

conc_problema_lb = (a_problema - ajuste_lb.intercept) / ajuste_lb.slope
dentro_intervalo = lineal.index.min() <= conc_problema_lb <= lineal.index.max()

print(f"A = {a_problema:.3f} → c = {conc_problema_lb:.3e} mol/L")
print(f"¿Dentro del intervalo calibrado? {dentro_intervalo}")
""")


# --- Ejercicio 4: regla de Lipinski --------------------------------------------

def _ej4(ns):
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


ej4 = sesion.agregar(
    "ej4", "Regla de los 5 de Lipinski", _ej4,
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


# --- Ejercicio 5: integrador ---------------------------------------------------

def _ej5(ns):
    df = obtener(ns, "df")
    r_logp = obtener(ns, "r_logp")
    ax = _ejes_de(ns, "fig_logp")
    if len(df) not in _puntos_graficados(ax):
        raise Incorrecto("La gráfica debe mostrar un punto por molécula del DataFrame: "
                         '`ax.scatter(df["MolLogP"], df["Solubility"])`.')
    comparar_numero("r_logp", r_logp,
                    df["MolLogP"].corr(df["Solubility"]), rel=1e-3)


ej5 = sesion.agregar(
    "ej5", "LogP contra solubilidad", _ej5,
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


# --- Ejercicio 6: RDKit ----------------------------------------------------------

def _ej6(ns):
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


ej6 = sesion.agregar(
    "ej6", "Búsqueda de subestructuras", _ej6,
    pista="`df[\"Mols\"].apply(tiene_benceno)` aplica la función a cada molécula. Para contar, "
          "suma la columna: `int(df[\"tiene_benceno\"].sum())`.",
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


# --- Proyecto final (opcional): curva de valoración potenciométrica ---------------------

PKA_LITERATURA = 8.5              # pKa aparente de F-PEG-NH2 reportado en la Tabla 1 del artículo

# Tabla 1 del artículo: archivo de cada nanopartícula y sus pKa aparentes (uno por transición)
TABLA_1 = {
    "F-PEG-NH2": ("Amine new.csv", [8.5]),
    "F-PEG-Gln": ("Gln.csv", [6.9]),
    "F-PEG-GA": ("+-.csv", [6.3, 8.3]),
    "F-PEG-SA": ("SucA.csv", [8.0]),
}


def _titulacion(ns):
    """DataFrame del estudiante con columnas V_uL y pH, ya revisado."""
    titulacion = obtener(ns, "titulacion")
    if not hasattr(titulacion, "columns") or not {"V_uL", "pH"} <= set(titulacion.columns):
        raise Incorrecto('`titulacion` debe ser un DataFrame con las columnas "V_uL" y "pH".')
    return titulacion


def _derivadas(titulacion):
    """Primera y segunda derivada por diferencias finitas, como las calcula Origin."""
    import numpy as np
    V = titulacion["V_uL"].to_numpy(float)
    pH = titulacion["pH"].to_numpy(float)
    primera = np.gradient(pH, V)
    segunda = np.gradient(primera, V)
    return V, pH, primera, segunda


def _cruce_segunda(V, segunda, j):
    """Volumen donde la segunda derivada cruza por cero junto al máximo de la primera."""
    k = j - 1 if segunda[j] < 0 else j
    return V[k] - segunda[k] * (V[k + 1] - V[k]) / (segunda[k + 1] - segunda[k])


def _pf1(ns):
    crudo = obtener(ns, "crudo")
    titulacion = _titulacion(ns)
    import numpy as np
    if titulacion[["V_uL", "pH"]].isna().any().any():
        raise Incorrecto("`titulacion` todavía tiene valores nulos; usa `.dropna()`.")
    if not titulacion["V_uL"].is_monotonic_increasing:
        raise Incorrecto('Ordena `titulacion` por volumen con `.sort_values("V_uL")`.')
    esperado = crudo.iloc[:, :2].dropna().astype(float)
    if len(titulacion) != len(esperado):
        raise Incorrecto(f"`titulacion` tiene {len(titulacion)} filas y se esperaban "
                         f"{len(esperado)}. Usa solo las dos primeras columnas: las últimas "
                         "repiten los mismos datos.")
    if not np.allclose(np.sort(titulacion["pH"]), np.sort(esperado.iloc[:, 1])):
        raise Incorrecto("Los valores de pH no coinciden con la segunda columna del archivo.")
    return f"{len(titulacion)} lecturas, de {titulacion['V_uL'].max():.0f} µL de NaOH en total."


pf1 = sesion.agregar(
    "pf1", "(Proyecto) Ingesta y limpieza", _pf1,
    pista="`crudo.iloc[:, :2]` toma las dos primeras columnas (volumen y pH). Renómbralas, "
          "quita los nulos con `.dropna()`, convierte a `float` y ordena por volumen.",
    solucion="""
titulacion = crudo.iloc[:, :2].copy()
titulacion.columns = ["V_uL", "pH"]
titulacion = (titulacion.dropna()
              .astype(float)
              .sort_values("V_uL")
              .reset_index(drop=True))

print(f"{len(titulacion)} lecturas entre {titulacion['V_uL'].min():.0f} y "
      f"{titulacion['V_uL'].max():.0f} µL")
titulacion.head()
""")


def _pf2(ns):
    titulacion = _titulacion(ns)
    import numpy as np
    V, pH, primera, segunda = _derivadas(titulacion)
    for nombre, esperado in (("primera", primera), ("segunda", segunda)):
        obtenido = obtener(ns, nombre)
        if np.shape(obtenido) != np.shape(esperado) or not np.allclose(obtenido, esperado):
            raise Incorrecto(f"`{nombre}` no coincide con la derivada esperada. Usa "
                             "`np.gradient(y, V)` con el volumen como segundo argumento.")
    j = int(np.argmax(primera))
    comparar_numero("V_eq_d1", obtener(ns, "V_eq_d1"), V[j], unidades="uL")
    comparar_numero("pKa_aparente", obtener(ns, "pKa_aparente"), pH[j], rel=1e-3)
    v_cruce = _cruce_segunda(V, segunda, j)
    comparar_numero("V_eq_d2", obtener(ns, "V_eq_d2"), v_cruce, rel=1e-3, unidades="uL")
    comparar_numero("pH_eq_d2", obtener(ns, "pH_eq_d2"), float(np.interp(v_cruce, V, pH)),
                    rel=1e-3)
    return (f"Máximo de dpH/dV en {V[j]:.0f} µL (pH {pH[j]:.2f}); la segunda derivada cruza por "
            f"cero en {v_cruce:.1f} µL (pH {np.interp(v_cruce, V, pH):.2f}). El artículo "
            f"reporta pKa aparente = {PKA_LITERATURA}.")


pf2 = sesion.agregar(
    "pf2", "(Proyecto) Primera y segunda derivada", _pf2,
    pista="`np.gradient(pH, V)` calcula dpH/dV punto a punto y `np.gradient(primera, V)` la "
          "segunda derivada. El índice del máximo es `np.argmax(primera)`. La segunda derivada "
          "cambia de signo entre dos puntos vecinos: interpola linealmente dónde vale cero.",
    solucion="""
V = titulacion["V_uL"].to_numpy()
pH = titulacion["pH"].to_numpy()

primera = np.gradient(pH, V)          # dpH/dV (µL⁻¹)
segunda = np.gradient(primera, V)     # d²pH/dV² (µL⁻²)

# Método de la primera derivada: el punto de inflexión es su máximo
j = np.argmax(primera)
V_eq_d1 = V[j]
pKa_aparente = pH[j]

# Método de la segunda derivada: el punto de inflexión es donde cruza por cero
k = j - 1 if segunda[j] < 0 else j
V_eq_d2 = V[k] - segunda[k] * (V[k + 1] - V[k]) / (segunda[k + 1] - segunda[k])
pH_eq_d2 = np.interp(V_eq_d2, V, pH)

print(f"Primera derivada: V = {V_eq_d1:.0f} µL, pH = {pKa_aparente:.2f}")
print(f"Segunda derivada: V = {V_eq_d2:.1f} µL, pH = {pH_eq_d2:.2f}")
""")


def _pf3(ns):
    titulacion = _titulacion(ns)
    spline = obtener(ns, "spline")
    V_fina = obtener(ns, "V_fina")
    import numpy as np
    if not hasattr(spline, "derivative"):
        raise Incorrecto("`spline` debe ser un `UnivariateSpline` de `scipy.interpolate`.")
    if len(V_fina) < 500:
        raise Incorrecto("Usa una malla fina de al menos 500 volúmenes con `np.linspace`.")
    residuo = np.sqrt(np.mean((spline(titulacion["V_uL"]) - titulacion["pH"]) ** 2))
    if residuo > 0.1:
        raise Incorrecto(f"El spline se aleja en promedio {residuo:.3f} unidades de pH de los "
                         "datos: el suavizado es excesivo. Reduce el parámetro `s`.")
    v_eq = V_fina[int(np.argmax(spline.derivative()(V_fina)))]
    comparar_numero("V_eq_spline", obtener(ns, "V_eq_spline"), v_eq, rel=1e-3, unidades="uL")
    comparar_numero("pH_eq_spline", obtener(ns, "pH_eq_spline"), float(spline(v_eq)), rel=1e-3)
    return (f"Con el spline, la inflexión está en {v_eq:.0f} µL y pH {float(spline(v_eq)):.2f}. "
            "Compara con las diferencias finitas: el salto es tan abrupto que el pH en la "
            "inflexión depende del método.")


pf3 = sesion.agregar(
    "pf3", "(Proyecto) Suavizado con spline", _pf3,
    pista="`UnivariateSpline(V, pH, k=3, s=0.05)` ajusta un spline cúbico. Evalúa su derivada "
          "(`spline.derivative()`) en `V_fina` y busca el máximo con `np.argmax`.",
    solucion="""
from scipy.interpolate import UnivariateSpline

spline = UnivariateSpline(V, pH, k=3, s=0.05)
V_fina = np.linspace(V.min(), V.max(), 5000)
pH_suave = spline(V_fina)
primera_suave = spline.derivative()(V_fina)

V_eq_spline = V_fina[np.argmax(primera_suave)]
pH_eq_spline = float(spline(V_eq_spline))
print(f"Spline: V = {V_eq_spline:.0f} µL, pH = {pH_eq_spline:.2f}")
""")


def _inflexiones_referencia(V, pH, n):
    """Los n máximos más altos de dpH/dV, ordenados por volumen: [(V_eq, pH), ...]."""
    import numpy as np
    from scipy.signal import find_peaks
    primera = np.gradient(pH, V)
    picos, _ = find_peaks(primera)
    mayores = sorted(picos[np.argsort(-primera[picos], kind="stable")[:n]])
    return [(float(V[i]), float(pH[i])) for i in mayores]


def _pf4(ns):
    leer_origin = obtener_funcion(ns, "leer_origin")
    inflexiones = obtener_funcion(ns, "inflexiones")
    tabla = obtener(ns, "tabla_pka")
    import numpy as np
    esperado = []
    for nombre, (archivo, pkas) in TABLA_1.items():
        datos = leer_origin(archivo).iloc[:, :2].dropna().astype(float)
        datos = datos.sort_values(datos.columns[0]).drop_duplicates(datos.columns[0])
        V, pH = datos.iloc[:, 0].to_numpy(), datos.iloc[:, 1].to_numpy()
        referencia = _inflexiones_referencia(V, pH, len(pkas))
        try:
            obtenido = inflexiones(V, pH, len(pkas))
        except Exception as e:
            raise Incorrecto(f"`inflexiones(V, pH, {len(pkas)})` falló con los datos de {nombre}: "
                             f"`{type(e).__name__}: {e}`") from None
        if obtenido is None:
            raise Incorrecto("`inflexiones` devolvió `None`. ¿Olvidaste usar `return`?")
        if len(obtenido) != len(referencia) or not np.allclose(
                np.asarray(obtenido, dtype=float), np.asarray(referencia), rtol=1e-6):
            devuelto = [(round(float(v)), round(float(p), 2)) for v, p in obtenido]
            raise Incorrecto(f"Para {nombre}, `inflexiones` devolvió {devuelto}, pero se esperaba "
                             f"{[(round(v), round(p, 2)) for v, p in referencia]}. Toma los "
                             "máximos **más altos** de dpH/dV (en un empate, el de menor volumen) y "
                             "ordénalos por volumen.")
        esperado += [(nombre, p, articulo) for (_, p), articulo in zip(referencia, pkas)]
    if not hasattr(tabla, "columns") or not {"nanoparticula", "pKa_aparente",
                                             "pKa_articulo"} <= set(tabla.columns):
        raise Incorrecto('`tabla_pka` debe ser un DataFrame con las columnas "nanoparticula", '
                         '"V_eq", "pKa_aparente" y "pKa_articulo".')
    if len(tabla) != len(esperado):
        raise Incorrecto(f"`tabla_pka` tiene {len(tabla)} filas y se esperaban {len(esperado)}: "
                         "una por transición (F-PEG-GA tiene dos).")
    filas = sorted(zip(tabla["nanoparticula"], tabla["pKa_aparente"], tabla["pKa_articulo"]))
    for (nombre, p, articulo), (n2, p2, a2) in zip(sorted(esperado), filas):
        if nombre != n2 or abs(p - p2) > 1e-6 or abs(articulo - a2) > 1e-6:
            raise Incorrecto(f"La fila de {nombre} no coincide: se esperaba pKa aparente "
                             f"{p:.2f} y {articulo} en el artículo.")
    diferencia = max(abs(p - a) for _, p, a in esperado)
    return (f"Las {len(esperado)} transiciones coinciden con la Tabla 1 con una diferencia "
            f"máxima de {diferencia:.2f} unidades de pH.")


pf4 = sesion.agregar(
    "pf4", "(Proyecto) Comparación con la Tabla 1", _pf4,
    pista="El número de transiciones de cada nanopartícula es `len(pkas_articulo)`: F-PEG-GA tiene "
          "dos y las demás, una.",
    solucion="""
from scipy.signal import find_peaks

def inflexiones(V, pH, n):
    \"\"\"Volumen y pH de los n máximos más altos de dpH/dV, ordenados por volumen.\"\"\"
    derivada = np.gradient(pH, V)
    picos, _ = find_peaks(derivada)
    mayores = sorted(picos[np.argsort(-derivada[picos], kind="stable")[:n]])
    return [(V[i], pH[i]) for i in mayores]

tabla_1 = {                      # nanopartícula: (archivo, pKa aparentes de la Tabla 1)
    "F-PEG-NH2": ("Amine new.csv", [8.5]),
    "F-PEG-Gln": ("Gln.csv", [6.9]),
    "F-PEG-GA": ("+-.csv", [6.3, 8.3]),
    "F-PEG-SA": ("SucA.csv", [8.0]),
}

filas = []
curvas = {}
for nanoparticula, (archivo, pkas_articulo) in tabla_1.items():
    datos = leer_origin(archivo).iloc[:, :2].dropna().astype(float)
    datos.columns = ["V", "pH"]
    datos = datos.sort_values("V").drop_duplicates("V")
    curvas[nanoparticula] = datos
    encontradas = inflexiones(datos["V"].to_numpy(), datos["pH"].to_numpy(), len(pkas_articulo))
    for (v_eq, pka), pka_articulo in zip(encontradas, pkas_articulo):
        filas.append({"nanoparticula": nanoparticula, "V_eq": v_eq,
                      "pKa_aparente": pka, "pKa_articulo": pka_articulo})

tabla_pka = pd.DataFrame(filas)
tabla_pka["diferencia"] = tabla_pka["pKa_aparente"] - tabla_pka["pKa_articulo"]
tabla_pka.round(2)
""")


def _pf5(ns):
    resultados = obtener(ns, "resultados")
    figura = obtener(ns, "fig_proyecto")
    from matplotlib.figure import Figure
    if not isinstance(figura, Figure) or len(figura.axes) < 3:
        raise Incorrecto("`fig_proyecto` debe ser una figura con al menos 3 paneles: "
                         "`fig_proyecto, ejes = plt.subplots(1, 3)`.")
    sin_etiquetas = [i + 1 for i, ax in enumerate(figura.axes[:3])
                     if not ax.get_xlabel().strip() or not ax.get_ylabel().strip()]
    if sin_etiquetas:
        raise Incorrecto(f"Al panel {sin_etiquetas[0]} le faltan etiquetas en los ejes.")
    variables = {"V_eq_uL": "V_eq_d1", "pKa_aparente": "pKa_aparente",
                 "pH_eq_d2": "pH_eq_d2", "pH_eq_spline": "pH_eq_spline"}
    claves = set(variables) | {"pKa_articulo", "comparacion"}
    if not isinstance(resultados, dict) or not claves <= set(resultados):
        raise Incorrecto(f"`resultados` debe ser un diccionario con las claves {sorted(claves)}.")
    if any(isinstance(valor, _PorCompletar) for valor in resultados.values()):
        raise Pendiente("Sustituye los `____` del diccionario `resultados`.")
    import json
    import os
    if not os.path.exists("resultados_titulacion.json"):
        raise Incorrecto("Guarda `resultados` en el archivo `resultados_titulacion.json` con "
                         "`json.dump`.")
    try:
        with open("resultados_titulacion.json", encoding="utf-8") as archivo:
            guardado = json.load(archivo)
    except ValueError:
        raise Incorrecto("`resultados_titulacion.json` está incompleto o dañado: vuelve a "
                         "ejecutar la celda que lo guarda.") from None
    for clave, variable in variables.items():
        comparar_numero(f'resultados["{clave}"]', guardado.get(clave),
                        float(obtener(ns, variable)), rel=1e-6)
    comparar_numero('resultados["pKa_articulo"]', guardado.get("pKa_articulo"), PKA_LITERATURA)
    if len(guardado.get("comparacion", [])) != sum(len(p) for _, p in TABLA_1.values()):
        raise Incorrecto('`resultados["comparacion"]` debe contener las filas de `tabla_pka`: '
                         'usa `tabla_pka.to_dict("records")`.')
    return "Proyecto completo: figura del reporte y resultados guardados en JSON."


pf5 = sesion.agregar(
    "pf5", "(Proyecto) Reporte final", _pf5,
    pista="Crea tres paneles con `plt.subplots(1, 3)`: curva de F-PEG-NH2 con la inflexión, sus "
          "derivadas con V_eq marcado (`ax.axvline`) y la comparación de `tabla_pka` con el "
          "artículo. Guarda el diccionario con `json.dump(resultados, archivo)`.",
    solucion="""
import json

fig_proyecto, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.3))

ax1.plot(V, pH, "o", ms=3, color="gray", label="Experimental")
ax1.plot(V_fina, pH_suave, color="tab:blue", label="Spline cúbico")
ax1.axhline(8.5, color="tab:green", linestyle=":", label="pKa aparente del artículo (8.5)")
ax1.axvline(V_eq_d1, color="tab:red", linestyle="--", label=f"V_eq = {V_eq_d1:.0f} µL")
ax1.set_xlabel("V de NaOH (µL)")
ax1.set_ylabel("pH")
ax1.set_title("Curva de valoración de F-PEG-NH2")
ax1.legend(fontsize=8)

ax2.plot(V, primera, color="tab:purple", label="dpH/dV")
ax2.axvline(V_eq_d1, color="tab:red", linestyle="--")
ax2.set_xlabel("V de NaOH (µL)")
ax2.set_ylabel("dpH/dV (µL⁻¹)")
ax2.set_title("Primera y segunda derivada")
ax2b = ax2.twinx()                    # Segundo eje y para la segunda derivada
ax2b.plot(V, segunda, color="tab:orange", alpha=0.7, label="d²pH/dV²")
ax2b.axhline(0, color="gray", linewidth=0.8)
ax2b.set_ylabel("d²pH/dV² (µL⁻²)")
ax2.legend(loc="upper left", fontsize=8)
ax2b.legend(loc="upper right", fontsize=8)

ax3.plot([6, 9], [6, 9], color="gray", linestyle=":", label="Coincidencia perfecta")
for nanoparticula, grupo in tabla_pka.groupby("nanoparticula"):
    ax3.plot(grupo["pKa_articulo"], grupo["pKa_aparente"], "o", ms=8, label=nanoparticula)
ax3.set_xlabel("pKa aparente del artículo (Tabla 1)")
ax3.set_ylabel("pKa aparente calculado")
ax3.set_title("Comparación con la literatura")
ax3.legend(fontsize=8)

fig_proyecto.tight_layout()
plt.show()

resultados = {
    "V_eq_uL": float(V_eq_d1),
    "pKa_aparente": float(pKa_aparente),
    "pH_eq_d2": float(pH_eq_d2),
    "pH_eq_spline": float(pH_eq_spline),
    "pKa_articulo": 8.5,
    "comparacion": tabla_pka.to_dict("records"),
}
with open("resultados_titulacion.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, indent=2, ensure_ascii=False)
print(json.dumps(resultados, indent=2, ensure_ascii=False))
""")

# Ejercicios adicionales del equipo docente (contenido_extra/sesion3/)
globals().update(sesion.cargar_adicionales(
    os.path.join(os.path.dirname(__file__), "adicionales_sesion3.json")))

__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
