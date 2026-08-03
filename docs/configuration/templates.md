# Template variables

Node names and `output.remark_nodes` support `${name}` placeholders:

| Variable | Value |
|---|---|
| `${key}` | URL subscription key |
| `${key_name}` | key `name`, or the URL key when no name is configured |
| `${date}` | local server date as `YYYY-MM-DD` |
| `${time}` | local server time as `HH:MM` |
| `${datetime}` | local server date and time as `YYYY-MM-DD HH:MM` |

All values for one response use the same timestamp. Use `$$` for a literal dollar sign.
Unknown or malformed placeholders make the configuration invalid.
