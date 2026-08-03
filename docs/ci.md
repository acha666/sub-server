# Continuous integration and releases

## Pull requests and main

`.github/workflows/ci.yml` runs four independent checks:

- Ruff lint and formatting checks on Python 3.13
- tests on Python 3.12 and 3.13
- wheel and source distribution builds
- Docker image build without publishing

Concurrent runs for the same branch are cancelled when a newer commit arrives.

## Releases

`.github/workflows/release-please.yml` maintains the changelog and release PR. After a
GitHub release is created, a separate least-privilege job builds the released commit and
publishes its image to GHCR with:

- the release tag
- `latest`
- build provenance
- an SBOM

Only the image-publishing job receives `packages: write`.
