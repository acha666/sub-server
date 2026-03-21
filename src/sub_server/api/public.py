from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from sub_server.core.settings import get_settings

router = APIRouter()


@router.get("/")
def root() -> JSONResponse:
    settings = get_settings()
    return JSONResponse(
        {
            "service": settings.title,
            "config_dir": str(settings.config_dir),
            "usage": "GET /{key} or /{key}?raw=1",
        }
    )


@router.get("/{key}")
def get_subscription(request: Request, key: str, raw: int = 0) -> PlainTextResponse:
    resolved = request.app.state.config_resolver().resolve_key(key)
    body = request.app.state.subscription_service.render_subscription(resolved, force_raw=bool(raw))
    return PlainTextResponse(
        body,
        headers={
            "Cache-Control": request.app.state.settings.cache_control,
            "X-Subscription-Servers": str(len(resolved.servers)),
        },
    )

