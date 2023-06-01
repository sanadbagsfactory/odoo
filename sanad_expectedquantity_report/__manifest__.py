# -*- coding: utf-8 -*-
{
    'name': "sanad Expected Quantity Report",

    'summary': """This module is all about purchase report of expected qty""",

    'description': """In this module we are printing expected quantity of purchase line
    """,

    'author': "Cognetive Force",

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report.xml',
        'report/report_temp.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
