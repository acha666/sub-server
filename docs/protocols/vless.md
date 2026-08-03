# VLESS

Implemented fields:

- `auth.uuid`
- `tls.mode`, `tls.sni`, `tls.alpn`, `tls.fp`, `tls.insecure`
- `tls.reality.public_key`, `tls.reality.short_id`, `tls.reality.spider_x`
- `transport.type`, `transport.host`, `transport.path`, `transport.serviceName`,
  `transport.authority`
- `options.encryption`
- `options.flow`
- `routing.vless_route`

## VLESS route

`routing.vless_route` sets bytes 7 and 8 of the UUID used in the generated link. This is
the client-side counterpart of Xray routing rule `vlessRoute`.

```yaml
routing:
  vless_route: 14
```

The value may be an integer from `0` to `65535`, a decimal string, a `0x`-prefixed
hexadecimal string, or a four-digit hexadecimal string such as `"000e"`. It is encoded as
big-endian `uint16`; the configured `auth.uuid` remains unchanged in memory.

See Project X's
[routing documentation](https://xtls.github.io/en/config/routing.html#ruleobject) for the
server-side rule and byte layout.

## Link format

Links follow the
[Xray VMessAEAD/VLESS sharing proposal](https://github.com/XTLS/Xray-core/discussions/716).
Query values are percent-encoded and IPv6 authorities are bracketed.
