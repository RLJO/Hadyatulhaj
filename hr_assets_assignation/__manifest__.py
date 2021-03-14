# -*- coding: utf-8 -*-
{
    'name': 'hr_assets_assignation',
    'version': '13.0.1',
    'summary': 'asset_account_request',
    'category': 'hr',
    'author': 'Magdy,TeleNoc',
    'description': """
    asset_account_request
    """,
    'depends': ['base', 'mail', 'hr', 'fleet', 'account_asset'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/wizard_reason.xml',
        'views/asset_request_cron.xml',
        'views/asset_request_sequence.xml',
        'views/asset_account_request.xml',
        'report/employee_assets_report.xml',
        'report/department_clearance_report.xml',
    ]
}
