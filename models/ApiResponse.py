from typing import Any, Optional
from fastapi.responses import JSONResponse


class ApiResponse:
    """Static/utility class to handle common API responses."""

    @staticmethod
    def success(message: str, data: Optional[Any] = None) -> JSONResponse:
        """
        Returns a success response with HTTP 200.
        """
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": message,
                "data": data,
            },
        )

    @staticmethod
    def error(message: str, status_code: int = 400) -> JSONResponse:
        """
        Returns an error response with HTTP status code (default is 400).
        """
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
            },
        )

    @staticmethod
    def not_found(message: str = "Resource not found") -> JSONResponse:
        """
        Returns a 404 not found response.
        """
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": message,
            },
        )
