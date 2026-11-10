"""Settings and protection rules with no Endstone dependency, so they can be unit tested without a server."""

from collections.abc import Mapping
from dataclasses import dataclass

AREA_WORLD = "world"
AREA_RADIUS = "radius"
DEFAULT_DIMENSION = "Overworld"
DEFAULT_RADIUS = 64


def _as_bool(value: object, default: bool) -> bool:
    return value if isinstance(value, bool) else default


def _as_number(value: object, default: float) -> float:
    # bool is a subclass of int; a config value of `true` is not a coordinate.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return value


@dataclass(frozen=True)
class Settings:
    protect_blocks: bool = True
    protect_pvp: bool = True
    protect_mobs: bool = True
    area: str = AREA_RADIUS
    dimension: str = DEFAULT_DIMENSION
    center_x: float = 0
    center_z: float = 0
    radius: float = DEFAULT_RADIUS

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "Settings":
        """Build settings from the plugin config, falling back to defaults for missing or invalid values."""
        area = data.get("area")
        if area not in (AREA_WORLD, AREA_RADIUS):
            area = AREA_RADIUS
        dimension = data.get("dimension")
        if not isinstance(dimension, str) or not dimension.strip():
            dimension = DEFAULT_DIMENSION
        radius = _as_number(data.get("radius"), DEFAULT_RADIUS)
        if radius < 0:
            radius = DEFAULT_RADIUS
        return cls(
            protect_blocks=_as_bool(data.get("protect_blocks"), True),
            protect_pvp=_as_bool(data.get("protect_pvp"), True),
            protect_mobs=_as_bool(data.get("protect_mobs"), True),
            area=area,
            dimension=dimension.strip(),
            center_x=_as_number(data.get("center_x"), 0),
            center_z=_as_number(data.get("center_z"), 0),
            radius=radius,
        )


def is_protected(settings: Settings, dimension_name: str, x: float, z: float) -> bool:
    """Return True when the position lies inside the protected area."""
    if dimension_name.casefold() != settings.dimension.casefold():
        return False
    if settings.area == AREA_WORLD:
        return True
    return abs(x - settings.center_x) <= settings.radius and abs(z - settings.center_z) <= settings.radius


def describe(settings: Settings) -> str:
    """One-line summary of what is protected, shown by /spawnprotect."""
    enabled = [
        name
        for name, on in (
            ("blocks", settings.protect_blocks),
            ("pvp", settings.protect_pvp),
            ("mobs", settings.protect_mobs),
        )
        if on
    ]
    if settings.area == AREA_WORLD:
        where = f"all of {settings.dimension}"
    else:
        center = f"({settings.center_x:g}, {settings.center_z:g})"
        where = f"{settings.dimension} within {settings.radius:g} blocks of {center}"
    return f"Protecting {', '.join(enabled) if enabled else 'nothing'} in {where}"
