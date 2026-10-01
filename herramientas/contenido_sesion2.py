"""Contenido de la Sesión 2: estructuras de datos, ciclos y clases."""

from bloques import cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(2, "Estructuras de datos, decisiones y ciclos", """
En la sesión anterior aprendimos los tipos de datos, las operaciones, NumPy y las unidades con
pint. Ahora aprenderemos a **guardar colecciones de datos** (`list`, `tuple`, `dict`), a **tomar
decisiones** con condicionales (`if`, `elif`, `else`) y a **repetir instrucciones** con los ciclos
`for` y `while`. Si queda tiempo, veremos dos temas extra: cómo escribir nuestras propias
**funciones** y una introducción a la **programación orientada a objetos**.

**Al terminar podrás:**
- Crear, consultar y modificar listas, tuplas y diccionarios.
- Comparar valores y usar `if`, `elif` y `else` para clasificar resultados.
- Recorrer colecciones con `for` y repetir cálculos con `while`.
- Filtrar datos experimentales de forma automática, con ciclos y con máscaras de NumPy.
""", carpeta, archivo)
        + instrucciones(2)
        + md("""
## **Listas**

Son colecciones **ordenadas** de elementos (números, textos u otras listas) que se definen con
corchetes `[]`. Nos permiten organizar, almacenar y manipular conjuntos de datos.
""")
        + code("""
calificaciones = [9.0, 6.7, 10.0, 8.0]
print(calificaciones)

num_calificaciones = len(calificaciones)   # Tamaño de la lista
print(f"Tamaño: {num_calificaciones}")
print(f"Máximo: {max(calificaciones)}")
print(f"Mínimo: {min(calificaciones)}")
print(f"Suma: {sum(calificaciones)}")
print(f"Promedio: {sum(calificaciones) / num_calificaciones}")
""")
        + md("Las listas son **mutables**: podemos agregar, quitar o cambiar elementos después de crearlas.")
        + code("""
asignaturas = ["Álgebra", "Cálculo", "Física", "Química"]

# Verificar si un elemento está en la lista
print("Álgebra" in asignaturas)
print("Ciencia y Sociedad" in asignaturas)

# Agregar un elemento al final
asignaturas.append("Ciencia y Sociedad")
print(asignaturas)

# Eliminar un elemento
asignaturas.remove("Álgebra")
print(asignaturas)
""")
        + md("""
Como las listas conservan el **orden**, podemos acceder a sus elementos por su **índice**.
En Python los índices empiezan en **0**, y los índices negativos cuentan desde el final.
""")
        + code("""
print(f"Primer elemento: {asignaturas[0]}")
print(f"Tercer elemento: {asignaturas[2]}")
print(f"Último elemento: {asignaturas[-1]}")
""")
        + md("Una lista puede mezclar tipos de datos, aunque para eso suele ser mejor un diccionario (lo veremos más adelante).")
        + code("""
resultado_parcial = [
    "Álgebra",   # Asignatura
    8.5,         # Calificación
    2,           # Número de examen parcial
    True,        # ¿Aprobado?
]

resultado_parcial[1]
""")
        + md("""
### **Ejercicio 1a: Tus asignaturas**

Crea la lista `mis_asignaturas` con las asignaturas que estás cursando (al menos tres) y guarda:

- su tamaño en `num_asignaturas`,
- el segundo elemento en `segundo_elemento`,
- el penúltimo elemento en `penultimo_elemento`.
""")
        + ejercicio("ej1a", """
mis_asignaturas = ____

num_asignaturas = ____
segundo_elemento = ____
penultimo_elemento = ____
print(num_asignaturas, segundo_elemento, penultimo_elemento)
""")
        + md("""
### **Ejercicio 1b: Modificar la lista**

Elimina de `mis_asignaturas` la asignatura que menos te guste y agrega `"Curso de Python"`.
""")
        + ejercicio("ej1b", """
____
____
print(mis_asignaturas)
""")
        + md("""
## **Tuplas**

Son análogas a las listas, pero **inmutables**: una vez creadas no pueden modificarse. Se
definen con paréntesis `()` y son útiles para datos que no deben cambiar por accidente, como
constantes o coordenadas.
""")
        + code("""
asignaturas_tupla = ("Álgebra", "Cálculo", "Física", "Química")

# Se accede a los elementos igual que en una lista
asignaturas_tupla[-1] == "Química"
""")
        + code("""
# Intentar modificar una tupla produce un error (TypeError). ¡Es lo esperado!
asignaturas_tupla[0] = "Ciencia y Sociedad"
""", error_esperado=True)
        + code("""
# Si necesitamos cambiar un dato, convertimos la tupla en lista y de regreso
calificaciones_grupo = (10.0, 9.0, 6.0)

lista_temporal = list(calificaciones_grupo)
lista_temporal[2] = 7.0                      # Corregimos la tercera calificación
calificaciones_grupo = tuple(lista_temporal)

calificaciones_grupo
""")
        + md("""
## **Diccionarios**

Son colecciones de pares `clave: valor` que se definen con llaves `{}`. En lugar de acceder por
posición, accedemos **por clave**, lo que los hace ideales para tablas de datos como masas
molares o propiedades de sustancias. Los valores pueden ser de cualquier tipo, incluso listas u
otros diccionarios.
""")
        + code("""
datos_estudiante = {
    "nombre": "Roberto",
    "edad": 24,
    "carrera": "Química",
    "asignaturas": ["Cálculo", "Física", "Química"],
}
print("Diccionario inicial:", datos_estudiante)

# Acceder a un valor usando su clave
print("Nombre:", datos_estudiante["nombre"])

# Modificar un valor
datos_estudiante["edad"] = 25

# Añadir un nuevo par clave-valor
datos_estudiante["escuela"] = "Facultad de Química"

# Eliminar un par clave-valor
del datos_estudiante["asignaturas"]
print("Diccionario final:", datos_estudiante)
""")
        + md("""
### **Ejercicio 2a: Masa molar**

Usa el diccionario `masas_molares` para calcular la masa molar del ácido nítrico (HNO₃) y
guárdala en `masa_molar_hno3`.
""")
        + code("""
# Masas atómicas en g/mol
masas_molares = {
    "hidrógeno": 1.0,
    "helio": 4.0,
    "litio": 6.9,
    "berilio": 9.0,
    "boro": 10.8,
    "carbono": 12.0,
    "nitrógeno": 14.0,
    "oxígeno": 16.0,
    "flúor": 19.0,
    "neón": 20.2,
}
""")
        + ejercicio("ej2a", """
masa_molar_hno3 = ____
print(f"M(HNO₃) = {masa_molar_hno3} g/mol")
""")
        + md("""
### **Ejercicio 2b: Agregar un elemento**

Agrega el hierro (55.85 g/mol) al diccionario y calcula la masa molar del óxido de hierro(III),
Fe₂O₃ (`masa_molar_fe2o3`).
""")
        + ejercicio("ej2b", """
____
masa_molar_fe2o3 = ____
print(f"M(Fe₂O₃) = {masa_molar_fe2o3} g/mol")
""")
        + md("""
## **Variables booleanas y comparaciones**

Una variable booleana solo puede valer `True` (verdadero) o `False` (falso). Se obtienen al
comparar valores con los operadores `<`, `<=`, `>`, `>=`, `==` (igual) y `!=` (diferente).

> ⚠️ `=` **asigna** un valor; `==` **compara** dos valores.
""")
        + code("""
ph = 4

# ¿El pH es menor que 7?
ph < 7
""")
        + code("""
# ¿El pH es exactamente igual a 7?
ph == 7
""")
        + code("""
# ¿El pH es mayor o igual que 7?
ph >= 7
""")
        + code("""
# ¿El pH es diferente de 7?
ph != 7
""")
        + md("""
## **El condicional `if`**

Las estructuras `if`, `elif` y `else` controlan el flujo del programa con base en
**condiciones**:

- `if`: ejecuta un bloque de código si la condición es verdadera.
- `elif` (*else if*): evalúa una nueva condición si las anteriores fueron falsas. Puede haber
  varios.
- `else`: se ejecuta si ninguna condición anterior fue verdadera. Es opcional.

Los bloques se delimitan con **sangría** (4 espacios) después de los dos puntos `:`.
""")
        + code("""
# Clasificamos el estado de agregación del agua a 1 atm según su temperatura
T_fusion = 0          # °C
T_ebullicion = 100    # °C

T = float(input("¿A qué temperatura está el agua? (°C): "))

if T > T_ebullicion:
    print("El agua está en fase gaseosa.")
elif T < T_fusion:      # Solo se evalúa si la condición del if fue falsa
    print("El agua está en fase sólida.")
else:                   # Se ejecuta cuando todas las condiciones anteriores son falsas
    print("El agua está en fase líquida.")
""")
        + md("""
## **Operadores lógicos**

Para combinar condiciones usamos `and`, `or` y `not`:

| A | B | `A and B` | `A or B` | `not A` |
| :-: | :-: | :-: | :-: | :-: |
| `True` | `True` | `True` | `True` | `False` |
| `True` | `False` | `False` | `True` | `False` |
| `False` | `True` | `False` | `True` | `True` |
| `False` | `False` | `False` | `False` | `True` |
""")
        + code("""
# Clasificamos disoluciones según su pH combinando condiciones con 'and'
ph = 8

if 0 <= ph < 7:                 # Equivale a (ph >= 0) and (ph < 7)
    print("La disolución es ácida.")
elif ph == 7:
    print("La disolución es neutra.")
elif (ph > 7) and (ph <= 14):
    print("La disolución es básica.")
else:
    print("El pH está fuera del intervalo 0–14.")
""")
        + md(r"""
### **Ejercicio 3: Clasificación de enlaces**

Según la diferencia de electronegatividad $\Delta \chi$ entre dos átomos, podemos predecir el tipo
de enlace que forman:

- Covalente no polar: $\Delta \chi < 0.5$
- Covalente polar: $0.5 \leq \Delta \chi < 1.7$
- Iónico: $\Delta \chi \geq 1.7$

Usa `if`, `elif` y `else` para guardar en `tipo_enlace` uno de los textos `"covalente no polar"`,
`"covalente polar"` o `"iónico"`, según el valor de `delta_chi`. La función `abs()` da el valor
absoluto de la diferencia.

Cuando funcione con Na–Cl, cambia los átomos (por ejemplo, C–H u O–H) y vuelve a ejecutar la celda
y la verificación.
""")
        + code("""
# Electronegatividades de Pauling
chi_H = 2.20
chi_C = 2.55
chi_N = 3.04
chi_O = 3.44
chi_F = 3.98
chi_Na = 0.93
chi_Mg = 1.31
chi_Cl = 3.16
""")
        + ejercicio("ej3", """
delta_chi = abs(chi_Na - chi_Cl)

if ____:
    tipo_enlace = "covalente no polar"
elif ____:
    tipo_enlace = ____
else:
    tipo_enlace = ____

print(f"Δχ = {delta_chi:.2f} → enlace {tipo_enlace}")
""")
        + md(r"""
### **Ejercicio 4: Temperatura de un gas ideal**

Despejando $PV = nRT$ obtenemos $T = \frac{PV}{nR}$, con $R = 0.0821~\frac{\text{atm·L}}{\text{mol·K}}$.

1. Calcula la cantidad de sustancia `n_agua` en 50.0 g de agua.
2. Calcula a qué temperatura se cumplen las siguientes condiciones y guarda los resultados en
   `T1` y `T2`:
   - $P = 3.0~\text{atm},~V = 20.0~\text{L}$
   - $P = 6.3~\text{atm},~V = 1.2~\text{L}$

> 🤔 **Para reflexionar:** ¿tiene sentido físico tratar al agua como gas ideal a esas
> temperaturas? ¿En qué fase estaría realmente?
""")
        + ejercicio("ej4", """
m_agua = 50.0       # g
MM_agua = ____      # g/mol
n_agua = ____
R = 0.0821          # atm·L/(mol·K)

T1 = ____           # P = 3.0 atm, V = 20.0 L
T2 = ____           # P = 6.3 atm, V = 1.2 L
print(f"T1 = {T1} K")
print(f"T2 = {T2} K")
""")
        + md("""
## **El ciclo `for`**

Repite un bloque de código **para cada elemento** de una secuencia (lista, tupla, texto,
rango, etc.):

```python
for elemento in secuencia:
    # Código que se ejecuta una vez por cada elemento
```
""")
        + code("""
asignaturas = ["Álgebra", "Cálculo", "Física", "Química", "Ciencia y Sociedad"]

print("Asignaturas de primer semestre:")
for asignatura in asignaturas:
    print("-", asignatura)
""")
        + md("""
Dos herramientas muy útiles con `for`:

- `range(inicio, fin)` genera los enteros desde `inicio` hasta `fin - 1`.
- `enumerate(lista)` entrega, en cada vuelta, el **índice** y el **elemento**.
""")
        + code("""
for n in range(1, 6):
    print(f"{n}² = {n**2}")

for i, asignatura in enumerate(asignaturas):
    print(f"Índice {i}: {asignatura}")
""")
        + code("""
# (Opcional) Recorrer un diccionario
for clave, valor in datos_estudiante.items():
    print(f"{clave}: {valor}")
""")
        + md("""
## **El ciclo `while`**

Repite un bloque de código **mientras** una condición sea verdadera:

```python
while condicion:
    # Código que se repite mientras la condición sea True
```

- Usamos `for` cuando conocemos de antemano los elementos o el número de repeticiones.
- Usamos `while` cuando no sabemos cuántas repeticiones hacen falta, pero sí **cuándo detenernos**.
""")
        + code("""
contador = 1

while contador <= 5:
    print(f"Contador: {contador}")
    contador += 1        # Equivale a contador = contador + 1

print("Fin del ciclo while")
""")
        + md("""
Si la condición nunca se vuelve falsa, el ciclo **no termina**. Descomenta la celda siguiente
solo si quieres ver qué ocurre, y detenla con el botón ■ (*Interrumpir ejecución*).
""")
        + code("""
# i = 1
# while i >= 0:     # i nunca cambia, así que la condición siempre es verdadera
#     print(i)
""")
        + md(r"""
## **Ejemplo con `for` y `while`: tiempo de vida media**

El tiempo de vida media ($t_{1/2}$) de un isótopo radiactivo es el tiempo que tarda en
desintegrarse la mitad de los núcleos de una muestra. Si tenemos **1.0 g** de carbono-14
($t_{1/2} = 5730$ años):

1. ¿Cuánta masa quedará después de cada uno de los primeros 5 tiempos de vida media? (`for`)
2. ¿Cuántos tiempos de vida media hacen falta para que queden menos de 0.001 g? (`while`)
""")
        + code("""
# 1. Con for: dividimos la masa entre 2 en cada tiempo de vida media
t_vida_media = 5730   # años
masa = 1.0            # g

for n in range(1, 6):
    masa = masa / 2
    print(f"Tras {n} vidas medias ({n * t_vida_media} años): {masa:.4f} g")
""")
        + md(r"""
Como la masa se divide a la mitad en cada tiempo de vida media, también podemos usar la fórmula
$m = m_0 \left(\frac{1}{2}\right)^{n}$ sin acumular resultados:
""")
        + code("""
masa_inicial = 1.0   # g

for n in range(1, 6):
    masa = masa_inicial * 0.5**n
    print(f"Tras {n} vidas medias ({n * t_vida_media} años): {masa:.4f} g")
""")
        + code("""
# 2. Con while: repetimos mientras la masa siga siendo mayor que el límite
masa = 1.0
masa_limite = 0.001   # g
n = 0

while masa > masa_limite:
    masa = masa / 2
    n += 1

print(f"Se necesitan {n} vidas medias ({n * t_vida_media} años); quedan {masa:.5f} g.")
""")
        + md("""
También podríamos usar un `for` con un número máximo de repeticiones y salir con `break`
cuando se cumpla la condición. Es útil cuando queremos garantizar que el ciclo termine.
""")
        + code("""
masa = 1.0

for n in range(1, 101):   # Como máximo 100 repeticiones
    masa = masa / 2
    if masa <= masa_limite:
        break              # Sale del ciclo en cuanto se cumple la condición

print(f"Se necesitan {n} vidas medias.")
""")
        + md("""
### **Ejercicio 5: Ahorros**

Ahorras \\$300 pesos al mes para comprar un celular que cuesta \\$7,000 pesos.

1. Con un `for`, construye la lista `ahorros` con lo que habrás ahorrado a los 10, 20 y 30 meses.
2. Con un `while`, calcula `meses_necesarios` para poder comprar el celular.
""")
        + ejercicio("ej5", """
precio_celular = 7000
ahorro_mensual = 300

ahorros = []
for mes in [10, 20, 30]:
    ____
print(ahorros)

ahorro_total = 0
meses_necesarios = 0
while ____:
    ____
    ____
print(f"Se necesitan {meses_necesarios} meses.")
""")
        + md("""
## **Aplicación: detección de muestras peligrosas**

Tienes 200 mediciones de concentración (ppm) de un contaminante. El límite de seguridad es de
50 ppm, y las concentraciones mayores a 100 ppm indican una falla del equipo de medición.

**Nota:** la celda siguiente *simula* los datos experimentales. No es necesario entender cómo
funciona; `random.seed()` garantiza que todos obtengamos los mismos datos.
""")
        + code("""
import random

random.seed(2026)
mediciones = []

for _ in range(200):
    probabilidad = random.random()             # Número al azar entre 0 y 1
    if probabilidad < 0.90:                    # 90 %: valores normales (10–80 ppm)
        valor = random.uniform(10, 80)
    elif probabilidad < 0.97:                  # 7 %: valores altos (81–100 ppm)
        valor = random.uniform(81, 100)
    else:                                      # 3 %: fallas del sensor (> 100 ppm)
        valor = random.uniform(101, 150)
    mediciones.append(round(valor, 2))

print(f"Se generaron {len(mediciones)} mediciones. Las primeras 10: {mediciones[:10]}")
print(f"Mínimo: {min(mediciones)} ppm, máximo: {max(mediciones)} ppm")
""")
        + md("""
### **Ejercicio 6: Clasificación de muestras**

Recorre `mediciones` y construye dos listas con los **índices** (posiciones) de las muestras:

- `indices_peligrosas`: concentración mayor a 50 ppm y menor o igual a 100 ppm.
- `indices_criticas`: concentración mayor a 100 ppm.
""")
        + ejercicio("ej6", """
indices_peligrosas = []
indices_criticas = []

for i, concentracion in enumerate(mediciones):
    ____

print(f"Muestras peligrosas: {len(indices_peligrosas)}")
print(f"Muestras críticas: {len(indices_criticas)}")
""")
        + md("""
Con los arreglos de NumPy (Sesión 1) y las comparaciones de esta sesión, el mismo filtrado
se hace **sin ciclo**: una comparación produce un arreglo de `True`/`False` (una *máscara*) que
sirve para seleccionar elementos.
""")
        + code("""
import numpy as np

concentraciones = np.array(mediciones)

peligrosas = (concentraciones > 50) & (concentraciones <= 100)   # Máscara booleana
print(f"Peligrosas: {peligrosas.sum()} muestras")
print(f"Índices: {np.where(peligrosas)[0]}")
print(f"Concentración promedio de las peligrosas: {concentraciones[peligrosas].mean():.1f} ppm")
""")
        + md("""
## **Resumen de la sesión**

| Estructura | Sintaxis | ¿Mutable? | Acceso |
| :--- | :--- | :---: | :--- |
| Lista | `[a, b, c]` | Sí | Por índice: `lista[0]` |
| Tupla | `(a, b, c)` | No | Por índice: `tupla[0]` |
| Diccionario | `{"clave": valor}` | Sí | Por clave: `dic["clave"]` |

**Funciones y métodos útiles:** `len()`, `max()`, `min()`, `sum()`, `lista.append(x)`,
`lista.remove(x)`, `range()`, `enumerate()`, `dic.items()`.

**Decisiones:** las comparaciones (`<`, `<=`, `==`, `!=`…) producen `True` o `False`; `if`,
`elif` y `else` ejecutan bloques según esas condiciones, que se combinan con `and`, `or` y `not`.

**Ciclos:**
- `for`: recorre cada elemento de una secuencia.
- `while`: repite mientras una condición sea verdadera. ¡Asegúrate de que en algún momento sea falsa!
- `break`: sale del ciclo.

**NumPy con comparaciones:** una comparación con un arreglo produce una máscara de
`True`/`False` que filtra sin ciclo: `arreglo[arreglo > 50]`.

**Tema extra 1, funciones:** `def nombre(parámetros): ... return resultado`. Los parámetros pueden
tener valores predeterminados (`R=0.0821`).

**Tema extra 2, clases:** `class` define el molde; `__init__` asigna los atributos; los métodos son
funciones que reciben `self` para acceder a los datos del objeto.
""")
        + md("## **Ejercicios de autoevaluación**")
        + md("""
### **Autoevaluación 1: Serie de Fibonacci con `for`**

En la serie de Fibonacci, cada número es la suma de los dos anteriores, $F_n = F_{n-1} + F_{n-2}$,
y los primeros son 0 y 1: `[0, 1, 1, 2, 3, 5, ...]`. Con un ciclo `for`, construye la lista `serie`
con los primeros `n = 10` números.
""")
        + ejercicio("auto1", """
n = 10
serie = [0, 1]

for _ in range(n - 2):          # Faltan n - 2 números
    ____

print(serie)
""")
        + md("""
### **Autoevaluación 2: Serie de Fibonacci con `while`**

Construye ahora la lista `serie_while` con los primeros **15** números de Fibonacci, usando un
ciclo `while`.

> 🤔 ¿Por qué la condición correcta es `len(serie_while) < 15` y no `len(serie_while) <= 15`?
> Prueba ambas y compara los resultados.
""")
        + ejercicio("auto2", """
serie_while = [0, 1]

while ____:
    ____

print(serie_while)
""")
        + md("""
### **Autoevaluación 3: Limpieza de una lista**

Al analizar datos es común encontrar valores "sucios" o nulos. Usa un ciclo para construir la
lista `datos_limpios` que contenga solo los valores numéricos de `mediciones_sucias`.

> 💡 `isinstance(dato, (int, float))` devuelve `True` si `dato` es un número.
""")
        + ejercicio("auto3", """
mediciones_sucias = [22.5, 23.0, "Error", 21.8, None, 24.1]
datos_limpios = []

for dato in mediciones_sucias:
    ____

print(f"Datos listos para analizar: {datos_limpios}")
""")
        + md(r"""
### **Autoevaluación 4: Fórmula de Gauss**

La suma de los primeros $n$ números naturales es:

$$S_n = \frac{n(n+1)}{2}$$

Úsala para sumar los primeros 100, 200 y 300 números naturales (`suma_100`, `suma_200` y
`suma_300`). Después comprueba el primer resultado sumando los números uno por uno con
`sum(range(1, 101))` y guárdalo en `comprobacion`.
""")
        + ejercicio("auto4", """
suma_100 = ____
suma_200 = ____
suma_300 = ____

comprobacion = ____
print(suma_100, suma_200, suma_300, comprobacion)
""")
        + md(r"""
### **Autoevaluación 5: Espontaneidad de una reacción**

El reformado de metano con vapor produce monóxido de carbono e hidrógeno:

$$\text{CH}_4(g) + \text{H}_2\text{O}(g) \rightarrow \text{CO}(g) + 3\,\text{H}_2(g)$$

con $\Delta H^\circ = 206.1~\text{kJ/mol}$ y $\Delta S^\circ = 215~\text{J/(mol·K)}$.

1. Calcula $\Delta G = \Delta H - T\Delta S$ a 25 °C, en kJ/mol (`delta_g_25`). Cuida las unidades
   de $\Delta S$.
2. Con `if`, `elif` y `else`, guarda en `clasificacion` el texto `"espontánea"` ($\Delta G < 0$),
   `"equilibrio"` ($\Delta G = 0$) o `"no espontánea"` ($\Delta G > 0$).
3. **Reto:** ¿a partir de qué temperatura la reacción se vuelve espontánea? (`T_inversion`)
""")
        + ejercicio("auto5", """
delta_h = 206.1                  # kJ/mol
delta_s = ____                   # kJ/(mol·K)
T = 25 + 273.15                  # K

delta_g_25 = ____

if ____:
    clasificacion = "espontánea"
elif ____:
    clasificacion = "equilibrio"
else:
    clasificacion = "no espontánea"
print(f"ΔG = {delta_g_25} kJ/mol → {clasificacion}")

T_inversion = ____
print(f"La reacción es espontánea por encima de {T_inversion} K")
""")
        + md("""
# **Temas extra (si hay tiempo): funciones y clases**

> ⏱️ Estos temas se cubren **solo si hay tiempo** en clase; también puedes estudiarlos por tu
> cuenta. No son necesarios para la Sesión 3: ahí, cuando aparece una función, basta con leerla y
> ejecutarla.
""")
        + md("""
## **Tema extra 1: funciones**

Las funciones son bloques de código reutilizable que realizan una tarea específica. Ayudan a
organizar el código, hacerlo más legible y evitar repeticiones. Su estructura básica es:

```python
def nombre_funcion(parametro1, parametro2):
    resultado = parametro1 + parametro2
    return resultado          # Devuelve el resultado a quien llamó a la función
```

Ya conoces varias funciones de Python: `print()`, `input()`, `type()` y `abs()` (valor absoluto).
""")
        + md(r"""
### **Ejemplo: ley de los gases ideales**

**Objetivo:** calcular la presión despejando $PV = nRT$:

$$P = \frac{nRT}{V}$$

donde $n$ es la cantidad de sustancia (mol), $T$ la temperatura (K), $V$ el volumen (L) y $R$ la
constante de los gases, $0.0821~\frac{\text{atm·L}}{\text{mol·K}}$.

Algunos parámetros pueden tener un **valor predeterminado** (como `R=0.0821`); los demás deben
proporcionarse obligatoriamente.
""")
        + code("""
def calcular_presion(n, T, V, R=0.0821):
    \"\"\"Presión (atm) de un gas ideal a partir de n (mol), T (K) y V (L).\"\"\"
    return n * R * T / V

P_atm = calcular_presion(1.0, 298.15, 22.4)   # R toma su valor predeterminado
print(f"La presión calculada es {P_atm:.2f} atm")
""")
        + md("Podemos indicar los argumentos por su nombre y cambiar el valor predeterminado:")
        + code("""
P = calcular_presion(n=1, T=273.15, V=22.4)
print(f"En condiciones normales: {P:.2f} atm")

# Con R en unidades del SI, V debe estar en m³ y el resultado sale en Pa
P_pa = calcular_presion(n=1, T=273.15, V=0.0224, R=8.314)
print(f"En unidades del SI: {P_pa:.0f} Pa")
""")
        + md(r"""
### **Extra 1: Una función para clasificar enlaces**

Convierte tu solución del Ejercicio 3 en la función `clasificar_enlace(delta_chi)`, que **devuelva**
(con `return`) el tipo de enlace. Así podrás clasificar cualquier enlace con una sola línea.
""")
        + ejercicio("extra1", """
def clasificar_enlace(delta_chi):
    ____

# Prueba tu función con distintos enlaces
print("C–H:", clasificar_enlace(abs(chi_C - chi_H)))
print("O–H:", clasificar_enlace(abs(chi_O - chi_H)))
print("Na–Cl:", clasificar_enlace(abs(chi_Na - chi_Cl)))
""")
        + md(r"""
### **Extra 2: Una función para la fórmula de Gauss**

Escribe la función `formula_gauss(n)` que devuelva $\frac{n(n+1)}{2}$ y úsala para calcular de
nuevo `suma_100`, `suma_200` y `suma_300`.
""")
        + ejercicio("extra2", """
def formula_gauss(n):
    ____

suma_100 = formula_gauss(100)
suma_200 = formula_gauss(200)
suma_300 = formula_gauss(300)
print(suma_100, suma_200, suma_300)
""")
        + md("""
## **Tema extra 2: programación orientada a objetos**

Este tema se apoya en el anterior: los métodos de una clase son funciones.

Hasta ahora hemos usado variables sueltas y funciones. En la práctica, los datos suelen estar
agrupados: una sustancia tiene nombre, fórmula y masa molar. Para agruparlos usamos **clases**.

- Una **clase** es un *molde*: define qué datos y qué acciones tendrá cada objeto.
- Un **objeto** (o *instancia*) es un caso concreto creado a partir del molde.
- Los **atributos** son los datos del objeto (el *qué tiene*).
- Los **métodos** son funciones que viven dentro de la clase (el *qué hace*).

| Concepto | Analogía química | En código |
| :--- | :--- | :--- |
| Clase | La ficha técnica de un reactivo | `class Sustancia:` |
| Objeto | Un frasco concreto de NaCl | `nacl = Sustancia(...)` |
| Atributo | Fórmula, masa molar | `self.masa_molar` |
| Método | Convertir gramos a moles | `def gramos_a_moles(self, gramos):` |

El método especial `__init__` (*constructor*) asigna los valores iniciales, y `self` se refiere
al propio objeto.
""")
        + code("""
class Sustancia:
    def __init__(self, nombre, formula, masa_molar):
        self.nombre = nombre
        self.formula = formula
        self.masa_molar = masa_molar      # g/mol

    def gramos_a_moles(self, gramos):
        \"\"\"Convierte una masa en gramos a cantidad de sustancia en mol.\"\"\"
        return gramos / self.masa_molar


agua = Sustancia("Agua", "H2O", 18.015)
print(f"{agua.nombre} ({agua.formula}): {agua.masa_molar} g/mol")

etanol = Sustancia("Etanol", "CH3CH2OH", 46.07)
masa_muestra = 150.0   # g
print(f"En {masa_muestra} g de {etanol.formula} hay {etanol.gramos_a_moles(masa_muestra):.4f} mol.")
""")
        + md("""
### **Extra 3: Objeto cloruro de sodio**

Crea el objeto `cloruro_sodio` con la clase `Sustancia` (nombre, fórmula `"NaCl"` y masa molar
correcta). Después usa su método para calcular los moles en 15 g de NaCl (`moles_nacl`).
""")
        + ejercicio("extra3", """
cloruro_sodio = ____
moles_nacl = ____

print(f"{cloruro_sodio.nombre}: {cloruro_sodio.masa_molar} g/mol")
print(f"En 15 g hay {moles_nacl} mol")
""")
        + md("Creemos ahora una clase para calcular concentraciones de una disolución:")
        + code("""
class Disolucion:
    def __init__(self, masa_soluto, masa_disolvente, volumen_ml, masa_molar):
        self.masa_soluto = masa_soluto                              # g
        self.masa_disolvente = masa_disolvente                      # g
        self.masa_disolucion = masa_soluto + masa_disolvente        # g
        self.volumen_ml = volumen_ml                                # mL de disolución
        self.masa_molar = masa_molar                                # g/mol del soluto

    def porcentaje_masa_masa(self):
        return self.masa_soluto / self.masa_disolucion * 100

    def porcentaje_masa_volumen(self):
        return self.masa_soluto / self.volumen_ml * 100


# 5 g de NaCl en 100 g de agua; el volumen final es de 103 mL
muestra = Disolucion(5, 100, 103, 58.44)
print(f"% m/m: {muestra.porcentaje_masa_masa():.2f} %")
print(f"% m/v: {muestra.porcentaje_masa_volumen():.2f} %")
""")
        + md("""
### **Extra 4: Métodos de la clase `Disolucion`**

Completa la clase `Disolucion` con tres métodos nuevos:

- `calcular_moles()`: mol de soluto.
- `calcular_molaridad()`: mol de soluto / L de disolución.
- `calcular_molalidad()`: mol de soluto / kg de disolvente.

Después calcula los moles en una disolución con 50 g de NaCl, 100 g de agua y 120 mL de volumen
final (`moles_50g`).
""")
        + ejercicio("extra4", """
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
        ____

    def calcular_molaridad(self):
        ____

    def calcular_molalidad(self):
        ____


muestra = Disolucion(5, 100, 103, 58.44)
print(f"Molaridad: {muestra.calcular_molaridad()} mol/L")
print(f"Molalidad: {muestra.calcular_molalidad()} mol/kg")

moles_50g = ____
print(f"En 50 g de NaCl hay {moles_50g} mol")
""")
        + cierre()
    )
