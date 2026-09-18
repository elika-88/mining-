import os
from dataclasses import dataclass


def env_float(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError:
        return default


@dataclass(frozen=True)
class RiskThresholds:
    gas_warning: float = env_float("GAS_WARNING_THRESHOLD", 10.0)
    gas_critical: float = env_float("GAS_CRITICAL_THRESHOLD", 20.0)
    temperature_warning: float = env_float("TEMPERATURE_WARNING_THRESHOLD", 40.0)
    temperature_critical: float = env_float("TEMPERATURE_CRITICAL_THRESHOLD", 50.0)
    visibility_warning: float = env_float("VISIBILITY_WARNING_THRESHOLD", 30.0)
    visibility_critical: float = env_float("VISIBILITY_CRITICAL_THRESHOLD", 10.0)
    co_presence_minutes: float = env_float("CO_PRESENCE_WINDOW_MINUTES", 5.0)
    context_minutes: float = env_float("RISK_CONTEXT_WINDOW_MINUTES", 10.0)
    active_window_minutes: float = env_float("ACTIVE_WINDOW_MINUTES", 30.0)


THRESHOLDS = RiskThresholds()

