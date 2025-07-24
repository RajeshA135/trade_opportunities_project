# utils/rate_limit.py
from fastapi import Request, HTTPException
from cachetools import TTLCache
from time import time

# Allow 5 requests per IP per 60 seconds
rate_cache = TTLCache(maxsize=1000, ttl=60)

def rate_limiter(request: Request):
    ip = request.client.host
    current = rate_cache.get(ip, 0)

    if current >= 5:
        raise HTTPException(status_code=429, detail="Too many requests, please wait.")
    
    rate_cache[ip] = current + 1
