import pytest

from battery_health import BatteryReading, load_config, score, score_fleet


@pytest.fixture(scope="module")
def config():
    return load_config()


def test_new_pack_scores_good(config):
    value, band = score(BatteryReading("PK-1", 100, 60, 0), config)
    assert value == 100.0
    assert band == "good"


def test_worn_pack_needs_replacement(config):
    value, band = score(BatteryReading("PK-2", 70, 130, 1800), config)
    assert value < 70
    assert band == "replace-soon"


def test_fleet_sorted_worst_first(config):
    rows = score_fleet(
        [BatteryReading("PK-A", 95, 65, 200), BatteryReading("PK-B", 80, 80, 900)],
        config,
    )
    assert [r["pack_id"] for r in rows] == ["PK-B", "PK-A"]
    assert rows[0]["band"] == "fair"


def test_config_weights_must_sum_to_one(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("weights: {capacity: 0.5, internal_resistance: 0.1, cycle_count: 0.1}\n")
    with pytest.raises(ValueError):
        load_config(bad)
