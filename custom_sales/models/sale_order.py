# -*- coding: utf-8 -*-

from odoo import models, fields, _



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):

        res = super(SaleOrder, self).action_confirm()

        if self.env.user.company_id.auto_validate_delivery == True:
            if res:
                self = self.with_context(validate_from_sale=True)
                self.picking_ids.button_validate()
        return res
