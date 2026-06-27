from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import write_json


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def create_run_dir(output_root: str | Path, experiment_id: str) -> Path:
    run_dir = Path(output_root) / f"{utc_timestamp()}_{experiment_id}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_manifest(run_dir: str | Path, manifest: dict[str, Any]) -> Path:
    manifest_path = Path(run_dir) / "manifest.json"
    write_json(manifest_path, manifest)
    return manifest_path

