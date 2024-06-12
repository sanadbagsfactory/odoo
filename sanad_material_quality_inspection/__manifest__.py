# -*- coding: utf-8 -*-
{
    'name': "sanad Material Quality Inspection",

    'summary': """This module is all about quality control """,

    'description': """
    In this module we are adding sections in tab form in quality point for product quality control
    """,

    'author': "Cognetive Force",


    'depends': ['base', 'quality_control'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
