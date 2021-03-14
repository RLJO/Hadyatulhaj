# -*- coding: utf-8 -*-

{
    'name': 'Official Announcements',
    'version': '13.0.2.0.0',
    'summary': """Managing Official Announcements""",
    'description': 'This module helps you to manage hr official announcements',
    'category': 'Generic Modules/Human Resources',
    'author': 'TeleNoc',
    'company': 'TeleNoc',
    'website': "http://www.TeleNoc.org",
    'depends': ['base', 'hr','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/reward_security.xml',
        'views/hr_announcement_view.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
