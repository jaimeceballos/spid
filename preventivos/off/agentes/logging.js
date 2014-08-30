{
    'loggers': {
        'root': {
            'level': 'ERROR',
            'handlers': 'firebug'
        },
        'doff.db.backends.gears.base': {
            'level':'ERROR',
            'handlers':'firebug',
            'propagate': true
        }
    },
    'handlers': {
        'firebug': {
            'class': 'FirebugHandler',
            'level':'DEBUG',
            'formatter': '%(time)s %(name)s(%(levelname)s):\n%(message)s',
            'args': []
        },
        'alert': {
            'class': 'AlertHandler',
            'level':'DEBUG',
            'formatter': '%(levelname)s:\n%(message)s',
            'args': []
        }
    }
}