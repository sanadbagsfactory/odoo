# -*- coding: utf-8 -*-
# from odoo import http


# class ContactCustomization(http.Controller):
#     @http.route('/contact_customization/contact_customization', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contact_customization/contact_customization/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contact_customization.listing', {
#             'root': '/contact_customization/contact_customization',
#             'objects': http.request.env['contact_customization.contact_customization'].search([]),
#         })

#     @http.route('/contact_customization/contact_customization/objects/<model("contact_customization.contact_customization"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contact_customization.object', {
#             'object': obj
#         })
