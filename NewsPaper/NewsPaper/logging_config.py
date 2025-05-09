import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_debug': {
            'format': '{asctime} - {levelname}: {message}',
            'style': '{'
        },
        'console_warning': {
            'format': '{asctime} - {levelname} - {pathname}: {message}',
            'style': '{'
        },
        'console_error': {
            'format': '{asctime} - {levelname} - {pathname}\n{exc_text}\n{message}',
            'style': '{'
        },
        'general': {
            'format': '{asctime} - {levelname} - {module}: {message}',
            'style': '{',
        },
        'errors': {
            'format': '{asctime} - {levelname} - {pathname}\n{exc_text}\n{message}',
            'style': '{'
        },
        'errors_mail': {
            'format': '{asctime} - {levelname} - {pathname}\n{message}',
            'style': '{',
        },
        'security': {
            'format': '{asctime} - {levelname} - {module}: {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug'
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
        },
        'general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'general.log'),
            'formatter': 'general',
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'formatter': 'errors',
        },
        'errors_mail': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'errors_mail',
        },
        'security': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'general'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['errors', 'errors_mail'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors', 'errors_mail'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.template': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.security': {
            'handlers': ['security'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
