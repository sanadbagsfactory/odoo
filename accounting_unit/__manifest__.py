# -*- coding: utf-8 -*-
{
    'name': "accounting_unit",

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
    'depends': ['base', 'account', 'sale', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inherited_account_move.xml',
        'views/templates.xml',
        'views/inherited_res_company.xml',
        'views/inherit_sale_order.xml',
        'views/inherit_purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
