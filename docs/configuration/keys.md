# keys.yaml

Top-level shape:

```yaml
keys:
  demo-public:
    enabled: true
    output:
      format: base64
      include_key_in_name: false
    select:
      include_ids: []
      include_tags: [public]
      exclude_ids: []
      exclude_tags: []
    overrides:
      hk-vless-01:
        patch:
          routing:
            vless_route: 14
```

## Selection order

1. Start from all enabled servers
2. Apply `include_ids` and `include_tags`
3. Apply `exclude_ids` and `exclude_tags`
4. Apply per-server override patches

## Output

- `base64`: multi-line share links wrapped in one base64 blob
- `raw`: plain multi-line share links
