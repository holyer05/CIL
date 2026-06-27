from __future__ import annotations

import os
import random
from typing import Any

import numpy as np
import torch


def seed_everything(seed: int, deterministic: bool = True) -> dict[str, Any]:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except TypeError:
            torch.use_deterministic_algorithms(True)
    return {
        "seed": seed,
        "deterministic": deterministic,
        "pythonhashseed": os.environ["PYTHONHASHSEED"],
        "torch_initial_seed": int(torch.initial_seed()),
    }


def resolve_device(device: str) -> torch.device:
    requested = device.lower()
    if requested.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(f"Requested {device}, but CUDA is not available.")
    if requested.startswith("cuda"):
        index = 0 if ":" not in requested else int(requested.split(":", 1)[1])
        if index >= torch.cuda.device_count():
            raise RuntimeError(
                f"Requested cuda:{index}, but only {torch.cuda.device_count()} CUDA device(s) exist."
            )
    return torch.device(requested)

