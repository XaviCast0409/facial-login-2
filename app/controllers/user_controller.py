import os
from fastapi import HTTPException
from app.services.facial_service import compare_faces
from app.database.db import users_collection
from app.models.user_model import User
import shutil

async def register_user(name, email, dni_photo, webcam_photo):
    # Ruta del directorio donde se guardarán las imágenes
    upload_dir = "uploads"
    
    # Crear el directorio si no existe
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Guardar las fotos localmente
    dni_path = os.path.join(upload_dir, dni_photo.filename)
    webcam_path = os.path.join(upload_dir, webcam_photo.filename)

    # Imprimir los nombres de los archivos de las fotos
    print(f"Guardando DNI en: {dni_path}")
    print(f"Guardando foto de webcam en: {webcam_path}")

    with open(dni_path, "wb") as f:
        shutil.copyfileobj(dni_photo.file, f)
    with open(webcam_path, "wb") as f:
        shutil.copyfileobj(webcam_photo.file, f)

    # Comparar las fotos
    if not compare_faces(dni_path, webcam_path):
        print("Las fotos no coinciden")
        shutil.rmtree(upload_dir)
        raise HTTPException(status_code=400, detail="Las fotos no coinciden")
    # # Crear usuario en la base de datos
    # user = User(name=name, email=email, dni_photo_path=dni_path, webcam_photo_path=webcam_path)

    # # Imprimir la información del usuario antes de guardarla en la base de datos
    # print(f"Registrando usuario: {user}")

    # result = await users_collection.insert_one(user.dict(by_alias=True))

    # # Imprimir el ID del nuevo usuario registrado
    # print(f"Usuario registrado exitosamente con ID: {result.inserted_id}")

    # return {"message": "Usuario registrado exitosamente", "user_id": str(result.inserted_id)}
    shutil.rmtree(upload_dir)
    return {"message": "Fotos validadas correctamente."}
