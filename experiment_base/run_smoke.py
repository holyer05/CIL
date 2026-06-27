from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any

import torch

from .core.config import load_json, write_json
from .core.data import build_class_order, build_dataset, build_loader, inspect_first_batch
from .core.env import collect_environment
from .core.manifest import create_run_dir, write_manifest
from .core.repro import resolve_device, seed_everything


def run(config_path: str) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc).isoformat()
    timer_start = time.perf_counter()
    repo_root = Path.cwd()
    config = load_json(config_path)
    run_dir = create_run_dir(config["output_root"], config["experiment_id"])

    seed_state = seed_everything(int(config["seed"]), bool(config.get("deterministic", True)))
    device = resolve_device(config.get("device", "cuda:0"))
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    train_set, test_set, dataset_info = build_dataset(config["data"])
    loader = build_loader(train_set, config.get("loader", {}))
    first_batch = inspect_first_batch(loader)

    order_seed = int(config.get("class_order", {}).get("seed", config["seed"]))
    strategy = config.get("class_order", {}).get("strategy", "random")
    order_a = build_class_order(dataset_info.num_classes, strategy, order_seed)
    order_b = build_class_order(dataset_info.num_classes, strategy, order_seed)
    order_c = build_class_order(dataset_info.num_classes, strategy, order_seed + 1)

    config_snapshot_path = run_dir / "config.snapshot.json"
    write_json(config_snapshot_path, config)
    elapsed_seconds = time.perf_counter() - timer_start
    finished_at = datetime.now(timezone.utc).isoformat()
    gpu_memory = None
    if device.type == "cuda":
        gpu_memory = {
            "device": str(device),
            "allocated_mib": round(torch.cuda.memory_allocated(device) / 1024 / 1024, 3),
            "reserved_mib": round(torch.cuda.memory_reserved(device) / 1024 / 1024, 3),
            "max_allocated_mib": round(torch.cuda.max_memory_allocated(device) / 1024 / 1024, 3),
        }

    manifest = {
        "status": "completed",
        "experiment_id": config["experiment_id"],
        "started_at": started_at,
        "finished_at": finished_at,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "run_dir": str(run_dir),
        "config_path": str(config_path),
        "config_snapshot": str(config_snapshot_path),
        "environment": collect_environment(repo_root),
        "seed_state": seed_state,
        "device": str(device),
        "dataset": asdict(dataset_info),
        "class_order": {
            "strategy": strategy,
            "seed": order_seed,
            "first_20": order_a[:20],
            "same_seed_reproducible": order_a == order_b,
            "different_seed_changes_order": order_a != order_c,
        },
        "loader_smoke": first_batch,
        "metrics": {
            "smoke": {
                "dataset_train_size": dataset_info.train_size,
                "dataset_test_size": dataset_info.test_size,
                "num_classes": dataset_info.num_classes,
                "same_seed_reproducible": order_a == order_b,
                "different_seed_changes_order": order_a != order_c,
            },
            "accuracy_matrices": {},
        },
        "resources": {
            "gpu_memory": gpu_memory,
        },
    }
    manifest_path = write_manifest(run_dir, manifest)
    print(f"SMOKE_OK manifest={manifest_path}")
    print(
        "DATASET "
        f"name={dataset_info.name} train={dataset_info.train_size} "
        f"test={dataset_info.test_size} classes={dataset_info.num_classes}"
    )
    print(
        "REPRO "
        f"same_seed={manifest['class_order']['same_seed_reproducible']} "
        f"diff_seed={manifest['class_order']['different_seed_changes_order']}"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the trusted experiment-base smoke test.")
    parser.add_argument("--config", required=True, help="Path to a JSON smoke config.")
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
