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
- `protocol`: `vless`, `vmess`, `trojan`, `shadowsocks`, or `hysteria2`
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

## From an Xray outbound

`outbound` takes the Xray outbound that connects to the server, as it stands in an Xray
client configuration, and fills `protocol`, `endpoint`, `auth`, `tls`, `transport` and
`options` from it. One definition then serves both Xray and the subscriptions:

```yaml
servers:
  - id: hk-xhttp-01
    enabled: true
    name: HK XHTTP Reality 01
    tags: [public, hk]
    outbound:
      protocol: vless
      settings:
        address: hk1.example.com
        port: 443
        id: 11111111-2222-0000-3333-444444444444
        encryption: none
      streamSettings:
        network: xhttp
        security: reality
        realitySettings:
          fingerprint: chrome
          serverName: www.example.com
          publicKey: YOUR_REALITY_PUBLIC_KEY
          shortId: "0000000000000000"
        xhttpSettings:
          path: /path
          mode: auto
```

Fields written next to `outbound` are deep-merged over the fields it gives, so a link field
that Xray does not have, such as `transport.headerType` or an entry of `options`, is written
there. A derived server, a key override and a key-local server accept `outbound` too.

| Outbound | Server |
| --- | --- |
| `protocol` | `protocol`; `hysteria` becomes `hysteria2` |
| `settings.address`, `settings.port` | `endpoint` |
| `settings.id`, `settings.password`, `settings.method` | `auth` |
| `settings.encryption`, `settings.flow` | `options` |
| `streamSettings.network` and its `host`, `path`, `mode`, `serviceName`, `authority` | `transport`; `raw` becomes `tcp` |
| `streamSettings.security` with `realitySettings` or `tlsSettings` | `tls` |
| `realitySettings.mldsa65Verify` | `options.pqv` |
| `hysteriaSettings.auth` | `auth.password` |
| `tlsSettings.pinnedPeerCertSha256`, a `salamander` mask of `finalmask.udp` | `options.pinSHA256`, `options.obfs` and `options.obfs-password` of Hysteria 2 |

The outbound uses the flat `settings` form with `address` and `port`.

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
