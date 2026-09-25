"""Genera los notebooks interactivos del curso a partir de una sola fuente.

Para cada sesión se producen dos versiones:

* notebooks_kaggle/Sesion_N.ipynb      — versión del estudiante: los ejercicios
  traen espacios `____` por completar y celdas para verificar la respuesta.
* soluciones/Sesion_N_soluciones.ipynb — solucionario: los mismos notebooks
  con las soluciones de referencia del paquete `verificador`.

Además genera seguimiento/Tablero_docente.ipynb, el tablero de seguimiento del grupo.

Uso (desde la carpeta Curso_Python_FQ):

    python herramientas/construir_notebooks.py
"""

import importlib
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from bloques import md

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# ---------------------------------------------------------------------------
# Construcción de los archivos .ipynb
# ---------------------------------------------------------------------------

def _celdas(bloques, modulo, solucionario):
    celdas = []
    for bloque in bloques:
        tipo = bloque[0]
        if tipo == "md":
            celdas.append(new_markdown_cell(bloque[1]))
        elif tipo == "code":
            celda = new_code_cell(bloque[1])
            if bloque[2]:
                celda.metadata["tags"] = ["raises-exception"]
            celdas.append(celda)
        else:
            _, clave, inicial = bloque
            ej = getattr(modulo, clave)
            celdas.append(new_code_cell(ej._solucion if solucionario else inicial))
            celdas.append(new_code_cell(f"# Verifica tu respuesta\n{clave}.verificar()"))
            if not solucionario:
                celdas.append(new_code_cell(
                    f"# Quita el # de la línea que necesites\n"
                    f"# {clave}.pista()\n# {clave}.solucion()"))
    return celdas


def _guardar(celdas, ruta):
    nb = new_notebook(cells=celdas)
    nb.metadata = {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nbformat.validate(nb)
    nbformat.write(nb, ruta)
    print(f"  {ruta.relative_to(RAIZ)} ({len(celdas)} celdas)")


def construir(numero, fuente):
    modulo = importlib.import_module(f"verificador.sesion{numero}")
    for solucionario in (False, True):
        carpeta = "soluciones" if solucionario else "notebooks_kaggle"
        archivo = f"Sesion_{numero}{'_soluciones' if solucionario else ''}.ipynb"
        bloques = fuente(carpeta, archivo)
        if solucionario:
            bloques = md("> 📘 **Solucionario.** Esta versión contiene las soluciones de "
                         "todos los ejercicios; está pensada para el equipo docente.") + bloques
        _guardar(_celdas(bloques, modulo, solucionario), RAIZ / carpeta / archivo)


def construir_simple(fuente, carpeta, archivo):
    """Notebook sin ejercicios verificables (p. ej., el tablero docente)."""
    _guardar(_celdas(fuente(carpeta, archivo), None, False), RAIZ / carpeta / archivo)


if __name__ == "__main__":
    from contenido_sesion1 import fuente as sesion1
    from contenido_sesion2 import fuente as sesion2
    from contenido_sesion3 import fuente as sesion3
    from contenido_tablero import fuente as tablero

    print("Generando notebooks:")
    construir(1, sesion1)
    construir(2, sesion2)
    construir(3, sesion3)
    construir_simple(tablero, "seguimiento", "Tablero_docente.ipynb")
