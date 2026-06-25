from odoo import models, fields


class ChatbotHistory(models.Model):
    _name = 'chatbot.history'
    _description = 'Chatbot History'
    _order = 'create_date desc'

    user_message = fields.Text(string='User Message')
    bot_response = fields.Text(string='Bot Response')
    create_date = fields.Datetime(string='Date', readonly=True)
    session_id = fields.Char(string='Session ID', index=True)
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        index=True,
    )