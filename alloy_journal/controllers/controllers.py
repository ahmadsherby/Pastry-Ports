# -*- coding: utf-8 -*-
from odoo import http

# class AlloyJournal(http.Controller):
#     @http.route('/alloy_journal/alloy_journal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alloy_journal/alloy_journal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alloy_journal.listing', {
#             'root': '/alloy_journal/alloy_journal',
#             'objects': http.request.env['alloy_journal.alloy_journal'].search([]),
#         })

#     @http.route('/alloy_journal/alloy_journal/objects/<model("alloy_journal.alloy_journal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alloy_journal.object', {
#             'object': obj
#         })