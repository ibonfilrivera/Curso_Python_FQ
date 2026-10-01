"""Integra al curso los notebooks que el equipo docente deja en contenido_extra/.

Cada notebook de contenido_extra/sesionN/ se agrega al final de la sesión N, en la
sección «Material adicional». Sus celdas se copian tal cual, salvo las celdas de
ejercicio, que empiezan con marcas en comentarios:

    #@ejercicio Densidad del etanol          ← título (obligatorio)
    #@revisar densidad g/mL                  ← variable a revisar y, opcionalmente, unidades
    #@revisar masa tol=1%                    ← tolerancia relativa (por defecto 0.1 %)
    #@pista La densidad es masa entre volumen.
    masa = 39.45
    volumen = 50.0
    densidad = masa / volumen                ← la solución, escrita normalmente

El generador ejecuta la solución para obtener los valores esperados, crea la versión
del estudiante sustituyendo las asignaciones revisadas por `____` y escribe la
especificación en verificador/adicionales_sesionN.json, que el verificador carga.
Un ejercicio sin `#@revisar` se incluye sin verificación automática.
"""

import ast
import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "contenido_extra"
MARCA_SALIDA = "@@VALORES_ADICIONALES@@"


class ErrorAdicional(Exception):
    """Problema en un notebook de contenido_extra/, con un mensaje para quien lo escribió."""


def leer_marcas(codigo):
    """Separa las marcas #@ de una celda. Devuelve None si no es un ejercicio."""
    lineas = codigo.splitlines()
    if not lineas or not lineas[0].strip().startswith("#@ejercicio"):
        return None
    ejercicio = {"titulo": "", "revisar": [], "pista": "", "solucion": []}
    for linea in lineas:
        texto = linea.strip()
        if texto.startswith("#@ejercicio"):
            ejercicio["titulo"] = texto[len("#@ejercicio"):].strip()
        elif texto.startswith("#@revisar"):
            partes = texto[len("#@revisar"):].split()
            if not partes:
                raise ErrorAdicional("Una línea #@revisar no indica qué variable revisar.")
            criterio = {"variable": partes[0]}
            unidades = []
            for parte in partes[1:]:
                if parte.startswith("tol="):
                    criterio["tolerancia"] = float(parte[4:].rstrip("%")) / 100
                else:
                    unidades.append(parte)
            if unidades:
                criterio["unidades"] = " ".join(unidades)
            ejercicio["revisar"].append(criterio)
        elif texto.startswith("#@pista"):
            ejercicio["pista"] = texto[len("#@pista"):].strip()
        else:
            ejercicio["solucion"].append(linea)
    if not ejercicio["titulo"]:
        raise ErrorAdicional("La marca #@ejercicio necesita un título.")
    ejercicio["solucion"] = "\n".join(ejercicio["solucion"]).strip("\n")
    return ejercicio


def version_estudiante(solucion, variables):
    """Sustituye la última asignación de cada variable revisada por `variable = ____`."""
    arbol = ast.parse(solucion)
    lineas = solucion.splitlines()
    reemplazos = {}
    for variable in variables:
        asignaciones = [nodo for nodo in arbol.body
                        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1
                        and isinstance(nodo.targets[0], ast.Name) and nodo.targets[0].id == variable]
        if not asignaciones:
            raise ErrorAdicional(f"No encontré una línea `{variable} = ...` (fuera de ciclos o "
                                 "funciones) en la celda del ejercicio.")
        nodo = asignaciones[-1]
        reemplazos[nodo.lineno - 1] = (nodo.end_lineno - 1, f"{variable} = ____")
    resultado, i = [], 0
    while i < len(lineas):
        if i in reemplazos:
            fin, texto = reemplazos[i]
            resultado.append(texto)
            i = fin + 1
        else:
            resultado.append(lineas[i])
            i += 1
    return "\n".join(resultado)


_PRELUDIO = f'''
import json as _json

def _valor_adicional(valor, unidades):
    if all(hasattr(valor, a) for a in ("magnitude", "units", "to")):       # Cantidad de pint
        valor = valor.to(unidades).magnitude if unidades else valor.magnitude
    if isinstance(valor, bool):
        return "booleano", valor
    if isinstance(valor, str):
        return "texto", valor
    try:
        import numpy as _np
        if _np.ndim(valor) == 0:
            return "numero", float(valor)
        return "arreglo", _np.asarray(valor, dtype=float).tolist()
    except (TypeError, ValueError):
        raise TypeError(f"No sé revisar valores de tipo {{type(valor).__name__}}") from None

def _capturar(clave, criterios):
    salida = []
    for criterio in criterios:
        tipo, valor = _valor_adicional(globals()[criterio["variable"]], criterio.get("unidades"))
        salida.append(dict(criterio, tipo=tipo, valor=valor))
    print("{MARCA_SALIDA}" + _json.dumps({{"clave": clave, "revisar": salida}}))
'''


def _ejecutar_soluciones(ruta, celdas_ejercicio):
    """Ejecuta el notebook con las soluciones y devuelve los valores de cada ejercicio."""
    nb = nbformat.read(ruta, as_version=4)
    ejecutable = nbformat.v4.new_notebook()
    ejecutable.cells.append(nbformat.v4.new_code_cell(_PRELUDIO))
    for indice, celda in enumerate(nb.cells):
        if celda.cell_type != "code":
            continue
        if indice in celdas_ejercicio:
            clave, ejercicio = celdas_ejercicio[indice]
            ejecutable.cells.append(nbformat.v4.new_code_cell(ejercicio["solucion"]))
            if ejercicio["revisar"]:
                ejecutable.cells.append(nbformat.v4.new_code_cell(
                    f"_capturar({clave!r}, {json.dumps(ejercicio['revisar'])})"))
        else:
            ejecutable.cells.append(nbformat.v4.new_code_cell(celda.source))
    NotebookClient(ejecutable, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": str(RAIZ / "notebooks_verificador")}}).execute()
    valores = {}
    for celda in ejecutable.cells:
        for salida in celda.get("outputs", []):
            for linea in salida.get("text", "").splitlines():
                if linea.startswith(MARCA_SALIDA):
                    datos = json.loads(linea[len(MARCA_SALIDA):])
                    valores[datos["clave"]] = datos["revisar"]
    return valores


def procesar_sesion(numero, md, code, ejercicio, variante, carpeta=CARPETA):
    """Devuelve (bloques para el notebook, especificación para el verificador)."""
    archivos = sorted((carpeta / f"sesion{numero}").glob("*.ipynb"))
    if not archivos:
        return [], []
    bloques = md(f"""
# **Material adicional**

Secciones y ejercicios preparados por el equipo docente para la Sesión {numero}.
""")
    especificacion = []
    verificables = 0
    for ruta in archivos:
        nb = nbformat.read(ruta, as_version=4)
        celdas_ejercicio = {}
        for indice, celda in enumerate(nb.cells):
            if celda.cell_type != "code":
                continue
            try:
                marcas = leer_marcas(celda.source)
            except ErrorAdicional as e:
                raise ErrorAdicional(f"{ruta.name}, celda {indice + 1}: {e}") from None
            if marcas:
                clave = None
                if marcas["revisar"]:                # Solo los verificables reciben clave
                    verificables += 1
                    clave = f"adic{verificables}"
                celdas_ejercicio[indice] = (clave, marcas)
        try:
            valores = _ejecutar_soluciones(ruta, celdas_ejercicio) if celdas_ejercicio else {}
        except Exception as e:
            raise ErrorAdicional(f"{ruta.name}: la solución produjo un error al ejecutarse.\n"
                                 f"{str(e)[-800:]}") from None
        for indice, celda in enumerate(nb.cells):
            if celda.cell_type == "markdown":
                bloques += md(celda.source)
            elif indice not in celdas_ejercicio:
                bloques += code(celda.source)
            else:
                clave, marcas = celdas_ejercicio[indice]
                if not marcas["revisar"]:
                    bloques += md(f"> ℹ️ *{marcas['titulo']}* no tiene verificación automática: "
                                  "comenta tu resultado con tu profesor/a.")
                    bloques += variante("# Escribe tu código aquí\n", marcas["solucion"])
                    continue
                try:
                    inicial = version_estudiante(marcas["solucion"],
                                                 [c["variable"] for c in marcas["revisar"]])
                except ErrorAdicional as e:
                    raise ErrorAdicional(f"{ruta.name}, ejercicio «{marcas['titulo']}»: {e}") from None
                especificacion.append({"clave": clave, "titulo": f"(Adicional) {marcas['titulo']}",
                                       "pista": marcas["pista"], "solucion": marcas["solucion"],
                                       "revisar": valores[clave], "origen": ruta.name})
                bloques += ejercicio(clave, inicial)
    return bloques, especificacion
