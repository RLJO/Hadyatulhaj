# -*- coding: utf-8 -*-
{
    'name': 'ncss_mandate_passenger',
    'version': '13.0.1',
    'summary': 'ncss_mandate_passenger',
    'category': 'ncss_mandate_passenger',
    'author': 'Magdy,TeleNoc',
    'description': """
    crm_project
    """,
    'depends': ['base', 'mail', 'hr', 'hr_attendance'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mandate_passenger_sequence.xml',
        'views/hr_department.xml',
        'views/mandate_passenger.xml',
    ]
}
