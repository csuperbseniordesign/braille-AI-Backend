from app.utils.api_utility import verify_api_key, get_api_key
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secure-data")
def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access to secure data"}