from fastapi import APIRouter, HTTPException
from app.db import get_connection
import pymysql

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])

@router.post("/")
def crear_candidato(
    cc: str,
    id_partido_politico: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO candidato (CC, IDPartidoPolitico) VALUES (%s, %s)",
                (cc, id_partido_politico)
            )
        return {"msg": "Candidato creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El candidato ya existe o datos inválidos")
    finally:
        conn.close()

@router.get("/")
def listar_candidatos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, IDPartidoPolitico FROM candidato")
            return cursor.fetchall()
    finally:
        conn.close()

@router.put("/{cc}")
def modificar_candidato(
    cc: str,
    id_partido_politico: int = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if id_partido_politico is not None:
                updates.append("IDPartidoPolitico = %s")
                params.append(id_partido_politico)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(cc)
            sql = f"UPDATE candidato SET {', '.join(updates)} WHERE CC = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidato no encontrado")
        return {"msg": "Candidato modificado correctamente"}
    finally:
        conn.close()

@router.delete("/{cc}")
def eliminar_candidato(cc: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM candidato WHERE CC = %s", (cc,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidato no encontrado")
        return {"msg": "Candidato eliminado"}
    finally:
        conn.close() 