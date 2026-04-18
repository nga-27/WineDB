import logging.config
from pathlib import Path


LOGGER_NAME = "wine_db_api"

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOG_DIR / "wine_db_api.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE_PATH),
            "mode": "a",
            "encoding": "utf-8",
            "formatter": "default",
        },
        # "console": {
        #     "class": "logging.StreamHandler",
        #     "formatter": "default",
        # },
    },
    "loggers": {
        "app": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
