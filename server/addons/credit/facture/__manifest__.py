# -*- coding: utf-8 -*-
{
    'name': 'ITDEV Engagement',
    'version': '17.0',
    'author': 'ITDS',
    'category': 'Service',
    'license': 'LGPL-3',
    'sequence': 1,
    'website': 'site',
    'description': """
    """,

    'depends': ['base', 'mail', 'engagement'],
    'images' : ['static/description/icon.png', ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/facture.xml',
        'views/convention.xml',
        'views/menu.xml',

    ],
    'demo': [],
    'test': [],

    'installable': True,
    'application': False,
    'auto_install': False,
}
