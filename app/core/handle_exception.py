from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from functools import wraps
from app.core.logger import logger


def exception_handler(func):
    """
    Decorator to handle general exceptions

    :param func: Callable function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Exception handler wrapper
        """
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            logger.exception(exc)
            raise
        except HTTPException as exc:
            logger.exception(exc)
            return JSONResponse(
                status_code=exc.status_code, content=exc.detail
            )
        except Exception as exc:
            logger.exception(exc)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Something went wrong",
            )

    return wrapper
