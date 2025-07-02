from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/integrantes_lista", tags=["IntegrantesLista"])

@router.post("/")
def crear_integrante_lista(
    cc: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO integranteLista (CC) VALUES (%s)",
                (cc,)
            )
        return {"msg": "Integrante de lista creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El integrante ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_integrantes_lista():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC FROM integranteLista")
            return cursor.fetchall()
    finally:
        conn.close()

@router.delete("/{cc}")
def eliminar_integrante_lista(cc: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM integranteLista WHERE CC = %s", (cc,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Integrante no encontrado")
        return {"msg": "Integrante de lista eliminado"}
    finally:
        conn.close() 