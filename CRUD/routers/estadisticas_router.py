from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.estadisticas_model import Crear_estadistica

estadisticas_list = []
estadisticas_route = APIRouter()

@estadisticas_route.post('/agregar_estadistica', tags=["Estadisticas"], status_code=status.HTTP_201_CREATED, response_description="Crea una nueva estadistica")
async def create_estadistica(estadistica: Crear_estadistica) -> Crear_estadistica:
    try:
        estadisticas_list.append(estadistica)
        content = estadistica.model_dump()
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede registrar la estadistica")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@estadisticas_route.options('/agregar_estadistica', tags=["Estadisticas"])
async def options_estadistica():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@estadisticas_route.get('/obtener_estadisticas', tags=["Estadisticas"], status_code=status.HTTP_200_OK, response_description="Obtener estadisticas registradas")
async def obtener_estadisticas():
    try:
        content = [estadistica.model_dump() for estadistica in estadisticas_list]
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
