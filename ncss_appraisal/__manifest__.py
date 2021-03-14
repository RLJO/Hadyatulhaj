# -*- coding: utf-8 -*-
{
    'name': 'NCSS Appraisal',
    'version': '13.0.1',
    'summary': 'NCSS Appraisal',
    'category': 'hr',
    'author': 'Magdy,TeleNoc',
    'description': """
    NCSS Survey
    """,
    'depends': ['base', 'mail', 'hr_appraisal'],
    'demo': [
        'demo/demo.xml'
    ],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/sequence.xml',
        'views/hr_employee_appraisal.xml',
        'views/hr_appraisal.xml',
        # 'report/print_barcode_report.xml',
        # 'report/administrative_communication_report.xml',
    ]
}
