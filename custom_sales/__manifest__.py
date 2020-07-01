# -*- coding: utf-8 -*-
{
    'name': "Custom sales",
    'summary': 'Custom sales',
    'category': 'Sale',
    'version': '13.0.1.0.1',
    'description': """
        Custom sales
    """,
    'author': "Mr. Warrag , TeleNoc",
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/sales_report_view.xml',
        'view/res_config_settings_views.xml',
        'wizards/clean_data_view.xml',
    ],
}
