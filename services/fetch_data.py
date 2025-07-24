import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def get_market_news(sector: str) -> str:
    try:
        url = "https://newsapi.org/v2/everything"
        query = f"{sector} sector India"

        params = {
            "q": query,
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 5
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if "articles" not in data or not data["articles"]:
                return {
                    "message" : f"No current news found for {sector} sector.",
                    "error": e,
                }

            headlines = [f"- {article['title']} - {article.get('description', '')}" for article in data["articles"]]
            return "\n".join(headlines)

    except Exception as e:
        return {
            "message" : "Error fetching news for {sector} sector.",
            "error": e,
        }
