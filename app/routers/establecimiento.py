from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/establecimientos", tags=["Establecimientos"])

@router.post("/")
def crear_establecimiento(
    id: int,
    nombre: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Establecimiento (ID, nombre) VALUES (%s, %s)",
                (id, nombre)
            )
        return {"msg": "Establecimiento creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El establecimiento ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_establecimientos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, nombre FROM Establecimiento")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{id}")
def modificar_establecimiento(
    id: int,
    nombre: str = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if nombre is not None:
                updates.append("nombre = %s")
                params.append(nombre)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(id)
            sql = f"UPDATE Establecimiento SET {', '.join(updates)} WHERE ID = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
        return {"msg": "Establecimiento modificado correctamente"}
    finally:
        conn.close()

@router.delete("/{id}")
def eliminar_establecimiento(id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Establecimiento WHERE ID = %s", (id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Establecimiento no encontrado")
        return {"msg": "Establecimiento eliminado"}
    finally:
        conn.close() 