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
        'views/contrat.xml',


        'views/AvenantPret.xml',
        'wizard/create_avenant.xml',
        'wizard/create_avenant_pret_wizard_view.xml',
        'views/menu.xml',
        'views/pret.xml',
        'views/rubrique.xml',


    ],
    'demo': [],
    'test': [],

    'installable': True,
    'application': False,
    'auto_install': False,
}
