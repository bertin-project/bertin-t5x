MODEL_DIR="gs://bertin-project/t5/t5_1_1_base_from_t5_vocab_unigram"
python -m t5x.train \
  --gin_file=finetune_t5_base.gin \
  --gin.MODEL_DIR=\"${MODEL_DIR}\" \
  --alsologtostderr
