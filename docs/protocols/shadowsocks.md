# Shadowsocks

Implemented fields:

- `auth.method`
- `auth.password`
- `options.plugin`

## Link format

Links follow [SIP002](https://github.com/shadowsocks/shadowsocks-org/blob/master/docs/doc/sip002.md).
They use URL-safe base64 userinfo, percent-encoded plugin parameters, and bracketed IPv6
authorities. AEAD-2022 methods use the plain userinfo form.
