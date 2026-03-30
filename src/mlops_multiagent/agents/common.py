from __future__ import annotations

from mlops_multiagent.state import FlowState


def ensure_security_ok(state: FlowState) -> None:
    if not state.get("security_check", {}).get("is_safe", False):
        raise ValueError("Flödet stoppades eftersom dokumentet inte godkändes i säkerhetskontrollen.")