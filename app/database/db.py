from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://diegote:Pacita10%40@cluster0.v2kiayc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = os.getenv("DATABASE_NAME", "facial_login_db")

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]
users_collection = database["users"]
