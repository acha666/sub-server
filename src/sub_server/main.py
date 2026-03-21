from __future__ import annotations

import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sub_server.api.health import router as health_router
from sub_server.api.public import router as public_router
from sub_server.config.cache import ConfigStore
from sub_server.config.resolver import ConfigResolver
from sub_server.core.exceptions import (
    ConfigError,
    SubscriptionKeyNotFoundError,
    UnsupportedProtocolError,
)
from sub_server.core.logging import configure_logging
from sub_server.core.settings import get_settings
from sub_server.services.subscription import SubscriptionService

configure_logging()
logger = logging.getLogger("sub-backend")
settings = get_settings()
config_store = ConfigStore(settings.config_dir)
subscription_service = SubscriptionService()


app = FastAPI(title=settings.title)


@app.on_event("startup")
def on_startup() -> None:
    config_store.get()


@app.middleware("http")
async def access_log(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    forwarded = request.headers.get("x-forwarded-for")
    client_ip = forwarded or (request.client.host if request.client else "-")
    logger.info(
        'client="%s" method=%s path="%s" status=%s ms=%s',
        client_ip,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.exception_handler(SubscriptionKeyNotFoundError)
def handle_key_not_found(_: Request, exc: SubscriptionKeyNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": f"subscription key not found: {exc}"})


@app.exception_handler(ConfigError)
def handle_config_error(_: Request, exc: ConfigError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(UnsupportedProtocolError)
def handle_unsupported_protocol(_: Request, exc: UnsupportedProtocolError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": f"unsupported protocol: {exc}"})


@app.exception_handler(NotImplementedError)
def handle_not_implemented(_: Request, exc: NotImplementedError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def build_resolver() -> ConfigResolver:
    loaded = config_store.get()
    return ConfigResolver(loaded.servers.servers, loaded.keys.keys)


app.state.settings = settings
app.state.config_store = config_store
app.state.subscription_service = subscription_service
app.state.config_resolver = build_resolver

app.include_router(health_router)
app.include_router(public_router)


def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()

