from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/integra", tags=["Integra"])

@router.post("/")
def crear_integra(
    cc: str,
    numero_lista: int,
    orden_integrantes: int,
    organo: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO integra (CC, numeroLista, ordenIntegrantes, organo) VALUES (%s, %s, %s, %s)",
                (cc, numero_lista, orden_integrantes, organo)
            )
        return {"msg": "Integración creada correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="La integración ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_integra():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, numeroLista, ordenIntegrantes, organo FROM integra")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{cc}/{numero_lista}")
def modificar_integra(
    cc: str,
    numero_lista: int,
    orden_integrantes: int = None,
    organo: str = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if orden_integrantes is not None:
                updates.append("ordenIntegrantes = %s")
                params.append(orden_integrantes)
            if organo is not None:
                updates.append("organo = %s")
                params.append(organo)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.extend([cc, numero_lista])
            sql = f"UPDATE integra SET {', '.join(updates)} WHERE CC = %s AND numeroLista = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Integración no encontrada")
        return {"msg": "Integración modificada correctamente"}
    finally:
        conn.close()

@router.delete("/{cc}/{numero_lista}")
def eliminar_integra(cc: str, numero_lista: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM integra WHERE CC = %s AND numeroLista = %s", (cc, numero_lista))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Integración no encontrada")
        return {"msg": "Integración eliminada"}
    finally:
        conn.close() 