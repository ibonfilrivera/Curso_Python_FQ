"""Muestra qué cambió un asesor en una copia editada de un notebook generado.

Los notebooks de notebooks_kaggle/ y soluciones/ se generan desde herramientas/. Si
alguien edita una copia en Colab, este script lista las celdas agregadas, eliminadas
y modificadas para trasladar los cambios a herramientas/contenido_sesionN.py (o a
contenido_extra/, si es material nuevo).

Uso (desde la carpeta Curso_Python_FQ):

    python herramientas/comparar_notebook.py copia_editada.ipynb notebooks_kaggle/Sesion_1.ipynb
"""

import difflib
import sys

import nbformat


def _celdas(ruta):
    nb = nbformat.read(ruta, as_version=4)
    return [f"[{celda.cell_type}]\n{celda.source.strip()}" for celda in nb.cells]


def comparar(editado, original):
    antes, despues = _celdas(original), _celdas(editado)
    cambios = 0
    comparador = difflib.SequenceMatcher(a=antes, b=despues, autojunk=False)
    for operacion, i1, i2, j1, j2 in comparador.get_opcodes():
        if operacion == "equal":
            continue
        cambios += 1
        print(f"\n{'=' * 78}\n{operacion.upper()}: celdas {i1 + 1}–{i2} del original "
              f"→ celdas {j1 + 1}–{j2} de la copia editada")
        diferencia = difflib.unified_diff("\n\n".join(antes[i1:i2]).splitlines(),
                                         "\n\n".join(despues[j1:j2]).splitlines(),
                                         "original", "editado", lineterm="")
        print("\n".join(diferencia))
    print(f"\n{cambios} bloque(s) de cambios." if cambios else "Sin cambios.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    comparar(sys.argv[1], sys.argv[2])
