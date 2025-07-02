from fastapi import Depends, HTTPException, status
from app.auth import get_current_user

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.get("rol") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el rol '{required_role}'"
            )
        return user
    return role_checker

def require_admin(user=Depends(get_current_user)):
    if user.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere el rol 'admin'"
        )
    return user

def require_operator(user=Depends(get_current_user)):
    if user.get("rol") != "operador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere el rol 'operador'"
        )
    return user