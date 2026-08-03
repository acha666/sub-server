# keys.yaml

Each key defines one `/{key}` subscription:

```yaml
keys:
  demo-public:
    enabled: true
    name: Public demo
    output:
      format: base64
      include_key_in_name: false
      remark_nodes: |
        ${key_name}
        Updated ${datetime}
    select:
      include_ids: []
      include_tags: [public]
      exclude_ids: []
      exclude_tags: []
    overrides:
      hk-vless-01:
        auth:
          uuid: aaaaaaaa-bbbb-0000-cccc-dddddddddddd
```

`name` is the human-friendly key name exposed through `${key_name}`. If omitted, the
subscription key itself is used.

## Key names

Key names form the URL path. They must be non-empty, must not contain `/` or use dot
segments, and must not collide with `healthz`, `docs`, `redoc`, or `openapi.json`.
Every key must explicitly set `enabled`.

## Server assembly

Servers are assembled in this order:

1. Select enabled global servers by `include_ids` / `include_tags`.
2. Remove matches from `exclude_ids` / `exclude_tags`.
3. Deep-merge `overrides` into the selected global servers.
4. Append enabled anonymous servers from the key's `servers` list.

An anonymous server can inherit a global server:

```yaml
servers:
  - extends: hk-vless-01
    name: HK second identity
    auth:
      uuid: eeeeeeee-ffff-0000-aaaa-bbbbbbbbbbbb
```

It can also be defined in full by omitting `extends`. Anonymous servers have no
configuration `id`; their generated internal IDs are not selectable or overrideable.

This allows one key to contain the same endpoint more than once. For example, one selected
server can be overridden with UUID A while an anonymous copy uses UUID B:

```yaml
select:
  include_ids: [hk-vless-01]
overrides:
  hk-vless-01:
    auth:
      uuid: aaaaaaaa-bbbb-0000-cccc-dddddddddddd
servers:
  - extends: hk-vless-01
    auth:
      uuid: eeeeeeee-ffff-0000-aaaa-bbbbbbbbbbbb
```

## Output

- `format: base64` wraps the complete multi-line subscription in base64.
- `format: raw` returns plain share links.
- `include_key_in_name` appends the URL key to real node names.
- `remark_nodes` is a multi-line string. Each non-empty line becomes a non-functional
  VLESS remark node placed before all real nodes.

Remark nodes use a valid VLESS sharing URI with a nil UUID and `127.0.0.1:1`, so parsers
can import them while the endpoint remains local and unusable as a remote proxy. See
[template variables](templates.md) for dynamic text.
