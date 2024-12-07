from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: EmailStr
    dni_photo_path: str  # Ruta de la foto del DNI
    webcam_photo_path: str  # Ruta de la foto de la webcam
