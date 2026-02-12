from fastapi import FastAPI

app = FastAPI(title="MultiNegócios AI")

@app.get("/health")
async def health():
    return {"status": "ok"}
