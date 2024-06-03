from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import uuid
from models.users_model import *

usuarios_list = []
usuarios_route = APIRouter()

@usuarios_route.post('/agregar_usuario', tags=["Usuarios"], status_code=status.HTTP_201_CREATED, response_description="Crea un nuevo usuario")
async def create_usuario(usuario: Crear_usuario) -> Crear_usuario:
    try:
        usuarios_list.append(usuario)
        content = [usuario.model_dump()]
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except ValueError:
        HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail="No se puede registar el usuario")
    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
@usuarios_route.options('/agregar_usuario', tags=["Usuarios"])
async def options_usuario():
    return JSONResponse(content={"allow": "POST, OPTIONS"}, status_code=status.HTTP_200_OK)

@usuarios_route.get('/obtener_usuarios', tags=["Usuarios"], status_code=status.HTTP_200_OK, response_description="Obtener usuarios registrados")
async def obtener_usuario():
    try:
        content = [usuario.model_dump() for usuario in usuarios_list]
        return JSONResponse(content = content)
    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER, detail=str(e))

@usuarios_route.put('/modificar_usuarios', tags=["Usuarios"], status_code=status.HTTP_200_OK, response_description="Modificar un usuario registrado")
async def modificar_usuario(id_usuario: uuid.UUID, editar_usuario: EditarUsuario)->EditarUsuario:
    try:
        id = str(id_usuario)
        for usuario in usuarios_list:
            if usuario.id == id:
                usuario.usuario = editar_usuario.usuario
                usuario.contraseña = editar_usuario.contraseña
                usuario.nombre = editar_usuario.nombre
                usuario.apellidos = editar_usuario.apellidos
                usuario.correro = editar_usuario.correo
                usuario.tipo = editar_usuario.tipo
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Usuario no encontrado")
        content = [usuario.model_dump() for usuario in usuarios_list]
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede editar el usuario")
    except Exception as e:
        raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
@usuarios_route.delete('/borrar_usuario', tags=["Usuarios"], status_code=status.HTTP_200_OK, response_description="Borrar un usuario registrado")
def borrar_usuario(id_usuario: uuid.UUID):
    try:
        id = str(id_usuario)
        for usuario in usuarios_list:
            if usuario.id == id:
                usuarios_list.remove(usuario)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        content = [usuario.model_dump() for usuario in usuarios_list]
        
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al intentar borrar el usuario")