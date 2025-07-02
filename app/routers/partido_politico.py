from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/partidos_politicos", tags=["PartidosPoliticos"])

@router.post("/")
def crear_partido_politico(
    id: int,
    direccion_sede: str,
    autoridades: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO partidoPolitico (ID, direccionSede, autoridades) VALUES (%s, %s, %s)",
                (id, direccion_sede, autoridades)
            )
        return {"msg": "Partido político creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El partido ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_partidos_politicos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, direccionSede, autoridades FROM partidoPolitico")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{id}")
def modificar_partido_politico(
    id: int,
    direccion_sede: str = None,
    autoridades: str = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if direccion_sede is not None:
                updates.append("direccionSede = %s")
                params.append(direccion_sede)
            if autoridades is not None:
                updates.append("autoridades = %s")
                params.append(autoridades)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(id)
            sql = f"UPDATE partidoPolitico SET {', '.join(updates)} WHERE ID = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Partido no encontrado")
        return {"msg": "Partido político modificado correctamente"}
    finally:
        conn.close()

@router.delete("/{id}")
def eliminar_partido_politico(id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM partidoPolitico WHERE ID = %s", (id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Partido no encontrado")
        return {"msg": "Partido político eliminado"}
    finally:
        conn.close() 