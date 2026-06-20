{
    'name': 'Edit Profil Website',
    'version': '1.0',
    'summary': 'Fitur edit profil user pada website Odoo',

    'description': """
        Module Edit Profil Website
        ==========================
        
        Modul ini digunakan untuk:
        - Menampilkan halaman edit profil
        - Mengubah nama user
        - Mengubah email
        - Mengubah nomor telepon
        - Mengubah alamat user
        
        Tampilan dibuat menggunakan website Odoo.
    """,

    'author': 'Nufaisa',
    'category': 'Website',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'website',
    ],

    'data': [
        'views/profile_views.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'edit_profil2/static/src/css/style.css',
        ],
    },

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}