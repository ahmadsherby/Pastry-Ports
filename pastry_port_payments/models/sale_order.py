# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'out_receipt': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
    'in_receipt': 'supplier',
}


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_ref = fields.Char('Reference')
    sale_order_id = fields.Many2one('sale.order')

    # @api.model
    # def default_get(self, default_fields):
    #     print("++++++++++++   ", default_fields)
    #     # rec = super(AccountPayment, self).default_get(default_fields)
    #     active_ids = self._context.get('active_ids') or self._context.get('active_id')
    #     active_model = self._context.get('active_model')
        

    #     if active_model == 'sale.order':
    #         # if 'move_line_ids' not in default_fields:
    #         print(".............................", self._context.get('default_amount'))
    #         rec = super(AccountPayment, self).default_get(default_fields)
    #         rec.update({
    #             'currency_id': self._context.get('default_currency_id'),
    #             'payment_type': 'inbound',
    #             'partner_id': self._context.get('default_partner_id'),
    #             'partner_type': 'customer',
    #             'communication': self._context.get('default_communication'),
    #             'amount': abs(self._context.get('default_amount')),
    #         })
    #         print(";;;; ", rec)
    #         return rec

    #     print("vvvvvvvvvvvvvvv", active_model)
        
    #     # Check for selected invoices ids
    #     rec = super(AccountPayment, self).default_get(default_fields)
    #     print("cccccccc")
    #     # print(rec)
    #     if not active_ids or active_model != 'account.move':
    #         return rec
    #         # if active_model == 'sale.order':
    #         #     if 'move_line_ids' not in default_fields:
    #         #         print(".............................")
    #         #         print("mmmmmmmm   ", rec)
    #         #         # rec.update({
    #         #         #     'currency_id': self._context.get('default_currency_id'),
    #         #         #     'payment_type': 'inbound',
    #         #         #     'partner_id': self._context.get('default_partner_id'),
    #         #         #     'partner_type': 'customer',
    #         #         #     'communication': self._context.get('default_communication'),
    #         #         #     'amount': abs(self._context.get('default_amount')),
    #         #         # })
    #         #         print(";;;; ", rec)
    #         #         return rec
    #         #     else:
    #         #         print("zzzzzzzzzzzzzzz")
    #         #         print("mmmmmmmm  nnnnnnnnnnnnn ", rec)
    #         #         rec.update({
    #         #             'currency_id': self._context.get('default_currency_id'),
    #         #             'payment_type': 'inbound',
    #         #             'partner_id': self._context.get('default_partner_id'),
    #         #             'partner_type': 'customer',
    #         #             'communication': self._context.get('default_communication'),
    #         #             'amount': abs(self._context.get('default_amount')),
    #         #         })
    #         #         print(";;;; jjjj", rec)
    #         #         return rec
    #     print("7777777")
    #     print("mmmmmmmm  nnnnnnnnnnnnn cccccccccccccccc", rec)
    #     invoices = self.env['account.move'].browse(active_ids).filtered(lambda move: move.is_invoice(include_receipts=True))

    #     # Check all invoices are open
    #     if not invoices or any(invoice.state != 'posted' for invoice in invoices):
    #         raise UserError(_("You can only register payments for open invoices"))
    #     # Check if, in batch payments, there are not negative invoices and positive invoices
    #     dtype = invoices[0].type
    #     for inv in invoices[1:]:
    #         if inv.type != dtype:
    #             if ((dtype == 'in_refund' and inv.type == 'in_invoice') or
    #                     (dtype == 'in_invoice' and inv.type == 'in_refund')):
    #                 raise UserError(_("You cannot register payments for vendor bills and supplier refunds at the same time."))
    #             if ((dtype == 'out_refund' and inv.type == 'out_invoice') or
    #                     (dtype == 'out_invoice' and inv.type == 'out_refund')):
    #                 raise UserError(_("You cannot register payments for customer invoices and credit notes at the same time."))

    #     amount = self._compute_payment_amount(invoices, invoices[0].currency_id, invoices[0].journal_id, rec.get('payment_date') or fields.Date.today())
    #     rec.update({
    #         'currency_id': invoices[0].currency_id.id,
    #         'amount': abs(666),
    #         'payment_type': 'inbound' if amount > 0 else 'outbound',
    #         'partner_id': invoices[0].commercial_partner_id.id,
    #         'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
    #         'communication': invoices[0].invoice_payment_ref or invoices[0].ref or invoices[0].name,
    #         'invoice_ids': [(6, 0, invoices.ids)],
    #     })
    #     print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,   ",rec)
    #     return rec

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_ref = fields.Char('Reference')
    total_payments = fields.Float('Total Payments', compute='get_total_payments')
    fully_paied = fields.Boolean(string='fully_paied', default=False)
    def get_total_payments(self):
        for record in self:
            payment = self.env['account.payment']
            payment_obj = payment.search([('sale_order_id', '=', record.id)])
            total = 0.0
            if payment_obj:
                total = sum([line.amount for line in payment_obj])
            record.total_payments = total

            if record.total_payments >= record.amount_total:
                record.fully_paied = True

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
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def action_invoice_register_payment(self):
        return self.with_context(active_ids=self.ids, 
                                 default_payment_type='inbound',
                                 default_currency_id=self.currency_id.id,
                                 default_communication=self.name,
                                 default_sale_order_id=self.id,
                                 default_payment_ref=self.payment_ref,
                                 default_partner_id=self.partner_id.id,
                                 default_amount=self.amount_total,
                                 active_model='sale.order', 
                                 active_id=self.id).action_register_payment()
