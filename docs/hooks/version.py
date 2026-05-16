import importlib.metadata


def on_config(config):
    config.extra["version"] = importlib.metadata.version("pireal")
    return config
