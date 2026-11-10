from endstone_spawnprotect.settings import AREA_RADIUS, AREA_WORLD, Settings, describe, is_protected


def test_defaults_protect_everything_in_a_radius():
    settings = Settings()
    assert settings.protect_blocks and settings.protect_pvp and settings.protect_mobs
    assert settings.area == AREA_RADIUS


def test_reads_values_from_config():
    settings = Settings.from_mapping(
        {"protect_pvp": False, "area": "world", "dimension": "Nether", "center_x": 10, "center_z": -5.5, "radius": 20}
    )
    assert not settings.protect_pvp
    assert settings.area == AREA_WORLD
    assert settings.dimension == "Nether"
    assert (settings.center_x, settings.center_z, settings.radius) == (10, -5.5, 20)


def test_falls_back_when_config_is_missing_or_invalid():
    assert Settings.from_mapping({}) == Settings()
    bad = Settings.from_mapping(
        {"protect_blocks": "yes", "area": "everywhere", "dimension": "", "center_x": True, "radius": -3}
    )
    assert bad == Settings()


def test_radius_area_is_a_square_around_the_center():
    settings = Settings(center_x=100, center_z=100, radius=10)
    assert is_protected(settings, "Overworld", 100, 100)
    assert is_protected(settings, "Overworld", 110, 90)
    assert not is_protected(settings, "Overworld", 111, 100)
    assert not is_protected(settings, "Overworld", 100, 89)


def test_other_dimensions_are_not_protected_and_names_ignore_case():
    settings = Settings(area=AREA_WORLD)
    assert is_protected(settings, "overworld", 5000, -5000)
    assert not is_protected(settings, "Nether", 0, 0)


def test_describe_lists_enabled_protections():
    assert "blocks, pvp, mobs" in describe(Settings())
    assert describe(Settings(protect_blocks=False, protect_pvp=False, protect_mobs=False)).startswith(
        "Protecting nothing"
    )
    assert "all of Overworld" in describe(Settings(area=AREA_WORLD))
