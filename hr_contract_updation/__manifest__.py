# -*- coding: utf-8 -*-
{
    'name': "Telenoc Hr Contract",
    'summary': """
        Hr Contract""",
    'description': """
        Hr Contract
    """,
    'author': "Magdy, helcon",
    'website': "https://telenoc.org",
    'category': 'hr',
    'version': '0.1',
    'depends': ['hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_employee_contract_setting.xml',
    ],
}
