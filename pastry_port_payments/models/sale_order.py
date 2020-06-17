# -*- coding: utf-8 -*-

from odoo import models, fields, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_ref = fields.Char('Reference')
    sale_order_id = fields.Many2one('sale.order')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_ref = fields.Char('Reference')
    total_payments = fields.Float('Total Payments', compute='get_total_payments')

    def get_total_payments(self):
        for record in self:
            payment = self.env['account.payment']
            payment_obj = payment.search([('sale_order_id', '=', record.id)])
            total = 0.0
            if payment_obj:
                total = sum([line.amount for line in payment_obj])
            record.total_payments = total

    def action_get_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Payment',
            'res_model': 'account.payment',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'target': 'current',
        }

    def action_register_payment(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return ''
        print(self.env.context)
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment',
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_account_payment_invoice_form').id,
            'context': self.env.context,
            # 'context': {'default_communication': 'test'},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def action_invoice_register_payment(self):
        return self.with_context(active_ids=self.ids, default_payment_type='inbound',
                                 default_communication=self.name,
                                 default_sale_order_id=self.id,
                                 default_payment_ref=self.payment_ref,
                                 default_partner_id=self.partner_id.id,
                                 active_model='sale.order', active_id=self.id)\
            .action_register_payment()
