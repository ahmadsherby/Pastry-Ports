# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    auto_validate_delivery = fields.Boolean("Auto Validate Delivery")
    auto_create_invoice = fields.Boolean("Auto Create Invoice")
    auto_validate_invoice = fields.Boolean("Auto Validate Invoice")
    auto_reconcile_invoice = fields.Boolean("Auto Reconcile Invoice")




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)

    auto_validate_delivery = fields.Boolean("Auto Validate Delivery", default=lambda self: self.env.user.company_id.auto_validate_delivery)
    auto_create_invoice = fields.Boolean("Auto Create Invoice", default=lambda self: self.env.user.company_id.auto_create_invoice)
    auto_validate_invoice = fields.Boolean("Auto Validate Invoice", default=lambda self: self.env.user.company_id.auto_validate_invoice)
    auto_reconcile_invoice = fields.Boolean("Auto Reconcile Invoice", default=lambda self: self.env.user.company_id.auto_reconcile_invoice)
    

    @api.model
    def create(self, vals):
        if 'company_id' in vals and 'auto_validate_delivery' in vals:
            self.env.user.company_id.write({'auto_validate_delivery':vals['auto_validate_delivery']})

        if 'company_id' in vals and 'auto_create_invoice' in vals:
            self.env.user.company_id.write({'auto_create_invoice':vals['auto_create_invoice']})

        if 'company_id' in vals and 'auto_validate_invoice' in vals:
            self.env.user.company_id.write({'auto_validate_invoice':vals['auto_validate_invoice']})

        if 'company_id' in vals and 'auto_reconcile_invoice' in vals:
            self.env.user.company_id.write({'auto_reconcile_invoice':vals['auto_reconcile_invoice']})


        res = super(ResConfigSettings, self).create(vals)
        return res
