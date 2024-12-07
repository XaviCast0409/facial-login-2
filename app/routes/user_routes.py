from fastapi import APIRouter, UploadFile, Form, HTTPException
from app.controllers.user_controller import register_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    dni_photo: UploadFile = None,
    webcam_photo: UploadFile = None,
):
    return await register_user(name, email, dni_photo, webcam_photo)
