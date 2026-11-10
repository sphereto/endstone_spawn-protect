"""Event handlers. Each one only cancels events; the rules live in settings.py."""

from collections.abc import Callable

from endstone import Player
from endstone.actor import Mob
from endstone.event import (
    ActorDamageEvent,
    ActorSpawnEvent,
    BlockBreakEvent,
    BlockPlaceEvent,
    event_handler,
)
from endstone.plugin import Plugin

from .settings import Settings, is_protected

BYPASS_PERMISSION = "spawnprotect.bypass"


class SpawnprotectListener:
    def __init__(self, plugin: Plugin, get_settings: Callable[[], Settings]) -> None:
        self._plugin = plugin
        self._get_settings = get_settings

    @event_handler
    def on_block_break(self, event: BlockBreakEvent) -> None:
        self._guard_block(event, event.player)

    @event_handler
    def on_block_place(self, event: BlockPlaceEvent) -> None:
        self._guard_block(event, event.player)

    @event_handler
    def on_actor_spawn(self, event: ActorSpawnEvent) -> None:
        settings = self._get_settings()
        actor = event.actor
        # Players are Mobs too; items, projectiles and other non-living actors are left alone.
        if not settings.protect_mobs or not isinstance(actor, Mob) or isinstance(actor, Player):
            return
        location = actor.location
        if is_protected(settings, actor.dimension.name, location.x, location.z):
            event.cancel()

    @event_handler
    def on_actor_damage(self, event: ActorDamageEvent) -> None:
        settings = self._get_settings()
        victim = event.actor
        if not settings.protect_pvp or not isinstance(victim, Player):
            return
        source = event.damage_source
        # `actor` is the cause (the shooter for an arrow), `damaging_actor` the direct source.
        attacker = source.actor or source.damaging_actor
        if not isinstance(attacker, Player) or attacker is victim:
            return
        location = victim.location
        if is_protected(settings, victim.dimension.name, location.x, location.z):
            event.cancel()

    def _guard_block(self, event: BlockBreakEvent | BlockPlaceEvent, player: Player) -> None:
        settings = self._get_settings()
        if not settings.protect_blocks or player.has_permission(BYPASS_PERMISSION):
            return
        block = event.block
        if is_protected(settings, block.dimension.name, block.x, block.z):
            event.cancel()
            player.send_popup("This area is protected")
