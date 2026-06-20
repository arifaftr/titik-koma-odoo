from odoo import http, fields
from odoo.http import request
import base64

class StudentJournalWebsite(http.Controller):

    @http.route('/journaling', type='http', auth="public", website=True)
    def journal_dashboard(self, **post):
        journals = request.env['student.journal'].sudo().search([])
        return request.render("student_journaling.website_journal_list", {
            'journals': journals,
        })

    @http.route('/journaling/list', type='http', auth="public", website=True)
    def journal_list(self, **post):
        return request.redirect('/journaling')

    @http.route('/journaling/new', type='http', auth="public", website=True)
    def journal_new(self, **post):
        return request.render("student_journaling.website_journal_form", {})

    @http.route('/journaling/save', type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def journal_save(self, **post):
        vals = {
            'name': post.get('name') or "Catatan Hari Ini",
            'category': post.get('category'),
            'color_theme': post.get('color_theme'),
            'content': post.get('content'),
            'date': fields.Date.today(),
        }
        
        if post.get('image'):
            image_data = post.get('image').read()
            vals['image'] = base64.b64encode(image_data)
            
        request.env['student.journal'].sudo().create(vals)
        return request.redirect('/journaling/list')

    @http.route('/journaling/detail/<model("student.journal"):journal>', type='http', auth="public", website=True)
    def journal_detail(self, journal, **post):
        return request.render("student_journaling.website_journal_detail", {
            'journal': journal,
        })

    @http.route('/journaling/delete/<int:journal_id>', type='http', auth="public", website=True, csrf=False)
    def journal_delete(self, journal_id, **post):
        journal = request.env['student.journal'].sudo().browse(journal_id)
        if journal.exists():
            journal.unlink()
        return request.redirect('/journaling/list')
