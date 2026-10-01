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
    estado, salida = verificar(s2.extra1, capsys)
    assert estado == "incorrecto" and "clasificar_enlace(0.5)" in salida


def test_texto_acepta_mayusculas_y_acentos(ns, capsys):
    ns["clasificar_enlace"] = lambda d: ("Covalente no polar." if d < 0.5
                                         else "Covalente polar" if d < 1.7 else "IONICO")
    assert verificar(s2.extra1, capsys)[0] == "correcto"


def test_masa_molar_del_cloro(ns, capsys):
    class Sustancia:
        def __init__(self, nombre, formula, masa_molar):
            self.nombre, self.formula, self.masa_molar = nombre, formula, masa_molar

        def gramos_a_moles(self, gramos):
            return gramos / self.masa_molar

    ns.update(Sustancia=Sustancia, cloruro_sodio=Sustancia("NaCl", "NaCl", 35.45),
              moles_nacl=15 / 35.45)
    estado, salida = verificar(s2.extra3, capsys)
    assert estado == "incorrecto" and "cloro" in salida


def test_rotacion_con_grados_en_lugar_de_radianes(ns, capsys):
    R = np.array([[np.cos(90), -np.sin(90)], [np.sin(90), np.cos(90)]])
    ns.update(R=R, v_rotado=R @ np.array([3, 4]))
    estado, salida = verificar(s1.ej3, capsys)
    assert estado == "incorrecto" and "radianes" in salida


def test_rotacion_con_producto_elemento_a_elemento(ns, capsys):
    R = np.array([[0.0, -1.0], [1.0, 0.0]])
    ns.update(R=R, v_rotado=R * np.array([3, 4]))
    estado, salida = verificar(s1.ej3, capsys)
    assert estado == "incorrecto" and "R @ v" in salida


def test_cramer_con_columna_equivocada(ns, capsys):
    A = np.array([[3, 2], [4, -1]], dtype=float)
    A_y = A.copy()
    A_y[:, 0] = [12, 5]                                     # Sustituyó la primera columna
    delta = np.linalg.det(A)
    ns.update(delta=delta, x=2.0, y=np.linalg.det(A_y) / delta)
    assert verificar(s1.ej4, capsys)[0] == "incorrecto"
    ns["y"] = 3.0
    assert verificar(s1.ej4, capsys)[0] == "correcto"


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
    assert verificar(s2.extra2, capsys)[0] == "pendiente"


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
    estado, salida = verificar(s1.ej5b, capsys)
    assert estado == "incorrecto" and "sin unidades" in salida
    ns["molaridad"] = (2.50 * ureg.g / (58.44 * ureg("g/mol")) / (250 * ureg.mL))
    assert verificar(s1.ej5b, capsys)[0] == "correcto"


def test_gas_ideal_con_pint(ns, capsys):
    presion = (0.250 * ureg.mol * 0.082057 * ureg("L*atm/(mol*K)")
               * ureg.Quantity(25.0, ureg.degC).to("K") / (500 * ureg.mL)).to("atm")
    ns.update(presion=presion, presion_kpa=presion.to("kPa"))
    assert verificar(s1.ej5a, capsys)[0] == "correcto"
    ns["presion_kpa"] = presion.to("Pa")
    estado, salida = verificar(s1.ej5a, capsys)
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
    # "inicio" se envía de forma síncrona; los demás van en hilos y pueden llegar en otro orden
    assert eventos[0] == ("", "inicio")
    assert sorted(eventos[1:]) == [("ej1", "correcto"), ("ej3", "pista")]
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


# --- Proyecto final: valoración potenciométrica -------------------------------------------

@pytest.fixture
def crudo():
    return pd.read_csv(RAIZ / "data/Amine new.csv", skiprows=[1, 2], encoding="utf-8-sig")


def _titulacion(crudo):
    titulacion = crudo.iloc[:, :2].dropna().astype(float)
    titulacion.columns = ["V_uL", "pH"]
    return titulacion.sort_values("V_uL").reset_index(drop=True)


def test_proyecto_columnas_duplicadas(ns, crudo, capsys):
    duplicada = crudo.iloc[:, [5, 6]].dropna().astype(float)
    duplicada.columns = ["V_uL", "pH"]
    ns.update(crudo=crudo, titulacion=pd.concat([_titulacion(crudo), duplicada]).sort_values("V_uL"))
    estado, salida = verificar(s3.pf1, capsys)
    assert estado == "incorrecto" and "repiten" in salida


def test_proyecto_derivadas_reproducen_el_articulo(ns, crudo, capsys):
    titulacion = _titulacion(crudo)
    V, pH = titulacion["V_uL"].to_numpy(), titulacion["pH"].to_numpy()
    primera = np.gradient(pH, V)
    segunda = np.gradient(primera, V)
    j = int(np.argmax(primera))
    k = j - 1 if segunda[j] < 0 else j
    v_d2 = V[k] - segunda[k] * (V[k + 1] - V[k]) / (segunda[k + 1] - segunda[k])
    ns.update(titulacion=titulacion, primera=primera, segunda=segunda, V_eq_d1=V[j],
              pKa_aparente=pH[j], V_eq_d2=v_d2, pH_eq_d2=float(np.interp(v_d2, V, pH)))
    assert verificar(s3.pf2, capsys)[0] == "correcto"
    assert abs(pH[j] - s3.PKA_LITERATURA) < 0.05          # 8.53 frente a 8.5 del artículo
    ns["V_eq_d1"] = V[j] / 1000                            # En mL por error
    estado, salida = verificar(s3.pf2, capsys)
    assert estado == "incorrecto" and "factor de 0.001" in salida


def test_proyecto_derivada_sin_volumen(ns, crudo, capsys):
    titulacion = _titulacion(crudo)
    ns.update(titulacion=titulacion, primera=np.gradient(titulacion["pH"].to_numpy()),
              segunda=np.zeros(len(titulacion)))
    estado, salida = verificar(s3.pf2, capsys)
    assert estado == "incorrecto" and "np.gradient" in salida


def test_proyecto_tabla_1(ns, capsys):
    def leer_origin(archivo):
        return pd.read_csv(RAIZ / "data" / archivo, skiprows=[1, 2], encoding="utf-8-sig")

    def solo_el_maximo(V, pH, n):                  # Error típico: ignora n y la segunda transición
        derivada = np.gradient(pH, V)
        i = int(np.argmax(derivada))
        return [(V[i], pH[i])]

    ns.update(leer_origin=leer_origin, inflexiones=solo_el_maximo, tabla_pka=pd.DataFrame())
    estado, salida = verificar(s3.pf4, capsys)
    assert estado == "incorrecto" and "F-PEG-GA" in salida

    filas = []
    for nombre, (archivo, pkas) in s3.TABLA_1.items():
        datos = leer_origin(archivo).iloc[:, :2].dropna().astype(float)
        datos = datos.sort_values(datos.columns[0]).drop_duplicates(datos.columns[0])
        V, pH = datos.iloc[:, 0].to_numpy(), datos.iloc[:, 1].to_numpy()
        for (v, p), articulo in zip(s3._inflexiones_referencia(V, pH, len(pkas)), pkas):
            assert abs(p - articulo) < 0.05             # Coincide con la Tabla 1 del artículo
            filas.append({"nanoparticula": nombre, "V_eq": v, "pKa_aparente": p,
                          "pKa_articulo": articulo})
    ns.update(inflexiones=s3._inflexiones_referencia, tabla_pka=pd.DataFrame(filas))
    assert verificar(s3.pf4, capsys)[0] == "correcto"


def test_energia_libre_sin_convertir_entropia(ns, capsys):
    T = np.array([298.15, 500.0, 750.0, 1000.0, 1250.0])
    ns.update(delta_g=206.1 - T * 215, T_inversion=206.1 / 215)
    estado, salida = verificar(s1.auto5, capsys)
    assert estado == "incorrecto" and "1000" in salida


# --- Material adicional del equipo docente (contenido_extra/) --------------------------------

def test_material_adicional_de_la_plantilla(tmp_path, ns, capsys):
    import shutil
    sys.path.insert(0, str(RAIZ / "herramientas"))
    import adicionales
    from bloques import code, ejercicio, md, variante

    (tmp_path / "sesion1").mkdir()
    shutil.copy(RAIZ / "contenido_extra/plantilla_material_adicional.ipynb",
                tmp_path / "sesion1/01_ejemplo.ipynb")
    bloques, espec = adicionales.procesar_sesion(1, md, code, ejercicio, variante, carpeta=tmp_path)

    assert [e["clave"] for e in espec] == ["adic1", "adic2"]
    assert espec[0]["revisar"][0]["valor"] == pytest.approx(39.45 / 50.0)
    iniciales = [b[2] for b in bloques if b[0] == "ejercicio"]
    assert "densidad = ____" in iniciales[0] and "masa = 39.45" in iniciales[0]
    assert any(b[0] == "variante" for b in bloques)          # Ejercicio sin verificación

    ruta = tmp_path / "adicionales.json"
    ruta.write_text(json.dumps(espec), encoding="utf-8")
    sesion = nucleo.Sesion("Prueba", "SP")
    adic = sesion.cargar_adicionales(str(ruta))
    ns["densidad"] = 0.789
    assert verificar(adic["adic1"], capsys)[0] == "correcto"
    ns["densidad"] = 789.0 * ureg("kg/m^3")                    # Con pint y otras unidades
    assert verificar(adic["adic1"], capsys)[0] == "correcto"
    ns["densidad"] = 0.789 * 1000
    estado, salida = verificar(adic["adic1"], capsys)
    assert estado == "incorrecto" and "factor de 1000" in salida
    ns["corregidas"] = np.array([0.203, 0.418, 0.636])
    assert verificar(adic["adic2"], capsys)[0] == "correcto"


def test_material_adicional_con_errores_claros(tmp_path):
    sys.path.insert(0, str(RAIZ / "herramientas"))
    import adicionales
    with pytest.raises(adicionales.ErrorAdicional, match="densidad = ..."):
        adicionales.version_estudiante("for i in range(3):\n    densidad = i", ["densidad"])
    with pytest.raises(adicionales.ErrorAdicional, match="título"):
        adicionales.leer_marcas("#@ejercicio\nx = 1")


def test_placeholder_en_cadenas_con_formato():
    assert f"{nucleo.____:.3f}" == "____"


# --- Sesión 2 sin funciones ------------------------------------------------------------------

def test_enlace_con_if_usa_el_delta_del_estudiante(ns, capsys):
    ns.update(delta_chi=abs(0.93 - 3.16), tipo_enlace="Iónico")
    assert verificar(s2.ej3, capsys)[0] == "correcto"
    ns.update(delta_chi=0.5, tipo_enlace="covalente no polar")      # Límite mal resuelto
    estado, salida = verificar(s2.ej3, capsys)
    assert estado == "incorrecto" and "0.5 ya es covalente polar" in salida
    ns.update(delta_chi="0.5", tipo_enlace="covalente polar")
    estado, salida = verificar(s2.ej3, capsys)
    assert estado == "incorrecto" and "número" in salida


def test_fibonacci_sin_funciones(ns, capsys):
    ns.update(n=10, serie=[0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    assert verificar(s2.auto1, capsys)[0] == "correcto"
    ns["serie_while"] = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]   # 16: <=
    estado, salida = verificar(s2.auto2, capsys)
    assert estado == "incorrecto" and "< 15" in salida


def test_espontaneidad_con_if(ns, capsys):
    ns.update(delta_g_25=206.1 - 298.15 * 0.215, clasificacion="espontánea", T_inversion=958.6)
    estado, salida = verificar(s2.auto5, capsys)
    assert estado == "incorrecto" and "no espontánea" in salida
    ns["clasificacion"] = "No espontanea"
    assert verificar(s2.auto5, capsys)[0] == "correcto"
