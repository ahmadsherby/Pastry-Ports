# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models

ORDER_TYPE = [
    ('pos_order', 'Point of Sale Order'),
    ('sale_order', 'Sale Order')
]

ORDER_STATE = [
    ('draft', 'New/ Quotation'),
    ('sent', 'Quotation Sent'),
    ('sale', 'Sales Order'),
    ('done', 'Posted/ Sales Done'),
    ('invoiced', 'Invoiced'),
    ('paid', 'Paid'),
    ('cancel', 'Cancelled')
]


class SalesReport(models.Model):
    _name = "sales.report.overall"
    _description = "Overall Sales Transactions"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    order_type = fields.Selection(ORDER_TYPE, 'Order Type', readonly=True)
    name = fields.Char('Order Reference', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    qty = fields.Float('Qty', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    price_total = fields.Float('Total', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    nbr = fields.Integer('Number of Lines', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly=True)
    state = fields.Selection(ORDER_STATE, string='Status', readonly=True)

    def _sale_order_query(self):
        query_str = """
        WITH currency_rate as (%s)
        SELECT 
            MAX(sol.id) AS id,
            'sale_order' AS order_type,
            COUNT(*) AS nbr,
            so.date_order AS date,
            so.partner_id AS partner_id,
            sol.product_id AS product_id,
            ps.product_tmpl_id AS product_tmpl_id,
            sum(sol.product_uom_qty / u.factor * u2.factor) AS qty,
            sum(sol.price_subtotal / COALESCE(cr.rate, 1.0)) AS price_subtotal,
            sum(sol.price_total / COALESCE(cr.rate, 1.0)) AS price_total,
            pts.categ_id AS categ_id,
            so.user_id AS user_id,
            so.company_id AS company_id,
            so.state AS state,
            so.pricelist_id AS pricelist_id,
            so.name AS name
        FROM
            sale_order_line sol
            join sale_order so on (sol.order_id=so.id)
            join res_partner partner on so.partner_id = partner.id
            left join product_product ps on (sol.product_id=ps.id)
                left join product_template pts on (ps.product_tmpl_id=pts.id)
            left join uom_uom u on (u.id=sol.product_uom)
            left join uom_uom u2 on (u2.id=pts.uom_id)
            left join product_pricelist pps on (so.pricelist_id = pps.id)
            left join currency_rate cr on (cr.currency_id = pps.currency_id and
            cr.company_id = so.company_id and
            cr.date_start <= coalesce(so.date_order, now()) and
            (cr.date_end is null or cr.date_end > coalesce(so.date_order, now())))
        GROUP BY    
            sol.id,
            sol.product_id,
            ps.product_tmpl_id,
            so.partner_id,
            so.date_order,
            so.name,
            so.state,
            pts.categ_id,
            so.user_id,
            so.company_id,
            so.pricelist_id
        """ % self.env['res.currency']._select_companies_rates()

        return query_str

    def _pos_order_query(self):
        query_str = """
        SELECT 
            - MAX(pol.id) AS id,
            'pos_order' AS order_type,
            COUNT(*) AS nbr,
            po.date_order AS date,
            po.partner_id AS partner_id,
            pol.product_id AS product_id,
            pr.product_tmpl_id AS product_tmpl_id,
            SUM(pol.qty) AS qty,
            SUM(pol.qty * pol.price_unit) AS price_subtotal,
            SUM((pol.qty * pol.price_unit) * (100 - pol.discount) / 100) AS price_total,
            ptp.categ_id AS categ_id,
            po.user_id AS user_id,
            po.company_id AS company_id,
            po.state AS state,
            po.pricelist_id AS pricelist_id,
            po.name AS name
        FROM
            pos_order_line AS pol
            LEFT JOIN pos_order po ON (pol.order_id = po.id)
            LEFT JOIN product_product pr ON (pol.product_id=pr.id)
            LEFT JOIN product_template ptp ON (pr.product_tmpl_id=ptp.id)
        GROUP BY 
            pol.id,
            pol.product_id,
            pr.product_tmpl_id,
            po.partner_id,
            po.date_order,
            po.name,
            po.state,
            ptp.categ_id,
            po.user_id,
            po.company_id,
            po.pricelist_id
        """
        return query_str

    #@api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            UNION  
            %s
            )""" % (self._table, self._sale_order_query(), self._pos_order_query()))
