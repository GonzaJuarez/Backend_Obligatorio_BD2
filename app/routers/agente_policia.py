from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/agentes_policia", tags=["AgentesPolicia"])

@router.post("/")
def crear_agente_policia(
    cc: str,
    id_establecimiento: int,
    comisaria: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO agentePolicia (CC, IDEstablecimiento, Comisaria) VALUES (%s, %s, %s)",
                (cc, id_establecimiento, comisaria)
            )
        return {"msg": "Agente de policía creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El agente ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_agentes_policia():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, IDEstablecimiento, Comisaria FROM agentePolicia")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{cc}")
def modificar_agente_policia(
    cc: str,
    id_establecimiento: int = None,
    comisaria: str = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if id_establecimiento is not None:
                updates.append("IDEstablecimiento = %s")
                params.append(id_establecimiento)
            if comisaria is not None:
                updates.append("Comisaria = %s")
                params.append(comisaria)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(cc)
            sql = f"UPDATE agentePolicia SET {', '.join(updates)} WHERE CC = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Agente no encontrado")
        return {"msg": "Agente de policía modificado correctamente"}
    finally:
        conn.close()

@router.delete("/{cc}")
def eliminar_agente_policia(cc: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM agentePolicia WHERE CC = %s", (cc,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Agente no encontrado")
        return {"msg": "Agente de policía eliminado"}
    finally:
        conn.close() 