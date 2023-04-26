import logging.handlers
from pathlib import Path
current_dir = Path.cwd()
LOG_FILE = f"{current_dir}/variantannotator.log"

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(levelname)s: %(message)s'
        },
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-5s %(funcName)-10s (line %(lineno)d) %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'rotating_file': {
            'class': 'logging.handlers.RotatingFileHandler',  # Saves space by creating several logs - deleting as full
            'level': 'ERROR',
            'filename': LOG_FILE,
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 5,
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'VariantAnnotator': {
            'level': 'ERROR',
            'handlers': ['console', 'rotating_file'],
            'propagate': 'no',
        }
    }
}

logger = logging.getLogger("VariantAnnotator")
