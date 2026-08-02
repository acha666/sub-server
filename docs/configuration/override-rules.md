# Override rules

Overrides are applied as deep merge patches.

Optional sections such as `routing`, `tls`, and `transport` may be replaced with `null`.

Example:

```yaml
overrides:
  hk-vless-01:
    patch:
      transport:
        path: /user-a
      routing:
        vless_route: 14
```

## Special helper

- `routing.vless_route` rewrites the third UUID segment as a big-endian uint16 value.
- If `patch.auth.uuid` is present, the route is injected into that UUID.
- Otherwise, the route is injected into the effective UUID inherited from the base server.
