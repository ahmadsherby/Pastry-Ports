# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CleanData(models.TransientModel):
    _name = 'clean.data'
    _description = 'Clean Data'
    
    def check_and_delete(self,table):
        sql = """SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND   table_name = '%s');""" % table
        self._cr.execute(sql)
        res = self._cr.dictfetchall()
        res = res and res[0] or {}
        if res.get('exists', False):
            sql = """delete from %s ;""" % table
            self._cr.execute(sql)
            

    def clean_data(self):

        account_partial_reconcile = "account_partial_reconcile"
        self.check_and_delete(account_partial_reconcile)


        sql = "delete from account_move_line where move_id in (select id from account_move where type != 'entry')"
        self._cr.execute(sql)
        sql = "delete from account_move where type != 'entry'"
        self._cr.execute(sql)
        

        

        sq = "stock_quant"
        sml = "stock_move_line"
        sm = "stock_move"
        sp = "stock_picking"

        self.check_and_delete(sq)
        self.check_and_delete(sml)
        self.check_and_delete(sm)
        self.check_and_delete(sp)


        pol = 'purchase_order_line'
        po = 'purchase_order'

        self.check_and_delete(pol)
        self.check_and_delete(po)

        sol = "sale_order_line"
        so = "sale_order"

        self.check_and_delete(sol)
        self.check_and_delete(so)

        sol_pos = "pos_order_line"
        so_pos = "pos_order"

        self.check_and_delete(sol_pos)
        self.check_and_delete(so_pos)

        pos_session = "pos_session"

        self.check_and_delete(pos_session)
        

        pos_payment = "pos_payment"
        account_payment = "account_payment"
        at = "account_tax"
        
        self.check_and_delete(pos_payment)
        self.check_and_delete(account_payment)
        self.check_and_delete(at)
        
        


        