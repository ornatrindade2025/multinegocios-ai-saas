from fastapi import FastAPI, Request
from app.middleware.tenant import TenantMiddleware

app = FastAPI(title="MultiNegócios AI")

app.add_middleware(TenantMiddleware)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/whoami")
async def whoami(request: Request):
    return {
        "tenant_id": request.state.tenant_id
    }


