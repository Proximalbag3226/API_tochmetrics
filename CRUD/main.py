from fastapi import FastAPI, APIRouter, status, Depends, Request, Response
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uuid
import re

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
