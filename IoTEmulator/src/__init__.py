import logging.config

from .Client import CoAPClient
from .DeviceEmulator import DeviceEmulator
from .config_type import ConfigType, ControlConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": {"stdout"}},
        "asyncio": {"level": "ERROR", "handlers": {"stdout"}},
        "coap-server": {"level": "ERROR", "handlers": {"stdout"}},
        "coap": {"level": "ERROR", "handlers": {"stdout"}},
    }
}
logging.config.dictConfig(logging_config)
