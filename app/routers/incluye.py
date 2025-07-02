from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/incluye", tags=["Incluye"])

@router.post("/")
def crear_incluye(
    id_voto: int,
    numero_lista: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO incluye (IDVoto, numeroLista) VALUES (%s, %s)",
                (id_voto, numero_lista)
            )
        return {"msg": "Inclusión creada correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="La inclusión ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_incluye():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT IDVoto, numeroLista FROM incluye")
            return cursor.fetchall()
    finally:
        conn.close()

@router.delete("/{id_voto}/{numero_lista}")
def eliminar_incluye(id_voto: int, numero_lista: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM incluye WHERE IDVoto = %s AND numeroLista = %s", (id_voto, numero_lista))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Inclusión no encontrada")
        return {"msg": "Inclusión eliminada"}
    finally:
        conn.close() 