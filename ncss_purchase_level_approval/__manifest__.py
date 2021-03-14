# -*- coding: utf-8 -*-
{
    'name': "Ncss Purchase Level Approval",
    'summary': """Purchase Level Approval""",
    'description': """Purchase Level Approval""",
    'author': "Magdy,TeleNoc",
    'website': "https://telenoc.org",
    'category': 'purchase',
    'version': '0.13',
    'depends': ['base', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/purchase_order_setting.xml',
        'views/purchase_order.xml',
        'report/purchase_order_report.xml',
    ],
}
