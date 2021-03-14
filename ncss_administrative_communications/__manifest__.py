# -*- coding: utf-8 -*-
{
    'name': 'Administrative Communication',
    'version': '13.0.1',
    'summary': 'AdministrativeCommunication',
    'category': 'contact',
    'author': 'Magdy,TeleNoc',
    'description': """
    AdministrativeCommunication
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/administrative_communications_view.xml',
        'views/res_users.xml',
        'report/print_barcode_report.xml',
        'report/administrative_communication_report.xml',
    ]
}
