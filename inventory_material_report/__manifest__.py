# -*- coding: utf-8 -*-
{
    'name': "Inventory Material Report",

    'summary': """This module is all about inventory raw material report""",

    'description': """This module is all about inventory raw material report
    """,

    'author': "CognetiveForce",

    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report.xml',
        'report/material_receiving_voucher.xml',
        'report/consolidated_stock_report.xml',
    ],
}
