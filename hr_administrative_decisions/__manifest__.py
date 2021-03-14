# -*- coding: utf-8 -*-
{
    'name': "Hr Administrative Decisions",
    'summary': """
        Hr Administrative Decisions""",
    'description': """
        Hr Administrative Decisions
    """,
    'author': "Magdy, helcon",
    'website': "https://telenoc.org",
    'category': 'hr',
    'version': '0.1',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/administrative_decisions_view.xml',
        'views/hr_employee.xml',
        'report/administrative_decision.xml',
    ],
}
