/**
 * Registro de avance del Curso de Python FQ.
 *
 * Recibe los resultados que envía el paquete `verificador` desde los notebooks
 * y los guarda en dos hojas de este libro de Google Sheets:
 *
 *   Eventos  — una fila por cada verificación, pista o solución (historial completo).
 *   Tablero  — una fila por estudiante y una columna por ejercicio, con su estado
 *              más reciente (✅ se conserva aunque después haya un intento fallido).
 *
 * Instalación: ver seguimiento/README.md.
 */

const HOJA_EVENTOS = "Eventos";
const HOJA_TABLERO = "Tablero";
const ENCABEZADOS = ["recibido", "marca_cliente", "alumno", "sesion", "ejercicio",
                     "evento", "intento", "detalle"];
const ICONOS = { correcto: "✅", incorrecto: "❌", pendiente: "✏️" };
const COLORES = { correcto: "#d9f2e0", incorrecto: "#fbe0dc", pendiente: "#dde9fb" };
const COLUMNA_INICIAL = 3;   // A: alumno, B: resueltos, C en adelante: ejercicios

function doGet() {
  return responder({ ok: true, mensaje: "Registro del Curso de Python FQ activo." });
}

function doPost(e) {
  let datos;
  try {
    datos = JSON.parse(e.postData.contents);
  } catch (error) {
    return responder({ ok: false, error: "datos no válidos" });
  }

  const clave = PropertiesService.getScriptProperties().getProperty("CLAVE");
  if (!clave || datos.clave !== clave) {
    return responder({ ok: false, error: "clave del grupo incorrecta" });
  }
  const alumno = texto(datos.alumno, 60);
  if (!alumno) {
    return responder({ ok: false, error: "falta el identificador del estudiante" });
  }

  const candado = LockService.getScriptLock();
  candado.waitLock(10000);
  try {
    const libro = SpreadsheetApp.getActiveSpreadsheet();
    const sesion = texto(datos.sesion, 10);
    const ejercicio = texto(datos.ejercicio, 20);
    const evento = texto(datos.evento, 20);
    hoja(libro, HOJA_EVENTOS, ENCABEZADOS).appendRow([
      new Date(), texto(datos.marca_tiempo, 40), alumno, sesion, ejercicio, evento,
      Number(datos.intento) || 0, texto(datos.detalle, 300),
    ]);
    if (ICONOS[evento]) {
      actualizarTablero(libro, alumno, sesion + " · " + ejercicio, evento);
    }
  } finally {
    candado.releaseLock();
  }
  return responder({ ok: true });
}

function actualizarTablero(libro, alumno, columna, evento) {
  const tablero = hoja(libro, HOJA_TABLERO, ["Alumno", "Resueltos"]);

  const encabezados = tablero.getRange(1, 1, 1, tablero.getLastColumn()).getValues()[0];
  let col = encabezados.indexOf(columna) + 1;
  if (col === 0) {
    col = Math.max(tablero.getLastColumn() + 1, COLUMNA_INICIAL);
    tablero.getRange(1, col).setValue(columna).setFontWeight("bold");
  }

  const filas = tablero.getLastRow();
  const alumnos = filas > 1 ? tablero.getRange(2, 1, filas - 1, 1).getValues().flat() : [];
  let fila = alumnos.indexOf(alumno) + 2;
  if (fila === 1) {
    fila = filas + 1;
    tablero.getRange(fila, 1).setValue(alumno);
    tablero.getRange(fila, 2).setFormula(`=COUNTIF(C${fila}:${fila}, "✅")`);
  }

  const celda = tablero.getRange(fila, col);
  if (celda.getValue() === ICONOS.correcto) return;   // Lo resuelto se queda resuelto
  celda.setValue(ICONOS[evento]).setBackground(COLORES[evento]).setHorizontalAlignment("center");
}

function hoja(libro, nombre, encabezados) {
  let h = libro.getSheetByName(nombre);
  if (!h) {
    h = libro.insertSheet(nombre);
    h.getRange(1, 1, 1, encabezados.length).setValues([encabezados]).setFontWeight("bold");
    h.setFrozenRows(1);
    h.setFrozenColumns(1);
  }
  return h;
}

/** Recorta y neutraliza textos que Sheets podría interpretar como fórmulas. */
function texto(valor, maximo) {
  const limpio = String(valor === undefined || valor === null ? "" : valor).trim().slice(0, maximo);
  return /^[=+\-@]/.test(limpio) ? "'" + limpio : limpio;
}

function responder(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}
