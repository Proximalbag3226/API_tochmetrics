import os
import uuid
from fastapi import APIRouter, FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from models.ligas_model import *

IMAGEDIR = "images/"
DOCDIR = "documents/"  

if not os.path.exists(IMAGEDIR):
    os.makedirs(IMAGEDIR)
if not os.path.exists(DOCDIR):
    os.makedirs(DOCDIR)

ligas_list = []

app = FastAPI()
ligas_route = APIRouter()
images_route = APIRouter()
documents_route = APIRouter()  

@ligas_route.post('/agregar_liga', tags=["ligas"], status_code=status.HTTP_201_CREATED, response_description="Crea una nueva liga")
async def create_liga(
    nombre_liga: str = Form(...),
    fecha_creacion: str = Form(...),
    descripcion: str = Form(...),
    imagen: UploadFile = File(None),
    documento: UploadFile = File(None)  
):
    try:
        id = str(uuid.uuid4()) 
        filename_imagen = None
        filename_documento = None

        if imagen:
            filename_imagen = f"{uuid.uuid4()}.jpg"
            filepath_imagen = os.path.join(IMAGEDIR, filename_imagen)
            with open(filepath_imagen, "wb") as f:
                contents = await imagen.read()
                f.write(contents)

        if documento:
            filename_documento = f"{uuid.uuid4()}.{documento.filename.split('.')[-1]}"  
            filepath_documento = os.path.join(DOCDIR, filename_documento)
            with open(filepath_documento, "wb") as f:
                contents = await documento.read()
                f.write(contents)

        nueva_liga = Liga(
            id=id,
            nombre_liga=nombre_liga,
            fecha_creacion=fecha_creacion,
            descripcion=descripcion,
            imagen=filename_imagen,
            documento=filename_documento  
        )
        ligas_list.append(nueva_liga)
        return JSONResponse(content=nueva_liga.dict(), status_code=status.HTTP_201_CREATED)
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
async def borrar_liga(id_liga: str):
    try:
        for liga in ligas_list:
            if liga.id == id_liga:
                ligas_list.remove(liga)
                if liga.imagen:
                    os.remove(os.path.join(IMAGEDIR, liga.imagen))
                if liga.documento:  
                    os.remove(os.path.join(DOCDIR, liga.documento))
                content = [liga.dict() for liga in ligas_list]
                return JSONResponse(content=content, status_code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@images_route.get("/imagenes/{imagen_name}", tags=["imagenes"])
async def read_image_file(imagen_name: str):
    try:
        path = os.path.join(IMAGEDIR, imagen_name)
        if not os.path.exists(path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imagen no encontrada")
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_route.get("/documentos/{documento_name}", tags=["documentos"])
async def read_document_file(documento_name: str):
    try:
        path = os.path.join(DOCDIR, documento_name)
        if not os.path.exists(path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

app.include_router(ligas_route, prefix="/ligas")
app.include_router(images_route)
app.include_router(documents_route)  
