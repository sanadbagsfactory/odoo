{
    'name': 'Multiple Branch(Unit) Operation Setup for All Applications Odoo/odoo',
    'version': '16.0',
    'category': 'Sales',
    'summary': 'Multiple Branch/Unit Operation on Sales, Purchases, Accounting/Invoicing,'
               ' Voucher, Payment, Accounting Reports for single company',
    "description": """
    Multiple Unit operation management for single company Multiple Branch management for single company multiple
    operation for single company branching company in odoo multiple store multiple company in odoo Branch for Sales 
    Branch for Purchase Branch for all Branch for Accounting Branch for invoicing Branch for Payment order Branch for
    point of sales Branch for voucher Branch for All Accounting reports Branch Accounting filter Branch for warehouse
    branch for sale stock branch for location.

    """,
    'author': 'M.Rizwan',
    'license': 'LGPL-3',
    'website': 'http://www.cognitiveforce.cloud',
    'depends': ['base', 'sale_management', 'purchase', 'stock', 'account', 'purchase_stock', 'account_accountant'],
    'data': [
        'security/branch_security.xml',
        'security/ir.model.access.csv',
        'views/res_branch_view.xml',
        'views/inherited_res_users.xml',
        'views/inherited_sale_order.xml',
        'views/inherited_stock_picking.xml',
        'views/inherited_stock_move.xml',
        'views/inherited_account_invoice.xml',
        'views/inherited_purchase_order.xml',
        'views/inherited_stock_warehouse.xml',
        'views/inherited_stock_location.xml',
        'views/inherited_account_bank_statement.xml',
        'wizard/inherited_account_payment.xml',
        # 'views/inherited_stock_inventory.xml',
        'views/inherited_product.xml',
        'views/inherited_partner.xml',
        'views/inherited_account_payment_wizard_view.xml',
        'views/inherited_account_journal.xml',
        'views/inherited_account_analytic.xml',

    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "images": ['static/description/Banner.png'],
    # 'post_init_hook': 'post_init_hook',
}
