from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid

IMAGEDIR = "images/"

# Verificar si el directorio de imágenes existe, si no, créalo
if not os.path.exists(IMAGEDIR):
    os.makedirs(IMAGEDIR)


images_router= APIRouter()
 
 
@images_router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    # Generar un nombre de archivo único para evitar colisiones
    filename = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(IMAGEDIR, filename)

    # Guardar el archivo en el directorio de imágenes
    with open(filepath, "wb") as f:
        contents = await file.read()
        f.write(contents)
 
    return {"filename": filename}
 
 
@images_router.get("/show/")
async def read_random_file():
    # Obtener una lista de archivos en el directorio de imágenes
    files = os.listdir(IMAGEDIR)
    
    if not files:
        return {"message": "No hay imágenes disponibles"}

    # Seleccionar un archivo aleatorio del directorio
    random_index = randint(0, len(files) - 1)
    random_file = files[random_index]

    # Devolver la imagen seleccionada como respuesta
    path = os.path.join(IMAGEDIR, random_file)
    return FileResponse(path)
