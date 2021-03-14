# -*- coding: utf-8 -*-
{
    'name': 'hr_eos_computation_configuration',
    'version': '13.0.1',
    'summary': 'hr_eos_computation_configuration',
    'description': """
        hr_eos_computation_configuration
    """,
    'category': 'hr',
    'author': 'Magdy,TeleNoc',
    'depends': ['base', 'mail', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_configuration_setting.xml',
    ]
}
