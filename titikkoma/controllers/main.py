from odoo import http
from odoo.http import request
from datetime import date
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


def _is_assessment_done():
    uid = request.session.uid
    if not uid:
        return False
    user = request.env['res.users'].sudo().browse(uid)
    partner_id = user.partner_id.id if user.partner_id else False
    survey_model = request.env['survey.user_input'].sudo()
    fields = survey_model._fields

    # Build a safe domain depending on available fields on the model
    criteria = []
    if 'partner_id' in fields and partner_id:
        criteria.append(('partner_id', '=', partner_id))
    if 'user_id' in fields:
        criteria.append(('user_id', '=', user.id))

    if not criteria:
        return False

    # Combine criteria as OR and require state='done'
    if len(criteria) == 1:
        domain = ['&', ('state', '=', 'done'), criteria[0]]
    else:
        # when two criteria: ['&', ('state','=','done'), '|', crit1, crit2]
        domain = ['&', ('state', '=', 'done'), '|', criteria[0], criteria[1]]

    return survey_model.search_count(domain) > 0

class TitikKomaController(http.Controller):

    def _is_assessment_done(self):
        return _is_assessment_done()

    @http.route('/', type='http', auth='user', website=True, sitemap=False)
    def homepage(self, **kw):
        user = request.env.user
        assessment_retry_url = '/assessment/retry/4591d5f4-b6f7-4991-aab7-9fdae2847b7e'

        today = date.today()
        bulan = [
            '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
        ]
        tanggal_str = f"{today.day} {bulan[today.month]} {today.year}"

        # Count completed assessments for this user/partner if fields exist
        survey_model = request.env['survey.user_input'].sudo()
        sa_fields = survey_model._fields
        jumlah_assessment = 0
        if 'partner_id' in sa_fields and user.partner_id:
            jumlah_assessment = survey_model.search_count([
                ('partner_id', '=', user.partner_id.id),
                ('state', '=', 'done'),
            ])
        elif 'user_id' in sa_fields:
            jumlah_assessment = survey_model.search_count([
                ('user_id', '=', user.id),
                ('state', '=', 'done'),
            ])

        # Mood hari ini
        mood_entry = request.env['moodtracker.entry'].sudo().search([
            ('user_id', '=', user.id),
            ('tanggal', '=', today),
        ], limit=1)

        mood_display = {
            'luar_biasa': 'Luar Binasa',
            'baik': 'Baik',
            'buruk': 'Buruk',
            'sangat_buruk': 'Sangat Buruk',
        }

        last_mood = mood_display.get(mood_entry.mood, None) if mood_entry else None

        journal_count = request.env['student.journal'].sudo().search_count([
            ('student_id', '=', user.id),
        ])

        mood_count = request.env['moodtracker.entry'].sudo().search_count([
            ('user_id', '=', user.id),
        ])

        
        assessment_done = request.env['survey.user_input'].sudo().search_count([
            ('partner_id', '=', user.partner_id.id),
            ('state', '=', 'done'),
        ]) > 0 if user.partner_id else False

        values = {
            'user': user,
            'last_mood': last_mood,
            'journal_count': journal_count,
            'mood_count': mood_count,
            'tanggal': tanggal_str,
            'jumlah_assessment': jumlah_assessment,
            'assessment_done': assessment_done,
            'show_assessment_popup': not assessment_done,
            'assessment_retry_url': assessment_retry_url,
        }

        return request.render('titikkoma.custom_homepage', values)

    @http.route('/self-help-tools', type='http', auth='user', website=True)
    def selfhelp_tools(self, **kw):
        user = request.env.user
        return request.render('titikkoma.selfhelp_tools_page', {
            'user': user,
            'assessment_done': self._is_assessment_done(),
        })

class CustomAuthSignup(AuthSignupHome):

    def web_auth_signup(self, *args, **kw):
        response = super().web_auth_signup(*args, **kw)
        if request.session.uid:
            return request.redirect('/')
        return response
