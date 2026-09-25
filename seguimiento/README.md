# Seguimiento del grupo para el equipo docente

Cada vez que un estudiante ejecuta `verificar()`, `pista()` o `solucion()`, el verificador puede
enviar el resultado a una hoja de cálculo de Google del equipo docente. Con esos datos, el
docente sabe **en tiempo real** si el grupo puede avanzar, quién necesita ayuda y qué errores
conviene repasar.

| Pieza | Qué hace |
| :--- | :--- |
| `verificador/registro.py` | Envía cada resultado en segundo plano. Si la red falla, la clase sigue sin interrupciones. |
| `registro_apps_script.gs` | Recibe los resultados en Google Sheets: hoja **Eventos** (historial) y hoja **Tablero** (✅ ❌ ✏️ por estudiante y ejercicio, en vivo). |
| `Tablero_docente.ipynb` | Análisis en Colab: semáforo por ejercicio, estudiantes atorados, errores frecuentes y ritmo del grupo. Trae datos de ejemplo para practicar. |

## Estrategia de seguimiento

### Antes de la clase

1. **Instala el registro** (ver abajo) y elige una **clave del grupo** nueva para cada sesión.
2. **Prepara una lista de identificadores.** Recomendamos alias (`A01`, `A02`, …) repartidos en
   una lista que solo tiene el equipo docente, en lugar de nombres. El número de cuenta también
   funciona, pero es un dato personal.
3. **Distribuye los papeles.** Quien imparte la clase mira el semáforo; si hay ayudantes, cada
   uno atiende la lista de estudiantes atorados.
4. **Practica con el tablero** abriendo `Tablero_docente.ipynb` sin configurar nada: usa una
   Sesión 1 simulada con 24 estudiantes.

### Durante la clase

| Momento | Qué mirar | Decisión |
| :--- | :--- | :--- |
| Minuto 5 | Hoja **Tablero**: ¿aparecen todos los estudiantes? | Ayudar a quien no se haya conectado (clave mal escrita, celda de configuración sin ejecutar). |
| Al terminar cada ejercicio | Semáforo del ejercicio | 🟢 ≥ 70 % resuelto: avanzar. 🟡 40–70 %: repasar 2–3 minutos el error más frecuente. 🔴 < 40 %: resolverlo en el pizarrón. |
| Cada 20–30 minutos | Estudiantes **atorados** (≥ 3 intentos fallidos) y **sin actividad** (≥ 15 min) | Un ayudante se acerca primero a quien lleva más intentos. |
| Antes de la autoevaluación | Ritmo del grupo | Si la mayoría no llegará, dejar la autoevaluación (y el tema extra) como tarea. |

La hoja **Tablero** se actualiza sola y basta para decidir en clase; el notebook añade el detalle
(errores frecuentes, ritmo) cuando hay un momento para revisarlo.

**Cómo leer las señales:**

- **Muchos ❌ con el mismo mensaje** → el error es de explicación, no de cada estudiante. Repasar
  con el grupo.
- **Soluciones vistas sin intentos previos** → el ejercicio parece inalcanzable. Dar la pista en
  voz alta y pedir que lo intenten antes de abrir la solución.
- **Un estudiante con ✏️ en todo** → probablemente no está ejecutando las celdas en orden. Una
  visita rápida suele resolverlo.

### Después de la clase

1. Ejecuta `Tablero_docente.ipynb` con `SESION` = la sesión del día.
2. Usa los **3 errores más frecuentes** para preparar un repaso de 10 minutos al inicio de la
   siguiente sesión.
3. Envía material de refuerzo a quienes no llegaron a la autoevaluación.
4. Anota qué ejercicios quedaron en 🔴 para ajustar el material de la siguiente edición.

## Instalación (una sola vez, unos 10 minutos)

1. **Crea la hoja de cálculo.** En Google Drive, crea una hoja nueva (por ejemplo, *Registro
   Curso Python FQ*). Las pestañas **Eventos** y **Tablero** se crean solas con el primer registro.
2. **Pega el script.** En la hoja: *Extensiones → Apps Script*. Borra el contenido de `Código.gs`,
   pega el de `registro_apps_script.gs` y guarda.
3. **Define la clave del grupo.** En Apps Script: *Configuración del proyecto (⚙️) → Propiedades
   de la secuencia de comandos → Agregar propiedad*. Nombre: `CLAVE`; valor: la clave que dirás
   en clase (por ejemplo, `quimica-s1`).
4. **Publica la aplicación web.** *Implementar → Nueva implementación → Tipo: Aplicación web*.
   - *Ejecutar como:* **Yo**.
   - *Quién tiene acceso:* **Cualquier usuario** (necesario para que Colab pueda enviar datos;
     sin la clave del grupo, los envíos se rechazan).

   Autoriza los permisos y copia la **URL de la aplicación web** (termina en `/exec`).
5. **Comprueba la URL** abriéndola en el navegador: debe responder
   `{"ok":true,"mensaje":"Registro del Curso de Python FQ activo."}`.
6. **Actívala en el verificador.** Pega la URL en `verificador/configuracion.py`
   (`URL_REGISTRO = "https://script.google.com/macros/s/.../exec"`) y súbela a la rama `main`.
   Los notebooks descargan el verificador cada vez que se abren, así que el cambio llega a todos
   los estudiantes sin regenerar nada.
7. **En clase**, los estudiantes escriben su identificador y la clave en la celda de configuración:

   ```python
   iniciar_registro(alumno="A07", clave="quimica-s1")
   ```

> Para cambiar la clave entre sesiones basta con editar la propiedad `CLAVE`; no hace falta volver
> a implementar. Si modificas el código del script, crea una **nueva versión** de la implementación
> (*Implementar → Administrar implementaciones → Editar → Nueva versión*) para conservar la URL.

## Privacidad

- **Qué se envía:** identificador, sesión, ejercicio, resultado, número de intento y el mensaje
  del verificador (por ejemplo, «`x` vale 77.1, pero no es el valor esperado»). **Nunca se envía
  el código del estudiante.**
- **Es opcional:** si el estudiante deja vacía la celda de `iniciar_registro`, no se envía nada.
  Informa al grupo al inicio del curso para qué se usan los datos.
- **Dónde queda:** en la hoja de cálculo privada de quien implementó el script. No la compartas
  fuera del equipo docente.
- **Cuánto tiempo:** al terminar el curso, borra la hoja o sustituye los identificadores.
- La URL de la aplicación web queda visible en el repositorio público; la clave del grupo evita
  envíos ajenos. Cámbiala en cada sesión.
