from odoo import models, fields
from datetime import date

class MoodEntry(models.Model):
    _name = 'moodtracker.entry'
    _description = 'Mood Harian Mahasiswa'
    _order = 'tanggal desc'

    user_id = fields.Many2one('res.users', string='Mahasiswa', required=True)
    tanggal = fields.Date(string='Tanggal', default=fields.Date.today, required=True)
    mood = fields.Selection([
        ('luar_biasa', 'Luar Biasa'),
        ('baik', 'Baik'),
        ('buruk', 'Buruk'),
        ('sangat_buruk', 'Sangat Buruk'),
    ], string='Mood', required=True)
    catatan = fields.Text(string='Catatan')

    _sql_constraints = [
        ('unique_user_tanggal', 'UNIQUE(user_id, tanggal)',
         'Kamu sudah mengisi mood untuk hari ini.')
    ]