import logging
import logging.config

logging_config: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s #%(lineno)d)'
        },
    },
    'handlers': {
        'default_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'muser.log',
            'encoding': 'utf8'
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'main': {
            'handlers': ['default_handler', 'console_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}


logging.config.dictConfig(logging_config)
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
critical = logger.critical
print = info

print("--------------------Muser new run--------------------")
