from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Request, Response
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uuid
import re
from routers.partidos_router import partidos_route
from datetime import datetime

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # Aquí coloca la URL de tu frontend
    "https://tu-dominio-frontend.com",  # Si tienes un dominio en producción, agrégalo aquí
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para manejar errores HTTP (si es necesario)
@app.middleware('http')
async def http_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Modelo Pydantic
class Crear_empleado(BaseModel):
    id: str = str(uuid.uuid4())
    usuario: str
    contraseña: str
    nombre: str
    apellidos: str
    correo: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'usuario': 'EjemploU',
                'contraseña':'EjemploC',
                'nombre': 'Ejemplo',
                'apellidos':'EjemploAp',
                'correo' : 'ejemplo@gmail.com'
            }
        }
    }

    @staticmethod
    def eliminar_puntuacion(texto: str) -> str:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()

    @validator('nombre')
    def validar_nombre(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value
    
    @validator('apellidos')
    def validar_apellidos(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value
class CrearPartido(BaseModel):
    id: str = str(uuid.uuid4())
    campo: str
    deportivo: str
    liga: str
    torneo: str
    categoria: str
    eq: str
    ev: str
    fecha: str
    arbitro: str
    hora: str
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'campo': 'CampoEjemplo',
                'deportivo': 'DeportivoEjemplo',
                'liga': 'LigaDeMiCasa',
                'torneo': 'TorneoEjemplo',
                'categoria': 'CategoriaEjemplo',
                'eq': 'EquipoLocal',
                'ev': 'EquipoVisitante',
                'fecha': '2024-12-05', 
                'arbitro': 'ArbitroEjemplo',
                'hora': '17:00'
                }
            }
    }

    @staticmethod
    def eliminar_puntuacion(texto: str) -> str:
        sin_signos = re.sub(r'[^\w\s]', '', texto)
        return sin_signos.strip().lower()

    @validator('campo', 'deportivo', 'liga', 'torneo', 'categoria', 'eq', 'ev', 'arbitro')
    def validar_nombre(cls, value):
        value = cls.eliminar_puntuacion(value)
        if not isinstance(value, str):
            raise ValueError("El campo debe ser un string")
        elif len(value) < 5 or len(value) > 25:
            raise ValueError("Los datos deben tener entre 5 y 25 caracteres")
        return value

    @validator('fecha')
    def validar_fecha(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD")
        return value

    @validator('hora')
    def validar_hora(cls, value):
        if not re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', value):
            raise ValueError("La hora debe tener el formato HH:MM (24 horas)")
        return value

empleados_list = []

# Definición del router
empleados_route = APIRouter()

@empleados_route.post('/agregar_empleado', tags=["Empleados"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo empleado")
def create_empleado(empleado: Crear_empleado) -> Crear_empleado:
    empleados_list.append(empleado)
    content = [empleado.dict()]
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)

@empleados_route.options('/agregar_empleado', tags=["Empleados"])
def options_empleado():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@empleados_route.get('obtener_empleados', tags=["Empleados"], status_code=status.HTTP_200_OK, response_description="Obtener empleados registrados")
def obtener_empleado():
    content = [empleado.dict() for empleado in empleados_list]
    return JSONResponse(content = content)

# Incluir el router en la aplicación principal
app.include_router(empleados_route, prefix="/empleados")

partidos_list = []

partidos_route = APIRouter()

@partidos_route.post('/agregar_partido', tags=["Partidos"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo partido")
async def create_partido(partido: CrearPartido) -> CrearPartido:
    try:
        partidos_list.append(partido)
        content = [partido.dict()]
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
@partidos_route.options('/agregar_partido', tags=["Partidos"])
async def options_partido():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)


@partidos_route.get('/obtener_partido', tags=["Partidos"], status_code=status.HTTP_200_OK, response_description="Obtener partidos")
async def obtener_partido():
    try:
        content = [partido.dict() for partido in partidos_list]
        return JSONResponse(content = content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@partidos_route.put('/editar_partido/{id}', tags=["Partidos"], status_code=status.HTTP_201_CREATED, response_description="Modificar un partido ya existente por ID")
async def editar_partido(partido_id:uuid.UUID, editar_partido: CrearPartido) -> CrearPartido:
    try:
        for index, partido in enumerate(partidos_list):
            if partido.id == str(partido_id):
                partidos_list[index] = editar_partido
                return editar_partido
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

@partidos_route.delete('/eliminar_partido/{id}', tags = ["Partidos"], status_code=status.HTTP_200_OK, response_description="Eliminar un partido existente")
async def eliminar_partido(id_partido: uuid.UUID) :
    try:
        id = str(id_partido)
        for partido in partidos_list:
            if partido.id == id:
                partidos_list.remove(partido)
        content = [partido.dict() for partido in partidos_list]
        
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

app.include_router(partidos_route, prefix="/partidos")

# Otros endpoints de ejemplo
@app.get('/', tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=status.HTTP_200_OK)

def common_parameters(startday: str, endday: str):
    return {"startday": startday, "endday": endday}

@app.get('/users', tags=["Users"])
def get_users(commons: dict = Depends(common_parameters)):
    return f"El usuario se registró el día {commons['startday']} y salió el día {commons['endday']}"

@app.get('/customers', tags=["Users"])
def get_customers(commons: dict = Depends(common_parameters)):
    return f"El cliente se registró el día {commons['startday']} y salió el día {commons['endday']}"

@app.get('/get_file')
def get_file():
    return FileResponse('lorem-ipsum.pdf')


# Ruta de películas (ejemplo)
# app.include_router(prefix='/movies', router=movie_router) # Descomentar si tienes el router de películas
