{
    'name': 'Mood Tracker',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Fitur mood tracker harian untuk mahasiswa',
    'author': 'Kelompok 2',
    'depends': ['base', 'website', 'titikkoma'],
    'data': [
        'security/ir.model.access.csv',
        'views/moodtracker_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}