# Trade Opportunities API
This FastAPI-based project provides real-time market news and AI-generated markdown reports for key sectors:

For example : Technology, Pharmaceuticals, Agriculture 

It fetches live data from external APIs, analyzes the content using Gemini AI, and supports:

- Session tracking by client IP

- Per-session/user rate limiting

- Lightweight token-based authentication

- Report saved in `.md` file for each sector

## API Endpoints

```bash
GET /analyze/{sector}
```
Analyzes the market news for the specified sector and generate and return an AI-analyzed markdown report for a that sector.

### Headers:
- `Content-Type`: application/json
- `X-API-Key`: samplekey
### Response:

```bash
{
    "message": "{sector} Report generated successfully."
}
```

### Curl command: 
```bash
curl -X GET http://127.0.0.1:8000/analyze/{sector} \
  -H "x-api-key: samplekey" \
  -H "Content-Type: application/json"
```
### Run the FastAPI App:
```bash
    uvicorn main:app --reload
```