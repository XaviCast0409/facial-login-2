from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes

# Crear instancia de FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar orígenes permitidos, por ejemplo, ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

# Registrar las rutas
app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "API de reconocimiento facial activa"}
