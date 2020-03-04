# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.move"

    employee=fields.Many2one("hr.employee","Employee",compute="employee_hournal_view")
    # employee_name=fields.Char()

    @api.one
    def employee_hournal_view(self):
        self.ensure_one()
        self.employee=self.line_ids[0].x_studio_field_n0ak7
        # self.employee_name=self.employee.name


#class AccountMoveLine(models.Model):
 #   _inherit = "account.move.line"

  #  employee = fields.Many2one("hr.employee", "Employee")





