from app.utils.auth import verify_api_key, fetch_model_api_key
from app.utils.sys_check import run_system_check
from fastapi import FastAPI, Depends, Request, Response
from fastapi.security.api_key import APIKeyHeader
import httpx
import json

run_system_check()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secure-data")
def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access to secure data"}

@app.get("/generate")
async def generate_text(request: Request):
    # extract raw json data
    data = await request.json()
    

    # check if prompt exist
    prompt = data.get("prompt")

    # if prompt doesn't exist
    # return error notify no prompt is given
    if not prompt:
        return {"error" : "Prompt is required"}
    
    json_data = json.dumps(data)
    model_key = fetch_model_api_key()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(model_key, data=json_data)

            if response.status_code != 200:
                return {"response" : response.status_code}
            
        except:
            return {"error" : "unable to connect to local model"}

        # convert response.text to json from string
        response_json = json.loads(response.text)

        return response_json