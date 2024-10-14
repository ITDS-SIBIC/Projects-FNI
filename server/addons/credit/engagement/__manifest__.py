# -*- coding: utf-8 -*-
{
    'name': 'credit',
    'version': '17.0',
    'author': ' ITDS',
    'category': 'Service',
    'license': 'LGPL-3',
    'sequence': 1,
    'website': 'site',
    'description': """
    """,

    'depends': ['base', 'mail', ],
    'images' : ['static/description/icon.png', ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/convention.xml',

        'views/client.xml',
        'wizard/create_avenant_CN.xml',
        'wizard/create_enr_CN.xml',

        'views/menu.xml',
    ],
    'demo': [],
    'test': [],

    'installable': True,

    'application': True,
    'auto_install': False,
}
