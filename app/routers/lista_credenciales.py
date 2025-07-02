from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/lista_credenciales", tags=["ListaCredenciales"])

@router.post("/")
def crear_lista_credencial(
    cc: str,
    id_circuito: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO listaCredenciales (CC, IDCircuito) VALUES (%s, %s)",
                (cc, id_circuito)
            )
        return {"msg": "Credencial agregada correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="La credencial ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_lista_credenciales():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, IDCircuito FROM listaCredenciales")
            return cursor.fetchall()
    finally:
        conn.close()

@router.delete("/{cc}/{id_circuito}")
def eliminar_lista_credencial(cc: str, id_circuito: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM listaCredenciales WHERE CC = %s AND IDCircuito = %s", (cc, id_circuito))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Credencial no encontrada")
        return {"msg": "Credencial eliminada"}
    finally:
        conn.close() 