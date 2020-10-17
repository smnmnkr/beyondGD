from geneticNLP.models import POSTagger
from geneticNLP.data import PreProcessed
from geneticNLP.embeddings import FastText
from geneticNLP.utils import Encoding, time_track


#
#
#  -------- load_tagger -----------
#
@time_track
def load_tagger(
    model_config: dict,
    embedding: FastText,
    encoding: Encoding,
) -> POSTagger:

    # --- add data dependent model config
    model_config["lstm"]["in_size"] = embedding.dimension
    model_config["score"]["hid_size"] = len(encoding)

    # --- return model and updated config
    return (POSTagger(model_config), model_config)


#
#
#  -------- load_resources -----------
#
@time_track
def load_resources(
    data_config: dict,
) -> tuple:

    # --- try loading external resources
    try:
        # --- create embedding and encoding objects
        embedding = FastText(data_config.get("embedding"))
        encoding = Encoding(data_config.get("encoding"))

        # --- load and preprocess train and dev data
        data_train = PreProcessed(
            data_config.get("train"), embedding, encoding
        )
        data_dev = PreProcessed(data_config.get("dev"), embedding, encoding)

    # --- handle file not found
    except FileNotFoundError as error:
        raise error

    # --- (optional) load test data
    data_test: PreProcessed = None
    if data_config.get("test", None) != None:
        data_test = PreProcessed(
            data_config.get("test"), embedding, encoding
        )

    # --- return (FastText, Encoding, {"data": type})
    return (
        embedding,
        encoding,
        {"train": data_train, "dev": data_dev, "test": data_test},
    )
