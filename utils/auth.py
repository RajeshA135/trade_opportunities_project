# utils/auth.py
import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("X-API-KEY")

def verify_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
