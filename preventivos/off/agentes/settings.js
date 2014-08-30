// DJANGO OFFLINE SETTINGS FILE
// Please note that Javascript is not Python. You must not end your lists nor
// dictionaries with semicolon.
{
    DEBUG: true,
    TEMPLATE_DEBUG: this.DEBUG,
    
    // Data for status tab
    PROJECT_NAME: 'Vendedor Viajante',
    
    //Database
    DATABASE_ENGINE: 'gears',
    DATABASE_NAME: 'agentes_sqlite.db',
    DATABASE_OPTIONS: {},

    MEDIA_URL: '/static/',

    ROOT_URLCONF: 'agentes.urls',

    INSTALLED_APPS: [
        'doff.contrib.extradata',
        'doff.contrib.offline',
        'agentes.ventas',
        'agentes.core'
    ],

    TOOLBAR_CLASSES: [
             'doff.utils.toolbars.status.Status',
             'doff.utils.toolbars.dbquery.DataBaseQuery',
             'doff.utils.toolbars.logger.Logger',
             'doff.contrib.offline.toolbar.Sync'
        ],

    TEMPLATE_LOADERS: [
                'doff.template.loaders.url.load_template_source'
            ]
}