# routers/analyze.py
from fastapi import APIRouter, HTTPException, Request , Depends
from services.fetch_data import get_market_news
from services.ai_analysis import analyze_with_gemini
from utils.auth import verify_token
from utils.sessions import get_client_ip, is_rate_limited, track_request

router = APIRouter()

@router.get("/analyze/{sector}", dependencies=[Depends(verify_token)])
async def analyze_sector(sector: str, request: Request):
    allowed_sectors = ["pharmaceuticals", "technology", "agriculture"]
    if sector.lower() not in allowed_sectors:
        raise HTTPException(status_code=400, detail="Sector not supported.")
    
    client_ip = get_client_ip(request)

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in a minute.")

    track_request(client_ip)

    # Step 1: Fetch market headlines
    news_content = await get_market_news(sector)
    if not news_content:
        raise HTTPException(status_code=500, detail="Unable to fetch market data.")

    # Step 2: Generate markdown report using Gemini
    markdown_report = await analyze_with_gemini(sector, news_content)
    if not markdown_report or markdown_report.startswith("Gemini Error"):
        raise HTTPException(status_code=500, detail="AI failed to generate report.")
    
    return {
        "message": f"{sector} report generated successfully.",
        "Client IP Addess": client_ip
    }
