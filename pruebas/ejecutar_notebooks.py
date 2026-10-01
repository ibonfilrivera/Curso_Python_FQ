"""Ejecuta todos los notebooks del curso y comprueba el resultado del verificador.

* Solucionarios: todas las celdas `ejN.verificar()` deben mostrar ✅ Correcto y
  ninguna celda puede fallar (salvo las marcadas con "raises-exception").
* Notebooks del estudiante (sin resolver): todas las verificaciones deben quedar
  en ✏️ Pendiente; un ❌ o un error del verificador indica un problema.
* Tablero docente: debe ejecutarse sin errores con los datos de ejemplo.

Uso (desde la carpeta Curso_Python_FQ):

    python pruebas/ejecutar_notebooks.py            # todo
    python pruebas/ejecutar_notebooks.py 2 3        # solo las sesiones 2 y 3
"""

import os
import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent.parent

# Ejercicios cuyo código inicial está mal a propósito (no tienen ____): en el notebook del
# estudiante sin resolver deben mostrar ❌, no ✏️.
INCORRECTOS_A_PROPOSITO = {
    "Sesion_1.ipynb": {"ej6"},   # Código de un asistente de IA con un error de unidades
}

# Sin ventanas de Matplotlib ni envíos a la hoja de registro real
os.environ["MPLBACKEND"] = "Agg"
os.environ["CURSO_PYTHON_SIN_REGISTRO"] = "1"


def ejecutar(ruta):
    nb = nbformat.read(ruta, as_version=4)
    for celda in nb.cells:
        # input() necesita a una persona: se sustituye por una respuesta fija
        if celda.cell_type == "code":
            celda.source = celda.source.replace("input(", '(lambda _: "25")(')
    NotebookClient(nb, timeout=900, kernel_name="python3", allow_errors=True,
                   resources={"metadata": {"path": str(ruta.parent)}}).execute()
    return nb


def estado_verificacion(celda):
    html = " ".join(o.get("data", {}).get("text/html", "") for o in celda.outputs)
    for texto, estado in (("¡Correcto!", "correcto"), ("Incorrecto", "incorrecto"),
                          ("Pendiente", "pendiente"), ("produjo un error", "error")):
        if texto in html:
            return estado
    return "sin salida"


def revisar(ruta, esperado):
    """Devuelve (número de verificaciones, lista de problemas)."""
    nb = ejecutar(ruta)
    problemas, verificaciones = [], 0
    for celda in nb.cells:
        if celda.cell_type != "code":
            continue
        clave = re.search(r"(\w+)\.verificar\(\)", celda.source)
        errores = [o for o in celda.outputs if o.output_type == "error"]
        if clave:
            verificaciones += 1
            estado = estado_verificacion(celda)
            if esperado == "pendiente" and clave.group(1) in INCORRECTOS_A_PROPOSITO.get(ruta.name, ()):
                esperado_aqui = "incorrecto"
            else:
                esperado_aqui = esperado
            if estado != esperado_aqui:
                problemas.append(f"{clave.group(1)}: se esperaba {esperado_aqui}, "
                                 f"se obtuvo {estado}")
        elif errores and "raises-exception" not in celda.metadata.get("tags", []):
            # En el notebook del estudiante, las celdas con ____ fallan: es lo esperado
            if esperado == "correcto" or "____" not in celda.source:
                error = errores[0]
                problemas.append(f"celda {celda.source[:50]!r}: {error.ename}: {error.evalue[:150]}")
    return verificaciones, problemas


def main(sesiones):
    objetivos = []
    for n in sesiones:
        objetivos.append((RAIZ / f"soluciones/Sesion_{n}_soluciones.ipynb", "correcto"))
        objetivos.append((RAIZ / f"notebooks_kaggle/Sesion_{n}.ipynb", "pendiente"))
    objetivos.append((RAIZ / "seguimiento/Tablero_docente.ipynb", None))

    fallos = 0
    for ruta, esperado in objetivos:
        verificaciones, problemas = revisar(ruta, esperado)
        nombre = ruta.relative_to(RAIZ)
        if problemas:
            fallos += len(problemas)
            print(f"❌ {nombre}")
            for problema in problemas:
                print(f"     {problema}")
        else:
            detalle = f"{verificaciones} verificaciones: {esperado}" if esperado else "sin errores"
            print(f"✅ {nombre} ({detalle})")
    return fallos


if __name__ == "__main__":
    sesiones = [int(a) for a in sys.argv[1:]] or [1, 2, 3]
    sys.exit(1 if main(sesiones) else 0)
