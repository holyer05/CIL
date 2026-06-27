from __future__ import annotations

import importlib.metadata
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import torch


PACKAGE_NAMES = [
    "numpy",
    "scipy",
    "scikit-learn",
    "POT",
    "quadprog",
    "PyYAML",
    "torch",
    "torchvision",
    "joblib",
    "threadpoolctl",
]


def collect_environment(repo_root: str | Path = ".") -> dict[str, Any]:
    repo_root = Path(repo_root)
    packages = {}
    for package in PACKAGE_NAMES:
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None

    return {
        "python": sys.version,
        "platform": platform.platform(),
        "packages": packages,
        "git": collect_git_state(repo_root),
        "cuda": collect_cuda_state(),
    }


def collect_git_state(repo_root: Path) -> dict[str, Any]:
    def run_git(args: list[str]) -> str:
        try:
            return subprocess.check_output(
                ["git", *args],
                cwd=str(repo_root),
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            return ""

    status = run_git(["status", "--short"])
    return {
        "commit": run_git(["rev-parse", "HEAD"]),
        "branch": run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "dirty": bool(status),
        "status_short": status.splitlines(),
    }


def collect_cuda_state() -> dict[str, Any]:
    if not torch.cuda.is_available():
        return {"available": False}
    device_count = torch.cuda.device_count()
    devices = []
    for idx in range(device_count):
        props = torch.cuda.get_device_properties(idx)
        devices.append(
            {
                "index": idx,
                "name": props.name,
                "total_memory_mib": int(props.total_memory / 1024 / 1024),
            }
        )
    return {
        "available": True,
        "torch_cuda": torch.version.cuda,
        "device_count": device_count,
        "devices": devices,
    }

