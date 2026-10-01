# Guía para asesores: agregar material y ejercicios al curso

No necesitas conocer el sistema de verificación ni instalar nada. Escribe un **notebook normal**
en Google Colab y súbelo a esta carpeta desde la página de GitHub. El sistema lo integra solo a
la sesión que elijas.

## Resumen en 30 segundos

1. Abre [`plantilla_material_adicional.ipynb`](plantilla_material_adicional.ipynb) en Colab y
   guarda una copia en tu Drive.
2. Escribe tu explicación y tus ejercicios **con su solución**, como lo harías normalmente.
3. En cada ejercicio que quieras revisar automáticamente, agrega al inicio de la celda dos o tres
   líneas de comentario: `#@ejercicio`, `#@revisar` y, si quieres, `#@pista`.
4. Ejecuta todo el notebook (*Entorno de ejecución → Ejecutar todas*): no debe haber errores.
5. Descárgalo (*Archivo → Descargar → Descargar .ipynb*) y súbelo a `contenido_extra/sesion1/`,
   `sesion2/` o `sesion3/` (*Add file → Upload files* en GitHub).

Unos 5 minutos después, tu material aparece al final de esa sesión, en la sección **«Material
adicional»**, tanto en el notebook de estudiantes como en el solucionario.

## Cómo se marca un ejercicio

Escribe la celda con la **solución completa** y agrega las marcas en las primeras líneas:

```python
#@ejercicio Densidad del etanol
#@revisar densidad g/mL
#@pista La densidad es la masa dividida entre el volumen.
masa = 39.45       # g
volumen = 50.0     # mL
densidad = masa / volumen
print(f"Densidad del etanol: {densidad:.3f} g/mL")
```

El sistema hace el resto:

| Tú escribes | El estudiante ve |
| :--- | :--- |
| `densidad = masa / volumen` | `densidad = ____` (el resto de la celda queda igual) |
| La solución completa | Disponible con `adic1.solucion()` y en el solucionario |
| `#@pista ...` | `adic1.pista()` |
| `#@revisar densidad g/mL` | `adic1.verificar()` compara su `densidad` con el valor de tu solución |

| Marca | Para qué sirve |
| :--- | :--- |
| `#@ejercicio Título` | **Obligatoria.** Va en la primera línea e indica que la celda es un ejercicio. |
| `#@revisar variable` | Variable cuyo valor se revisa. Puedes poner varias líneas `#@revisar`. |
| `#@revisar variable g/mL` | Agrega las unidades: si el estudiante usa pint, se convierten solas. |
| `#@revisar variable tol=1%` | Cambia la tolerancia (por defecto, 0.1 %). |
| `#@pista Texto` | La pista que verá el estudiante. |

Se pueden revisar números, textos, `True`/`False`, listas y arreglos de NumPy. La variable debe
asignarse en una línea propia (`variable = ...`), fuera de ciclos y funciones.

## ¿Y si no quiero, o no puedo, preparar la verificación?

No pasa nada; el curso sigue funcionando igual. Hay tres niveles, y todos son válidos:

| Lo que entregas | Lo que ve el estudiante |
| :--- | :--- |
| **Solo texto y código**, sin marcas | Tu material tal cual, como un notebook normal. Los ejercicios se revisan en clase. |
| **Ejercicio con `#@ejercicio`, sin `#@revisar`** | Una celda vacía con el aviso «sin verificación automática». Tu solución queda en el solucionario. |
| **Ejercicio con `#@ejercicio` y `#@revisar`** | La experiencia completa: `____`, verificación, pista y solución. |

Más adelante, la coordinación puede convertir cualquier ejercicio en verificable agregando las dos
líneas de marcas; no hace falta reescribir nada.

## Reglas para que todo funcione

- **El notebook debe ejecutarse de principio a fin sin errores**, porque el sistema ejecuta tus
  soluciones para obtener las respuestas correctas.
- **Incluye tus `import`** (por ejemplo, `import numpy as np`) dentro de tu notebook: se ejecuta
  por separado del resto de la sesión.
- **Usa las bibliotecas del curso**: NumPy, pandas, SciPy, Matplotlib, SymPy, pint y RDKit.
- **Datos:** sube tus archivos CSV a la carpeta `data/` y léelos con su dirección de GitHub, para
  que funcionen en Colab:
  `pd.read_csv("https://raw.githubusercontent.com/ibonfilrivera/Curso_Python_FQ/main/data/mi_archivo.csv")`
- **Orden:** los notebooks de una carpeta se agregan en orden alfabético. Usa nombres como
  `01_densidad.ipynb` y `02_titulacion.ipynb`.
- **No edites** los notebooks de `notebooks_verificador/` ni de `soluciones/`: se generan
  automáticamente y los cambios hechos a mano se pierden. Si lo intentas, GitHub detiene la
  publicación y te avisa.

## ¿Cómo sé si funcionó?

En la pestaña **Actions** del repositorio aparece «Pruebas del curso»:

- ✅ **Verde:** tu material ya está en los notebooks. GitHub hizo un commit automático llamado
  «Regenerar notebooks con el material de contenido_extra/».
- ❌ **Rojo:** abre la ejecución y busca el paso que falló. El mensaje dice qué archivo y qué celda
  revisar; por ejemplo: «01_densidad.ipynb, ejercicio «Densidad»: No encontré una línea
  `densidad = ...`». Corrige tu notebook y vuelve a subirlo con el mismo nombre.

## Quiero cambiar algo que ya existe en el curso

El contenido original de las sesiones se escribe en `herramientas/contenido_sesionN.py`, en un
formato que solo necesita conocer la coordinación. Para proponer cambios:

1. **Cambios pequeños** (una errata, un dato, una frase): abre un *Issue* en GitHub o comenta con
   la coordinación qué celda cambiar y cómo.
2. **Cambios grandes:** haz tus cambios en una copia del notebook en Colab y envíala a la
   coordinación. Con `python herramientas/comparar_notebook.py tu_copia.ipynb
   notebooks_verificador/Sesion_1.ipynb`, la coordinación ve exactamente qué celdas cambiaste y los
   traslada a la fuente.
3. **Material nuevo:** mejor como notebook en esta carpeta; así no hace falta esperar a nadie.
