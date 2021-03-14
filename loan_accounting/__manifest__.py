# -*- coding: utf-8 -*-

{
    'name': 'Loan Accounting',
    'version': '13.0.1.0.0',
    'summary': 'Loan Accounting',
    'description': """
        Create accounting entries for loan requests.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': "TeleNoc Team, Eng. Ahmed Sherby",
    'company': 'TeleNoc',
    'maintainer': 'TeleNoc',
    'website': "https://www.TeleNoc.org",
    'depends': [
        'base', 'hr_payroll', 'hr', 'account', 'loan',
    ],
    'data': [
        'views/hr_loan_config.xml',
        'views/hr_loan_acc.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
