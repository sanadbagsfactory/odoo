# -*- coding: utf-8 -*-

{
    'name': 'RFQ_Comparison Dashboard',
    'version': '16.0.0',
    'depends': ['base','purchase'],
    'category': 'purchases',
    'author': 'Preciseways',
    'website': "http://www.preciseways.com",
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/purchase_comparison_view.xml',
        'views/res_config_setting_view.xml',
        'report/purchase_comparion_report.xml',
        'report/report_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pways_quotations_comparison_dashboard/static/src/js/rfq_comp_dashboard.js',
            'pways_quotations_comparison_dashboard/static/src/css/rfq_dashboard.css',
            'pways_quotations_comparison_dashboard/static/src/xml/rfq_comp_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'price': 35.0,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
}
