# bertin-t5x
BERTIN Project T5X training files

1. Clone the repo and cd to it
2. Clone https://github.com/google-research/t5x inside with name `t5x_repo` and install in edit mode
3. Symlink `t5x_repo/t5x` to `t5x` in the cloned folder of this repo
3. Install dependencies jax for TPU and seqio (this one from repo)
4. Run `run.sh`

Lists of checkpoints can be found:
- https://console.cloud.google.com/storage/browser/t5-data
- https://console.cloud.google.com/storage/browser/scenic-bucket

If meeting segmentation faults when writing checkpoints to the buckets, the reasone might be `tensorstore` version `0.1.18`. As a temporal fix, try using version `0.1.14` instead.
