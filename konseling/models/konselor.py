from odoo import models, fields

class Konselor(models.Model):
    _name = 'konseling.konselor'
    _description = 'Data Konselor'

    name = fields.Char(string='Nama Konselor', required=True)
    spesialisasi = fields.Char(string='Spesialisasi')
    deskripsi = fields.Text(string='Deskripsi')
    nomor_wa = fields.Char(string='Nomor WhatsApp')
    foto = fields.Binary(string='Foto', attachment=True)
    foto_filename = fields.Char(string='Nama File Foto')
    aktif = fields.Boolean(string='Aktif', default=True)