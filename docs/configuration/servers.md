# servers.yaml

Top-level shape:

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

- `id`: internal unique server identifier
- `enabled`: whether the server participates in selection
- `protocol`: `vless`, `vmess`, `trojan`, or `shadowsocks` in this first version
- `name`: display name in generated links
- `tags`: free-form labels for include/exclude matching
- `endpoint.host`, `endpoint.port`: target server address
- `auth`: protocol-specific identity fields
- `tls`: TLS / Reality related fields
- `transport`: transport-specific fields such as `type`, `host`, `path`
- `routing`: protocol-specific routing helpers, currently `vless_route`
- `options`: additional protocol-specific query fields
