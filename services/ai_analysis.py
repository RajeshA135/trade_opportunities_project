import os
import httpx
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def analyze_with_gemini(sector: str, context: str) -> str:
    prompt = f"""Act as a market analyst. Based on the following real-time news, generate a professional markdown report for the Indian {sector} sector. Include:

    - A concise summary
    - Key trends
    - 3 trade opportunities

    News:
    {context}
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
            headers=headers,
            params={"key": GEMINI_API_KEY},
            json=payload
        )

        result = response.json()

        if "candidates" not in result:
            return {
                "message": f"Gemini Error: {result.get('error', {}).get('message', 'Unknown error')}",
            }

        markdown_report = result["candidates"][0]["content"]["parts"][0]["text"]

        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)

        file_path = os.path.join(reports_dir, f"{sector}_report.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_report)

        return markdown_report
