"""Score battery health from capacity, internal resistance and cycle count."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "scoring.yaml"


@dataclass(frozen=True)
class BatteryReading:
    pack_id: str
    capacity_pct: float  # remaining capacity versus new, 0-100
    resistance_mohm: float
    cycles: int


def load_config(path: str | Path = DEFAULT_CONFIG) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh)
    total = round(sum(config["weights"].values()), 6)
    if total != 1:
        raise ValueError(f"weights must sum to 1, got {total}")
    return config


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def score(reading: BatteryReading, config: dict) -> tuple[float, str]:
    w, lim = config["weights"], config["limits"]
    capacity = _clamp(reading.capacity_pct / 100)
    span = lim["max_resistance_mohm"] - lim["nominal_resistance_mohm"]
    resistance = _clamp(1 - (reading.resistance_mohm - lim["nominal_resistance_mohm"]) / span)
    cycles = _clamp(1 - reading.cycles / lim["max_cycles"])
    value = round(100 * (w["capacity"] * capacity + w["internal_resistance"] * resistance + w["cycle_count"] * cycles), 1)
    label = next(b["label"] for b in config["bands"] if value >= b["min_score"])
    return value, label


def score_fleet(readings: list[BatteryReading], config: dict) -> list[dict]:
    rows = [{"pack_id": r.pack_id, "score": s, "band": b} for r in readings for s, b in [score(r, config)]]
    return sorted(rows, key=lambda row: row["score"])
