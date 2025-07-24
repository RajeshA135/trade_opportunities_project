# utils/session.py

from fastapi import Request
import time
from typing import Dict

# In-memory storage
session_data: Dict[str, list] = {}

# Rate limit: 5 requests per 60 seconds
RATE_LIMIT = 5
WINDOW = 60  # seconds

def get_client_ip(request: Request) -> str:
    return request.client.host or "unknown"

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    timestamps = session_data.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW]
    session_data[ip] = timestamps
    return len(timestamps) >= RATE_LIMIT

def track_request(ip: str):
    now = time.time()
    session_data.setdefault(ip, []).append(now)
