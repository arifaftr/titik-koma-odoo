from odoo import models, fields

class ChatbotConfig(models.Model):
    _name = 'chatbot.config'
    _description = 'Chatbot Configuration'

    name = fields.Char(string='Name', required=True)
    api_key = fields.Char(string='API Key')
    model_name = fields.Char(string='Model Name', default='gemini-2.5-flash')
    temperature = fields.Float(string='Temperature', default=0.7)