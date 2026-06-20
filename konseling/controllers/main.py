from odoo import http
from odoo.http import request

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
        })