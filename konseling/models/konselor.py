import re
from urllib.parse import quote

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

    def _normalize_wa_phone(self, phone):
        if not phone:
            return ''
        digits = re.sub(r'\D', '', str(phone))
        if digits.startswith('0'):
            digits = '62' + digits[1:]
        return digits

    def _build_wa_consultation_message(self, user):
        partner = user.partner_id
        nama = (user.name or partner.name or '').strip() or '(Isi Nama)'
        nim = (getattr(partner, 'x_nim', None) or '').strip() or '(Isi NIM)'
        prodi = (getattr(partner, 'x_prodi', None) or '').strip() or '(Isi Prodi)'

        return (
            'Halo Admin 👋\n\n'
            'Saya ingin mengajukan konsultasi dengan konselor/psikolog terkait '
            'kondisi kesehatan mental yang sedang saya alami.\n\n'
            f'Nama: {nama}\n'
            f'NIM: {nim}\n'
            f'Program Studi: {prodi}\n'
            'Tanggal Konsultasi yang Diinginkan: (Isi Tanggal)\n'
            'Jam Konsultasi yang Diinginkan: (Isi Jam)\n'
            'Keluhan Singkat: (Isi Keluhan)\n\n'
            'Mohon informasi terkait jadwal yang tersedia.\n\n'
            'Terima kasih'
        )

    def _whatsapp_chat_url(self, phone, message):
        normalized = self._normalize_wa_phone(phone)
        if not normalized:
            return '#'
        return f'https://wa.me/{normalized}?text={quote(message)}'

    def get_whatsapp_url(self, user):
        self.ensure_one()
        message = self._build_wa_consultation_message(user)
        return self._whatsapp_chat_url(self.nomor_wa, message)