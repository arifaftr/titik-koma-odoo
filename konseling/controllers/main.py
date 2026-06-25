import re
from urllib.parse import quote

from odoo import http
from odoo.http import request
from odoo.addons.titikkoma.controllers.main import _is_assessment_done


def _normalize_wa_phone(phone):
    if not phone:
        return ''
    digits = re.sub(r'\D', '', str(phone))
    if digits.startswith('0'):
        digits = '62' + digits[1:]
    return digits


def _build_wa_consultation_message(user):
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


def _whatsapp_chat_url(phone, message):
    normalized = _normalize_wa_phone(phone)
    if not normalized:
        return '#'
    return f'https://wa.me/{normalized}?text={quote(message)}'


def _konselor_whatsapp_urls(konselors, user):
    message = _build_wa_consultation_message(user)
    return {k.id: _whatsapp_chat_url(k.nomor_wa, message) for k in konselors}


class KonselingController(http.Controller):

    @http.route('/konseling', type='http', auth='user', website=True)
    def konseling_page(self, **kw):
        user = request.env.user
        konselors = request.env['konseling.konselor'].sudo().search([
            ('aktif', '=', True)
        ])
        return request.render('konseling.konseling_page', {
            'user': user,
            'konselors': konselors,
            'konselor_wa_urls': _konselor_whatsapp_urls(konselors, user),
            'assessment_done': _is_assessment_done(),
        })