{
    'name': 'Student Journaling',
    'version': '1.0',
    'summary': 'Modul untuk mencatat jurnal harian mahasiswa',
    'category': 'Education',
    'depends': ['base', 'student_mood_tracking', 'website', 'titikkoma'],
    'data': [
        'security/ir.model.access.csv',
        'views/journal_views.xml',
        'views/dashboard_views.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'website.assets_frontend': [
            'student_journaling/static/src/css/journal_style.css',
        ],
        'web.assets_frontend': [
            'student_journaling/static/src/css/journal_style.css',
        ],
        'web.assets_backend': [
            'student_journaling/static/src/css/journal_style.css',
        ],
    },
    'installable': True,
    'application': True,
}
