{
    'name': 'Konseling',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Fitur konseling & rekomendasi bantuan kesehatan mental',
    'author': 'Kelompok 2',
    'depends': ['base', 'website', 'titikkoma', 'survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/konselor_views.xml',
        'views/konseling_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'konseling/static/src/css/konseling.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}