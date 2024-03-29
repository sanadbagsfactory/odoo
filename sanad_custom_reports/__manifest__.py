# -*- coding: utf-8 -*-
{
    'name': "sanad_custom_reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "M.Rizwan",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sanad_overall', 'sale', 'account'],

    # always loaded
    'data': [
        'report/reports.xml',
        # 'report/purchase_quote_print_template.xml',
        'report/po_print_template.xml',
        'report/invoices_print_template.xml',
        'data/test_template.xml',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    'assets': {
        'web.report_assets_common': [
            "sanad_custom_reports/static/src/css/report_styles.css"
        ],
    },
}
