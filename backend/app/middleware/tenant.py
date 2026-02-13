from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.security import decode_token


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/health"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
            )

        token = auth_header.split(" ")[1]

        try:
            payload = decode_token(token)
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"},
            )

        tenant_id = payload.get("sub")

        if not tenant_id:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token payload"},
            )

        request.state.tenant_id = tenant_id

        response = await call_next(request)
        return response
