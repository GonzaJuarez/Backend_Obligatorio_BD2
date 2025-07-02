from fastapi import APIRouter, Depends, HTTPException
from app.db import get_connection
from app.dependencies import require_operator, get_current_user
import pymysql
from datetime import datetime

router = APIRouter(prefix="/votos", tags=["Votos"])

@router.post("/", dependencies=[Depends(require_operator)])
def emitir_voto(
    id_circuito: int,
    estado: str,
    observado: str,
    numero_lista: int
):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO voto (fechaHora, IDCircuito, estado, observado) VALUES (%s, %s, %s, %s)",
                (datetime.now(), id_circuito, estado, observado)
            )
            voto_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO incluye (IDVoto, numeroLista) VALUES (%s, %s)",
                (voto_id, numero_lista)
            )
        return {"msg": "Voto emitido correctamente"}
    finally:
        conn.close()


@router.get("/por_circuito/{id_circuito}")
def votos_por_circuito(id_circuito: int, user=Depends(get_current_user)):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT v.ID, v.fechaHora, v.estado, v.observado, i.numeroLista "
                "FROM voto v "
                "JOIN incluye i ON v.ID = i.IDVoto "
                "WHERE v.IDCircuito = %s",
                (id_circuito,)
            )
            return cursor.fetchall()
    finally:
        conn.close()

@router.get("/resultados/{id_eleccion}")
def resultados_por_eleccion(id_eleccion: int, user=Depends(get_current_user)):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT l.numero, l.departamento, l.IDPartidoPolitico, COUNT(i.IDVoto) as votos "
                "FROM lista l "
                "LEFT JOIN incluye i ON l.numero = i.numeroLista "
                "LEFT JOIN voto v ON i.IDVoto = v.ID "
                "WHERE l.IDEleccion = %s "
                "GROUP BY l.numero, l.departamento, l.IDPartidoPolitico",
                (id_eleccion,)
            )
            return cursor.fetchall()
    finally:
        conn.close()