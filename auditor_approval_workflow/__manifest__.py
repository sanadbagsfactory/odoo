# -*- coding: utf-8 -*-
{
    'name': "auditor_approval_workflow",

    'summary': """
        Auditor Approval workflow: The system should book VAT amount in the VAT Clearing Account in Purchases. After the auditor approves when it moves to Input Account, or in case of rejection, it moves to the Expense Account.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "M.Rizwan",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_inherited_view.xml',
        'views/res_config_inherited.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
