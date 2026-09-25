"""Ejercicios de la Sesión 2: estructuras de datos, ciclos y clases."""

from .nucleo import (Incorrecto, Sesion, ____, comparar_numero, lista_no_vacia, obtener,
                     obtener_funcion, probar_funcion)

sesion = Sesion("Sesión 2", "S2")
progreso = sesion.progreso
iniciar_registro = sesion.iniciar_registro

MM_NACL = 58.44   # g/mol


def _cerca_arreglo(obtenido, esperado):
    import numpy as np
    obtenido = np.asarray(obtenido, dtype=float)
    return obtenido.shape == np.shape(esperado) and np.allclose(obtenido, esperado, atol=1e-6)


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
    comparar_numero("masa_molar_hno3", obtener(ns, "masa_molar_hno3"), 1.0 + 14.0 + 3 * 16.0)


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
    comparar_numero("masa_molar_fe2o3", masa_fe2o3, 2 * masas["hierro"] + 3 * 16.0)


ej2b = sesion.agregar(
    "ej2b", "Masa molar del Fe₂O₃", _ej2b,
    pista='Agrega un par clave-valor con `masas_molares["hierro"] = 55.85`. El óxido de '
          'hierro(III) es Fe₂O₃.',
    solucion="""
masas_molares["hierro"] = 55.85
masa_molar_fe2o3 = 2 * masas_molares["hierro"] + 3 * masas_molares["oxígeno"]
print(f"M(Fe₂O₃) = {masa_molar_fe2o3:.2f} g/mol")
""")


# --- Ejercicio 3: for y while ------------------------------------------------

def _ej3(ns):
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


ej3 = sesion.agregar(
    "ej3", "Ahorro para un celular", _ej3,
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


# --- Ejercicio 4: muestras peligrosas ----------------------------------------

def _ej4(ns):
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


ej4 = sesion.agregar(
    "ej4", "Detección de muestras peligrosas", _ej4,
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


# --- Ejercicio 5: NumPy, matriz de rotación ------------------------------------------

def _ej5(ns):
    funcion = obtener_funcion(ns, "rotar_vector")
    r = 2 ** 0.5
    casos = [
        (([1, 0], 90), {}, [0.0, 1.0]),
        (([0, 1], 90), {}, [-1.0, 0.0]),
        (([2, 0], 180), {}, [-2.0, 0.0]),
        (([1, 1], 45), {}, [0.0, r]),
        (([3, 4], 0), {}, [3.0, 4.0]),
    ]
    probar_funcion("rotar_vector", funcion, casos, comparar=_cerca_arreglo)


ej5 = sesion.agregar(
    "ej5", "Rotación de un vector", _ej5,
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


# --- Ejercicio 6: NumPy, regla de Cramer ---------------------------------------------

def _ej6_numpy(ns):
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


ej6 = sesion.agregar(
    "ej6", "Regla de Cramer", _ej6_numpy,
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
    _probar_fibonacci(ns, "fibonacci_for")


auto1 = sesion.agregar(
    "auto1", "Fibonacci con for", _auto1,
    pista="Empieza con `serie = [0, 1]` y agrega `serie[-1] + serie[-2]` en cada vuelta. "
          "¿Qué debe devolver la función si `n` es 1?",
    solucion="""
def fibonacci_for(n):
    \"\"\"Devuelve una lista con los primeros n números de Fibonacci.\"\"\"
    serie = [0, 1][:n]          # Funciona también para n = 1
    for _ in range(n - 2):
        serie.append(serie[-1] + serie[-2])
    return serie

fibonacci_for(10)
""")


def _auto2(ns):
    _probar_fibonacci(ns, "fibonacci_while")


auto2 = sesion.agregar(
    "auto2", "Fibonacci con while", _auto2,
    pista="Repite mientras `len(serie) < n`.",
    solucion="""
def fibonacci_while(n):
    serie = [0, 1][:n]
    while len(serie) < n:
        serie.append(serie[-1] + serie[-2])
    return serie

fibonacci_while(10)
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


# --- Tema extra: clases ------------------------------------------------------

def _extra1(ns):
    Sustancia = obtener(ns, "Sustancia")
    nacl = obtener(ns, "cloruro_sodio")
    if not isinstance(nacl, Sustancia):
        raise Incorrecto("`cloruro_sodio` debe crearse con `Sustancia(...)`.")
    if getattr(nacl, "formula", None) != "NaCl":
        raise Incorrecto('El atributo `formula` debe ser "NaCl".')
    masa = getattr(nacl, "masa_molar", None)
    if masa is not None and abs(masa - 35.45) < 0.01:
        raise Incorrecto("35.45 g/mol es la masa molar del cloro, no la del NaCl.")
    comparar_numero("cloruro_sodio.masa_molar", masa, MM_NACL, rel=2e-3)
    comparar_numero("moles_nacl", obtener(ns, "moles_nacl"), 15 / MM_NACL, rel=2e-3)


extra1 = sesion.agregar(
    "extra1", "(Extra) Objeto cloruro de sodio", _extra1,
    pista="La masa molar del NaCl es la suma de Na (22.99) y Cl (35.45). Para los "
          "moles, llama al método: `cloruro_sodio.gramos_a_moles(15)`.",
    solucion="""
cloruro_sodio = Sustancia("Cloruro de sodio", "NaCl", 58.44)
moles_nacl = cloruro_sodio.gramos_a_moles(15)
print(f"En 15 g de {cloruro_sodio.formula} hay {moles_nacl} mol.")
""")


def _extra2(ns):
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
    comparar_numero("moles_50g", obtener(ns, "moles_50g"), 50 / MM_NACL, rel=2e-3)


extra2 = sesion.agregar(
    "extra2", "(Extra) Métodos de la clase Disolucion", _extra2,
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


__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
