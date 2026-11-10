# Contributing to endstone_spawnprotect

Thanks for helping out! This guide covers the workflow. Please also read the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Development setup

You need [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/sphereto/endstone_spawn-protect.git
cd endstone_spawn-protect
uv sync --extra dev
uv run pytest
```

## Making a change

1. Create a branch from `main`.
2. Keep logic that does not need the Endstone API in `settings.py` (or another Endstone-free module) and add tests for it.
3. Run `uv run ruff check .` and `uv run ruff format .`.
4. Add an entry under `## [Unreleased]` in `CHANGELOG.md`. CI requires this for source changes; use the
   `skip-changelog` label for changes users will not notice.
5. Update the README tables if you changed commands, permissions or configuration.
6. Open a pull request. Describe what changed and how you tried it in-game.

CI runs lint, tests on Python 3.10 to 3.14, and builds the wheel. Every run uploads the wheel as an artifact,
so you can try a branch on a test server without building locally.

## Code style

- One reason to change per file. Keep closely related code together; do not split for its own sake.
- No `utils` or `helpers` modules. Name files after what they do.
- Only `plugin.py` and `listener.py` use the Endstone API at runtime.

## Releasing (maintainers)

Releases are one click: **Actions → Release → Run workflow**, then enter the version (for example `0.2.0`).
Tick **dry run** first to preview the notes. The release notes come from the `[Unreleased]` section of
`CHANGELOG.md`, so keep that section accurate. The package version is taken from the git tag.

## Reporting issues

Use [GitHub Issues](https://github.com/sphereto/endstone_spawn-protect/issues). For security problems see [SECURITY.md](SECURITY.md).
