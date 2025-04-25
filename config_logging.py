import logging
import os

_USE_DEBUG = False

if os.getenv("DEBUG"):
    _USE_DEBUG = True


def config_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if _USE_DEBUG else logging.INFO)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG if _USE_DEBUG else logging.INFO)
    sh_fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(sh_fmt)
    root_logger.addHandler(sh)


config_logging()
