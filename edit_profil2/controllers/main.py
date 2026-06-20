import base64

from odoo import http
from odoo.http import request


class EditProfil(http.Controller):

    @http.route([
        '/edit-profil'
    ],
                type='http',
                auth='user',
                website=True)
    def edit_profil(self, **kw):

        user = request.env.user

        return request.render('edit_profil2.edit_profile_template', {
            'user': user,
            'partner': user.partner_id,
        })

    @http.route([
        '/update-profil'
    ],
                type='http',
                auth='user',
                methods=['POST'],
                website=True)
    def update_profil(self, **post):

        partner = request.env.user.partner_id

        # Data umum
        partner.write({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'x_nim': post.get('nim'),
            'x_institusi': post.get('institusi'),
            'x_prodi': post.get('prodi'),
        })

        # Upload foto
        foto = post.get('foto')
        if foto and hasattr(foto, 'read'):
            foto_data = base64.b64encode(foto.read())
            partner.write({'image_1920': foto_data})

        # Ganti password (hanya kalau diisi dan cocok)
        password_baru = post.get('password_baru')
        password_konfirmasi = post.get('password_konfirmasi')
        if password_baru and password_baru == password_konfirmasi:
            request.env.user.sudo()._change_password(password_baru)
            # Logout lalu arahkan ke login — ini cara paling aman di Odoo 17
            request.session.logout(keep_db=True)
            return request.redirect('/web/login?message=Password+berhasil+diubah+silakan+login+ulang')
        # Redirect dengan pesan sukses
        return request.redirect('/edit-profil?saved=1')