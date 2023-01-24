# -*- coding: utf-8 -*-
{
    'name': "No Expire DB 14",

    'summary': """
        Database Will Never Expire V14""",

    'description': """
        Database Will Never Expire V14
    """,

    'author': "M.Rizwan",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'DB',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'views/res_partner_view.xml',
    ],

}
