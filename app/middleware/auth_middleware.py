from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, HTTPException, status
from app.core.logger import logger
from app.api import CREATE_USER_ENDPOINT, API_PREFIX
from app.middleware import middleware_helper
from app.core.config import HEADER_SECRET_KEY, HEADER_SECRET_VALUE

EXCLUDE_VERIFICATION_ENDPOINTS = {
    "GET": [
        "/docs",
        "/redoc",
        "/openapi.json"
    ],
    "POST": [
        f"{API_PREFIX}{CREATE_USER_ENDPOINT}"
    ],
}

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check authentication for endpoint access
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        logger.info(
            "Request received for endpoint."
            " %s : %s" % (request.method, request.url)
        )

        try:
            if middleware_helper.request_to_exclude(request, EXCLUDE_VERIFICATION_ENDPOINTS):
                response = await call_next(request)
            else:
                if request.headers.get(HEADER_SECRET_KEY, None) == HEADER_SECRET_VALUE:
                    response = await call_next(request)
                else:
                    logger.exception("Missing or invalid Secret-Token in the header")
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Secret-Token in the header")
            return response
        except HTTPException as exc:
            logger.exception(exc)
            return JSONResponse(
                status_code=exc.status_code, content=exc.detail
            )
        except Exception as exc:
            logger.exception(exc)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Something went wrong"
            )
        finally:
            logger.info(
                "Request completed for endpoint."
                " %s : %s" % (request.method, request.url)
            )
