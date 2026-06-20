{
    'name': 'Titik Koma',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Dashboard kesehatan mental mahasiswa dengan fitur lengkap',
    'description': """
        Titik Koma - Sistem Kesehatan Mental Mahasiswa
        =============================================
        Fitur:
        - Self Assessment (Survey)
        - Mood Tracker
        - Journaling
        - Chat AI (Live Chat)
        - Konselor (WhatsApp)
        - Self Help Tools (Blog)
        
        Design calming dengan tema ungu modern
    """,
    'author': 'Kelompok 2',
    'depends': ['base', 'website', 'survey', 'website_livechat'],
    'data': [
        'views/website_override.xml',
        'views/selfhelp_tools.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'titikkoma/static/src/css/titikkoma.css',
            'titikkoma/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}