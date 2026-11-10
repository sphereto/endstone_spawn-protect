# AGENTS.md

Instructions for AI coding agents working on **endstone_spawnprotect**: Spawn protection for Endstone: blocks mob spawns, PvP and block changes while doors and chests keep working.
Endstone Python plugin, targeting Endstone API 0.11. The Endstone API reference for agents is at the
bottom of this file; the project rules come first and take priority.

## Commands

| Task | Command |
|------|---------|
| Install | `uv sync --extra dev` |
| Tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Build wheel | `uv build` |

## Layout

```
src/endstone_spawnprotect/plugin.py     lifecycle + command dispatch (uses the Endstone API)
src/endstone_spawnprotect/listener.py   event handlers (uses the Endstone API)
src/endstone_spawnprotect/settings.py   Endstone-free logic and settings (unit tested)
src/endstone_spawnprotect/config.toml   default config, copied to the server on first run
tests/                       unit tests for Endstone-free code
```

## Rules

1. **Plan first.** Before writing code, state which files you will change, any new commands, permissions
   or config keys, and wait for approval on anything non-trivial.
2. **Keep the core Endstone-free.** Logic that does not need the server API goes in `settings.py` or a new
   Endstone-free module, with tests in `tests/`. Only `plugin.py` and `listener.py` use Endstone at runtime.
3. **One reason to change per file, minimum files.** Keep closely related code together. Add a module only
   when a second independent concern appears or a file passes roughly 400 lines. Never create `utils`,
   `helpers` or `common` modules; name files after what they do.
4. **Every new command needs all of:** its entry in `commands`, its entry in `permissions` (both in
   `plugin.py`), the handler in `on_command`, a row in the README commands and permissions tables, and a
   test for any logic. Every new config key needs a default in `config.toml`, a safe fallback in
   `settings.py` (admins delete keys), and a README row.
5. **Never block the server thread.** Use the server scheduler for slow work (see the API guide below).
6. **Changelog.** Add a line under `## [Unreleased]` in `CHANGELOG.md` for every user-facing change. Release
   notes are copied from that section, so write them for server owners, not developers.
7. **Do not edit release plumbing.** The version comes from the git tag (hatch-vcs); never hardcode one. The
   Release workflow moves the `[Unreleased]` heading; do not do it by hand.
8. **Keep names in sync.** The entry point in `pyproject.toml`, the plugin class, and the permission prefix
   must agree. `api_version` in `plugin.py` must match the Endstone major.minor you target.
9. Commit messages: short, imperative, one change each (for example `Add sethome command`).

## Looking up the Endstone API (read only what you need)

The offline API reference in `docs/endstone-api/` is large (about 0.2 MB). **Never read it whole. Never list or `cat` whole
folders or the big index files.** Look things up in this order:

1. **Class name known:** open that one page, `docs/endstone-api/python/<module>.md` (see `CLASSES.md` for which page holds a class).
2. **Name unknown:** `python docs/endstone-api/lookup.py find <word>` (about 15 lines of matches), or `grep -i <word> docs/endstone-api/CLASSES.md`.
3. **One method, property or enum:** `python docs/endstone-api/lookup.py py <Class> <member>`. Inherited members are followed to the declaring class.
4. **What a class offers:** `python docs/endstone-api/lookup.py py <Class>` prints a short header and member names only.
5. **Events:** `python docs/endstone-api/lookup.py events`.
6. **A page you must open is big** (`Player`, `Server`, `Inventory`): read a line range, and find line numbers with `grep -n "^### " <file>`.
7. **Do not open** `less-useful/`, `class_member_*.md`, `hierarchy.md`, `annotated.md`. Grep them if you must.
8. **Not in the docs?** Do not invent an API. Say so, or check the headers/stubs of the pinned Endstone tag.
   If `docs/endstone-api/` is missing: `git clone --depth 1 --branch v0.11.15 https://github.com/EndstoneMC/endstone /tmp/endstone-src`
   (outside this repo) and grep only `endstone/*.pyi`.

## Definition of done

- `uv run pytest` passes and new logic has tests.
- `uv run ruff check .` and `uv run ruff format --check .` are clean.
- `CHANGELOG.md`, README tables and `AGENTS.md` are updated where behavior or layout changed.
- Say what you could not verify. Behavior inside a real server cannot be tested by CI, so list what the
  maintainer should check in-game.

---

# Endstone Plugin Development Guide

> Adapted from the official EndstoneMC `python-example-plugin` template (MIT). Check https://endstone.dev/latest/ for API changes.

This file helps AI coding agents understand how to build Endstone plugins in Python.

Endstone is a plugin framework for Minecraft Bedrock Dedicated Server (BDS). Plugins are
Python packages installed into the server's `plugins/` folder as `.whl` files.

Docs: https://endstone.dev/latest/

## Project Setup

Package name convention: `endstone-<name>` (PyPI) / `endstone_<name>` (Python package).

Minimal `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "endstone-my-plugin"
version = "0.1.0"
description = "My Endstone plugin"

[project.entry-points."endstone"]
my-plugin = "endstone_my_plugin:MyPlugin"
```

The entry point under `[project.entry-points."endstone"]` tells Endstone which class to load.

## Plugin Class

Every plugin extends `endstone.plugin.Plugin` and declares `api_version`:

```python
from endstone.plugin import Plugin

class MyPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        self.logger.info("Plugin enabled!")

    def on_disable(self) -> None:
        self.logger.info("Plugin disabled!")
```

Lifecycle methods (all optional):
- `on_load()` -- called when the plugin is loaded (before enable, rarely needed)
- `on_enable()` -- called when the plugin is enabled (register events, load config here)
- `on_disable()` -- called when the plugin is disabled (cleanup here)

Key properties available on `self`:
- `self.logger` -- plugin logger
- `self.server` -- the Server instance
- `self.config` -- plugin config (dict-like, loaded from config.toml)
- `self.data_folder` -- path to plugin's data directory

## Commands

Define commands and permissions as class-level dicts:

```python
from endstone import Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.plugin import Plugin

class MyPlugin(Plugin):
    api_version = "0.11"

    commands = {
        "greet": {
            "description": "Send a greeting",
            "usages": ["/greet [player: target]"],
            "aliases": ["hi"],
            "permissions": ["my_plugin.command.greet"],
        },
    }

    permissions = {
        "my_plugin.command.greet": {
            "description": "Allow users to use the /greet command.",
            "default": True,  # True = everyone, "op" = operators only, False = no one
        },
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        match command.name:
            case "greet":
                if isinstance(sender, Player):
                    sender.send_message(f"Hello, {sender.name}!")
                elif isinstance(sender, ConsoleCommandSender):
                    self.logger.info("Hello from the console!")
        return True
```

### Command Parameter Types

Parameters in `usages` use the syntax `<name: type>` (mandatory) or `[name: type]` (optional).

Built-in types: `int`, `float`, `bool`, `str`, `message`, `json`, `target`, `block_pos`, `pos`,
`block`, `block_states`, `entity_type`.

User-defined enums: `(value1|value2|value3)` -- e.g. `/home (add|list|del)<action: HomeAction>`.

### Permission Defaults

- `True` or `"true"` -- everyone can use
- `False` or `"false"` -- no one can use (must be granted)
- `"op"` -- operators only (default if not specified)
- `"not_op"` -- non-operators only
- `"console"` -- console only

## Events

Use the `@event_handler` decorator. Register listeners with `self.register_events()`:

```python
from endstone import ColorFormat
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, event_handler
from endstone.plugin import Plugin

class MyListener:
    def __init__(self, plugin: Plugin) -> None:
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        event.join_message = f"{ColorFormat.YELLOW}{event.player.name} joined"

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        event.quit_message = f"{ColorFormat.YELLOW}{event.player.name} left"
```

Register in `on_enable`:

```python
def on_enable(self) -> None:
    self.register_events(MyListener(self))
    # You can also register the plugin itself if it has @event_handler methods:
    self.register_events(self)
```

Event handlers can also be defined directly on the Plugin class.

### Event Priorities

```python
from endstone.event import EventPriority, event_handler

@event_handler(priority=EventPriority.HIGH, ignore_cancelled=True)
def on_player_join(self, event: PlayerJoinEvent) -> None:
    ...
```

Priorities (lowest runs first): `LOWEST`, `LOW`, `NORMAL` (default), `HIGH`, `HIGHEST`, `MONITOR`.

### Common Events

Player: `PlayerJoinEvent`, `PlayerQuitEvent`, `PlayerChatEvent`, `PlayerCommandEvent`,
`PlayerInteractEvent`, `PlayerDeathEvent`, `PlayerMoveEvent`, `PlayerTeleportEvent`,
`PlayerLoginEvent`, `PlayerKickEvent`, `PlayerGameModeChangeEvent`.

Block: `BlockBreakEvent`, `BlockPlaceEvent`, `BlockExplodeEvent`.

Actor: `ActorSpawnEvent`, `ActorDeathEvent`, `ActorDamageEvent`.

Server: `ServerLoadEvent`, `ServerListPingEvent`, `ServerCommandEvent`.

Packet: `PacketReceiveEvent`, `PacketSendEvent` (for low-level protocol access).

## Configuration

Place a `config.toml` next to your plugin module. Call `self.save_default_config()` in
`on_enable` to copy it to the plugin's data folder on first run:

```toml
# config.toml
greeting = "Hello"
max_homes = 3
```

```python
def on_enable(self) -> None:
    self.save_default_config()
    # Use .get() with defaults to avoid KeyError if the admin removes a key
    greeting = self.config.get("greeting", "Hello")
    max_homes = self.config.get("max_homes", 3)
```

## Scheduler

Schedule delayed or repeating tasks (1 second = 20 ticks):

```python
def on_enable(self) -> None:
    # Run once after 5 seconds
    self.server.scheduler.run_task(self, self.my_task, delay=100)

    # Run every 10 seconds
    self.server.scheduler.run_task(self, self.my_repeating_task, delay=0, period=200)
```

## Color Formatting

```python
from endstone import ColorFormat

msg = f"{ColorFormat.GREEN}Success! {ColorFormat.RESET}Back to normal."
```

Common codes: `BLACK`, `DARK_BLUE`, `DARK_GREEN`, `DARK_AQUA`, `DARK_RED`, `DARK_PURPLE`,
`GOLD`, `GRAY`, `DARK_GRAY`, `BLUE`, `GREEN`, `AQUA`, `RED`, `LIGHT_PURPLE`, `YELLOW`,
`WHITE`, `BOLD`, `ITALIC`, `OBFUSCATED`, `RESET`.

Always end colored text with `ColorFormat.RESET`.

## Common Imports

```python
# Plugin base
from endstone.plugin import Plugin

# Commands
from endstone.command import Command, CommandSender, CommandExecutor, ConsoleCommandSender

# Events
from endstone.event import event_handler, EventPriority
from endstone.event import PlayerJoinEvent, PlayerQuitEvent, PlayerChatEvent
from endstone.event import BlockBreakEvent, BlockPlaceEvent
from endstone.event import ActorDamageEvent, ActorDeathEvent

# Entities and formatting
from endstone import Player, ColorFormat, GameMode

# Forms (GUI)
from endstone.form import ActionForm, ModalForm, MessageForm
```

## Player Methods

```python
player.send_message("text")          # Chat message
player.send_popup("text")            # Popup on screen
player.send_tip("text")              # Tip at top
player.send_title("title", "sub")    # Title screen
player.send_toast("title", "body")   # Toast notification
player.kick("reason")                # Kick from server
player.perform_command("say hi")     # Execute command as player
player.teleport(location)            # Teleport
```

## Building and Installing

```bash
uv build                    # Build .whl
uv sync --extra dev         # Install dev dependencies
uv run ruff check src/      # Lint
```

Copy the `.whl` from `dist/` to your server's `plugins/` folder.

For development, use editable installs: `pip install -e .` (with the server's venv activated),
then `/reload` in-game to pick up changes.