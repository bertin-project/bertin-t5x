MODEL_DIR="gs://bertin-project/t5/mt5_large"
TFDS_DATA_DIR="gs://bertin-project/t5/tfds"

python -m t5x.train \
  --gin_file=finetune_mt5_large.gin \
  --gin.MODEL_DIR=\"${MODEL_DIR}\" \
  --tfds_data_dir=\"${TFDS_DATA_DIR}\" \
  --alsologtostderr
