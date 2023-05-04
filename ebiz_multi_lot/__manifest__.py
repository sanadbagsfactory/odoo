# -*- coding: utf-8 -*-
{
    'name': "EBIZ Multi Lot",

    'summary': """This module is all about multi lot number selection in stock picking""",

    'description': """
    In this module we are selecting multi lot number and assign in stock picking line 
    """,
    'depends': ['base', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/lot_assign_view.xml',
    ],
}
