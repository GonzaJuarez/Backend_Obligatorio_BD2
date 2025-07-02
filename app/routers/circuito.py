from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])

@router.post("/")
def crear_circuito(
    id: int,
    departamento: str,
    localidad: str,
    direccion: str,
    barrio: str,
    accesible: bool,
    id_establecimiento: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO circuito (ID, departamento, localidad, direccion, barrio, accesible, IDEstablecimiento) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id, departamento, localidad, direccion, barrio, accesible, id_establecimiento)
            )
        return {"msg": "Circuito creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El circuito ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_circuitos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, departamento, localidad, direccion, barrio, accesible, IDEstablecimiento FROM circuito")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{id}")
def modificar_circuito(
    id: int,
    departamento: str = None,
    localidad: str = None,
    direccion: str = None,
    barrio: str = None,
    accesible: bool = None,
    id_establecimiento: int = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if departamento is not None:
                updates.append("departamento = %s")
                params.append(departamento)
            if localidad is not None:
                updates.append("localidad = %s")
                params.append(localidad)
            if direccion is not None:
                updates.append("direccion = %s")
                params.append(direccion)
            if barrio is not None:
                updates.append("barrio = %s")
                params.append(barrio)
            if accesible is not None:
                updates.append("accesible = %s")
                params.append(accesible)
            if id_establecimiento is not None:
                updates.append("IDEstablecimiento = %s")
                params.append(id_establecimiento)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(id)
            sql = f"UPDATE circuito SET {', '.join(updates)} WHERE ID = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Circuito no encontrado")
        return {"msg": "Circuito modificado correctamente"}
    finally:
        conn.close()

@router.delete("/{id}")
def eliminar_circuito(id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM circuito WHERE ID = %s", (id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Circuito no encontrado")
        return {"msg": "Circuito eliminado"}
    finally:
        conn.close() 