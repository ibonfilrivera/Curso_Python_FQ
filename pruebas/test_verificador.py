"""Pruebas del paquete verificador: mensajes ante errores típicos, pint y registro."""

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from verificador import configuracion, nucleo, registro  # noqa: E402
from verificador import sesion1 as s1  # noqa: E402
from verificador import sesion2 as s2  # noqa: E402
from verificador import sesion3 as s3  # noqa: E402

ureg = pytest.importorskip("pint").UnitRegistry()


@pytest.fixture
def ns(monkeypatch):
    """Espacio de nombres falso que el verificador lee en lugar del notebook."""
    espacio = {}
    monkeypatch.setattr(nucleo, "_espacio_usuario", lambda: espacio)
    return espacio


def verificar(ejercicio, capsys):
    ejercicio.verificar()
    return ejercicio.estado, capsys.readouterr().out


# --- Errores típicos --------------------------------------------------------------

def test_jerarquia_sin_parentesis(ns, capsys):
    ns["x"] = 8 * 10 + 2 * 11 / 20 - 4
    estado, salida = verificar(s1.ej1, capsys)
    assert estado == "incorrecto" and "ej1.pista()" in salida


def test_factor_mil_en_unidades(ns, capsys):
    ns.update(masa_molar_hcn=27.03, moles_hcn=10 / 27.03 * 1000)
    estado, salida = verificar(s1.ej2a, capsys)
    assert estado == "incorrecto" and "factor de 1000" in salida


def test_limite_de_enlace(ns, capsys):
    def clasificar_enlace(delta):
        if delta <= 0.5:
            return "covalente no polar"
        return "covalente polar" if delta < 1.7 else "iónico"
    ns["clasificar_enlace"] = clasificar_enlace
    estado, salida = verificar(s1.ej3, capsys)
    assert estado == "incorrecto" and "clasificar_enlace(0.5)" in salida


def test_texto_acepta_mayusculas_y_acentos(ns, capsys):
    ns["clasificar_enlace"] = lambda d: ("Covalente no polar." if d < 0.5
                                         else "Covalente polar" if d < 1.7 else "IONICO")
    assert verificar(s1.ej3, capsys)[0] == "correcto"


def test_codigo_de_ia_con_error_de_mililitros(ns, capsys):
    ns["calcular_molaridad"] = lambda m, mm, v: m / mm / v
    estado, salida = verificar(s1.ej5, capsys)
    assert estado == "incorrecto" and "factor de 0.001" in salida
    ns["calcular_molaridad"] = lambda m, mm, v: m / mm / (v / 1000)
    assert verificar(s1.ej5, capsys)[0] == "correcto"


def test_codigo_de_ia_que_falla_o_no_devuelve(ns, capsys):
    ns["calcular_molaridad"] = lambda m, mm, v: m / 0
    estado, salida = verificar(s1.ej5, capsys)
    assert estado == "incorrecto" and "ZeroDivisionError" in salida
    ns["calcular_molaridad"] = lambda m, mm, v: None
    estado, salida = verificar(s1.ej5, capsys)
    assert estado == "incorrecto" and "return" in salida


def test_masa_molar_del_cloro(ns, capsys):
    class Sustancia:
        def __init__(self, nombre, formula, masa_molar):
            self.nombre, self.formula, self.masa_molar = nombre, formula, masa_molar

        def gramos_a_moles(self, gramos):
            return gramos / self.masa_molar

    ns.update(Sustancia=Sustancia, cloruro_sodio=Sustancia("NaCl", "NaCl", 35.45),
              moles_nacl=15 / 35.45)
    estado, salida = verificar(s2.extra1, capsys)
    assert estado == "incorrecto" and "cloro" in salida


def test_cramer_con_truncamiento_entero(ns, capsys):
    def resolver_cramer_2x2(A, b):
        A_x, A_y = A.copy(), A.copy()
        A_x[:, 0], A_y[:, 1] = b, b
        d = np.linalg.det(A)
        return np.array([np.linalg.det(A_x) / d, np.linalg.det(A_y) / d])
    ns["resolver_cramer_2x2"] = resolver_cramer_2x2
    estado, salida = verificar(s2.ej6, capsys)
    assert estado == "incorrecto" and "dtype=float" in salida


def test_grafica_sin_etiquetas(ns, capsys):
    fig, ax = plt.subplots()
    ax.scatter(s3.CONC_CALIBRACION, s3.ABS_CALIBRACION)
    ax.plot([0, 10], [0, 1])
    ns.update(fig_calibracion=fig, conc_problema=4.63)
    estado, salida = verificar(s3.ej2, capsys)
    plt.close(fig)
    assert estado == "incorrecto" and "etiquetas" in salida


# --- Espacios por completar ---------------------------------------------------------

def test_espacios_sin_llenar_quedan_pendientes(ns, capsys):
    ns["x"] = nucleo.____
    assert verificar(s1.ej1, capsys)[0] == "pendiente"

    # Así queda la función cuando el estudiante ejecuta la celda sin completarla
    exec("def formula_gauss(n):\n    ____\n", {"____": nucleo.____}, ns)
    assert verificar(s1.auto4, capsys)[0] == "pendiente"


def test_variable_inexistente_queda_pendiente(ns, capsys):
    estado, salida = verificar(s1.auto1, capsys)
    assert estado == "pendiente" and "Aún no defines" in salida


def test_placeholder_no_permite_ciclos_infinitos():
    with pytest.raises(TypeError):
        while nucleo.____:
            pass


# --- Unidades con pint ----------------------------------------------------------------

def test_cantidad_en_otras_unidades_se_convierte(ns, capsys):
    ns.update(masa_molar_hcn=27.03 * ureg("g/mol"), moles_hcn=(10 / 27.03 * 1000) * ureg.mmol)
    assert verificar(s1.ej2a, capsys)[0] == "correcto"


def test_temperatura_en_celsius_se_convierte(ns, capsys):
    ns["T_K"] = ureg.Quantity(300, ureg.degC)
    assert verificar(s1.auto1, capsys)[0] == "correcto"


def test_dimension_incorrecta(ns, capsys):
    ns.update(masa_molar_hcn=27.03 * ureg("g/mol"), moles_hcn=0.37 * ureg.g)
    estado, salida = verificar(s1.ej2a, capsys)
    assert estado == "incorrecto" and "se esperaban unidades" in salida


def test_ejercicio_de_pint_exige_unidades(ns, capsys):
    ns["molaridad"] = 0.1711
    estado, salida = verificar(s2.ej7b, capsys)
    assert estado == "incorrecto" and "sin unidades" in salida
    ns["molaridad"] = (2.50 * ureg.g / (58.44 * ureg("g/mol")) / (250 * ureg.mL))
    assert verificar(s2.ej7b, capsys)[0] == "correcto"


def test_gas_ideal_con_pint(ns, capsys):
    presion = (0.250 * ureg.mol * 0.082057 * ureg("L*atm/(mol*K)")
               * ureg.Quantity(25.0, ureg.degC).to("K") / (500 * ureg.mL)).to("atm")
    ns.update(presion=presion, presion_kpa=presion.to("kPa"))
    assert verificar(s2.ej7a, capsys)[0] == "correcto"
    ns["presion_kpa"] = presion.to("Pa")
    estado, salida = verificar(s2.ej7a, capsys)
    assert estado == "incorrecto" and "kPa" in salida


# --- Lambert-Beer --------------------------------------------------------------------

def test_lambert_beer_con_todos_los_puntos_es_incorrecto(ns, capsys):
    from scipy.stats import linregress
    datos_lb = pd.read_csv(RAIZ / "data/lambert_beer_kmno4.csv")
    resumen = (datos_lb[datos_lb["tipo"] == "estandar"]
               .groupby("concentracion_mol_L")["absorbancia"]
               .agg(promedio="mean", desviacion="std"))
    ajuste = linregress(resumen.index, resumen["promedio"])   # Sin excluir la zona no lineal
    fig, ax = plt.subplots()
    ax.set_xlabel("c")
    ax.set_ylabel("A")
    ax.plot([0, 1], [0, 1], label="ajuste")
    ax.legend()
    ns.update(datos_lb=datos_lb, resumen=resumen, fig_lb=fig, epsilon=ajuste.slope,
              r2_lineal=ajuste.rvalue**2, r2_todos=ajuste.rvalue**2)
    assert verificar(s3.ej3a, capsys)[0] == "correcto"
    assert verificar(s3.ej3b, capsys)[0] == "incorrecto"
    plt.close(fig)


# --- Registro para el seguimiento docente ---------------------------------------------

class _AppsScriptFalso(BaseHTTPRequestHandler):
    """Imita la aplicación web: valida la clave y responde con una redirección 302."""

    recibidos = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        datos = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.recibidos.append(datos)
        ok = int(datos.get("clave") == "clave-prueba")
        self.send_response(302)
        self.send_header("Location", f"/respuesta?ok={ok}")
        self.end_headers()

    def do_GET(self):
        ok = self.path.endswith("ok=1")
        cuerpo = {"ok": True} if ok else {"ok": False, "error": "clave del grupo incorrecta"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(cuerpo).encode())


@pytest.fixture
def servidor(monkeypatch):
    srv = HTTPServer(("127.0.0.1", 0), _AppsScriptFalso)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    _AppsScriptFalso.recibidos = []
    monkeypatch.delenv("CURSO_PYTHON_SIN_REGISTRO", raising=False)
    monkeypatch.setattr(configuracion, "URL_REGISTRO", f"http://127.0.0.1:{srv.server_port}/exec")
    monkeypatch.setattr(registro, "_estado", {"alumno": None, "clave": None})
    yield srv
    srv.shutdown()
    srv.server_close()


def test_registro_rechaza_clave_incorrecta(servidor, capsys):
    s1.iniciar_registro("A01", "otra")
    assert "rechazó" in capsys.readouterr().out
    assert not registro.activo()


def test_registro_envia_resultados_sin_codigo(servidor, ns, capsys):
    s1.iniciar_registro("A01", "clave-prueba")
    assert "activo" in capsys.readouterr().out
    ns["x"] = 6.375
    s1.ej1.verificar()
    s1.ej3.pista()
    for _ in range(50):
        if len(_AppsScriptFalso.recibidos) >= 3:
            break
        time.sleep(0.05)
    eventos = [(d["ejercicio"], d["evento"]) for d in _AppsScriptFalso.recibidos]
    assert eventos == [("", "inicio"), ("ej1", "correcto"), ("ej3", "pista")]
    assert all(set(d) == {"clave", "alumno", "sesion", "ejercicio", "evento", "intento",
                          "detalle", "marca_tiempo"} for d in _AppsScriptFalso.recibidos)


def test_registro_caido_no_interrumpe(servidor, ns, capsys):
    s1.iniciar_registro("A01", "clave-prueba")
    servidor.shutdown()
    servidor.server_close()
    ns["x"] = 1
    s1.ej1.verificar()           # No debe lanzar excepciones
    assert s1.ej1.estado == "incorrecto"


def test_variable_de_entorno_desactiva_el_registro(monkeypatch, capsys):
    monkeypatch.setenv("CURSO_PYTHON_SIN_REGISTRO", "1")
    monkeypatch.setattr(registro, "_estado", {"alumno": None, "clave": None})
    s1.iniciar_registro("A01", "clave-prueba")
    assert "desactivado" in capsys.readouterr().out
    assert not registro.activo()
