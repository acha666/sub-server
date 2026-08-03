# Reuse and override rules

All configuration reuse uses recursive mapping merges. A nested mapping updates only the
specified leaves; lists and scalar values replace their inherited values. Optional
sections such as `routing`, `tls`, and `transport` can be cleared with `null`.

## Named derivation

Use `extends` in `servers.yaml` when the result is a reusable server with its own `id`:

```yaml
- id: base
  # complete server definition

- id: routed
  extends: base
  name: Routed copy
  routing:
    vless_route: 14
```

## Per-key override

Use `overrides` when a key should edit a selected global server in place:

```yaml
overrides:
  base:
    auth:
      uuid: aaaaaaaa-bbbb-0000-cccc-dddddddddddd
    transport:
      path: /user-a
```

The result keeps the same server identity and occupies the same position in selection;
an `id` inside the override cannot rename it.

## Anonymous instance

Use a key-local `servers` entry when the key needs an additional instance:

```yaml
servers:
  - extends: base
    auth:
      uuid: eeeeeeee-ffff-0000-aaaa-bbbbbbbbbbbb
```

This creates a separate subscription node and does not change the selected `base` server.
A full server definition without `extends` creates an instance private to that key.
