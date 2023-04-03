# -*- coding: utf-8 -*-
{
    'name': "sanad_overall",

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
    'depends': ['base', 'hr', 'account', 'purchase', 'stock', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_move_view.xml',
        'views/account_account_view.xml',
        'views/department_document_type_view.xml',
        'views/hr_department_view.xml',
        'views/inherited_product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
