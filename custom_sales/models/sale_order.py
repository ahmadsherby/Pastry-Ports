# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):

        if not self.fully_paied:
            raise UserError(_('Please receive all the amount from customr first'))
        res = super(SaleOrder, self).action_confirm()

        if self.env.user.company_id.auto_validate_delivery == True:
            if res:
                self = self.with_context(validate_from_sale=True)
                self.picking_ids.button_validate()

        if self.env.user.company_id.auto_create_invoice == True:
            if res:
                self._create_invoices()

        if self.env.user.company_id.auto_validate_invoice == True:
            if res:
                for invoice in self.invoice_ids:
                    invoice.action_post()

        if self.env.user.company_id.auto_reconcile_invoice == True:
            if res:
                for invoice in self.invoice_ids:
                    payment_obj = self.env['account.payment'].search([
                        ('payment_type', '=', "inbound"),
                        ('partner_type', '=', "customer"),
                        ('partner_id', '=', self.partner_id.id),
                    ])

                    if payment_obj:
                        for pay in payment_obj:
                            if not pay.move_reconciled:
                                for line in pay.move_line_ids:
                                    if line.account_id == self.partner_id.property_account_receivable_id and pay.partner_id == self.partner_id:
                                        invoice.js_assign_outstanding_line(line.id)

        return res
