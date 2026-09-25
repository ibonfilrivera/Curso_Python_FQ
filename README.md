# Curso de Python — Facultad de Química (UNAM)

Material didáctico, código y datos del curso introductorio de Python del Departamento de Física
y Química Teórica. Curso intensivo de 12 horas (3 sesiones de 4 horas) en Google Colab.

## 📅 Estructura del curso

| Sesión | Temas | Aplicaciones químicas | Abrir en Colab |
| :--- | :--- | :--- | :---: |
| **1** | Tipos de datos, operaciones, `if`/`elif`/`else`, funciones | Moles y moléculas, gases ideales, tipo de enlace, ΔG | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_1.ipynb) |
| **2** | Listas, tuplas, diccionarios, `for`, `while`, clases | Masas molares, vida media, control de calidad, concentraciones | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_2.ipynb) |
| **3** | SciPy, NumPy, Matplotlib, Pandas, RDKit | Calibración, cinética, regla de Lipinski, solubilidad | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ibonfilrivera/Curso_Python_FQ/blob/main/notebooks_kaggle/Sesion_3.ipynb) |

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

## 📁 Contenido del repositorio

```
Curso_Python_FQ/
├── notebooks_kaggle/     Notebooks para estudiantes (con verificación automática)
├── soluciones/           Solucionarios para el equipo docente
├── notebooks/            Versión original del curso (referencia)
├── verificador/          Paquete que revisa los ejercicios (uno por sesión)
├── herramientas/         Generador de los notebooks a partir de una sola fuente
└── data/                 curated_solubility.csv (AqSolDB)
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

4. Ejecuta el solucionario completo: todas las celdas `verificar()` deben mostrar ✅.

> El verificador se descarga de la rama `main`, así que los cambios en `verificador/` llegan a
> los estudiantes en cuanto se suben a GitHub.

## 📊 Datos

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
