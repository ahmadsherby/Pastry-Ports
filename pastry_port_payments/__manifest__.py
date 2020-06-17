# -*- coding: utf-8 -*-
{
    'name': "Pastry Port Payments",
    'summary': 'Pastry Port Payments',
    'category': 'Sale',
    'version': '13.0.1.0.1',
    'description': """
        Pastry Port Payments
    """,
    'author': "Magdy, TeleNoc",
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'report/sales_report_view.xml',
    ],
}
