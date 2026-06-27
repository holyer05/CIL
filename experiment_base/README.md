# Experiment Base

This directory is the trusted experiment base for the A05/A03 diagnostics. It is intentionally separate from `PyCIL/`.

Current scope:

- lock and verify core dependencies;
- configure dataset paths without hard-coding them in Python code;
- make seeds control Python, NumPy, PyTorch, CUDA and class-order generation;
- write a structured manifest for every run;
- run a minimal smoke test without training a model.

What is copied from PyCIL at this stage:

- CIFAR-100 normalization statistics;
- the seeded class-order idea used by `DataManager`;
- the closed-world all-seen class-incremental setting.

What is not copied yet:

- legacy trainer/model code with hard-coded `.cuda()`;
- ImageNet classes with `[DATA-PATH]` placeholders;
- methods that need missing diagnostics or unsupported datasets.

CIFAR-100 policy:

- prefer the public archive at `/root/autodl-pub/cifar-100/cifar-100-python.tar.gz`;
- extract it into the writable project cache `experiment_base/data/cifar-100`;
- never write into `/root/autodl-pub`.

Run the smoke test from the repository root:

```bash
python -m experiment_base.run_smoke --config experiment_base/configs/smoke_cifar100.json
```

The smoke test writes a manifest under `experiment_base/runs/`.
