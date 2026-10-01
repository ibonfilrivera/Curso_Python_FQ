"""Ejercicios de la Sesión 2: estructuras de datos, condicionales y ciclos; funciones y clases como temas extra."""

import os

from .nucleo import (Incorrecto, Pendiente, Sesion, ____, comparar_numero, es_numero, lista_no_vacia,
                     normalizar_texto, obtener, obtener_funcion, probar_funcion)

sesion = Sesion("Sesión 2", "S2")
progreso = sesion.progreso
iniciar_registro = sesion.iniciar_registro

MM_NACL = 58.44   # g/mol
MM_AGUA = 18.015      # g/mol
R_ATM = 0.0821         # atm·L/(mol·K)


# --- Ejercicio 1: listas -----------------------------------------------------

def _lista_de_asignaturas(ns):
    asignaturas = obtener(ns, "mis_asignaturas")
    if not isinstance(asignaturas, list):
        raise Incorrecto("`mis_asignaturas` debe ser una lista, definida con corchetes `[]`.")
    if len(asignaturas) < 3:
        raise Incorrecto("Incluye al menos tres asignaturas en `mis_asignaturas`.")
    if not all(isinstance(a, str) for a in asignaturas):
        raise Incorrecto("Todos los elementos de `mis_asignaturas` deben ser textos (`str`).")
    return asignaturas


def _ej1a(ns):
    asignaturas = _lista_de_asignaturas(ns)
    if obtener(ns, "num_asignaturas") != len(asignaturas):
        raise Incorrecto("`num_asignaturas` no coincide con el tamaño de tu lista. Usa `len()`.")
    if obtener(ns, "segundo_elemento") != asignaturas[1]:
        raise Incorrecto("`segundo_elemento` no es el segundo elemento de la lista. "
                         "Recuerda que los índices empiezan en 0.")
    if obtener(ns, "penultimo_elemento") != asignaturas[-2]:
        raise Incorrecto("`penultimo_elemento` no es el penúltimo elemento. "
                         "Los índices negativos cuentan desde el final.")
    if "Curso de Python" in asignaturas:
        return "Nota: tu lista ya incluye el Curso de Python; continúa con el ejercicio 1b."


ej1a = sesion.agregar(
    "ej1a", "Tamaño e índices de una lista", _ej1a,
    pista="`len(lista)` da el tamaño, `lista[1]` el segundo elemento y `lista[-2]` "
          "el penúltimo.",
    solucion="""
mis_asignaturas = ["Álgebra", "Cálculo", "Física", "Química", "Ciencia y Sociedad"]

num_asignaturas = len(mis_asignaturas)
segundo_elemento = mis_asignaturas[1]
penultimo_elemento = mis_asignaturas[-2]
print(num_asignaturas, segundo_elemento, penultimo_elemento)
""")


def _ej1b(ns):
    asignaturas = _lista_de_asignaturas(ns)
    if "Curso de Python" not in asignaturas:
        raise Incorrecto('Agrega el texto "Curso de Python" a la lista con `.append()`.')
    if len(asignaturas) != obtener(ns, "num_asignaturas"):
        raise Incorrecto("La lista debería tener el mismo tamaño que al inicio: eliminaste "
                         "una asignatura y agregaste otra. ¿Ejecutaste la celda más de una vez? "
                         "Vuelve a ejecutar la celda del ejercicio 1a y después esta.")


ej1b = sesion.agregar(
    "ej1b", "Modificar una lista", _ej1b,
    pista='Usa `mis_asignaturas.remove("Nombre exacto")` y después '
          '`mis_asignaturas.append("Curso de Python")`.',
    solucion="""
mis_asignaturas.remove("Ciencia y Sociedad")
mis_asignaturas.append("Curso de Python")
print(mis_asignaturas)
""")


# --- Ejercicio 2: diccionarios -----------------------------------------------

def _ej2a(ns):
    comparar_numero("masa_molar_hno3", obtener(ns, "masa_molar_hno3"), 1.0 + 14.0 + 3 * 16.0, unidades="g/mol")


ej2a = sesion.agregar(
    "ej2a", "Masa molar del HNO₃", _ej2a,
    pista='Accede a cada masa con `masas_molares["oxígeno"]` y multiplica por el '
          'número de átomos de cada elemento.',
    solucion="""
masa_molar_hno3 = (masas_molares["hidrógeno"]
                   + masas_molares["nitrógeno"]
                   + 3 * masas_molares["oxígeno"])
print(f"M(HNO₃) = {masa_molar_hno3} g/mol")
""")


def _ej2b(ns):
    masa_fe2o3 = obtener(ns, "masa_molar_fe2o3")
    masas = obtener(ns, "masas_molares")
    if "hierro" not in masas:
        raise Incorrecto('Agrega la clave "hierro" al diccionario `masas_molares`.')
    comparar_numero('masas_molares["hierro"]', masas["hierro"], 55.85, rel=2e-3)
    comparar_numero("masa_molar_fe2o3", masa_fe2o3, 2 * masas["hierro"] + 3 * 16.0, unidades="g/mol")


ej2b = sesion.agregar(
    "ej2b", "Masa molar del Fe₂O₃", _ej2b,
    pista='Agrega un par clave-valor con `masas_molares["hierro"] = 55.85`. El óxido de '
          'hierro(III) es Fe₂O₃.',
    solucion="""
masas_molares["hierro"] = 55.85
masa_molar_fe2o3 = 2 * masas_molares["hierro"] + 3 * masas_molares["oxígeno"]
print(f"M(Fe₂O₃) = {masa_molar_fe2o3:.2f} g/mol")
""")


# --- Ejercicio 3: condicionales --------------------------------------------------

def _mismo_enlace(obtenido, esperado):
    if not isinstance(obtenido, str):
        return False
    texto = normalizar_texto(obtenido)
    if texto.startswith("enlace "):
        texto = texto[len("enlace "):]
    return texto == normalizar_texto(esperado)


def _tipo_enlace(delta_chi):
    if delta_chi < 0.5:
        return "covalente no polar"
    return "covalente polar" if delta_chi < 1.7 else "iónico"


def _ej3(ns):
    delta_chi = obtener(ns, "delta_chi")
    if not es_numero(delta_chi):
        raise Incorrecto("`delta_chi` debe ser un número: la diferencia de electronegatividades.")
    tipo = obtener(ns, "tipo_enlace")
    esperado = _tipo_enlace(float(delta_chi))
    if not isinstance(tipo, str) or not _mismo_enlace(tipo, esperado):
        raise Incorrecto(f"Con Δχ = {float(delta_chi):.2f}, `tipo_enlace` vale {tipo!r}, pero el "
                         f"enlace es {esperado!r}. Revisa las condiciones y sus límites "
                         "(0.5 ya es covalente polar y 1.7 ya es iónico).")
    return (f"Correcto para Δχ = {float(delta_chi):.2f} ({esperado}). Cambia los átomos, por "
            "ejemplo H y Cl o C y H, y vuelve a verificar.")


ej3 = sesion.agregar(
    "ej3", "Clasificación de enlaces", _ej3,
    pista="Usa `if`, `elif` y `else` para asignar el texto a `tipo_enlace`. Cuida los límites: "
          "0.5 ya es *covalente polar* y 1.7 ya es *iónico*.",
    solucion="""
delta_chi = abs(chi_Na - chi_Cl)

if delta_chi < 0.5:
    tipo_enlace = "covalente no polar"
elif delta_chi < 1.7:
    tipo_enlace = "covalente polar"
else:
    tipo_enlace = "iónico"

print(f"Δχ = {delta_chi:.2f} → enlace {tipo_enlace}")
""")


# --- Ejercicio 4: gas ideal ---------------------------------------------------------

def _ej4(ns):
    n = 50.0 / MM_AGUA
    comparar_numero("n_agua", obtener(ns, "n_agua"), n, rel=5e-3, unidades="mol")
    comparar_numero("T1", obtener(ns, "T1"), 3.0 * 20.0 / (n * R_ATM), rel=5e-3, unidades="K")
    comparar_numero("T2", obtener(ns, "T2"), 6.3 * 1.2 / (n * R_ATM), rel=5e-3, unidades="K")


ej4 = sesion.agregar(
    "ej4", "Temperatura de un gas ideal", _ej4,
    pista="Despeja T de PV = nRT: T = PV / (nR). Calcula primero `n_agua` a partir de 50.0 g de "
          "agua (M ≈ 18.015 g/mol).",
    solucion="""
m_agua = 50.0      # g
MM_agua = 18.015   # g/mol
n_agua = m_agua / MM_agua
R = 0.0821         # atm·L/(mol·K)

T1 = 3.0 * 20.0 / (n_agua * R)     # P = 3.0 atm, V = 20.0 L
T2 = 6.3 * 1.2 / (n_agua * R)      # P = 6.3 atm, V = 1.2 L
print(f"T1 = {T1:.2f} K, T2 = {T2:.2f} K")
""")


# --- Ejercicio 5: for y while ------------------------------------------------

def _ej5(ns):
    ahorros = lista_no_vacia("ahorros", obtener(ns, "ahorros"), "completa el ciclo `for`.")
    if len(ahorros) != 3:
        raise Incorrecto("`ahorros` debe ser una lista con tres valores "
                         "(10, 20 y 30 meses). Usa `.append()` dentro del `for`.")
    if [float(a) for a in ahorros] != [3000.0, 6000.0, 9000.0]:
        raise Incorrecto(f"`ahorros` vale {ahorros}; revisa la multiplicación "
                         "ahorro mensual × meses.")
    meses = obtener(ns, "meses_necesarios")
    if meses == 23:
        raise Incorrecto("Con 23 meses se ahorran $6,900, que no alcanzan. Revisa la "
                         "condición de tu `while`.")
    comparar_numero("meses_necesarios", meses, 24)


ej5 = sesion.agregar(
    "ej5", "Ahorro para un celular", _ej5,
    pista="Para el `while`, repite mientras `ahorro_total < precio_celular`, sumando "
          "$300 y un mes en cada vuelta.",
    solucion="""
precio_celular = 7000
ahorro_mensual = 300

ahorros = []
for mes in [10, 20, 30]:
    ahorros.append(ahorro_mensual * mes)
print(ahorros)

ahorro_total = 0
meses_necesarios = 0
while ahorro_total < precio_celular:
    ahorro_total += ahorro_mensual
    meses_necesarios += 1
print(f"Se necesitan {meses_necesarios} meses.")
""")


# --- Ejercicio 6: muestras peligrosas ----------------------------------------

def _ej6(ns):
    mediciones = obtener(ns, "mediciones")
    peligrosas = [i for i, c in enumerate(mediciones) if 50 < c <= 100]
    criticas = [i for i, c in enumerate(mediciones) if c > 100]
    if not obtener(ns, "indices_peligrosas") and not obtener(ns, "indices_criticas"):
        lista_no_vacia("indices_peligrosas", [], "completa el `if` dentro del ciclo.")
    for nombre, esperado in (("indices_peligrosas", peligrosas),
                             ("indices_criticas", criticas)):
        obtenido = obtener(ns, nombre)
        if not isinstance(obtenido, list):
            raise Incorrecto(f"`{nombre}` debe ser una lista de índices.")
        if obtenido == [mediciones[i] for i in esperado]:
            raise Incorrecto(f"`{nombre}` contiene las concentraciones; se piden los "
                             "índices (posiciones) de las muestras.")
        if obtenido != esperado:
            raise Incorrecto(f"`{nombre}` tiene {len(obtenido)} elementos, pero hay "
                             f"{len(esperado)} muestras en esa categoría. Revisa las "
                             "condiciones (> 50 y ≤ 100 para peligrosas; > 100 para críticas).")
    return f"Hay {len(peligrosas)} muestras peligrosas y {len(criticas)} críticas."


ej6 = sesion.agregar(
    "ej6", "Detección de muestras peligrosas", _ej6,
    pista="`enumerate(mediciones)` te da, en cada vuelta, el índice y el valor. "
          "Una muestra es peligrosa si `50 < c <= 100` y crítica si `c > 100`.",
    solucion="""
indices_peligrosas = []
indices_criticas = []

for i, concentracion in enumerate(mediciones):
    if 50 < concentracion <= 100:
        indices_peligrosas.append(i)
    elif concentracion > 100:
        indices_criticas.append(i)

print(f"Peligrosas: {len(indices_peligrosas)} → {indices_peligrosas}")
print(f"Críticas: {len(indices_criticas)} → {indices_criticas}")
""")


# --- Autoevaluación -----------------------------------------------------------

def _fibonacci(n):
    serie = [0, 1][:n]
    while len(serie) < n:
        serie.append(serie[-1] + serie[-2])
    return serie


def _probar_fibonacci(ns, nombre):
    funcion = obtener_funcion(ns, nombre)
    casos = [((n,), {}, _fibonacci(n)) for n in (10, 2, 1, 15)]
    probar_funcion(nombre, funcion, casos, comparar=lambda o, e: list(o) == e)


def _auto1(ns):
    serie = lista_no_vacia("serie", obtener(ns, "serie"), "completa el ciclo `for`.")
    if serie == [0, 1]:
        raise Pendiente("`serie` todavía es `[0, 1]`: completa el ciclo `for`.")
    n = obtener(ns, "n")
    if serie != _fibonacci(int(n)):
        raise Incorrecto(f"`serie` tiene {len(serie)} elementos: {serie[:6]}… Debe tener los "
                         f"primeros {n} números de Fibonacci, empezando con 0 y 1.")
    return f"Los primeros {n} números de Fibonacci: {serie}."


auto1 = sesion.agregar(
    "auto1", "Fibonacci con for", _auto1,
    pista="Empieza con `serie = [0, 1]` y repite `n - 2` veces: agrega `serie[-1] + serie[-2]`.",
    solucion="""
n = 10
serie = [0, 1]
for _ in range(n - 2):
    serie.append(serie[-1] + serie[-2])
print(serie)
""")


def _auto2(ns):
    serie = lista_no_vacia("serie_while", obtener(ns, "serie_while"),
                           "completa el ciclo `while`.")
    if serie == [0, 1]:
        raise Pendiente("`serie_while` todavía es `[0, 1]`: completa el ciclo `while`.")
    if serie != _fibonacci(15):
        raise Incorrecto(f"`serie_while` tiene {len(serie)} elementos; debe tener los primeros 15 "
                         "números de Fibonacci. ¿Usaste `len(serie_while) < 15`?")


auto2 = sesion.agregar(
    "auto2", "Fibonacci con while", _auto2,
    pista="Repite mientras `len(serie_while) < 15`.",
    solucion="""
serie_while = [0, 1]
while len(serie_while) < 15:
    serie_while.append(serie_while[-1] + serie_while[-2])
print(serie_while)
""")


def _auto3(ns):
    datos = lista_no_vacia("datos_limpios", obtener(ns, "datos_limpios"),
                           "completa el `if` dentro del ciclo.")
    if datos != [22.5, 23.0, 21.8, 24.1]:
        raise Incorrecto(f"`datos_limpios` vale {datos}; debe contener solo los "
                         "valores numéricos, en el mismo orden.")


auto3 = sesion.agregar(
    "auto3", "Limpieza de una lista", _auto3,
    pista="`isinstance(dato, (int, float))` es `True` solo para números.",
    solucion="""
mediciones_sucias = [22.5, 23.0, "Error", 21.8, None, 24.1]
datos_limpios = []

for dato in mediciones_sucias:
    if isinstance(dato, (int, float)):
        datos_limpios.append(dato)

print(datos_limpios)
""")


def _auto4(ns):
    for n in (100, 200, 300):
        comparar_numero(f"suma_{n}", obtener(ns, f"suma_{n}"), n * (n + 1) // 2)
    comparar_numero("comprobacion", obtener(ns, "comprobacion"), 5050)


auto4 = sesion.agregar(
    "auto4", "Fórmula de Gauss", _auto4,
    pista="Aplica `n * (n + 1) // 2` con n = 100, 200 y 300. Para comprobar, `sum(range(1, 101))` "
          "suma los números del 1 al 100.",
    solucion="""
suma_100 = 100 * (100 + 1) // 2
suma_200 = 200 * (200 + 1) // 2
suma_300 = 300 * (300 + 1) // 2

comprobacion = sum(range(1, 101))     # Sumando uno por uno
print(suma_100, suma_200, suma_300, comprobacion)
""")


def _mismo_criterio(obtenido, esperado):
    return isinstance(obtenido, str) and normalizar_texto(obtenido).removeprefix("en ") == esperado


def _auto5(ns):
    delta_g = 206.1 - 298.15 * 0.215
    comparar_numero("delta_g_25", obtener(ns, "delta_g_25"), delta_g, unidades="kJ/mol")
    clasificacion = obtener(ns, "clasificacion")
    if not _mismo_criterio(clasificacion, "no espontanea"):
        raise Incorrecto(f"`clasificacion` vale {clasificacion!r}. Con ΔG > 0 la reacción es "
                         "«no espontánea»; revisa el orden de tus condiciones.")
    comparar_numero("T_inversion", obtener(ns, "T_inversion"), 206.1 / 0.215, rel=5e-3,
                    unidades="K")
    return ("A 25 °C la reacción no es espontánea; por encima de ≈ 959 K el término TΔS domina "
            "y ΔG se vuelve negativo.")


auto5 = sesion.agregar(
    "auto5", "Espontaneidad de una reacción", _auto5,
    pista="ΔS está en J/(mol·K) y ΔH en kJ/mol: divide ΔS entre 1000. Con `if`, `elif` y `else` "
          "asigna «espontánea», «equilibrio» o «no espontánea» a `clasificacion`.",
    solucion="""
delta_h = 206.1                  # kJ/mol
delta_s = 215 / 1000             # kJ/(mol·K)
T = 25 + 273.15                  # K

delta_g_25 = delta_h - T * delta_s

if delta_g_25 < 0:
    clasificacion = "espontánea"
elif delta_g_25 == 0:
    clasificacion = "equilibrio"
else:
    clasificacion = "no espontánea"
print(f"ΔG = {delta_g_25:.2f} kJ/mol → {clasificacion}")

T_inversion = delta_h / delta_s
print(f"La reacción es espontánea por encima de {T_inversion:.1f} K")
""")


# --- Tema extra: funciones -----------------------------------------------------

def _extra1(ns):
    funcion = obtener_funcion(ns, "clasificar_enlace")
    casos = [
        ((0.0,), {}, "covalente no polar"),
        ((0.35,), {}, "covalente no polar"),
        ((0.5,), {}, "covalente polar"),
        ((1.2,), {}, "covalente polar"),
        ((1.7,), {}, "iónico"),
        ((2.1,), {}, "iónico"),
    ]
    probar_funcion("clasificar_enlace", funcion, casos, comparar=_mismo_enlace)
    return "Tu función clasifica correctamente todos los casos, incluidos los límites 0.5 y 1.7."


extra1 = sesion.agregar(
    "extra1", "(Extra) Función para clasificar enlaces", _extra1,
    pista="Usa `if`, `elif` y `else` dentro de la función y devuelve el texto con "
          "`return`. Cuida los límites: 0.5 ya es *covalente polar* y 1.7 ya es *iónico*.",
    solucion="""
def clasificar_enlace(delta_chi):
    if delta_chi < 0.5:
        return "covalente no polar"
    elif delta_chi < 1.7:
        return "covalente polar"
    else:
        return "iónico"

print("Na–Cl:", clasificar_enlace(abs(chi_Na - chi_Cl)))
""")


def _extra2(ns):
    funcion = obtener_funcion(ns, "formula_gauss")
    casos = [((n,), {}, n * (n + 1) // 2) for n in (1, 10, 100, 1000)]
    probar_funcion("formula_gauss", funcion, casos)
    for n in (100, 200, 300):
        comparar_numero(f"suma_{n}", obtener(ns, f"suma_{n}"), n * (n + 1) // 2)


extra2 = sesion.agregar(
    "extra2", "(Extra) Función de Gauss", _extra2,
    pista="La función debe devolver `n * (n + 1) / 2`. Usa `//` (división entera) si "
          "quieres obtener un `int` en lugar de un `float`.",
    solucion="""
def formula_gauss(n):
    return n * (n + 1) // 2

suma_100 = formula_gauss(100)
suma_200 = formula_gauss(200)
suma_300 = formula_gauss(300)
print(suma_100, suma_200, suma_300)
""")


# --- Tema extra: clases ------------------------------------------------------

def _extra3(ns):
    Sustancia = obtener(ns, "Sustancia")
    nacl = obtener(ns, "cloruro_sodio")
    if not isinstance(nacl, Sustancia):
        raise Incorrecto("`cloruro_sodio` debe crearse con `Sustancia(...)`.")
    if getattr(nacl, "formula", None) != "NaCl":
        raise Incorrecto('El atributo `formula` debe ser "NaCl".')
    masa = getattr(nacl, "masa_molar", None)
    if masa is not None and abs(masa - 35.45) < 0.01:
        raise Incorrecto("35.45 g/mol es la masa molar del cloro, no la del NaCl.")
    comparar_numero("cloruro_sodio.masa_molar", masa, MM_NACL, rel=2e-3, unidades="g/mol")
    comparar_numero("moles_nacl", obtener(ns, "moles_nacl"), 15 / MM_NACL, rel=2e-3, unidades="mol")


extra3 = sesion.agregar(
    "extra3", "(Extra) Objeto cloruro de sodio", _extra3,
    pista="La masa molar del NaCl es la suma de Na (22.99) y Cl (35.45). Para los "
          "moles, llama al método: `cloruro_sodio.gramos_a_moles(15)`.",
    solucion="""
cloruro_sodio = Sustancia("Cloruro de sodio", "NaCl", 58.44)
moles_nacl = cloruro_sodio.gramos_a_moles(15)
print(f"En 15 g de {cloruro_sodio.formula} hay {moles_nacl} mol.")
""")


def _extra4(ns):
    Disolucion = obtener(ns, "Disolucion")
    muestra = Disolucion(5, 100, 103, MM_NACL)
    for metodo in ("calcular_molaridad", "calcular_molalidad", "calcular_moles"):
        if not hasattr(muestra, metodo):
            raise Incorrecto(f"La clase `Disolucion` no tiene el método `{metodo}`.")
    probar_funcion("Disolucion(5, 100, 103, 58.44).calcular_molaridad",
                   muestra.calcular_molaridad, [((), {}, 5 / MM_NACL / 0.103)])
    probar_funcion("Disolucion(5, 100, 103, 58.44).calcular_molalidad",
                   muestra.calcular_molalidad, [((), {}, 5 / MM_NACL / 0.100)])
    probar_funcion("Disolucion(5, 100, 103, 58.44).calcular_moles",
                   muestra.calcular_moles, [((), {}, 5 / MM_NACL)])
    comparar_numero("moles_50g", obtener(ns, "moles_50g"), 50 / MM_NACL, rel=2e-3, unidades="mol")


extra4 = sesion.agregar(
    "extra4", "(Extra) Métodos de la clase Disolucion", _extra4,
    pista="Molaridad = mol de soluto / L de disolución; molalidad = mol de soluto / kg "
          "de disolvente. Recuerda convertir mL → L y g → kg dividiendo entre 1000.",
    solucion="""
class Disolucion:
    def __init__(self, masa_soluto, masa_disolvente, volumen_ml, masa_molar):
        self.masa_soluto = masa_soluto
        self.masa_disolvente = masa_disolvente
        self.masa_disolucion = masa_soluto + masa_disolvente
        self.volumen_ml = volumen_ml
        self.masa_molar = masa_molar

    def porcentaje_masa_masa(self):
        return self.masa_soluto / self.masa_disolucion * 100

    def porcentaje_masa_volumen(self):
        return self.masa_soluto / self.volumen_ml * 100

    def calcular_moles(self):
        return self.masa_soluto / self.masa_molar

    def calcular_molaridad(self):
        return self.calcular_moles() / (self.volumen_ml / 1000)

    def calcular_molalidad(self):
        return self.calcular_moles() / (self.masa_disolvente / 1000)

muestra = Disolucion(5, 100, 103, 58.44)
print(f"Molaridad: {muestra.calcular_molaridad():.3f} mol/L")
print(f"Molalidad: {muestra.calcular_molalidad():.3f} mol/kg")

moles_50g = Disolucion(50, 100, 120, 58.44).calcular_moles()
print(f"En 50 g de NaCl hay {moles_50g:.4f} mol")
""")


# Ejercicios adicionales del equipo docente (contenido_extra/sesion2/)
globals().update(sesion.cargar_adicionales(
    os.path.join(os.path.dirname(__file__), "adicionales_sesion2.json")))

__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
