from odoo import http
from odoo.http import request
from datetime import date
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

class TitikKomaController(http.Controller):

    @http.route('/', type='http', auth='user', website=True, sitemap=False)
    def homepage(self, **kw):
        user = request.env.user

        today = date.today()
        bulan = [
            '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
        ]
        tanggal_str = f"{today.day} {bulan[today.month]} {today.year}"

        jumlah_assessment = request.env['survey.user_input'].sudo().search_count([
            ('partner_id', '=', user.partner_id.id),
            ('state', '=', 'done'),
        ])

        # Mood hari ini
        mood_entry = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '=', today),
        ], limit=1)

        mood_display = {
            'luar_biasa': 'Luar Biasa',
            'baik': 'Baik',
            'buruk': 'Buruk',
            'sangat_buruk': 'Sangat Buruk',
        }

        last_mood = mood_display.get(mood_entry.mood, None) if mood_entry else None

        journal_count = 3

        
        values = {
            'user': user,
            'last_mood': last_mood,
            'journal_count': journal_count,
            'tanggal': tanggal_str,
            'jumlah_assessment': jumlah_assessment,
        }

        return request.render('titikkoma.custom_homepage', values)

    @http.route('/self-help-tools', type='http', auth='user', website=True)
    def selfhelp_tools(self, **kw):
        user = request.env.user
        return request.render('titikkoma.selfhelp_tools_page', {
            'user': user,
        })

class CustomAuthSignup(AuthSignupHome):

    def web_auth_signup(self, *args, **kw):
        response = super().web_auth_signup(*args, **kw)
        if request.session.uid:
            return request.redirect('/')
        return response