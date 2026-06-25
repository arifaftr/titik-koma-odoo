from odoo import http
from odoo.http import request
from datetime import date, timedelta
from odoo.addons.titikkoma.controllers.main import _is_assessment_done

class MoodTrackerController(http.Controller):

    @http.route('/mood-tracker', type='http', auth='user', website=True)
    def mood_tracker(self, **kw):
        user = request.env.user

        # Cek mood hari ini
        today = date.today()
        mood_hari_ini = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '=', today),
        ], limit=1)

        # History 30 hari terakhir
        tiga_puluh_hari = today - timedelta(days=29)
        history = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '>=', tiga_puluh_hari),
        ])

        # Statistik 7 hari terakhir
        tujuh_hari = today - timedelta(days=6)
        minggu_ini = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '>=', tujuh_hari),
        ])

        total = len(minggu_ini)
        positif = len(minggu_ini.filtered(lambda m: m.mood in ['luar_biasa', 'baik']))
        persen_positif = round((positif / total * 100)) if total else 0

        mood_counts = {
            'luar_biasa': len(minggu_ini.filtered(lambda m: m.mood == 'luar_biasa')),
            'baik': len(minggu_ini.filtered(lambda m: m.mood == 'baik')),
            'buruk': len(minggu_ini.filtered(lambda m: m.mood == 'buruk')),
            'sangat_buruk': len(minggu_ini.filtered(lambda m: m.mood == 'sangat_buruk')),
        }

        # Mood dominan
        mood_dominan = max(mood_counts, key=mood_counts.get) if total else None

        mood_label = {
            'luar_biasa': 'Luar Biasa 😄',
            'baik': 'Baik 😊',
            'buruk': 'Buruk 😔',
            'sangat_buruk': 'Sangat Buruk 😞',
        }

        return request.render('moodtracker.moodtracker_page', {
            'user': user,
            'mood_hari_ini': mood_hari_ini,
            'history': history,
            'total': total,
            'persen_positif': persen_positif,
            'mood_dominan': mood_dominan,
            'mood_label': mood_label,
            'mood_counts': mood_counts,
            'today': today,
            'assessment_done': _is_assessment_done(),
        })

    @http.route('/mood-tracker/simpan', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def simpan_mood(self, mood=None, catatan=None, **kw):
        user = request.env.user
        today = date.today()

        existing = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '=', today),
        ], limit=1)

        if existing:
            existing.sudo().write({'mood': mood, 'catatan': catatan})
        else:
            request.env['moodtracker.entry'].sudo().create({
                'user_id': user.id,
                'tanggal': today,
                'mood': mood,
                'catatan': catatan or '',
            })

        return request.redirect('/mood-tracker')