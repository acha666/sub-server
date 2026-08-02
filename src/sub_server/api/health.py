from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from sub_server.core.exceptions import ConfigError

router = APIRouter()


@router.get("/healthz")
def healthz(request: Request) -> JSONResponse:
    try:
        request.app.state.config_resolver()
    except ConfigError:
        return JSONResponse(status_code=503, content={"ok": False})
    return JSONResponse(content={"ok": True})
