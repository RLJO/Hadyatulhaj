# -*- coding: utf-8 -*-
{
    'name': "ncss purchase order restriction",
    'summary': """
        Add restrictions and level of approval on purchase order""",
    'description': """
        Add restrictions and level of approval on purchase order
    """,
    'author': "Magdy,TeleNoc",
    'website': "https:www.telenoc.org",
    'category': 'purchase',
    'version': '0.13',
    'depends': ['base', 'purchase'],
    'data': [
        'security/security.xml',
        'views/views.xml',
    ],
}
