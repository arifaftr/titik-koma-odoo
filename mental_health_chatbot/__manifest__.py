{
    'name': 'Mental Health Chatbot',
    'version': '1.1',
    'summary': 'Chatbot AI Gemini untuk kesehatan mental mahasiswa',
    'category': 'Website',
    'depends': ['base', 'website', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/chatbot_data.xml',
        'views/chatbot_config_view.xml',
        'views/chatbot_history_view.xml',
        'views/chatbot_menu.xml',
        'views/chatbot_templates.xml',
    ],
    'assets': {
        'chatbot.assets_chatbot': [
            'mental_health_chatbot/static/src/css/chatbot.css',
            'mental_health_chatbot/static/src/js/chatbot.js',
        ],
    },
    'installable': True,
    'application': True,
}