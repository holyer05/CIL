# CIL

Exemplar-free class-incremental learning research workspace based on PyCIL.

## Repository layout

- `PyCIL/`: baseline code and research implementations.
- `papers/`: local literature workspace. Third-party PDF files are intentionally excluded from Git.
- `AGENTS.md`: research and collaboration constraints.
- `scripts/sync_to_github.sh`: commit and push the current workspace state.

## Data

Datasets and generated model artifacts are not committed. On AutoDL, shared datasets are available under `/root/autodl-pub`.

## Versioning workflow

Every meaningful project update should be committed and pushed to `main` so it can be reviewed or rolled back later.

```bash
cd /root/autodl-tmp/CIL
./scripts/sync_to_github.sh "describe the change"
```

This server uses a repository-scoped deploy key. The key can only access `holyer05/CIL`.
