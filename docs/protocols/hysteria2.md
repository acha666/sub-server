# Hysteria 2

Implemented fields:

- `auth.password`
- `tls.sni`, `tls.insecure`
- arbitrary `options` become query parameters, such as `pinSHA256`, `obfs` and
  `obfs-password`

## Link format

Links follow the
[Hysteria 2 URI scheme](https://v2.hysteria.network/docs/developers/URI-Scheme/):
`hysteria2://<auth>@<host>:<port>/?<query>#<name>`. The password is percent-encoded as URL
userinfo and IPv6 endpoints use bracketed authorities.
