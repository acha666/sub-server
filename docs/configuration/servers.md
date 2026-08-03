# servers.yaml

`servers.yaml` contains reusable, named server definitions:

```yaml
servers:
  - id: hk-vless-01
    enabled: true
    protocol: vless
    name: HK VLESS Reality 01
    tags: [public, hk]
    endpoint:
      host: hk1.example.com
      port: 443
    auth:
      uuid: 11111111-2222-0000-3333-444444444444
```

## Core fields

- `id`: unique internal identifier
- `enabled`: switch controlling whether the server participates in selection
- `protocol`: `vless`, `vmess`, `trojan`, or `shadowsocks`
- `name`: node name in generated links; [template variables](templates.md) are supported
- `tags`: labels used by key selection
- `endpoint.host`, `endpoint.port`: target address
- `auth`: protocol-specific identity
- `tls`: TLS and Reality settings
- `transport`: transport settings such as `type`, `host`, and `path`
- `routing`: protocol-specific routing helpers
- `options`: additional protocol query fields

Ports, credentials, Reality settings, and routing values are validated after inheritance is
resolved.

## Derived servers

A named server can inherit another server and specify only the facts that differ:

```yaml
servers:
  - id: la
    enabled: true
    protocol: vless
    name: Los Angeles
    tags: [us, vless]
    endpoint:
      host: la.example.com
      port: 443
    auth:
      uuid: 11111111-2222-0000-3333-444444444444

  - id: la-route-14
    extends: la
    name: Los Angeles route 14
    routing:
      vless_route: 14
```

Fields in the derived definition are deep-merged onto the parent. Nested values can be
cleared with `null`. References may point forward or backward in the file; unknown
references and inheritance cycles are rejected.
