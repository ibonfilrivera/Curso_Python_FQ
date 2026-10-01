# Curso de Python — Facultad de Química (UNAM)

[![Pruebas del curso](https://github.com/ibonfilrivera/Curso_Python_FQ/actions/workflows/pruebas.yml/badge.svg)](https://github.com/ibonfilrivera/Curso_Python_FQ/actions/workflows/pruebas.yml)

Material didáctico, código y datos del curso introductorio de Python del Departamento de Física
y Química Teórica. Curso intensivo de 12 horas (3 sesiones de 4 horas) en Google Colab.

**Elaboraron:** Iván Bonfil, Rafael Rodriguez, Roberto Rojas y Lizeth Franco Nolasco.

## 📅 Estructura del curso

| Sesión | Temas | Aplicaciones químicas | Abrir en Colab |
| :--- | :--- | :--- | :---: |
| **1** | Tipos de datos, operaciones, NumPy, unidades con pint | Moles y moléculas, réplicas, rotaciones y sistemas de ecuaciones, gases y disoluciones con unidades, ΔG | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_1.ipynb) |
| **2** | Listas, tuplas, diccionarios, `if`/`elif`/`else`, `for`, `while` · *temas extra:* funciones y clases | Masas molares, tipo de enlace, gases ideales, vida media, control de calidad, espontaneidad | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_2.ipynb) |
| **3** | SciPy, Matplotlib, Pandas, RDKit · *proyecto final opcional* | Cinética, ley de Lambert-Beer, regla de Lipinski, solubilidad, pKa aparente de nanopartículas | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_3.ipynb) |

## ✅ Ejercicios con verificación automática

Los notebooks de `notebooks_kaggle/` funcionan como los cursos de
[Kaggle Learn](https://www.kaggle.com/learn): cada ejercicio trae espacios `____` por completar
y una celda que revisa la respuesta.

```python
ej1.verificar()   # ✅ Correcto / ❌ Incorrecto (con una explicación) / ✏️ Pendiente
ej1.pista()       # Una ayuda sin revelar la respuesta
ej1.solucion()    # La solución de referencia
progreso()        # Resumen de ejercicios resueltos en la sesión
```

La primera celda de cada notebook descarga el paquete `verificador/` desde este repositorio,
así que funciona en Colab sin instalar nada.

El verificador acepta respuestas con unidades de [pint](https://pint.readthedocs.io): si un
estudiante responde `370 * ureg.mmol` donde se esperaban mol, convierte antes de comparar, y
avisa si las unidades no son compatibles.

## ➕ Material de otros asesores

Cualquier asesor puede agregar secciones y ejercicios **sin conocer el sistema de verificación**:
escribe un notebook normal en Colab con sus soluciones, marca los ejercicios con
`#@ejercicio` / `#@revisar` y lo sube a `contenido_extra/sesionN/`. GitHub Actions lo integra al
final de la sesión, genera la versión del estudiante y su verificación, ejecuta las pruebas y
publica los notebooks. Los ejercicios sin marcas también se integran, solo que sin verificación
automática. Guía completa: [`contenido_extra/README.md`](contenido_extra/README.md); resumen para
quien quiera contribuir: [`CONTRIBUTING.md`](CONTRIBUTING.md).

## 📋 Seguimiento del grupo

Si el equipo docente lo activa, cada verificación se registra en una hoja de cálculo de Google
(nunca se envía el código de los estudiantes). La hoja muestra en vivo el estado de cada
estudiante, y el notebook `seguimiento/Tablero_docente.ipynb` indica qué ejercicios necesitan
repaso y quién necesita ayuda. La estrategia y la instalación están en
[`seguimiento/README.md`](seguimiento/README.md).

## 📁 Contenido del repositorio

```
Curso_Python_FQ/
├── notebooks_kaggle/     Notebooks para estudiantes (con verificación automática)
├── soluciones/           Solucionarios para el equipo docente
├── notebooks/            Versión original del curso (referencia)
├── verificador/          Paquete que revisa los ejercicios (uno por sesión) y registro opcional
├── seguimiento/          Estrategia, Apps Script y tablero para el seguimiento del grupo
├── contenido_extra/      Material de otros asesores (se integra automáticamente)
├── herramientas/         Generador de los notebooks y de los datos simulados
├── pruebas/              Pruebas automáticas (pytest y ejecución de todos los notebooks)
├── .github/workflows/    Integración continua en GitHub Actions
└── data/                 AqSolDB, datos de Lambert-Beer y del proyecto final
```

## 🛠️ Para el equipo docente: modificar el material

Los notebooks de `notebooks_kaggle/` y `soluciones/` se **generan** con un script; no se editan
a mano, para que las dos versiones no se desincronicen.

1. Edita el texto y el código de una sesión en `herramientas/contenido_sesionN.py`.
2. Edita la revisión, la pista o la solución de un ejercicio en `verificador/sesionN.py`.
3. Regenera los notebooks:

   ```bash
   pip install nbformat
   python herramientas/construir_notebooks.py
   ```

4. Comprueba que todo funcione antes de subir los cambios:

   ```bash
   pip install -r pruebas/requirements.txt
   pytest -q pruebas                       # Pruebas del verificador
   python pruebas/ejecutar_notebooks.py    # Ejecuta todos los notebooks
   ```

### Integración continua

Con cada `push` a `main` (y en cada *pull request*), GitHub Actions ejecuta
[`.github/workflows/pruebas.yml`](.github/workflows/pruebas.yml): regenera los notebooks (con el
material de `contenido_extra/`) y comprueba que:

- el código del verificador pasa `ruff`, y el Apps Script no tiene errores de sintaxis;
- nadie editó a mano los notebooks generados (si el push solo trae material nuevo o cambios en
  las fuentes, los notebooks regenerados se suben automáticamente al terminar);
- los datos simulados de Lambert-Beer se reproducen idénticos;
- las pruebas del verificador pasan (errores típicos, pint, registro con un servidor simulado);
- en los solucionarios **todas** las verificaciones dan ✅, en los notebooks del estudiante sin
  resolver quedan en ✏️ y el tablero docente se ejecuta sin errores.

El resultado aparece en la pestaña **Actions** y en la insignia de arriba. Las pruebas definen
`CURSO_PYTHON_SIN_REGISTRO=1`, así que nunca escriben en la hoja de registro real.

> El verificador se descarga de la rama `main`, así que los cambios en `verificador/` llegan a
> los estudiantes en cuanto se suben a GitHub.

## 📊 Datos

`data/lambert_beer_kmno4.csv` contiene lecturas **simuladas** de un espectrofotómetro (KMnO₄ a
525 nm, estándares por triplicado y una muestra problema, con desviación de la linealidad por luz
parásita). Se regenera con `python herramientas/generar_datos_lambert_beer.py`.

Los archivos `Amine new.csv`, `Gln.csv`, `+-.csv` y `SucA.csv` contienen valoraciones
potenciométricas reales de nanopartículas F-PEG-k (k = NH2, Gln, GA y SA; volumen de NaOH en
µL), y `amine.csv` es una réplica de F-PEG-NH2. Se usan en el **proyecto final** de la Sesión 3
(opcional, si hay tiempo): en cada curva, el volumen de equivalencia es el punto de inflexión
(máximo de dpH/dV) y el pH en ese volumen es el pKa aparente, que se compara con la Tabla 1 del
artículo. Los archivos se exportaron desde Origin y tienen tres filas de encabezado.

- Artículo: *Self-Assembled PEG-Based Fluorosomes for Cellular Internalization*, *ACS Applied
  Nano Materials*. [doi:10.1021/acsanm.5c05222](https://doi.org/10.1021/acsanm.5c05222)
- Datos: [Zenodo, registro 21227471](https://zenodo.org/records/21227471) (CC-BY 4.0).

`data/curated_solubility.csv` es **AqSolDB**: solubilidad acuosa curada de 9 982 compuestos con
descriptores moleculares. Sorkun, M. C., Khetan, A. y Er, S. *Scientific Data* **6**, 143 (2019).
[doi:10.1038/s41597-019-0151-1](https://doi.org/10.1038/s41597-019-0151-1)

## 🚀 Uso local

```bash
git clone https://github.com/ibonfilrivera/Curso_Python_FQ.git
cd Curso_Python_FQ
pip install numpy pandas scipy matplotlib sympy rdkit jupyter
jupyter notebook notebooks_kaggle/
```
