from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://192.168.100.198:27017"

client = AsyncIOMotorClient(MONGO_URL)
db = client["sphx_db"]

def get_collection():
    return db["sensors"]