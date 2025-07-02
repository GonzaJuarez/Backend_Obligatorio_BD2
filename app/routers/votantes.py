from fastapi import APIRouter, Depends, HTTPException
from app.db import get_connection
from app.dependencies import require_admin
import pymysql

router = APIRouter(prefix="/votantes", tags=["Votantes"])


@router.post("/", dependencies=[Depends(require_admin)])
def crear_votante(
    cc: str,
    ci: str,
    nombre: str,
    direccion: str,
    fecha_nacimiento: str
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Votante (CC, CI, nombre, direccion, fechaNacimiento) VALUES (%s, %s, %s, %s, %s)",
                (cc, ci, nombre, direccion, fecha_nacimiento)
            )
        return {"msg": "Votante creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El votante ya existe o datos inválidos")
    finally:
        conn.close()


@router.get("/", dependencies=[Depends(require_admin)])
def listar_votantes():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, CI, nombre, direccion, fechaNacimiento FROM Votante")
            return cursor.fetchall()
    finally:
        conn.close()


@router.put("/{cc}", dependencies=[Depends(require_admin)])
def modificar_votante(
    cc: str,
    ci: str = None,
    nombre: str = None,
    direccion: str = None,
    fecha_nacimiento: str = None
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            updates = []
            params = []
            if ci:
                updates.append("CI = %s")
                params.append(ci)
            if nombre:
                updates.append("nombre = %s")
                params.append(nombre)
            if direccion:
                updates.append("direccion = %s")
                params.append(direccion)
            if fecha_nacimiento:
                updates.append("fechaNacimiento = %s")
                params.append(fecha_nacimiento)
            if not updates:
                raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            params.append(cc)
            sql = f"UPDATE Votante SET {', '.join(updates)} WHERE CC = %s"
            cursor.execute(sql, tuple(params))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Votante no encontrado")
        return {"msg": "Votante modificado correctamente"}
    finally:
        conn.close()


@router.delete("/{cc}", dependencies=[Depends(require_admin)])
def eliminar_votante(cc: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Votante WHERE CC = %s", (cc,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Votante no encontrado")
        return {"msg": "Votante eliminado"}
    finally:
        conn.close()