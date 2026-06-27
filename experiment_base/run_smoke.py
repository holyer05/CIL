from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .core.config import load_json, write_json
from .core.data import build_class_order, build_dataset, build_loader, inspect_first_batch
from .core.env import collect_environment
from .core.manifest import create_run_dir, write_manifest
from .core.repro import resolve_device, seed_everything


def run(config_path: str) -> dict[str, Any]:
    repo_root = Path.cwd()
    config = load_json(config_path)
    run_dir = create_run_dir(config["output_root"], config["experiment_id"])

    seed_state = seed_everything(int(config["seed"]), bool(config.get("deterministic", True)))
    device = resolve_device(config.get("device", "cuda:0"))

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

    manifest = {
        "status": "completed",
        "experiment_id": config["experiment_id"],
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

