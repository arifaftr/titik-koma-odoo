from odoo import models, fields

class Konsultasi(models.Model):
    _name = 'konseling.konsultasi'
    _description = 'Data Konsultasi'

    konsultasi_id = fields.Integer(string='ID Konsultasi')
    mahasiswa_id = fields.Many2one('res.users', string='Mahasiswa', required=True)
    konselor_id = fields.Many2one('konseling.konselor', string='Konselor', required=True)
    assessment_id = fields.Many2one('survey.user_input', string='Hasil Assessment')
    tanggal_konsultasi = fields.Date(string='Tanggal Konsultasi')
    status = fields.Selection([
        ('draft', 'Menunggu'),
        ('confirmed', 'Dikonfirmasi'),
        ('done', 'Selesai'),
    ], default='draft', string='Status')

    def kirim_permintaan(self):
        self.status = 'confirmed'