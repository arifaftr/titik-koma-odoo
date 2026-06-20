from odoo import http
from odoo.http import request

class AssessmentController(http.Controller):

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