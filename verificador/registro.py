"""Registro opcional del avance de cada estudiante para el seguimiento docente.

Solo se envía: el identificador que escribe el estudiante, la sesión, el
ejercicio, el resultado (correcto, incorrecto, pendiente, pista o solución),
el número de intento y el mensaje del verificador. Nunca se envía el código.
"""

import json
import threading
import urllib.request
from datetime import datetime, timezone

from . import configuracion

_TIEMPO_LIMITE = 8   # segundos
_estado = {"alumno": None, "clave": None}


def activo():
    return bool(configuracion.URL_REGISTRO and _estado["alumno"])


def _enviar(datos):
    """Hace el POST y devuelve la respuesta JSON del servidor (o None)."""
    solicitud = urllib.request.Request(
        configuracion.URL_REGISTRO,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(solicitud, timeout=_TIEMPO_LIMITE) as respuesta:
        try:
            return json.loads(respuesta.read().decode("utf-8"))
        except ValueError:
            return None


def _evento(sesion, ejercicio, evento, intento=0, detalle=""):
    return {
        "clave": _estado["clave"],
        "alumno": _estado["alumno"],
        "sesion": sesion,
        "ejercicio": ejercicio,
        "evento": evento,
        "intento": intento,
        "detalle": detalle[:300],
        "marca_tiempo": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def iniciar(sesion, alumno="", clave=""):
    """Activa el registro. Se llama desde la celda de configuración del notebook."""
    if not configuracion.URL_REGISTRO:
        print("ℹ️ Registro de avance desactivado (el equipo docente no lo ha configurado).")
        return
    alumno, clave = str(alumno).strip(), str(clave).strip()
    if not alumno or not clave:
        print("ℹ️ Registro de avance desactivado. Si tu docente lo pide, escribe tu "
              "identificador y la clave del grupo en iniciar_registro(...).")
        return
    _estado.update(alumno=alumno, clave=clave)
    try:
        respuesta = _enviar(_evento(sesion, "", "inicio"))
    except Exception as e:
        print(f"⚠️ No se pudo conectar con el registro ({type(e).__name__}). "
              "Puedes trabajar normalmente; avisa a tu docente.")
        return
    if isinstance(respuesta, dict) and not respuesta.get("ok", True):
        _estado.update(alumno=None, clave=None)
        print(f"⚠️ El registro rechazó la conexión: {respuesta.get('error', 'sin detalle')}. "
              "Revisa la clave del grupo.")
        return
    print(f"✔ Registro de avance activo para «{alumno}». Se envía el resultado de cada "
          "verificación (no tu código).")


def registrar(sesion, ejercicio, evento, intento=0, detalle=""):
    """Envía un evento en segundo plano; si la red falla, la clase sigue sin interrupciones."""
    if not activo():
        return
    datos = _evento(sesion, ejercicio, evento, intento, detalle)

    def tarea():
        try:
            _enviar(datos)
        except Exception:
            pass

    threading.Thread(target=tarea, daemon=True).start()
