# VMess

The renderer emits the widely supported `vmess://<base64-json>` format used by
[v2rayN](https://github.com/2dust/v2rayN/tree/master/v2rayN/ServiceLib/Handler/Fmt).
VMess with Reality is unsupported because this JSON envelope has no Reality fields.

Implemented fields:

- `auth.uuid`
- `options.scy`
- numeric `endpoint.port` and `auth.alterId`
- `tls.mode`, `tls.sni`, `tls.alpn`, `tls.fp`, `tls.insecure`
- WebSocket / HTTPUpgrade host and path
- gRPC mode, authority, and service name
