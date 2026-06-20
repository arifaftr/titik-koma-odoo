from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_nim = fields.Char(string='NIM')
    x_institusi = fields.Char(string='Institusi')
    x_prodi = fields.Char(string='Program Studi')