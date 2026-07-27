"""In-memory mission storage.

Known limitation (documented in PROJECT_CONTEXT.md): storage lives only for
the lifetime of the running process. Fine for a hackathon demo.
"""
from __future__ import annotations

from typing import Any

_MISSIONS: dict[str, dict[str, Any]] = {}


def save(mission_id: str, **fields: Any) -> None:
    record = _MISSIONS.setdefault(mission_id, {})
    record.update(fields)


def get(mission_id: str) -> dict[str, Any] | None:
    return _MISSIONS.get(mission_id)


def exists(mission_id: str) -> bool:
    return mission_id in _MISSIONS


def all_missions() -> dict[str, dict[str, Any]]:
    return dict(_MISSIONS)
