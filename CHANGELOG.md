# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Release Please updates this file from Conventional Commits merged into `main`.

## [0.2.0] - 2026-06-15

### Added

- Configurable VLESS `encryption` query parameter with `none` as the default.

## [0.1.1] - 2026-05-04

### Fixed

- Startup exits cleanly when configuration cannot be loaded.
- Request errors return controlled HTTP responses.
- Docker-in-Docker development containers explicitly use Moby.

### Changed

- Updated the development container and project tooling for Python 3.13.
- Updated runtime, development, and release workflow dependencies.

## [0.1.0] - 2026-03-21

### Added

- Initial FastAPI subscription service.
- YAML-based server, key, and runtime configuration.
- VLESS, VMess, Trojan, and Shadowsocks share-link renderers.
- Per-key selection and per-server override rules.
- Docker, Compose, CI, development container, documentation, and tests.

[0.2.0]: https://github.com/acha666/sub-server/compare/sub-server-v0.1.1...sub-server-v0.2.0
[0.1.1]: https://github.com/acha666/sub-server/compare/sub-server-v0.1.0...sub-server-v0.1.1
[0.1.0]: https://github.com/acha666/sub-server/releases/tag/sub-server-v0.1.0
