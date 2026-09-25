"""Bloques de celdas reutilizables para escribir el contenido de las sesiones."""

REPOSITORIO_GITHUB = "ibonfilrivera/Curso_Python_FQ"
URL_CRUDA = f"https://raw.githubusercontent.com/{REPOSITORIO_GITHUB}/main"

AUTORES = "Iván Bonfil, Rafael Rodriguez, Roberto Rojas y Lizeth Franco Nolasco"


def md(texto):
    return [("md", texto.strip("\n"))]


def code(texto, error_esperado=False):
    """Celda de código; con `error_esperado=True` la celda muestra un error a propósito."""
    return [("code", texto.strip("\n"), error_esperado)]


def ejercicio(clave, codigo_inicial):
    """Celda de trabajo + verificación (+ pista/solución en la versión del estudiante)."""
    return [("ejercicio", clave, codigo_inicial.strip("\n"))]


def encabezado(numero, titulo, descripcion, carpeta, archivo):
    badge = (f'<a href="https://colab.research.google.com/github/{REPOSITORIO_GITHUB}/'
             f'blob/main/{carpeta}/{archivo}" target="_parent">'
             '<img src="https://colab.research.google.com/assets/colab-badge.svg" '
             'alt="Abrir en Colab"/></a>')
    return md(badge) + md(f"""
# **Curso introductorio de Python**
## **Facultad de Química, UNAM** · Departamento de Física y Química Teórica

**Elaboraron:** {AUTORES}

---

# **Sesión {numero}: {titulo}**

{descripcion}
""")


def instrucciones(numero):
    return md("""
## **¿Cómo usar este notebook?**

Este notebook es **interactivo**: cada ejercicio tiene una celda de código para tu respuesta y
una celda que la **verifica automáticamente**, como en los cursos de [Kaggle Learn](https://www.kaggle.com/learn).

1. Ejecuta la celda de **configuración** que está justo abajo (una sola vez, al abrir el notebook).
2. En cada ejercicio, sustituye los espacios `____` por tu código y ejecuta la celda.
3. Ejecuta la celda `ejN.verificar()`. Verás uno de estos mensajes:
   - ✅ **¡Correcto!** — puedes continuar.
   - ❌ **Incorrecto** — el mensaje te dice qué revisar.
   - ✏️ **Pendiente** — aún falta completar algo.
4. Si te atoras, quita el `#` de `ejN.pista()` para recibir una pista, o de `ejN.solucion()`
   para ver una solución. **Intenta resolverlo antes de ver la solución.**
5. Ejecuta `progreso()` en cualquier momento para ver tu avance en la sesión.

> 📋 **Registro de avance.** Si tu docente lo solicita, escribe en la celda de configuración tu
> número de cuenta (o el alias que te asignen) y la clave del grupo. Así el equipo docente sabe
> en qué ejercicios necesita ayuda el grupo. Solo se envía el resultado de cada verificación,
> **nunca tu código**. Si no te lo piden, deja los campos vacíos.

> 💡 El verificador lee las variables del notebook. Si reinicias el entorno de ejecución, vuelve
> a ejecutar la celda de configuración y las celdas anteriores al ejercicio.
""") + code(f"""
# ⚙️ Configuración: ejecuta esta celda antes de empezar
import os
import sys
import urllib.request

REPOSITORIO = "{URL_CRUDA}"

if os.path.isdir("../verificador"):      # Copia local del repositorio
    sys.path.insert(0, "..")
else:                                     # Google Colab: descarga el verificador
    os.makedirs("verificador", exist_ok=True)
    for archivo in ["__init__.py", "nucleo.py", "registro.py", "configuracion.py",
                    "sesion{numero}.py"]:
        urllib.request.urlretrieve(f"{{REPOSITORIO}}/verificador/{{archivo}}",
                                   f"verificador/{{archivo}}")

from verificador.sesion{numero} import *

# 📋 Registro de avance (solo si tu docente lo pide): tu identificador y la clave del grupo
iniciar_registro(alumno="", clave="")
""")


def cierre():
    return md("""
## **Tu progreso**

Ejecuta la siguiente celda para ver cuántos ejercicios resolviste en esta sesión.
""") + code("progreso()")
