# settings.yaml

`settings.yaml` is optional and lives beside `servers.yaml` and `keys.yaml`.

```yaml
title: sub-server
cache_control: no-store
host: 0.0.0.0
port: 8000
trust_proxy_headers: true
trusted_proxy_ips:
  - 127.0.0.1
  - ::1
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16
  - 169.254.0.0/16
  - fc00::/7
  - fe80::/10
```

## Reverse proxies

Proxy headers are accepted only when the direct peer belongs to `trusted_proxy_ips`. The
defaults cover loopback, RFC1918 LAN and common Docker networks, plus IPv4/IPv6 link-local
networks. For an Internet-facing deployment, narrow the list to the reverse proxy's exact
address or network. Never use `*` unless every direct client is trusted.

## Environment overrides

- `SUB_SERVER_CONFIG_DIR`: directory containing the YAML files
- `SUB_SERVER_HOST`: bind address
- `SUB_SERVER_PORT`: bind port
- `SUB_SERVER_TRUST_PROXY_HEADERS`: boolean proxy-header switch
- `SUB_SERVER_TRUSTED_PROXY_IPS`: comma-separated trusted IP addresses or CIDR networks

Start the service with `sub-server` to apply the bind and proxy settings. Direct Uvicorn
invocation only uses options supplied on its command line.
