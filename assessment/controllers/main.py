from odoo import http
from odoo.http import request


def _format_assessment_date(dt):
    if not dt:
        return ''

    months = [
        '',
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember',
    ]
    return f"{dt.day:02d} {months[dt.month]} {dt.year}"


def _get_kategori(pct):
    if pct >= 67:
        return {
            'label': 'Butuh Dukungan Lebih',
            'tingkat': 'Tinggi',
            'color': '#ef4444',
            'emoji': '⚠️',
        }
    if pct >= 34:
        return {
            'label': 'Perlu Sedikit Perhatian',
            'tingkat': 'Sedang',
            'color': '#f59e0b',
            'emoji': '🌤️',
        }
    return {
        'label': 'Kamu Baik-Baik Saja',
        'tingkat': 'Rendah',
        'color': '#10b981',
        'emoji': '🌿',
    }


class AssessmentController(http.Controller):

    @http.route('/assessment', type='http', auth='user', website=True)
    def assessment_home(self, **kw):
        return request.redirect('/assessment/retry/4591d5f4-b6f7-4991-aab7-9fdae2847b7e')

    @http.route('/assessment/retry/<string:survey_token>', 
                type='http', auth='public', website=True)
    def retry_survey(self, survey_token, **kwargs):
        # Cari survey
        survey = request.env['survey.survey'].sudo().search([
            ('access_token', '=', survey_token)
        ], limit=1)

        if not survey:
            return request.redirect('/')

        # Invalidate sesi lama — set state jadi 'new' atau buat sesi baru
        partner = request.env.user.partner_id
        old_answers = request.env['survey.user_input'].sudo().search([
            ('survey_id', '=', survey.id),
            ('partner_id', '=', partner.id),
            ('state', '=', 'done'),
        ])

        # Buat sesi baru
        new_answer = survey.sudo()._create_answer(
            partner=partner,
            check_attempts=False,
        )

        return request.redirect(
            f'/survey/{survey.access_token}/{new_answer.access_token}'
        )

    @http.route('/assessment/history', auth='user', website=True)
    def assessment_history(self, **kw):
        user_inputs = request.env['survey.user_input'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('state', '=', 'done'),
        ], order='create_date desc')

        history = []
        for ui in user_inputs:
            pct = round(ui.scoring_percentage or 0)
            history.append({
                'id': ui.id,
                'tanggal': _format_assessment_date(ui.create_date),
                'skor': pct,
                'kategori': _get_kategori(pct),
            })

        values = {
            'history': history,
            'assessment_done': len(history) > 0,
            'active_menu': 'assessment',
        }
        return request.render('assessment.template_history', values)