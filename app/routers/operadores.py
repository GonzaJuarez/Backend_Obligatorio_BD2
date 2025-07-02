from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_connection
from app.security import verify_password, hash_password
from app.auth import create_access_token
from app.dependencies import require_admin
import pymysql

router = APIRouter(prefix="/operadores", tags=["Operadores"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cc = form_data.username
    password = form_data.password

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, password, rol FROM miembroMesa WHERE CC = %s", (cc,))
            user = cursor.fetchone()
            if not user or not verify_password(password, user["password"]):
                raise HTTPException(status_code=400, detail="Credenciales incorrectas")
            token = create_access_token({"sub": user["CC"], "rol": user["rol"]})
            return {"access_token": token, "token_type": "bearer"}
    finally:
        conn.close()


@router.post("/", dependencies=[Depends(require_admin)])
def crear_operador(
    cc: str,
    organismo_estado: str,
    password: str,
    rol: str = "operador",
    id_circuito: int = None
):
    if rol not in ("admin", "operador"):
        raise HTTPException(status_code=400, detail="Rol inválido")
    hashed_pw = hash_password(password)
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO miembroMesa (CC, organismoEstado, rol, password, IDCircuito) VALUES (%s, %s, %s, %s, %s)",
                (cc, organismo_estado, rol, hashed_pw, id_circuito)
            )
        return {"msg": f"{rol} creado correctamente"}
    except pymysql.err.IntegrityError:
        raise HTTPException(status_code=400, detail="El usuario ya existe o datos inválidos")
    finally:
        conn.close()


@router.get("/", dependencies=[Depends(require_admin)])
def listar_operadores():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CC, organismoEstado, rol, IDCircuito FROM miembroMesa")
            return cursor.fetchall()
    finally:
        conn.close()


@router.delete("/{cc}", dependencies=[Depends(require_admin)])
def eliminar_operador(cc: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM miembroMesa WHERE CC = %s", (cc,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Operador no encontrado")
        return {"msg": "Operador eliminado"}
    finally:
        conn.close()