"""Contenido del notebook de seguimiento para el equipo docente."""

from bloques import AUTORES, REPOSITORIO_GITHUB, URL_CRUDA, code, md


def fuente(carpeta, archivo):
    badge = (f'<a href="https://colab.research.google.com/github/{REPOSITORIO_GITHUB}/'
             f'blob/main/{carpeta}/{archivo}" target="_parent">'
             '<img src="https://colab.research.google.com/assets/colab-badge.svg" '
             'alt="Abrir en Colab"/></a>')
    return (
        md(badge)
        + md(f"""
# **Tablero de seguimiento del grupo**
## Curso introductorio de Python · Facultad de Química, UNAM

**Elaboraron:** {AUTORES}

Este notebook es **para el equipo docente**. Lee los resultados que los estudiantes envían al
ejecutar `verificar()`, `pista()` y `solucion()` y responde tres preguntas:

1. **¿Podemos avanzar?** Porcentaje del grupo que resolvió cada ejercicio (semáforo).
2. **¿Quién necesita ayuda ahora?** Estudiantes con varios intentos fallidos o sin actividad reciente.
3. **¿Qué hay que repasar?** Los errores más frecuentes de cada ejercicio.

La estrategia completa (antes, durante y después de la clase) y la instalación del registro
están en [`seguimiento/README.md`](https://github.com/{REPOSITORIO_GITHUB}/blob/main/seguimiento/README.md).

> 🔒 Los datos se leen de una hoja de cálculo privada del equipo docente. No publiques este
> notebook con sus salidas.
""")
        + md("""
## **Configuración**

- Deja `URL_HOJA` vacío para practicar con los **datos de ejemplo** (una Sesión 1 simulada).
- Durante la clase, pega la URL de la hoja de cálculo del registro. Colab pedirá permiso para
  leer tu Google Drive.
""")
        + code("""
URL_HOJA = ""              # URL de la hoja de Google Sheets con el registro
SESION = "S1"              # S1, S2 o S3
UMBRAL_INTENTOS = 3        # Intentos fallidos a partir de los cuales alguien necesita ayuda
MINUTOS_INACTIVO = 15      # Minutos sin actividad a partir de los cuales conviene acercarse
ZONA_HORARIA = "America/Mexico_City"
""")
        + code(f"""
import re

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

if URL_HOJA:
    from google.colab import auth
    import gspread
    from google.auth import default

    auth.authenticate_user()
    credenciales, _ = default()
    hoja = gspread.authorize(credenciales).open_by_url(URL_HOJA).worksheet("Eventos")
    eventos = pd.DataFrame(hoja.get_all_records())
else:
    try:
        eventos = pd.read_csv("../seguimiento/eventos_ejemplo.csv")
    except FileNotFoundError:
        eventos = pd.read_csv("{URL_CRUDA}/seguimiento/eventos_ejemplo.csv")
    print("Usando datos de ejemplo.")

eventos["alumno"] = eventos["alumno"].astype(str)
eventos["hora"] = (pd.to_datetime(eventos["marca_cliente"], utc=True, errors="coerce")
                   .dt.tz_convert(ZONA_HORARIA))
eventos = eventos[eventos["sesion"] == SESION].sort_values("hora")
eventos["detalle"] = eventos["detalle"].fillna("").astype(str)

alumnos = sorted(eventos["alumno"].unique())
print(f"{{SESION}}: {{len(eventos)}} eventos de {{len(alumnos)}} estudiantes")
print(f"Primer evento: {{eventos['hora'].min():%H:%M}}, último: {{eventos['hora'].max():%H:%M}}")
""")
        + md("""
## **1. ¿Podemos avanzar?**

Para cada ejercicio: cuántos estudiantes lo resolvieron, cuántos intentos necesitaron y cuántos
pidieron pista o solución. El semáforo compara lo resuelto con el total de estudiantes conectados:

| Semáforo | Resuelto | Sugerencia |
| :-: | :-: | :--- |
| 🟢 | ≥ 70 % | Avanzar; ayudar individualmente a quien falte. |
| 🟡 | 40–70 % | Repaso breve (2–3 min) del error más frecuente y avanzar. |
| 🔴 | < 40 % | Detenerse: resolverlo en el pizarrón con el grupo. |
""")
        + code("""
def orden_ejercicio(clave):
    \"\"\"ej1 < ej2a < ej2b < … < auto1 < … < extra1.\"\"\"
    partes = re.match(r"([a-z]+)(\\d+)([a-z]*)", clave)
    if not partes:
        return (9, 0, clave)
    prefijo, numero, letra = partes.groups()
    return ({"ej": 0, "auto": 1, "extra": 2}.get(prefijo, 3), int(numero), letra)


verificaciones = eventos[eventos["evento"].isin(["correcto", "incorrecto", "pendiente"])]
ejercicios = sorted(verificaciones["ejercicio"].unique(), key=orden_ejercicio)


def resumen_ejercicio(clave):
    ev = eventos[eventos["ejercicio"] == clave]
    resueltos = ev.loc[ev["evento"] == "correcto", "alumno"].unique()
    intentos = (ev[ev["evento"] == "correcto"].groupby("alumno")["intento"].min())
    porcentaje = 100 * len(resueltos) / len(alumnos)
    semaforo = "🟢" if porcentaje >= 70 else "🟡" if porcentaje >= 40 else "🔴"
    return {
        "ejercicio": clave,
        "semáforo": semaforo,
        "intentaron": ev.loc[ev["evento"].isin(["correcto", "incorrecto"]), "alumno"].nunique(),
        "resolvieron": len(resueltos),
        "% del grupo": round(porcentaje),
        "intentos (mediana)": intentos.median(),
        "pidieron pista": ev.loc[ev["evento"] == "pista", "alumno"].nunique(),
        "vieron solución": ev.loc[ev["evento"] == "solucion", "alumno"].nunique(),
    }


tabla = pd.DataFrame([resumen_ejercicio(e) for e in ejercicios]).set_index("ejercicio")
tabla
""")
        + md("""
### Mapa del grupo

Cada fila es un estudiante y cada columna un ejercicio, con el estado más reciente
(un ✅ se conserva aunque después haya otro intento).
""")
        + code("""
CODIGOS = {"sin intentar": 0, "pendiente": 1, "incorrecto": 2, "correcto": 3}
COLORES = ["#eceff4", "#b9d3f7", "#f2a39b", "#86cf9c"]


def estado_final(grupo):
    estados = set(grupo)
    for estado in ("correcto", "incorrecto", "pendiente"):
        if estado in estados:
            return CODIGOS[estado]
    return 0


mapa = (verificaciones.groupby(["alumno", "ejercicio"])["evento"].agg(estado_final)
        .unstack(fill_value=0)
        .reindex(index=alumnos, columns=ejercicios, fill_value=0))

fig, ax = plt.subplots(figsize=(1 + 0.6 * len(ejercicios), 1 + 0.28 * len(alumnos)))
ax.imshow(mapa.values, cmap=ListedColormap(COLORES), vmin=0, vmax=3, aspect="auto")
ax.set_xticks(range(len(ejercicios)), ejercicios, rotation=45, ha="right")
ax.set_yticks(range(len(alumnos)), alumnos)
ax.set_xlabel("Ejercicio")
ax.set_ylabel("Estudiante")
ax.set_title(f"Estado del grupo — {SESION}")
ax.legend(handles=[Patch(color=c, label=e) for e, c in zip(CODIGOS, COLORES)],
          loc="upper left", bbox_to_anchor=(1.01, 1))
plt.show()
""")
        + md("""
## **2. ¿Quién necesita ayuda ahora?**

- **Atorados:** tienen un ejercicio sin resolver con `UMBRAL_INTENTOS` o más intentos fallidos.
- **Sin actividad:** no han enviado nada en los últimos `MINUTOS_INACTIVO` minutos (respecto al
  último evento registrado) y todavía les faltan ejercicios.

Un ayudante puede acercarse primero a quien lleva más intentos.
""")
        + code("""
fallidos = (eventos[eventos["evento"] == "incorrecto"]
            .groupby(["alumno", "ejercicio"]).size().rename("intentos fallidos"))
resueltos = set(map(tuple, eventos.loc[eventos["evento"] == "correcto",
                                       ["alumno", "ejercicio"]].values))
atorados = (fallidos[[par not in resueltos for par in fallidos.index]]
            .loc[lambda s: s >= UMBRAL_INTENTOS]
            .sort_values(ascending=False)
            .reset_index())

ultimo = eventos.groupby("alumno")["hora"].max()
ahora = eventos["hora"].max()
minutos = ((ahora - ultimo).dt.total_seconds() / 60).round()
pendientes = mapa.lt(3).sum(axis=1)
inactivos = (pd.DataFrame({"minutos sin actividad": minutos, "ejercicios por resolver": pendientes})
             .query("`minutos sin actividad` >= @MINUTOS_INACTIVO and `ejercicios por resolver` > 0")
             .sort_values("minutos sin actividad", ascending=False))

print(f"Atorados ({len(atorados)}):")
display(atorados)
print(f"Sin actividad reciente ({len(inactivos)}):")
display(inactivos)
""")
        + md("""
## **3. ¿Qué hay que repasar?**

Los mensajes del verificador revelan el error concreto. Para agruparlos se sustituyen los
números por `#`, de modo que «`x` vale 77.1» y «`x` vale 12» cuentan como el mismo error.
""")
        + code("""
errores = eventos[eventos["evento"] == "incorrecto"].copy()
errores["error"] = (errores["detalle"]
                    .str.replace(r"-?\\d+(\\.\\d+)?(e[+-]?\\d+)?", "#", regex=True)
                    .str.slice(0, 140))

frecuentes = (errores.groupby(["ejercicio", "error"])["alumno"].nunique()
              .rename("estudiantes").reset_index()
              .sort_values(["ejercicio", "estudiantes"], ascending=[True, False])
              .groupby("ejercicio").head(3))
frecuentes["orden"] = frecuentes["ejercicio"].map(orden_ejercicio)
pd.set_option("display.max_colwidth", 150)
frecuentes.sort_values(["orden", "estudiantes"], ascending=[True, False]).drop(columns="orden")
""")
        + md("""
### Ritmo del grupo

Porcentaje acumulado del grupo que ha resuelto cada ejercicio a lo largo de la clase. Una curva
que tarda en subir indica un ejercicio que necesita más tiempo o una mejor explicación.
""")
        + code("""
primer_acierto = (eventos[eventos["evento"] == "correcto"]
                  .groupby(["ejercicio", "alumno"])["hora"].min().reset_index())

fig, ax = plt.subplots(figsize=(9, 4.5))
for clave in ejercicios:
    horas = primer_acierto.loc[primer_acierto["ejercicio"] == clave, "hora"].sort_values()
    if horas.empty:
        continue
    porcentaje = 100 * pd.Series(range(1, len(horas) + 1), index=horas) / len(alumnos)
    ax.step(porcentaje.index, porcentaje.values, where="post", label=clave)
ax.axhline(70, color="gray", linestyle=":", label="70 % del grupo")
ax.set_xlabel("Hora")
ax.set_ylabel("Estudiantes que lo resolvieron (%)")
ax.set_ylim(0, 105)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=ZONA_HORARIA))
ax.legend(ncol=2, fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
plt.show()
""")
        + md("""
## **Después de la clase**

1. Guarda la tabla del apartado 1 y los errores frecuentes: son la base del repaso de 10 minutos
   al inicio de la siguiente sesión.
2. Envía material de refuerzo a quienes no llegaron a la autoevaluación.
3. Al terminar el curso, borra la hoja de cálculo o quita los identificadores (ver la sección de
   privacidad del README de seguimiento).
""")
    )
