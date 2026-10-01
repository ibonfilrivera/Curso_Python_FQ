# Cómo contribuir al Curso de Python FQ

Gracias por ayudar a mejorar el curso. Elige la opción que corresponda a lo que quieres hacer.

## Agregar material o ejercicios nuevos (asesores)

No necesitas conocer el sistema de verificación ni instalar nada:

1. Abre la plantilla [`contenido_extra/plantilla_material_adicional.ipynb`](contenido_extra/plantilla_material_adicional.ipynb)
   en Google Colab y guarda una copia.
2. Escribe tu explicación y tus ejercicios **con su solución**. Para que un ejercicio se revise
   automáticamente, agrega al inicio de la celda `#@ejercicio Título` y `#@revisar variable`.
3. Ejecuta todo el notebook sin errores, descárgalo (`.ipynb`) y súbelo a
   `contenido_extra/sesion1/`, `sesion2/` o `sesion3/` con **Add file → Upload files**.

En unos minutos, GitHub Actions integra tu material al final de esa sesión. Los ejercicios sin
marcas también se integran, solo que sin verificación automática.

📖 Guía completa, con ejemplos y solución de problemas: [`contenido_extra/README.md`](contenido_extra/README.md).

## Proponer cambios al contenido existente

- **Una errata o un cambio pequeño:** abre un [*Issue*](https://github.com/ibonfilrivera/Curso_Python_FQ/issues) y describe la sesión, la celda
  y el cambio.
- **Cambios mayores:** edita una copia del notebook en Colab y envíala a la coordinación, que
  trasladará tus cambios a la fuente con `herramientas/comparar_notebook.py`.

> ⚠️ No edites directamente los archivos de `notebooks_kaggle/` ni de `soluciones/`: se generan
> automáticamente y GitHub Actions rechaza los cambios hechos a mano.

## Para la coordinación (cambios en la fuente)

El contenido base de cada sesión está en `herramientas/contenido_sesionN.py` y sus ejercicios
verificables, en `verificador/sesionN.py`. Después de editarlos:

```bash
pip install -r pruebas/requirements.txt
python herramientas/construir_notebooks.py     # Regenera los notebooks
pytest -q pruebas                              # Pruebas del verificador
python pruebas/ejecutar_notebooks.py           # Ejecuta todos los notebooks
```

Sube las fuentes junto con los notebooks regenerados. Si olvidas regenerarlos, GitHub Actions lo
hace por ti al terminar las pruebas.
