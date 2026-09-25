"""Núcleo del verificador de ejercicios del curso (al estilo de Kaggle Learn).

Cada ejercicio es un objeto con tres métodos que el estudiante llama desde el
notebook:

    ej1.verificar()   # ¿Mi respuesta es correcta?
    ej1.pista()       # Una ayuda sin revelar la respuesta
    ej1.solucion()    # La solución de referencia

El verificador lee las variables y funciones que el estudiante definió en el
notebook, así que no es necesario pasarle argumentos.
"""

import math
import traceback
import unicodedata
from html import escape

from . import registro


# ---------------------------------------------------------------------------
# Marcador de "espacio por completar"
# ---------------------------------------------------------------------------

class _PorCompletar:
    """Valor que ocupa el lugar de una respuesta que aún no se escribe."""

    def __repr__(self):
        return "____"

    def _error(self, *args, **kwargs):
        raise TypeError("Sustituye ____ por tu respuesta antes de ejecutar la celda.")

    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _error
    __truediv__ = __rtruediv__ = __pow__ = __rpow__ = __call__ = _error
    __lt__ = __le__ = __gt__ = __ge__ = __bool__ = __len__ = __iter__ = _error


____ = _PorCompletar()


# ---------------------------------------------------------------------------
# Excepciones que usan las funciones de verificación
# ---------------------------------------------------------------------------

class Incorrecto(Exception):
    """La respuesta existe, pero no es correcta. El mensaje orienta al estudiante."""


class Pendiente(Exception):
    """La respuesta aún no se ha escrito (variable inexistente o con ____)."""


# ---------------------------------------------------------------------------
# Presentación de mensajes
# ---------------------------------------------------------------------------

_ESTILOS = {
    "correcto":   ("#1e8e3e", "✅ ¡Correcto!"),
    "incorrecto": ("#d93025", "❌ Incorrecto"),
    "pendiente":  ("#1a73e8", "✏️ Pendiente"),
    "error":      ("#d93025", "⚠️ Tu código produjo un error"),
    "pista":      ("#f9ab00", "💡 Pista"),
    "solucion":   ("#5f6368", "📘 Solución"),
}


def _en_notebook():
    try:
        from IPython import get_ipython
    except ImportError:
        return False
    return get_ipython() is not None


def _mostrar(tipo, mensaje_html, mensaje_texto):
    color, titulo = _ESTILOS[tipo]
    if not _en_notebook():
        print(f"{titulo}: {mensaje_texto}")
        return
    from IPython.display import HTML, display
    display(HTML(
        f'<div style="border-left: 6px solid {color}; padding: 0.5em 1em; '
        f'margin: 0.3em 0; background: {color}14; border-radius: 4px;">'
        f'<strong style="color: {color};">{titulo}</strong>'
        f'{": " if mensaje_html else ""}{mensaje_html}</div>'
    ))


def _a_html(texto):
    """Convierte `código` en <code> y respeta saltos de línea."""
    partes = escape(texto).split("`")
    html = "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(partes))
    return html.replace("\n", "<br>")


# ---------------------------------------------------------------------------
# Acceso al espacio de nombres del notebook
# ---------------------------------------------------------------------------

def _espacio_usuario():
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            return ip.user_ns
    except ImportError:
        pass
    import __main__
    return vars(__main__)


def obtener(ns, nombre):
    """Devuelve la variable `nombre` del notebook o lanza Pendiente."""
    if nombre not in ns:
        raise Pendiente(f"Aún no defines `{nombre}`. Escribe tu código, ejecuta la celda "
                        "y vuelve a verificar.")
    valor = ns[nombre]
    if isinstance(valor, _PorCompletar):
        raise Pendiente(f"Sustituye `____` en `{nombre}` por tu respuesta.")
    return valor


def obtener_funcion(ns, nombre):
    funcion = obtener(ns, nombre)
    if not callable(funcion):
        raise Incorrecto(f"`{nombre}` debería ser una función definida con `def`, "
                         f"pero es de tipo `{type(funcion).__name__}`.")
    return funcion


# ---------------------------------------------------------------------------
# Comparaciones reutilizables
# ---------------------------------------------------------------------------

def es_numero(valor):
    try:
        import numpy as np
        if isinstance(valor, np.generic) and not isinstance(valor, np.bool_):
            return True
    except ImportError:
        pass
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _formato(valor):
    if es_numero(valor):
        valor = float(valor)
        if valor != 0 and (abs(valor) >= 1e6 or abs(valor) < 1e-3):
            return f"{valor:.4e}"
        return f"{valor:.6g}"
    return repr(valor)


def comparar_numero(nombre, valor, esperado, rel=1e-3, abs_=1e-9):
    """Compara un número con tolerancia y da pistas sobre errores comunes."""
    if isinstance(valor, str):
        raise Incorrecto(f"`{nombre}` es un texto ({valor!r}); debería ser un número. "
                         "¿Pusiste el número entre comillas?")
    if not es_numero(valor):
        raise Incorrecto(f"`{nombre}` debería ser un número, pero es de tipo "
                         f"`{type(valor).__name__}`.")
    if math.isclose(float(valor), esperado, rel_tol=rel, abs_tol=abs_):
        return
    mensaje = f"`{nombre}` vale {_formato(valor)}, pero no es el valor esperado."
    if esperado != 0:
        cociente = float(valor) / esperado
        for factor in (1e3, 1e-3, 1e2, 1e-2, 1e6, 1e-6):
            if math.isclose(cociente, factor, rel_tol=1e-2):
                mensaje += (f" Tu resultado difiere por un factor de {factor:g}: "
                            "revisa las conversiones de unidades.")
                break
        else:
            if math.isclose(cociente, -1, rel_tol=1e-2):
                mensaje += " Tu resultado tiene el signo opuesto."
    raise Incorrecto(mensaje)


def normalizar_texto(texto):
    """Minúsculas, sin acentos, sin puntuación final ni espacios extra."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().strip(" .!¡").split())


def _tiene_espacios(funcion):
    """True si el código de la función todavía contiene el marcador ____."""
    codigo = getattr(funcion, "__code__", None)
    return codigo is not None and "____" in codigo.co_names


def lista_no_vacia(nombre, valor, descripcion):
    """Exige una lista; si está vacía se considera que el ejercicio está pendiente."""
    if not isinstance(valor, list):
        raise Incorrecto(f"`{nombre}` debe ser una lista.")
    if not valor:
        raise Pendiente(f"`{nombre}` está vacía: {descripcion}")
    return valor


def describir_llamada(nombre, args, kwargs):
    partes = [_formato(a) for a in args] + [f"{k}={_formato(v)}" for k, v in kwargs.items()]
    return f"{nombre}({', '.join(partes)})"


def probar_funcion(nombre, funcion, casos, comparar=None):
    """Prueba `funcion` con una lista de casos (args, kwargs, esperado).

    `comparar(obtenido, esperado)` debe devolver True si coinciden; por
    defecto se comparan números con tolerancia relativa de 1e-3.
    """
    if _tiene_espacios(funcion):
        raise Pendiente(f"Completa `{nombre}`: sustituye los `____` por tu código.")
    for args, kwargs, esperado in casos:
        llamada = describir_llamada(nombre, args, kwargs)
        try:
            obtenido = funcion(*args, **kwargs)
        except Exception as e:
            raise Incorrecto(f"Al llamar `{llamada}` ocurrió un error: "
                             f"`{type(e).__name__}: {e}`") from None
        if obtenido is None:
            raise Incorrecto(f"`{llamada}` devolvió `None`. ¿Olvidaste usar `return`?")
        if comparar is not None:
            try:
                correcto = comparar(obtenido, esperado)
            except Exception:
                correcto = False
        elif es_numero(esperado):
            correcto = es_numero(obtenido) and math.isclose(
                float(obtenido), esperado, rel_tol=1e-3, abs_tol=1e-9)
        else:
            correcto = obtenido == esperado
        if not correcto:
            raise Incorrecto(f"`{llamada}` devolvió {_formato(obtenido)}, "
                             f"pero se esperaba {_formato(esperado)}.")


# ---------------------------------------------------------------------------
# Ejercicios y sesiones
# ---------------------------------------------------------------------------

class Ejercicio:
    """Un ejercicio verificable.

    `comprobar(ns)` recibe el espacio de nombres del notebook y debe lanzar
    `Incorrecto` o `Pendiente` si algo falla; si termina sin excepciones la
    respuesta se considera correcta. Puede devolver un texto opcional que se
    añade al mensaje de éxito.
    """

    def __init__(self, clave, titulo, comprobar, pista, solucion, sesion=""):
        self.clave = clave
        self.titulo = titulo
        self._comprobar = comprobar
        self._pista = pista
        self._solucion = solucion.strip("\n")
        self._sesion = sesion
        self.estado = "sin intentar"
        self.intentos = 0

    def verificar(self):
        ns = _espacio_usuario()
        self.intentos += 1
        detalle = ""
        try:
            extra = self._comprobar(ns)
        except Pendiente as e:
            self.estado, detalle = "pendiente", str(e)
            _mostrar("pendiente", _a_html(detalle), detalle)
        except Incorrecto as e:
            self.estado, detalle = "incorrecto", str(e)
            mensaje = detalle + f"\nSi te atoras, ejecuta `{self.clave}.pista()`."
            _mostrar("incorrecto", _a_html(mensaje), mensaje)
        except Exception as e:
            self.estado = "incorrecto"
            detalle = traceback.format_exception_only(type(e), e)[-1].strip()
            _mostrar("error", _a_html(f"`{detalle}`"), detalle)
        else:
            self.estado = "correcto"
            _mostrar("correcto", _a_html(extra or ""), extra or "")
        registro.registrar(self._sesion, self.clave, self.estado, self.intentos, detalle)

    def pista(self):
        _mostrar("pista", _a_html(self._pista), self._pista)
        registro.registrar(self._sesion, self.clave, "pista", self.intentos)

    def solucion(self):
        html = (f'<pre style="margin: 0.5em 0 0 0; white-space: pre-wrap;">'
                f'{escape(self._solucion)}</pre>')
        _mostrar("solucion", html, "\n" + self._solucion)
        registro.registrar(self._sesion, self.clave, "solucion", self.intentos)

    def __repr__(self):
        return (f"<{self.titulo} — usa {self.clave}.verificar(), "
                f"{self.clave}.pista() o {self.clave}.solucion()>")


class Sesion:
    """Agrupa los ejercicios de un notebook y muestra el progreso."""

    _ICONOS = {"correcto": "✅", "incorrecto": "❌", "pendiente": "✏️", "sin intentar": "⬜"}

    def __init__(self, nombre, corto):
        self.nombre = nombre
        self.corto = corto          # Etiqueta breve para el registro docente, p. ej. "S1"
        self.ejercicios = []

    def agregar(self, clave, titulo, comprobar, pista, solucion):
        ejercicio = Ejercicio(clave, titulo, comprobar, pista, solucion, sesion=self.corto)
        self.ejercicios.append(ejercicio)
        return ejercicio

    def iniciar_registro(self, alumno="", clave=""):
        """Activa el envío del avance al equipo docente (ver verificador/registro.py)."""
        registro.iniciar(self.corto, alumno, clave)

    def progreso(self):
        correctos = sum(e.estado == "correcto" for e in self.ejercicios)
        total = len(self.ejercicios)
        filas = "".join(
            f"<tr><td>{self._ICONOS[e.estado]}</td><td><code>{e.clave}</code></td>"
            f"<td>{escape(e.titulo)}</td></tr>"
            for e in self.ejercicios
        )
        texto = "\n".join(f"{self._ICONOS[e.estado]} {e.clave}: {e.titulo}"
                          for e in self.ejercicios)
        if not _en_notebook():
            print(f"{self.nombre}: {correctos}/{total} ejercicios correctos\n{texto}")
            return
        from IPython.display import HTML, display
        display(HTML(
            f"<h4>{escape(self.nombre)}: {correctos} de {total} ejercicios correctos</h4>"
            f'<progress value="{correctos}" max="{total}" style="width: 20em;"></progress>'
            f"<table>{filas}</table>"
        ))

    def bienvenida(self):
        print(f"✔ Verificador listo — {self.nombre}: {len(self.ejercicios)} ejercicios. "
              "Usa progreso() para ver tu avance.")
