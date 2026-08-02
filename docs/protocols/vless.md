# VLESS

Implemented fields:

- `auth.uuid`
- `tls.mode`, `tls.sni`, `tls.alpn`, `tls.fp`, `tls.insecure`
- `tls.reality.public_key`, `tls.reality.short_id`, `tls.reality.spider_x`
- `transport.type`, `transport.host`, `transport.path`, `transport.serviceName`, `transport.authority`
- `options.encryption`
- `options.flow`
- `routing.vless_route`

## Link format

Links follow the [Xray VMessAEAD/VLESS sharing proposal](https://github.com/XTLS/Xray-core/discussions/716).
Query values are percent-encoded and IPv6 authorities are bracketed.
