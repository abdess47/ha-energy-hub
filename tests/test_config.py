"""The entity substitution: options win over YAML, several entities per role."""

from __future__ import annotations

from custom_components.energy_hub.config import HubConfig, parse
from custom_components.energy_hub.const import CONF_ENTITIES
from custom_components.energy_hub.sources import Installation, _apply_yaml, role_entities

YAML = {
    "energy_hub": {
        "demo": True,
        "entities": {"grid_power": "sensor.indevolt_grid_power"},
    }
}


def test_options_replace_the_yaml_entities() -> None:
    cfg = parse(YAML["energy_hub"], {CONF_ENTITIES: {"grid_power": ["sensor.linky_zigbee_power"]}})
    assert cfg.entities["grid_power"] == ["sensor.linky_zigbee_power"]


def test_yaml_entities_are_kept_without_options() -> None:
    cfg = parse(YAML["energy_hub"], {})
    assert cfg.entities["grid_power"] == ["sensor.indevolt_grid_power"]


def test_a_role_accepts_several_entities() -> None:
    cfg = parse(
        YAML["energy_hub"],
        {CONF_ENTITIES: {"pv_power": ["sensor.fusionsolar_power", "sensor.indevolt_pv_power"]}},
    )
    assert cfg.entities["pv_power"] == ["sensor.fusionsolar_power", "sensor.indevolt_pv_power"]


def test_the_first_entity_present_here_drives_the_role() -> None:
    cfg = parse(
        YAML["energy_hub"],
        {CONF_ENTITIES: {"grid_power": ["sensor.indevolt_grid_power", "sensor.linky_zigbee_power"]}},
    )
    inst = Installation()
    # Only the Zigbee module exists in this Home Assistant: it becomes the primary, the other one stays a fallback.
    _apply_yaml(cfg, inst, ["sensor.linky_zigbee_power"])
    assert inst.roles["grid_power"] == "sensor.linky_zigbee_power"
    assert inst.alternatives["grid_power"] == ["sensor.indevolt_grid_power"]
    assert role_entities(inst, "grid_power") == ["sensor.linky_zigbee_power", "sensor.indevolt_grid_power"]


def test_options_entities_are_normalised() -> None:
    cfg: HubConfig = parse(YAML["energy_hub"], {CONF_ENTITIES: {"grid_power": "sensor.linky_zigbee_power"}})
    assert cfg.entities["grid_power"] == ["sensor.linky_zigbee_power"]
