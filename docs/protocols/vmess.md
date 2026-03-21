# VMess

This first version emits the common `vmess://<base64-json>` format.

Implemented fields:

- `auth.uuid`
- `auth.alterId`
- `options.scy`
- `tls.mode`, `tls.sni`, `tls.alpn`, `tls.fp`
- `transport.type`, `transport.host`, `transport.path`, `transport.headerType`
