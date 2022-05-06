MODEL_DIR="gs://bertin-project/t5/t5_1_1_base"
TFDS_DATA_DIR="gs://bertin-project/t5/tfds"

python -m t5x.train \
  --gin_file=pretrain_t5_1_1_base.gin \
  --gin.MODEL_DIR=\"${MODEL_DIR}\" \
  --tfds_data_dir=\"${TFDS_DATA_DIR}\" \
  --alsologtostderr
