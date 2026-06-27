from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tarfile
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


CIFAR100_MEAN = (0.5071, 0.4867, 0.4408)
CIFAR100_STD = (0.2675, 0.2565, 0.2761)


@dataclass(frozen=True)
class DatasetInfo:
    name: str
    train_size: int
    test_size: int
    num_classes: int
    root: str
    class_to_idx_sample: dict[str, int]


def build_class_order(num_classes: int, strategy: str, seed: int) -> list[int]:
    if strategy == "default":
        return list(range(num_classes))
    if strategy == "random":
        rng = np.random.default_rng(seed)
        return rng.permutation(num_classes).tolist()
    raise ValueError(
        f"Unsupported class-order strategy '{strategy}'. "
        "Use 'default' or 'random' until semantic orders are explicitly defined."
    )


def build_dataset(data_config: dict[str, Any]) -> tuple[Any, Any, DatasetInfo]:
    dataset_name = data_config["dataset"].lower()
    if dataset_name == "cifar100":
        return _build_cifar100(data_config)
    if dataset_name == "imagenet100":
        return _build_imagenet100(data_config)
    raise ValueError(f"Unsupported dataset '{dataset_name}'.")


def build_loader(dataset: Any, loader_config: dict[str, Any]) -> DataLoader:
    return DataLoader(
        dataset,
        batch_size=int(loader_config.get("batch_size", 64)),
        shuffle=False,
        num_workers=int(loader_config.get("num_workers", 0)),
        pin_memory=torch.cuda.is_available(),
    )


def inspect_first_batch(loader: DataLoader) -> dict[str, Any]:
    images, labels = next(iter(loader))
    return {
        "image_shape": list(images.shape),
        "label_shape": list(labels.shape),
        "labels": labels.tolist(),
        "dtype": str(images.dtype),
    }


def _build_cifar100(data_config: dict[str, Any]) -> tuple[Any, Any, DatasetInfo]:
    root = Path(data_config["root"]).expanduser()
    _prepare_cifar100_root(root, data_config)
    download = bool(data_config.get("download", False))
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=CIFAR100_MEAN, std=CIFAR100_STD),
        ]
    )
    train_set = datasets.CIFAR100(root=str(root), train=True, download=download, transform=transform)
    test_set = datasets.CIFAR100(root=str(root), train=False, download=download, transform=transform)
    info = DatasetInfo(
        name="cifar100",
        train_size=len(train_set),
        test_size=len(test_set),
        num_classes=len(train_set.classes),
        root=str(root),
        class_to_idx_sample=dict(list(train_set.class_to_idx.items())[:10]),
    )
    return train_set, test_set, info


def _prepare_cifar100_root(root: Path, data_config: dict[str, Any]) -> None:
    extracted_dir = root / "cifar-100-python"
    if extracted_dir.is_dir():
        return
    archive = data_config.get("archive")
    if archive:
        archive_path = Path(archive).expanduser()
        if not archive_path.is_file():
            raise FileNotFoundError(f"Configured CIFAR-100 archive does not exist: {archive_path}")
        root.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=root)
        if extracted_dir.is_dir():
            return
        raise RuntimeError(f"Extracted CIFAR-100 archive but did not find {extracted_dir}.")


def _build_imagenet100(data_config: dict[str, Any]) -> tuple[Any, Any, DatasetInfo]:
    train_dir = Path(data_config["train_dir"]).expanduser()
    val_dir = Path(data_config["val_dir"]).expanduser()
    if not train_dir.is_dir() or not val_dir.is_dir():
        raise FileNotFoundError(
            "ImageNet100 requires explicit train_dir and val_dir directories. "
            f"Got train_dir={train_dir}, val_dir={val_dir}."
        )
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )
    train_set = datasets.ImageFolder(str(train_dir), transform=transform)
    test_set = datasets.ImageFolder(str(val_dir), transform=transform)
    info = DatasetInfo(
        name="imagenet100",
        train_size=len(train_set),
        test_size=len(test_set),
        num_classes=len(train_set.classes),
        root=str(train_dir.parent),
        class_to_idx_sample=dict(list(train_set.class_to_idx.items())[:10]),
    )
    return train_set, test_set, info
