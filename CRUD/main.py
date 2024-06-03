from fastapi import FastAPI,status, Depends, Request
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.partidos_router import *
from routers.usuarios_router import *
from utils.error_handler import *

app = FastAPI()

origins = [
    "http://localhost:3000", 
    "https://tu-dominio-frontend.com"
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
app.include_router(prefix='/usuarios', router=usuarios_route)
app.include_router(prefix='/partidos', router=partidos_route)