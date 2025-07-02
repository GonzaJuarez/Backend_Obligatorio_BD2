# Sistema de Gestión Electoral - API Backend

Este backend implementa un sistema de gestión electoral con FastAPI y MySQL. Cada tabla del modelo relacional tiene su propio router con endpoints CRUD.

## Tablas y Endpoints

- **Votante** (`/votantes`)
  - POST `/` : Crear votante
  - GET `/` : Listar votantes
  - PUT `/{cc}` : Modificar votante
  - DELETE `/{cc}` : Eliminar votante

- **miembroMesa** (`/operadores`)
  - POST `/login` : Login operador/admin
  - POST `/` : Crear operador/admin
  - GET `/` : Listar operadores/admins
  - DELETE `/{cc}` : Eliminar operador/admin

- **circuito** (`/circuitos`)
  - POST `/` : Crear circuito
  - GET `/` : Listar circuitos
  - PUT `/{id}` : Modificar circuito
  - DELETE `/{id}` : Eliminar circuito

- **Establecimiento** (`/establecimientos`)
  - POST `/` : Crear establecimiento
  - GET `/` : Listar establecimientos
  - PUT `/{id}` : Modificar establecimiento
  - DELETE `/{id}` : Eliminar establecimiento

- **agentePolicia** (`/agentes_policia`)
  - POST `/` : Crear agente
  - GET `/` : Listar agentes
  - PUT `/{cc}` : Modificar agente
  - DELETE `/{cc}` : Eliminar agente

- **integranteLista** (`/integrantes_lista`)
  - POST `/` : Crear integrante
  - GET `/` : Listar integrantes
  - DELETE `/{cc}` : Eliminar integrante

- **partidoPolitico** (`/partidos_politicos`)
  - POST `/` : Crear partido
  - GET `/` : Listar partidos
  - PUT `/{id}` : Modificar partido
  - DELETE `/{id}` : Eliminar partido

- **candidato** (`/candidatos`)
  - POST `/` : Crear candidato
  - GET `/` : Listar candidatos
  - PUT `/{cc}` : Modificar candidato
  - DELETE `/{cc}` : Eliminar candidato

- **eleccion** (`/elecciones`)
  - POST `/` : Crear elección
  - GET `/` : Listar elecciones
  - DELETE `/{id_eleccion}` : Eliminar elección

- **lista** (`/elecciones/listas`)
  - POST `/` : Crear lista
  - GET `/` : Listar listas
  - DELETE `/{numero}/{id_eleccion}` : Eliminar lista

- **integra** (`/integra`)
  - POST `/` : Crear integración
  - GET `/` : Listar integraciones
  - PUT `/{cc}/{numero_lista}` : Modificar integración
  - DELETE `/{cc}/{numero_lista}` : Eliminar integración

- **incluye** (`/incluye`)
  - POST `/` : Crear inclusión
  - GET `/` : Listar inclusiones
  - DELETE `/{id_voto}/{numero_lista}` : Eliminar inclusión

- **listaCredenciales** (`/lista_credenciales`)
  - POST `/` : Agregar credencial
  - GET `/` : Listar credenciales
  - DELETE `/{cc}/{id_circuito}` : Eliminar credencial

- **registroDeEmision** (`/registro_emision`)
  - POST `/` : Crear registro
  - GET `/` : Listar registros
  - DELETE `/{cc}/{id_eleccion}` : Eliminar registro

- **voto** (`/votos`)
  - POST `/` : Emitir voto
  - GET `/por_circuito/{id_circuito}` : Listar votos por circuito
  - GET `/resultados/{id_eleccion}` : Ver resultados por elección

---

## Archivos del proyecto

- `main.py`: Inicializa la app y registra todos los routers.
- `db.py`: Conexión a la base de datos MySQL.
- `auth.py`: Lógica de autenticación y JWT.
- `security.py`: Hash y verificación de contraseñas.
- `dependencies.py`: Dependencias de roles y permisos.
- `routers/`: Carpeta con todos los routers/endpoints.
- `__init__.py`: Inicialización de módulos (vacío).

---

## Notas
- Todos los endpoints CRUD están implementados y disponibles.
- Solo el login de operador requiere autenticación, el resto de los endpoints son públicos.
- Puedes probar todos los endpoints desde `/docs` de FastAPI.