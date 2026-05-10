from __future__ import annotations

import logging
from dataclasses import dataclass

from litestar import Request, Response
from litestar.exceptions import HTTPException

logger = logging.getLogger(__name__)


@dataclass
class ApiError:
    """Einheitliche Fehlerantwort der API."""

    code: str
    message: str


# Mapping HTTP-Status -> (Code, deutsche Default-Nachricht)
_STATUS_DEFAULTS: dict[int, tuple[str, str]] = {
    400: ("VALIDATION_ERROR", "Die übermittelten Daten sind ungültig."),
    404: ("NOT_FOUND", "Die angeforderte Ressource wurde nicht gefunden."),
    405: ("METHOD_NOT_ALLOWED", "Diese HTTP-Methode ist auf der Ressource nicht erlaubt."),
    409: (
        "VERSION_CONFLICT",
        "Der Datensatz wurde zwischenzeitlich geändert. Bitte neu laden und erneut versuchen.",
    ),
    422: ("VALIDATION_ERROR", "Die übermittelten Daten sind ungültig."),
    500: ("INTERNAL_ERROR", "Ein unerwarteter Serverfehler ist aufgetreten."),
}


def _resolve(status_code: int, detail: str | None) -> ApiError:
    code, default_message = _STATUS_DEFAULTS.get(
        status_code, (f"HTTP_{status_code}", "Es ist ein Fehler aufgetreten.")
    )

    if status_code in (404, 409) and detail:
        message = detail
    else:
        message = default_message

    return ApiError(code=code, message=message)


def http_exception_handler(_: Request, exc: HTTPException) -> Response[ApiError]:
    detail = exc.detail if isinstance(exc.detail, str) else None
    error = _resolve(exc.status_code, detail)
    if exc.status_code >= 500:
        logger.exception("Server-Fehler bei der Anfrage", exc_info=exc)
    return Response(content=error, status_code=exc.status_code)


def generic_exception_handler(_: Request, exc: Exception) -> Response[ApiError]:
    """Fallback-Handler für alles, was nicht als HTTPException geworfen wurde."""
    logger.exception("Unbehandelte Exception", exc_info=exc)
    return Response(
        content=ApiError(
            code="INTERNAL_ERROR",
            message="Ein unerwarteter Serverfehler ist aufgetreten.",
        ),
        status_code=500,
    )


EXCEPTION_HANDLERS = {
    HTTPException: http_exception_handler,
    Exception: generic_exception_handler,
}

