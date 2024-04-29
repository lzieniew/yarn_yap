import toml


def get_tts_engine() -> str:
    with open("config.toml", "r") as f:
        config = toml.load(f)
    return config["tts_engine"]


def get_max_sentence_length() -> int:
    with open("config.toml", "r") as f:
        config = toml.load(f)
    return int(config["max_sentence_length"])
