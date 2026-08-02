from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        build_resolver()
    except ConfigError as exc:
        logger.error("startup config error: %s", exc)
        raise
    except Exception as exc:
        logger.error("unexpected startup error: %s", exc)
        raise
    yield


app = FastAPI(title=settings.title, lifespan=lifespan)


@app.middleware("http")
async def access_log(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - start) * 1000)
    route = request.scope.get("route")
    path = getattr(route, "path", "<unmatched>")
    client_ip = request.client.host if request.client else "-"
    logger.info(
        'client="%s" method=%s path="%s" status=%s ms=%s',
        client_ip,
        request.method,
        path,
        response.status_code,
        duration_ms,
    )
    return response


@app.exception_handler(SubscriptionKeyNotFoundError)
def handle_key_not_found(_: Request, __: SubscriptionKeyNotFoundError) -> JSONResponse:
    logger.info("subscription key not found")
    return JSONResponse(status_code=404, content={"detail": "subscription key not found"})


@app.exception_handler(ConfigError)
def handle_config_error(_: Request, exc: ConfigError) -> JSONResponse:
    logger.error("config error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "invalid server configuration"})


@app.exception_handler(UnsupportedProtocolError)
def handle_unsupported_protocol(_: Request, exc: UnsupportedProtocolError) -> JSONResponse:
    logger.info("unsupported protocol: %s", exc)
    return JSONResponse(status_code=400, content={"detail": f"unsupported protocol: {exc}"})


@app.exception_handler(NotImplementedError)
def handle_not_implemented(_: Request, exc: NotImplementedError) -> JSONResponse:
    logger.info("not implemented: %s", exc)
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
def handle_unhandled_exception(_: Request, exc: Exception) -> JSONResponse:
    # Catch-all for unexpected errors during request handling.
    # Log a short message so we don't produce huge tracebacks in production logs.
    logger.error("internal error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "internal server error"})


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
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        proxy_headers=settings.trust_proxy_headers,
        forwarded_allow_ips=settings.forwarded_allow_ips,
        access_log=False,
    )


if __name__ == "__main__":
    run()
