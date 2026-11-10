# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Block breaking and placing is cancelled inside the protected area; doors, chests and other interactions still work.
- Player-versus-player damage is cancelled inside the protected area.
- Mob spawning is cancelled inside the protected area.
- `spawnprotect.bypass` permission (operators by default) to build inside the area.
- `/spawnprotect` shows the active protection and `/spawnprotect reload` reloads the config.
- Configurable area: a square around a center point, or a whole dimension.
