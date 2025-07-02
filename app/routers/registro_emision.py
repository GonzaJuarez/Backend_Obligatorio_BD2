from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/registro_emision", tags=["RegistroEmision"])

@router.post("/")
def crear_registro_emision(
    cc: str,
    id_eleccion: int,
    fecha_hora: str,
    id_circuito: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO registroDeEmision (CC, IDEleccion, fechaHora, IDCircuito) VALUES (%s, %s, %s, %s)",
                (cc, id_eleccion, fecha_hora, id_circuito)
            )
        return {"msg": "Registro de emisión creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El registro ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_registros_emision():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, IDEleccion, fechaHora, IDCircuito FROM registroDeEmision")
            return cursor.fetchall()
    finally:
        conn.close()

@router.delete("/{cc}/{id_eleccion}")
def eliminar_registro_emision(cc: str, id_eleccion: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM registroDeEmision WHERE CC = %s AND IDEleccion = %s", (cc, id_eleccion))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Registro no encontrado")
        return {"msg": "Registro de emisión eliminado"}
    finally:
        conn.close() 