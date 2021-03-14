# -*- coding: utf-8 -*-

{
    'name': 'Employee Documents',
    'version': '13.0.2.0.0',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': """Manages Employee Related Documents with Expiry Notifications.""",
    'category': 'Generic Modules/Human Resources',
    'author': 'TeleNoc Team, Eng. Ahmed Sherby',
    'company': 'TeleNoc',
    'maintainer': 'TeleNoc',
    'website': "https://www.TeleNoc.org",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_document_view.xml',
        'views/document_type_view.xml',
        'views/hr_document_template.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
