# -*- coding: utf-8 -*-
{
    'name': 'Emprunt Module',
    'version': '17.0',
    'author': 'Your Company',
    'category': 'Service',
    'license': 'LGPL-3',
    'sequence': 1,
    'website': 'https://yourcompanywebsite.com',
    'description': """
    This module extends the functionality of the Engagement module to manage Emprunt (loans) related functionalities.
    """,
    'depends': ['engagement'],  # Depend on the 'engagement' module
    'data': [
        'data/sequence.xml',
        'views/emprunt_views.xml',
        'views/menus.xml',
        'wizard/create_emprunt_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
