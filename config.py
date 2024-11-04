import logging.config
import os

DEVICE_NAME = os.getenv("DEVICE_NAME", "iPhone 14 Pro Max")
BASE_UI_URL = os.getenv("BASE_UI_URL", "https://m.twitch.tv/")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
