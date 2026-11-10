# endstone_spawn-protect

[![CI](https://github.com/sphereto/endstone_spawn-protect/actions/workflows/ci.yml/badge.svg)](https://github.com/sphereto/endstone_spawn-protect/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sphereto/endstone_spawn-protect)](https://github.com/sphereto/endstone_spawn-protect/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Spawn protection for Endstone: blocks mob spawns, PvP and block changes while doors and chests keep working.

An [Endstone](https://endstone.dev) plugin for Minecraft Bedrock Dedicated Server, written in Python.

## Compatibility

| endstone_spawnprotect | Endstone | Python |
|----------|----------|--------|
| latest   | 0.11.x | 3.10+ |

## Install

1. Download the `.whl` file from the [latest release](https://github.com/sphereto/endstone_spawn-protect/releases/latest).
2. Put it in your server's `plugins/` folder.
3. Restart the server.

Each release includes `SHA256SUMS.txt` so you can verify your download.

## Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/spawnprotect` | Show what is protected | `spawnprotect.command.spawnprotect` |
| `/spawnprotect reload` | Reload `config.toml` without a restart | `spawnprotect.command.spawnprotect` |

## Permissions

| Permission | Description | Default |
|------------|-------------|---------|
| `spawnprotect.command.spawnprotect` | Allow users to use the `/spawnprotect` command | operators |
| `spawnprotect.bypass` | Break and place blocks inside the protected area | operators |

## Configuration

`config.toml` is created in the plugin's data folder on first run.

| Key | Default | Description |
|-----|---------|-------------|
| `protect_blocks` | `true` | Cancel block breaking and placing (doors, chests and other interactions are not touched) |
| `protect_pvp` | `true` | Cancel player-versus-player damage |
| `protect_mobs` | `true` | Cancel mob spawning (players, items and projectiles are not affected) |
| `area` | `"radius"` | `"radius"` protects a square around the center, `"world"` protects the whole dimension |
| `dimension` | `"Overworld"` | Dimension to protect, as the server names it |
| `center_x`, `center_z` | `0` | Center of the square when `area = "radius"` |
| `radius` | `64` | Half the side length of the square, in blocks |

Invalid or missing values fall back to these defaults.

## Development

Requirements: [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv build            # builds the wheel into dist/
```

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first, and follow the
[Code of Conduct](CODE_OF_CONDUCT.md). Report security problems as described in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
