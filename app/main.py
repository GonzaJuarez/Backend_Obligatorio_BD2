from fastapi import FastAPI
from app.routers import operadores, votantes, votos, elecciones, circuito_router, establecimiento_router, agente_policia_router, integrante_lista_router, integra_router, incluye_router, lista_credenciales_router, registro_emision_router

app = FastAPI(
    title="API Sistema de Votación Electrónico",
    description="API para gestión de elecciones, votantes, votos y operadores/admins.",
    version="1.0.0"
)

app.include_router(operadores.router)
app.include_router(votantes.router)
app.include_router(votos.router)
app.include_router(elecciones.router)
app.include_router(circuito_router)
app.include_router(establecimiento_router)
app.include_router(agente_policia_router)
app.include_router(integrante_lista_router)
app.include_router(integra_router)
app.include_router(incluye_router)
app.include_router(lista_credenciales_router)
app.include_router(registro_emision_router)