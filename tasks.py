import functools

import seqio
import tensorflow as tf
import t5.data
from datasets import load_dataset
from t5.data import postprocessors
from t5.data import preprocessors
from t5.evaluation import metrics
from seqio import FunctionDataSource, utils

TaskRegistry = seqio.TaskRegistry

DEFAULT_OUTPUT_FEATURES = {
    "inputs": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=True,
        required=False),
    "targets": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=True)
}


def gen_dataset(split, shuffle=False, seed=None, column="text", dataset_params=None):
    skip = dataset_params.pop("skip", None)
    dataset = load_dataset(**dataset_params)
    if shuffle:
        if seed:
            dataset = dataset.shuffle(seed=seed)
        else:
            dataset = dataset.shuffle()
    dataset = dataset[split]
    if skip is not None:
        print(f"Skipping {skip} samples...")
        dataset = dataset.skip(skip)
    while True:
        for item in dataset:
            yield item[column]


def dataset_fn(split, shuffle_files, seed=None, dataset_params=None):
    return tf.data.Dataset.from_generator(
        functools.partial(gen_dataset, split, shuffle_files, seed, dataset_params=dataset_params),
        output_signature=tf.TensorSpec(shape=(), dtype=tf.string, name=dataset_name)
    )


#@utils.map_over_dataset
#def target_to_key(x, key_map, target_key):
#    """Assign the value from the dataset to target_key in key_map"""
#    return {**key_map, target_key: x}


@utils.map_over_dataset
def target_to_key(x, key_map, target_key):
    """Assign the value from the dataset to target_key in key_map"""
    if not isinstance(target_key, (list, tuple)):
        target_key = [target_key]
    new_map = {**key_map}
    for key in target_key:
        new_map[key] = x
    return new_map


# Final pretraining task used in Raffel et al., 2019 adaptated to NCC
dataset_name = 'bertin-project/mc4-es-sampled'
dataset_params = {"path": dataset_name, "name": "gaussian", "streaming": True, "skip": 20000000}
dataset_shapes = None
#vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/oscar/es_32000_bpe.sp.model", extra_ids=100)
vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/wikipedia/es_32000_unigram.sp.model", extra_ids=100)
TaskRegistry.add(
    "mc4_es_gaussian_span_corruption_unigram",
    source=seqio.FunctionDataSource(
        dataset_fn=functools.partial(dataset_fn, dataset_params=dataset_params),
        splits=("train", "validation"),
        caching_permitted=False,
        num_input_examples=dataset_shapes,
    ),
    preprocessors=[
        functools.partial(
            target_to_key, key_map={
                "inputs": None,
                "targets": None,
            }, target_key="targets"),
        seqio.preprocessors.tokenize,
        # seqio.CacheDatasetPlaceholder(),
        preprocessors.span_corruption,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features={"targets": seqio.Feature(vocabulary=vocabulary, add_eos=True)},
    metric_fns=[]
)


# Final pretraining task used in Raffel et al., 2019 adaptated to mc4-es
dataset_name = 'bertin-project/mc4-es-sampled'
dataset_params = {"path": dataset_name, "name": "gaussian", "streaming": True, "skip": 10000000}
dataset_shapes = None
#vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/oscar/es_32000_bpe.sp.model", extra_ids=100)
#vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/wikipedia/es_32000_unigram.sp.model", extra_ids=100)
vocabulary = seqio.SentencePieceVocabulary("gs://t5-data/vocabs/mc4.250000.100extra/sentencepiece.model")
TaskRegistry.add(
    "mc4_es_gaussian_span_corruption_mt5",
    source=seqio.FunctionDataSource(
        dataset_fn=functools.partial(dataset_fn, dataset_params=dataset_params),
        splits=("train", "validation"),
        caching_permitted=False,
        num_input_examples=dataset_shapes,
    ),
    preprocessors=[
        functools.partial(
            target_to_key, key_map={
                "inputs": None,
                "targets": None,
            }, target_key="targets"),
        seqio.preprocessors.tokenize,
        # seqio.CacheDatasetPlaceholder(),
        preprocessors.span_corruption,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features={"targets": seqio.Feature(vocabulary=vocabulary, add_eos=True)},
    metric_fns=[]
)


# Final pretraining task used in Raffel et al., 2019 adaptated to NCC
dataset_name = 'bertin-project/mc4-es-sampled'
dataset_params = {"path": dataset_name, "name": "gaussian", "streaming": True, "skip": 0}
dataset_shapes = None
#vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/oscar/es_32000_bpe.sp.model", extra_ids=100)
#vocabulary = seqio.SentencePieceVocabulary("gs://bertin-project/t5/vocabs/wikipedia/es_32000_unigram.sp.model", extra_ids=100)
vocabulary = seqio.SentencePieceVocabulary("gs://t5-data/vocabs/mc4.250000.100extra/sentencepiece.model")
TaskRegistry.add(
    "mc4_es_gaussian_prefix_lm_mt5",
    source=seqio.FunctionDataSource(
        dataset_fn=functools.partial(dataset_fn, dataset_params=dataset_params),
        splits=("train", "validation"),
        caching_permitted=False,
        num_input_examples=dataset_shapes,
    ),
    preprocessors=[
        functools.partial(
            target_to_key, key_map={
                "inputs": None,
                "targets": None,
            }, target_key=["inputs", "targets"]),
        seqio.preprocessors.tokenize,
        # seqio.CacheDatasetPlaceholder(),
        preprocessors.prefix_lm,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features={
        "inputs": seqio.Feature(vocabulary=vocabulary, add_eos=True, required=False),
        "targets": seqio.Feature(vocabulary=vocabulary, add_eos=True)
    },
    metric_fns=[]
)
