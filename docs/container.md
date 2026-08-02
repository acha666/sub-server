# Container deployment

Mount a config directory into `/config` and expose the container behind Traefik or another
reverse proxy. The repository root contains an example Compose file.

## Health check

The image checks `/healthz`. This endpoint returns an unhealthy response when the current
configuration cannot be loaded.

## Reverse proxy

The container uses the bind and proxy settings from `settings.yaml`. Its default trusted
proxy list covers loopback, RFC1918 LAN and common Docker networks. Public deployments
should narrow `trusted_proxy_ips` to the actual proxy network.

Uvicorn's raw access log is disabled because subscription keys are part of request paths.
