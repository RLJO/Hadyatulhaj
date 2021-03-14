# -*- coding: utf-8 -*-
{
    'name': 'hr_employee_letter',
    'version' : '12.0.1',
    'summary': 'hr_employee_letter',
    'category': 'hr',
    'author' : 'Magdy,TeleNoc',
    'description': """
    hr_employee_letter
    """,
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_letter.xml',
        'report/letter_report.xml'
    ]
}
