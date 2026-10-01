"""Contenido de la Sesión 1: fundamentos de Python aplicados a cálculos químicos."""

from bloques import cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(1, "Fundamentos de Python, NumPy y unidades", """
En esta sesión conoceremos el entorno de Google Colab, realizaremos operaciones básicas,
trabajaremos con muchos datos a la vez usando **NumPy** y aprenderemos a cuidar las unidades con
**pint**.

**Al terminar podrás:**
- Distinguir los tipos de datos básicos (`int`, `float`, `str`, `bool`).
- Traducir fórmulas químicas a expresiones de Python.
- Resumir datos experimentales y operar con vectores y matrices usando NumPy.
- Evitar errores de unidades, como los factores de 1000, con la biblioteca pint.
""", carpeta, archivo)
        + instrucciones(1)
        + md("""
## **Contexto y motivación**

Programar es una habilidad valiosa porque fomenta el pensamiento lógico para resolver problemas
y permite automatizar tareas repetitivas, como los cálculos que solemos hacer en una hoja de cálculo.

Entre los lenguajes de programación, Python destaca por su sintaxis clara y legible, su
versatilidad en ciencia de datos y automatización, y su enorme comunidad, que ofrece gran
cantidad de recursos y bibliotecas científicas.

**Recursos para reforzar las bases**
- [Kaggle Learn: Intro to Programming](https://www.kaggle.com/learn/intro-to-programming)
- [Tutorial oficial de Python (en español)](https://docs.python.org/es/3/tutorial/)
""")
        + md(r"""
## **Tipos de celdas**

1. **Celda de texto** (*Markdown*): sirve para explicaciones y fórmulas en LaTeX, como la
   ecuación de van der Waals:

$$ \left(P + \frac{an^2}{V^2}\right)(V - nb) = nRT $$

2. **Celda de código**: sirve para ejecutar instrucciones de Python. Se ejecuta con
   `Shift + Enter` o con el botón ▶.
""")
        + code("""
print("¡Hola, mundo!")
""")
        + code("""
# Con input() el programa le pide información a quien lo usa
nombre = input("Introduce tu nombre: ")

# Con print() mostramos información; las cadenas f"..." insertan variables entre llaves
print(f"Tu nombre es {nombre}.")
""")
        + md("""
## **Tipos de datos**

En química manejamos distintos tipos de información:

| Tipo | Nombre en Python | Ejemplo químico |
| :--- | :--- | :--- |
| Entero | `int` | Número de átomos o de muestras |
| Decimal | `float` | Concentración, masa molar |
| Texto | `str` | Nombre o fórmula de una sustancia |
| Lógico | `bool` | ¿La disolución es ácida? (`True` / `False`) |
""")
        + code("""
# Modifica los valores de las variables y vuelve a ejecutar la celda
nombre_compuesto = "HCl"    # str
numero_muestras = 3         # int
concentracion_molar = 0.5   # float (mol/L)

print(f"Se analizaron {numero_muestras} muestras de {nombre_compuesto} "
      f"con una concentración de {concentracion_molar} mol/L.")
""")
        + md("Puedes consultar el tipo de una variable con la función `type()`.")
        + code("type(concentracion_molar)")
        + md("""
## **Operaciones básicas**

| Operación | Símbolo | Ejemplo | Resultado |
| :--- | :---: | :--- | :--- |
| Suma | `+` | `7 + 2` | `9` |
| Resta | `-` | `7 - 2` | `5` |
| Multiplicación | `*` | `7 * 2` | `14` |
| División | `/` | `7 / 2` | `3.5` |
| División entera | `//` | `7 // 2` | `3` |
| Residuo | `%` | `7 % 2` | `1` |
| Potencia | `**` | `7 ** 2` | `49` |

Python respeta la jerarquía de operaciones: primero paréntesis, luego potencias, después
multiplicaciones y divisiones y, al final, sumas y restas.
""")
        + code("""
# Podemos operar con números...
3 ** 2
""")
        + code("""
# ...con variables...
a = 3
b = 2
a ** b
""")
        + code("""
# ...o con ambos
a ** 2
""")
        + md(r"""
### **Ejercicio 1: Jerarquía de operaciones**

Guarda en la variable `x` el resultado de la siguiente operación, respetando la jerarquía de
operaciones:

$$ x = \frac{(8)(10) + (2)(11)}{20-4} $$
""")
        + ejercicio("ej1", """
# Escribe la operación completa en una sola línea
x = ____

print(f"x = {x}")
""")
        + md("""
## **El orden de ejecución importa**

Las variables guardan el **último valor asignado**, sin importar en qué lugar del notebook esté
la celda. Si usas una variable que no se ha definido, Python mostrará un `NameError`.
""")
        + code("""
a = 1
b = 2
print(f"Inicio: a = {a}, b = {b}")
""")
        + code("""
# Ejecuta esta celda varias veces. ¿Qué observas?
a = a * b
print(f"Ahora: a = {a}, b = {b}")
""")
        + md("""
> **Actividad:** reinicia la sesión (*Entorno de ejecución → Reiniciar sesión*) y ejecuta
> únicamente la celda anterior. ¿Por qué aparece un error? (Recuerda volver a ejecutar la celda
> de configuración después).
""")
        + md(r"""
## **Ejemplo: operaciones en química**

¿Cuántas moléculas hay en 1.0 g de HCl?

- Masa de HCl: $1.0~\text{g}$
- Masa molar de HCl: $36.46~\text{g/mol}$
- Constante de Avogadro: $N_A = 6.022 \times 10^{23}~\text{mol}^{-1}$

$$ N = 1.0~\text{g HCl}
\left( \frac{1~\text{mol HCl}}{36.46~\text{g HCl}} \right)
\left( \frac{6.022\times 10^{23}~\text{moléculas}}{1~\text{mol HCl}} \right)
= 1.65 \times 10^{22}~\text{moléculas} $$

Un buen programa sigue tres pasos: **definir datos → calcular → mostrar resultados**.
""")
        + code("""
# 1. Definir datos (con sus unidades en un comentario)
masa_hcl = 1.0                  # g
masa_molar_hcl = 36.46          # g/mol
constante_avogadro = 6.022e23   # mol⁻¹  (6.022e23 significa 6.022 × 10²³)

# 2. Calcular
numero_moleculas = masa_hcl / masa_molar_hcl * constante_avogadro

# 3. Mostrar el resultado; :.2e lo escribe en notación científica con 2 decimales
print(f"Hay {numero_moleculas:.2e} moléculas en {masa_hcl} g de HCl.")
""")
        + md("""
### **Ejercicio 2a: Conversión de masa a moles**

Calcula la cantidad de sustancia (`moles_hcn`) en 10.0 g de cianuro de hidrógeno (HCN).
Investiga su masa molar y guárdala en `masa_molar_hcn`.
""")
        + ejercicio("ej2a", """
masa_hcn = 10.0          # g
masa_molar_hcn = ____    # g/mol

moles_hcn = ____
print(f"Moles de HCN: {moles_hcn}")
""")
        + md("""
### **Ejercicio 2b: Número de moléculas**

Calcula el número de moléculas de HCN (`moleculas_hcn`). Aprovecha las variables que ya
definiste en las celdas anteriores.
""")
        + ejercicio("ej2b", """
moleculas_hcn = ____
print(f"Moléculas de HCN: {moleculas_hcn}")
""")
        + md("""
## **Introducción a NumPy**

Hasta ahora cada variable guarda un solo número. En el laboratorio, en cambio, trabajamos con
**muchos datos a la vez**: réplicas de una medición, una serie de temperaturas o las
concentraciones de una curva de calibración.

**NumPy** es la biblioteca base del cómputo científico en Python. Una **biblioteca** es un
conjunto de funciones que alguien más escribió y que podemos reutilizar; se carga con `import` y
es costumbre darle un alias corto. NumPy ofrece los **arreglos** (`np.array`): colecciones de
números, escritas entre corchetes `[ ]`, con las que podemos operar todos los elementos a la vez.
""")
        + code("""
import numpy as np
""")
        + code("""
# Cuatro réplicas de la valoración de una disolución de NaOH (mol/L)
replicas = np.array([0.1012, 0.1008, 0.1015, 0.1010])

print("Número de réplicas:", len(replicas))
print(f"Promedio: {replicas.mean():.4f} mol/L")
print(f"Desviación estándar: {replicas.std(ddof=1):.4f} mol/L")   # ddof=1: muestral
print(f"Mínimo y máximo: {replicas.min()} y {replicas.max()} mol/L")
""")
        + md("Una operación con un arreglo se aplica a **todos** sus elementos, sin tener que repetirla uno por uno:")
        + code("""
temperaturas_C = np.array([0.0, 25.0, 37.0, 100.0])
print("En kelvin:", temperaturas_C + 273.15)

# Moles de soluto en distintos volúmenes de una disolución 0.1 mol/L
volumenes_L = np.array([0.010, 0.025, 0.050])
print("Moles:", 0.1 * volumenes_L)
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
Cada elemento de un arreglo tiene una **posición** (índice) que empieza en **0**. Además podemos
extraer filas o columnas completas con **rebanadas** (*slicing*): `arr[fila, columna]`, donde `:`
significa "todas".
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
### **Ejercicio 3: Matriz de rotación**

Para rotar un vector en $\mathbb{R}^2$ un ángulo $\theta$ se multiplica por la matriz de rotación:

$$R(\theta) = \begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{pmatrix}$$

Construye la matriz `R` para θ = 90° y guarda en `v_rotado` el vector (3, 4) rotado. Recuerda
que `np.cos` y `np.sin` trabajan en **radianes**.
""")
        + ejercicio("ej3", """
theta = np.radians(90)            # 90° en radianes
R = np.array([[____, ____],
              [____, ____]])
v = np.array([3, 4])

v_rotado = ____
print(v_rotado)
""")
        + md(r"""
### **Ejercicio 4: Regla de Cramer**

Para un sistema de $2 \times 2$

$$\begin{aligned}
3x + 2y &= 12 \\
4x - y &= 5
\end{aligned}$$

la regla de Cramer da $x = \frac{\Delta_x}{\Delta}$ y $y = \frac{\Delta_y}{\Delta}$, donde $\Delta$
es el determinante de la matriz de coeficientes, y $\Delta_x$ y $\Delta_y$ son los determinantes de
esa matriz con la primera o la segunda columna sustituida por los resultados.

Calcula `delta`, `x` y `y`, y compara con `np.linalg.solve`.
""")
        + ejercicio("ej4", """
A = np.array([[3, 2], [4, -1]], dtype=float)
b = np.array([12, 5], dtype=float)

delta = ____

A_x = A.copy()
A_x[:, 0] = b           # Primera columna sustituida por b
A_y = A.copy()
____                    # Segunda columna sustituida por b

x = ____
y = ____
print(f"x = {x}, y = {y}")
print("Con np.linalg.solve:", np.linalg.solve(A, b))
""")
        + md("""
## **Unidades con pint**

Muchos errores en los cálculos químicos no son de programación sino de **unidades**: usar mL
donde iban L, g donde iban kg o °C donde iba K. El resultado sale 1000 veces más grande o más
pequeño, y Python no se queja porque solo ve números.

La biblioteca **pint** une cada número con su unidad. Así, las conversiones se hacen solas y
Python se detiene si intentas combinar unidades incompatibles.
""")
        + code("""
try:
    import pint
except ImportError:                     # Si no está instalada (por ejemplo, en Colab)
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pint"], check=True)

from pint import UnitRegistry

ureg = UnitRegistry()     # Catálogo de unidades
Q_ = ureg.Quantity        # Atajo para crear cantidades, útil con temperaturas
""")
        + md("Una **cantidad** es un número multiplicado por una unidad. Con `.to()` se convierte a otra unidad:")
        + code("""
volumen = 250 * ureg.mL
masa = 2.5 * ureg.kg

print(volumen.to("L"))
print(masa.to("g"))
print((1 * ureg.atm).to("kPa"))
print(f"{(8.314 * ureg('J/(mol*K)')).to('L*atm/(mol*K)'):.5f}")   # R en otras unidades
""")
        + md("""
Las unidades se multiplican y se dividen junto con los números. Veamos el error típico de
calcular una concentración con el volumen en mililitros:
""")
        + code("""
moles = 0.0428 * ureg.mol
volumen = 250 * ureg.mL

concentracion = moles / volumen
print(concentracion)                  # mol/mL: correcto, pero en unidades poco usuales
print(concentracion.to("mol/L"))      # pint hace la conversión por ti
""")
        + md("Si combinas unidades incompatibles, pint lanza un `DimensionalityError` en lugar de darte un resultado sin sentido:")
        + code("""
masa = 5 * ureg.g
volumen = 100 * ureg.mL

masa + volumen      # ¿Sumar gramos con mililitros? Error a propósito
""", error_esperado=True)
        + md("""
Las temperaturas en °C necesitan cuidado: 20 °C no es «el doble» de 10 °C. Crea la cantidad con
`Q_(valor, ureg.degC)` y conviértela a kelvin antes de multiplicar o dividir.
""")
        + code("""
T = Q_(25.0, ureg.degC)
print(T.to("K"))
""")
        + md(r"""
### **Ejercicio 5a: Gas ideal con unidades**

Calcula la presión de 0.250 mol de un gas ideal a 25.0 °C en un recipiente de 500 mL, usando
$R = 0.082057~\frac{\text{L·atm}}{\text{mol·K}}$ y $P = \frac{nRT}{V}$.

- Guarda en `presion` el resultado en **atm** (usa `.to("atm")`).
- Guarda en `presion_kpa` la misma presión en **kPa**.

Observa que no necesitas convertir los mL ni los °C a mano.
""")
        + ejercicio("ej5a", """
n = 0.250 * ureg.mol
T = Q_(25.0, ureg.degC)
V = ____
R = 0.082057 * ureg("L * atm / (mol * K)")

presion = ____
presion_kpa = ____
print(presion, presion_kpa)
""")
        + md("""
### **Ejercicio 5b: Molaridad con unidades**

Se disuelven 2.50 g de NaCl (58.44 g/mol) y se aforan a 250 mL. Calcula la molaridad en
`molaridad`, como cantidad de pint expresada en mol/L.
""")
        + ejercicio("ej5b", """
masa = ____
masa_molar = 58.44 * ureg("g/mol")
volumen = ____

molaridad = ____
print(molaridad)
""")
        + md("""
## **Resumen de la sesión**

**Tipos de datos:** `int` (enteros), `float` (decimales), `str` (texto), `bool` (`True`/`False`).

**Funciones integradas:** `print()`, `input()`, `type()`, `abs()`.

**NumPy:** `np.array()` crea arreglos; las operaciones se aplican a todos los elementos a la vez
(`temperaturas + 273.15`); `.mean()`, `.std()`, `.min()` y `.max()` resumen datos; `@` es el
producto matricial y `np.linalg` calcula determinantes y resuelve sistemas de ecuaciones.

**pint:** `ureg = UnitRegistry()` crea el catálogo de unidades; `5 * ureg.mL` es una cantidad;
`.to("L")` convierte; `Q_(25, ureg.degC)` crea temperaturas. Combinar unidades incompatibles
produce un `DimensionalityError`, que es justo lo que queremos.

**Buenas prácticas:**
- Intenta primero; usa la pista para entender, no para saltarte el ejercicio.
- Usa nombres de variables descriptivos (`masa_molar_hcl` en lugar de `m`).
- Anota las unidades en comentarios o, mejor aún, usa pint.
- Separa tu código en *datos → cálculo → resultado*.
""")
        + md("""
## **Ejercicios de autoevaluación**

Intenta resolver cada ejercicio por tu cuenta antes de pedir una pista o ver la solución.
""")
        + md(r"""
### **Autoevaluación 1: Conversión de temperatura**

Convierte $300~°\text{C}$ a kelvin con $T[\text{K}] = T[°\text{C}] + 273.15$ y guarda el resultado en `T_K`.
""")
        + ejercicio("auto1", """
T_C = 300
T_K = ____

print(f"T = {T_K} K")
""")
        + md(r"""
### **Autoevaluación 2: Disoluciones**

Se tiene una disolución madre de NaOH 0.5 mol/L. Si se toma una alícuota de 10.0 mL y se afora a
50.0 mL, ¿cuál es la concentración de la nueva disolución? Usa $C_1V_1 = C_2V_2$ y guarda el
resultado en `C_2`.
""")
        + ejercicio("auto2", """
C_1 = ____   # mol/L
V_1 = ____   # mL
V_2 = ____   # mL

C_2 = ____
print(f"C₂ = {C_2} mol/L")
""")
        + md("""
### **Autoevaluación 3: Caminata hasta la Luna**

La distancia de la Tierra a la Luna es de 384 400 km y el paso promedio de una persona mide
aproximadamente 70 cm.

1. ¿Cuántos pasos se necesitan para recorrer esa distancia? (`numero_pasos`)
2. Caminando a 5 km/h, ¿cuántas horas tomaría? (`tiempo_h`)
3. A ese ritmo, una persona de 70 kg gasta alrededor de 240 kcal por hora. ¿Cuánta energía
   requiere la caminata? (`energia_kcal`)
4. ¿Cuál es el costo energético de cada paso? (`costo_por_paso`)
""")
        + ejercicio("auto3", """
distancia_km = 384_400   # Python permite separar los miles con _
paso_cm = 70
rapidez_km_h = 5.0
gasto_kcal_h = 240

numero_pasos = ____
tiempo_h = ____
energia_kcal = ____
costo_por_paso = ____

print(f"Pasos: {numero_pasos}")
print(f"Tiempo: {tiempo_h} h")
print(f"Energía: {energia_kcal} kcal")
print(f"Costo por paso: {costo_por_paso} kcal/paso")
""")
        + md("""
### **Autoevaluación 4: Conversión de varias temperaturas**

Convierte a kelvin, con un arreglo de NumPy, las temperaturas de sublimación del hielo seco
(−78.5 °C), de fusión del hielo (0 °C), ambiente (25 °C), corporal (37 °C) y de ebullición del
agua (100 °C). Guarda el resultado en `temperaturas_K`.
""")
        + ejercicio("auto4", """
temperaturas_C = np.array([-78.5, 0.0, 25.0, 37.0, 100.0])
temperaturas_K = ____
print(temperaturas_K)
""")
        + md(r"""
### **Autoevaluación 5: Energía libre a varias temperaturas**

El reformado de metano con vapor produce monóxido de carbono e hidrógeno:

$$\text{CH}_4(g) + \text{H}_2\text{O}(g) \rightarrow \text{CO}(g) + 3\,\text{H}_2(g)$$

con $\Delta H^\circ = 206.1~\text{kJ/mol}$ y $\Delta S^\circ = 215~\text{J/(mol·K)}$.

1. Con el arreglo de temperaturas `T`, calcula $\Delta G = \Delta H - T\Delta S$ en kJ/mol para
   todas a la vez (`delta_g`). Cuida las unidades de $\Delta S$.
2. ¿A partir de qué temperatura la reacción se vuelve espontánea ($\Delta G < 0$)? Calcúlala en
   `T_inversion`, igualando $\Delta G = 0$.
""")
        + ejercicio("auto5", """
delta_h = 206.1                 # kJ/mol
delta_s = ____                  # kJ/(mol·K)
T = np.array([298.15, 500.0, 750.0, 1000.0, 1250.0])   # K

delta_g = ____
print(delta_g)

T_inversion = ____
print(f"ΔG = 0 a {T_inversion} K")
""")
        + cierre()
    )
