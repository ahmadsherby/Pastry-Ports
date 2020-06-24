# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    auto_validate_delivery = fields.Boolean("Auto Validate Delivery")




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)

    auto_validate_delivery = fields.Boolean("Auto Validate Delivery", default=lambda self: self.env.user.company_id.auto_validate_delivery)
    

    @api.model
    def create(self, vals):
        if 'company_id' in vals and 'auto_validate_delivery' in vals:
            self.env.user.company_id.write({'auto_validate_delivery':vals['auto_validate_delivery']})
        res = super(ResConfigSettings, self).create(vals)
        return res
