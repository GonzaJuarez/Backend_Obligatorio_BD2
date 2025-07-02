from fastapi import APIRouter, Depends, HTTPException
from app.db import get_connection
from app.dependencies import require_admin, get_current_user
import pymysql

router = APIRouter(prefix="/elecciones", tags=["Elecciones"])


@router.post("/", dependencies=[Depends(require_admin)])
def crear_eleccion(
    fecha: str,
    tipo: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO eleccion (fecha, tipo) VALUES (%s, %s)",
                (fecha, tipo)
            )
        return {"msg": "Elección creada correctamente"}
    finally:
        conn.close()


@router.get("/")
def listar_elecciones(user=Depends(get_current_user)):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, fecha, tipo FROM eleccion")
            return cursor.fetchall()
    finally:
        conn.close()


@router.delete("/{id_eleccion}", dependencies=[Depends(require_admin)])
def eliminar_eleccion(id_eleccion: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM eleccion WHERE ID = %s", (id_eleccion,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Elección no encontrada")
        return {"msg": "Elección eliminada"}
    finally:
        conn.close()


@router.post("/listas", dependencies=[Depends(require_admin)])
def crear_lista(
    numero: int,
    id_eleccion: int,
    departamento: str,
    id_partido_politico: int,
    cc_candidato: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO lista (numero, IDEleccion, departamento, IDPartidoPolitico, CCCandidato) VALUES (%s, %s, %s, %s, %s)",
                (numero, id_eleccion, departamento, id_partido_politico, cc_candidato)
            )
        return {"msg": "Lista creada correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="Datos inválidos o lista ya existe")
    finally:
        conn.close()

@router.get("/listas")
def listar_listas(user=Depends(get_current_user)):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT numero, IDEleccion, departamento, IDPartidoPolitico, CCCandidato FROM lista")
            return cursor.fetchall()
    finally:
        conn.close()

@router.delete("/listas/{numero}/{id_eleccion}", dependencies=[Depends(require_admin)])
def eliminar_lista(numero: int, id_eleccion: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM lista WHERE numero = %s AND IDEleccion = %s",
                (numero, id_eleccion)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Lista no encontrada")
        return {"msg": "Lista eliminada"}
    finally:
        conn.close()