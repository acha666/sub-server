# Trojan

Implemented fields:

- `auth.password`
- `tls.mode`, `tls.sni`, `tls.alpn`, `tls.fp`, `tls.insecure`
- `tls.reality.public_key`, `tls.reality.short_id`, `tls.reality.spider_x`
- `transport.type`, `transport.host`, `transport.path`
- `transport.serviceName`, `transport.authority`, `transport.mode`, `transport.headerType`
- arbitrary `options` become query parameters

## Link format

Passwords are percent-encoded as URL userinfo and IPv6 endpoints use bracketed authorities.
