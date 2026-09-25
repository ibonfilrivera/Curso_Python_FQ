"""Contenido de la Sesión 1: fundamentos de Python aplicados a cálculos químicos."""

from bloques import cierre, code, ejercicio, encabezado, instrucciones, md


def fuente(carpeta, archivo):
    return (
        encabezado(1, "Fundamentos de Python para cálculos químicos", """
En esta sesión conoceremos el entorno de Google Colab, realizaremos operaciones básicas,
tomaremos decisiones con condicionales y construiremos nuestras primeras funciones.

**Al terminar podrás:**
- Distinguir los tipos de datos básicos (`int`, `float`, `str`, `bool`).
- Traducir fórmulas químicas a expresiones de Python.
- Usar `if`, `elif` y `else` para clasificar resultados.
- Escribir funciones reutilizables con `def` y `return`.
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
        + md("""
## **Funciones**

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
## **Práctica dirigida: ley de los gases ideales**

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
### **Ejercicio 3: Clasificación de enlaces**

Según la diferencia de electronegatividad $\Delta \chi$ entre dos átomos, podemos predecir el tipo
de enlace que forman:

- Covalente no polar: $\Delta \chi < 0.5$
- Covalente polar: $0.5 \leq \Delta \chi < 1.7$
- Iónico: $\Delta \chi \geq 1.7$

Escribe la función `clasificar_enlace(delta_chi)` que **devuelva** (con `return`) uno de los textos
`"covalente no polar"`, `"covalente polar"` o `"iónico"`. Después úsala con los valores de
electronegatividad (escala de Pauling) de la celda siguiente.
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
def clasificar_enlace(delta_chi):
    ____

# Prueba tu función con distintos enlaces
print("C–H:", clasificar_enlace(abs(chi_C - chi_H)))
print("O–H:", clasificar_enlace(abs(chi_O - chi_H)))
print("Na–Cl:", clasificar_enlace(abs(chi_Na - chi_Cl)))
""")
        + md(r"""
### **Ejercicio 4: Temperatura de un gas ideal**

1. Calcula la cantidad de sustancia `n_agua` en 50.0 g de agua.
2. Define la función `calcular_temperatura(P, V, n, R=0.0821)` que devuelva $T = \frac{PV}{nR}$.
3. Calcula a qué temperatura se cumplen las siguientes condiciones y guarda los resultados en
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

def calcular_temperatura(P, V, n, R=0.0821):
    ____

T1 = calcular_temperatura(P=3.0, V=20.0, n=n_agua)
T2 = ____
print(f"T1 = {T1} K")
print(f"T2 = {T2} K")
""")
        + md("""
## **Resumen de la sesión**

**Tipos de datos:** `int` (enteros), `float` (decimales), `str` (texto), `bool` (`True`/`False`).

**Funciones integradas:** `print()`, `input()`, `type()`, `abs()`.

**Estructuras:**
- `if`, `elif`, `else`: condicionales.
- `def nombre(parámetros): ... return resultado`: funciones.

**Buenas prácticas:**
- Usa nombres de variables descriptivos (`masa_molar_hcl` en lugar de `m`).
- Anota las unidades en comentarios.
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
        + md(r"""
### **Autoevaluación 4: Fórmula de Gauss**

La suma de los primeros $n$ números naturales es:

$$S_n = \frac{n(n+1)}{2}$$

Define la función `formula_gauss(n)` y úsala para sumar los primeros 100, 200 y 300 números
naturales (`suma_100`, `suma_200` y `suma_300`).
""")
        + ejercicio("auto4", """
def formula_gauss(n):
    ____

suma_100 = ____
suma_200 = ____
suma_300 = ____
print(suma_100, suma_200, suma_300)
""")
        + md(r"""
### **Autoevaluación 5: Espontaneidad de una reacción**

El reformado de metano con vapor produce monóxido de carbono e hidrógeno:

$$\text{CH}_4(g) + \text{H}_2\text{O}(g) \rightarrow \text{CO}(g) + 3\,\text{H}_2(g)$$

con $\Delta H^\circ = 206.1~\text{kJ/mol}$ y $\Delta S^\circ = 215~\text{J/(mol·K)}$.

1. Escribe `calcular_delta_g(delta_h, delta_s, T)` que reciba $\Delta H$ en kJ/mol, $\Delta S$ en
   J/(mol·K) y $T$ en K, y devuelva $\Delta G = \Delta H - T\Delta S$ en kJ/mol.
2. Escribe `clasificar_reaccion(delta_g)` que devuelva `"espontánea"` ($\Delta G < 0$),
   `"equilibrio"` ($\Delta G = 0$) o `"no espontánea"` ($\Delta G > 0$).
3. Calcula $\Delta G$ a 25 °C (`delta_g_25`).
4. **Reto:** ¿a partir de qué temperatura la reacción se vuelve espontánea? (`T_inversion`)
""")
        + ejercicio("auto5", """
def calcular_delta_g(delta_h, delta_s, T):
    ____

def clasificar_reaccion(delta_g):
    ____

delta_g_25 = ____
print(f"ΔG = {delta_g_25} kJ/mol → {clasificar_reaccion(delta_g_25)}")

T_inversion = ____
print(f"La reacción es espontánea por encima de {T_inversion} K")
""")
        + cierre()
    )
