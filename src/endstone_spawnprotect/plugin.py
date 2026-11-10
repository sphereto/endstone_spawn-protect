"""Plugin lifecycle, commands and permissions. Protection rules live in settings.py, event handling in listener.py."""

from endstone.command import Command, CommandSender
from endstone.plugin import Plugin
from typing_extensions import override

from .listener import SpawnprotectListener
from .settings import Settings, describe


class SpawnprotectPlugin(Plugin):
    prefix = "SpawnprotectPlugin"

    # Must match the major.minor version of the Endstone API you are targeting.
    api_version = "0.11"

    commands = {
        "spawnprotect": {
            "description": "Show the spawn protection status or reload its config",
            "usages": ["/spawnprotect", "/spawnprotect (status|reload)<action: SpawnprotectAction>"],
            "permissions": ["spawnprotect.command.spawnprotect"],
        },
    }

    permissions = {
        "spawnprotect.command.spawnprotect": {
            "description": "Allow users to use the /spawnprotect command.",
            "default": "op",
        },
        "spawnprotect.bypass": {
            "description": "Allow breaking and placing blocks inside the protected area.",
            "default": "op",
        },
    }

    # Immutable, so sharing the default between instances is safe; replaced on enable and reload.
    _settings = Settings()

    @override
    def on_enable(self) -> None:
        # Copies config.toml to the plugin's data folder on first run and keeps the admin's edits afterwards.
        self.save_default_config()
        self._settings = Settings.from_mapping(self.config)
        self.register_events(SpawnprotectListener(self, lambda: self._settings))
        self.logger.info(describe(self._settings))

    @override
    def on_disable(self) -> None:
        self.logger.info(f"{self.name} disabled")

    @override
    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name != "spawnprotect":
            return False
        if args and args[0] == "reload":
            self._settings = Settings.from_mapping(self.reload_config())
            sender.send_message("Spawn protection config reloaded")
        sender.send_message(describe(self._settings))
        return True
