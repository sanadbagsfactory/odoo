# -*- coding: utf-8 -*-
{
    'name': "purchase_tender_management",

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
    'depends': ['base', 'purchase', 'purchase_requisition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/reports.xml',
        'report/rfq_print_template.xml',
        'data/email_template.xml',
        'data/sequence.xml',
        'views/inherited_purchase_requisition.xml',
        'views/inherited_purchase_order.xml',
        'views/purchase_tender_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
