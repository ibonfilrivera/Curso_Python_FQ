"""Contenido de la Sesión 2: estructuras de datos, ciclos y clases."""

from bloques import cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(2, "Estructuras de datos, ciclos y NumPy", """
En la sesión anterior aprendimos los tipos de datos, las operaciones y los condicionales
(`if`, `elif`, `else`). Ahora aprenderemos a **guardar colecciones de datos** (`list`, `tuple`,
`dict`), a **repetir instrucciones** con los ciclos `for` y `while`, y a hacer cálculos con
vectores y matrices usando **NumPy**. Si queda tiempo, veremos como tema extra una introducción
a la programación orientada a objetos.

**Al terminar podrás:**
- Crear, consultar y modificar listas, tuplas y diccionarios.
- Recorrer colecciones con `for` y repetir cálculos con `while`.
- Filtrar datos experimentales de forma automática, con ciclos y con máscaras de NumPy.
- Operar con vectores y matrices y resolver sistemas de ecuaciones con NumPy.
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
### **Ejercicio 3: Ahorros**

Ahorras \\$300 pesos al mes para comprar un celular que cuesta \\$7,000 pesos.

1. Con un `for`, construye la lista `ahorros` con lo que habrás ahorrado a los 10, 20 y 30 meses.
2. Con un `while`, calcula `meses_necesarios` para poder comprar el celular.
""")
        + ejercicio("ej3", """
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
### **Ejercicio 4: Clasificación de muestras**

Recorre `mediciones` y construye dos listas con los **índices** (posiciones) de las muestras:

- `indices_peligrosas`: concentración mayor a 50 ppm y menor o igual a 100 ppm.
- `indices_criticas`: concentración mayor a 100 ppm.
""")
        + ejercicio("ej4", """
indices_peligrosas = []
indices_criticas = []

for i, concentracion in enumerate(mediciones):
    ____

print(f"Muestras peligrosas: {len(indices_peligrosas)}")
print(f"Muestras críticas: {len(indices_criticas)}")
""")
        + md("""
## **Introducción a NumPy**

Las listas de Python son flexibles, pero lentas para cálculos numéricos. **NumPy** es la
biblioteca base del cómputo científico en Python: ofrece los **arreglos** (`np.array`), que
permiten operar con todos los elementos a la vez, sin escribir un ciclo, y son mucho más rápidos.

Una **biblioteca** es un conjunto de funciones que alguien más escribió y que podemos reutilizar.
Se carga con `import`, y es costumbre darle un alias corto:
""")
        + code("""
import time

import numpy as np
""")
        + md("Comparemos el tiempo para elevar al cuadrado un millón de números con una lista y con un arreglo:")
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
        + md("""
Con arreglos, el ejercicio de las muestras peligrosas se resuelve **sin ciclo**: una comparación
produce un arreglo de `True`/`False` (una *máscara*) que sirve para filtrar.
""")
        + code("""
concentraciones = np.array(mediciones)

peligrosas = (concentraciones > 50) & (concentraciones <= 100)   # Máscara booleana
print(f"Peligrosas: {peligrosas.sum()} muestras")
print(f"Índices: {np.where(peligrosas)[0]}")
print(f"Concentración promedio de las peligrosas: {concentraciones[peligrosas].mean():.1f} ppm")
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
### **Ejercicio 5: Matriz de rotación**

Para rotar un vector en $\mathbb{R}^2$ un ángulo $\theta$ se multiplica por la matriz de rotación:

$$R(\theta) = \begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{pmatrix}$$

Escribe la función `rotar_vector(vector, angulo_grados)` que devuelva el vector rotado.
""")
        + ejercicio("ej5", """
def rotar_vector(vector, angulo_grados):
    theta = ____
    R = ____
    return ____

print(rotar_vector([1, 0], 90))   # Debe dar aproximadamente [0, 1]
""")
        + md(r"""
### **Ejercicio 6: Regla de Cramer**

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
        + ejercicio("ej6", """
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
## **Resumen de la sesión**

| Estructura | Sintaxis | ¿Mutable? | Acceso |
| :--- | :--- | :---: | :--- |
| Lista | `[a, b, c]` | Sí | Por índice: `lista[0]` |
| Tupla | `(a, b, c)` | No | Por índice: `tupla[0]` |
| Diccionario | `{"clave": valor}` | Sí | Por clave: `dic["clave"]` |

**Funciones y métodos útiles:** `len()`, `max()`, `min()`, `sum()`, `lista.append(x)`,
`lista.remove(x)`, `range()`, `enumerate()`, `dic.items()`.

**Ciclos:**
- `for`: recorre cada elemento de una secuencia.
- `while`: repite mientras una condición sea verdadera. ¡Asegúrate de que en algún momento sea falsa!
- `break`: sale del ciclo.

**NumPy:** `np.array()` crea arreglos; las operaciones se aplican a todos los elementos a la vez
(`arreglo**2`), las máscaras filtran (`arreglo[arreglo > 50]`), `@` es el producto matricial y
`np.linalg` resuelve sistemas de ecuaciones, determinantes y valores propios.

**Tema extra, clases:** `class` define el molde; `__init__` asigna los atributos; los métodos son
funciones que reciben `self` para acceder a los datos del objeto.
""")
        + md("## **Ejercicios de autoevaluación**")
        + md("""
### **Autoevaluación 1: Serie de Fibonacci con `for`**

Escribe la función `fibonacci_for(n)` que **devuelva una lista** con los primeros `n` números de
la serie de Fibonacci, $F_n = F_{n-1} + F_{n-2}$. Los primeros elementos son 0 y 1, así que
`fibonacci_for(6)` debe devolver `[0, 1, 1, 2, 3, 5]`.

¿Tu función funciona también con `n = 1` y `n = 2`?
""")
        + ejercicio("auto1", """
def fibonacci_for(n):
    ____

fibonacci_for(10)
""")
        + md("""
### **Autoevaluación 2: Serie de Fibonacci con `while`**

Resuelve el mismo problema con un ciclo `while` en la función `fibonacci_while(n)`.

> 🤔 ¿Por qué la condición correcta es `len(serie) < n` y no `len(serie) <= n`? Prueba ambas y
> compara los resultados.
""")
        + ejercicio("auto2", """
def fibonacci_while(n):
    ____

fibonacci_while(10)
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
        + md("""
## **Tema extra: programación orientada a objetos**

> ⏱️ Esta sección se cubre **solo si hay tiempo** en clase; también puedes estudiarla por tu cuenta.
> No es necesaria para la Sesión 3.

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
### **Extra 1: Objeto cloruro de sodio**

Crea el objeto `cloruro_sodio` con la clase `Sustancia` (nombre, fórmula `"NaCl"` y masa molar
correcta). Después usa su método para calcular los moles en 15 g de NaCl (`moles_nacl`).
""")
        + ejercicio("extra1", """
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
### **Extra 2: Métodos de la clase `Disolucion`**

Completa la clase `Disolucion` con tres métodos nuevos:

- `calcular_moles()`: mol de soluto.
- `calcular_molaridad()`: mol de soluto / L de disolución.
- `calcular_molalidad()`: mol de soluto / kg de disolvente.

Después calcula los moles en una disolución con 50 g de NaCl, 100 g de agua y 120 mL de volumen
final (`moles_50g`).
""")
        + ejercicio("extra2", """
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
