from odoo import models, fields

class ChatbotHistory(models.Model):
    _name = 'chatbot.history'
    _description = 'Chatbot History'

    user_message = fields.Text(string='User Message')
    bot_response = fields.Text(string='Bot Response')
    create_date = fields.Datetime(string='Date', readonly=True)