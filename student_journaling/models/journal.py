from odoo import models, fields, api

class StudentJournal(models.Model):
    _name = 'student.journal'
    _description = 'Student Daily Journal'
    _order = 'date desc'

    name = fields.Char(string='Judul Jurnal', default='Jurnal Baru')
    student_id = fields.Many2one('res.users', string='Mahasiswa', default=lambda self: self.env.user, required=True)
    date = fields.Date(string='Tanggal', default=fields.Date.context_today, required=True)
    
    # Menggunakan HTML agar mahasiswa bisa menulis dengan format (bold, list, dll)
    content = fields.Html(string='Isi Jurnal', required=True)
    
    # Relasi opsional ke Mood hari tersebut
    mood_id = fields.Many2one('student.mood.tracking', string='Mood Terkait', 
                               domain="[('student_id', '=', student_id), ('date', '=', date)]")

    # Kategori Jurnal (Masa Lalu, Masa Ini, Masa Depan)
    category = fields.Selection([
        ('past', 'Masa Lalu'),
        ('present', 'Masa Ini'),
        ('future', 'Masa Depan')
    ], string='Kategori', default='present')

    # Warna Kartu Jurnal
    color_theme = fields.Selection([
        ('teal', 'Teal'),
        ('pink', 'Pink'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('blue', 'Blue'),
        ('red', 'Red')
    ], string='Tema Warna', default='teal')
    
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.date}] {record.name}"
            result.append((record.id, name))
        return result

