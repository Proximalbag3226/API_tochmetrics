import uuid
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.ligas_model import Crear_liga

ligas_list = []
ligas_route = APIRouter()

@ligas_route.post('/agregar_liga', tags=["ligas"], status_code=status.HTTP_201_CREATED, response_description="Crea una nueva liga")
async def create_liga(liga: Crear_liga) -> Crear_liga:
    try:
        ligas_list.append(liga)
        content = liga.dict()
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede registrar la liga")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@ligas_route.options('/agregar_liga', tags=["ligas"])
async def options_liga():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@ligas_route.get('/obtener_ligas', tags=["ligas"], status_code=status.HTTP_200_OK, response_description="Obtener ligas registradas")
async def obtener_ligas():
    try:
        content = [liga.dict() for liga in ligas_list]
        return JSONResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@ligas_route.delete('/borrar_liga/{id_liga}', tags=["ligas"], status_code=status.HTTP_200_OK, response_description="Borrar una liga registrada")
async def borrar_liga(id_liga: uuid.UUID):
    try:
        id = str(id_liga)
        for liga in ligas_list:
            if str(liga.id) == id:
                ligas_list.remove(liga)
                content = [liga.dict() for liga in ligas_list]
                return JSONResponse(content=content, status_code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
