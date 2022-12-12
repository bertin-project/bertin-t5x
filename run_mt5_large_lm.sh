MODEL_DIR="gs://bertin-project/t5/mt5_large_lm"

python -m t5x.train \
  --gin_file=finetune_mt5_large_lm.gin \
  --gin.MODEL_DIR=\"${MODEL_DIR}\" \
  --alsologtostderr
