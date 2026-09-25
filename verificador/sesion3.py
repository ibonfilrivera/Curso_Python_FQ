"""Ejercicios de la Sesión 3: SciPy, NumPy, Matplotlib, Pandas y RDKit."""

import math

from .nucleo import (Incorrecto, Pendiente, Sesion, ____, _tiene_espacios, comparar_numero,
                     obtener, obtener_funcion)

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
                    (0.500 - ordenada) / pendiente, rel=5e-3)


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
    comparar_numero("epsilon", epsilon, pendiente / PASO_OPTICO, rel=2e-3)
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
    comparar_numero("conc_problema_lb", conc, esperado, rel=5e-3)
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


__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
