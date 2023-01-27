# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta


class NewspaperReportDetails(models.AbstractModel):
    _name = 'report.pways_quotations_comparison_dashboard.report_rfq'
    _description = "comparison rfq"

    @api.model
    def _get_report_values(self, docids, data=None):
        active_id = docids[0]
        comparison_id = self.env['purchase.comparison'].browse(active_id)
        price_id = comparison_id.get_purchase_line_data('by_price', comparison_id.id)
        date_id = comparison_id.get_purchase_line_data('by_date', comparison_id.id)
        miminimum_price = price_id.get('total')
        miminimum_date = date_id.get('total')
        miminimum_price_id = False
        miminimum_date_id = False
        price_order_line_ids_data = []
        for min_date in miminimum_date:
            if min_date['option'] == 'by_date':
                miminimum_date_id = min_date.get('id')

        for min_price in miminimum_price:
            if min_price['option'] == 'by_price':
                miminimum_price_id = min_price.get('id')

        purchase_line_min_price_ids = self.env['purchase.order.line'].browse(date_id.get('price_order_line_ids'))
        purchase_line_min_date_ids = self.env['purchase.order.line'].browse(date_id.get('date_order_line_ids'))
        minimum_price_ll_id = self.env['purchase.order'].browse(miminimum_price_id)
        minimum_date_ll_id = self.env['purchase.order'].browse(miminimum_date_id)
        return {'minimum_price_id': minimum_price_ll_id,
                'minimum_date_id': minimum_date_ll_id,
                'user_name': comparison_id.user_id.name,
                'start_date': comparison_id.ordering_date.strftime("%Y-%m-%d") if comparison_id.ordering_date else '',
                'end_date': comparison_id.end_date.strftime("%Y-%m-%d") if comparison_id.end_date else '',
                'name': comparison_id.name,
                'purchase_line_min_price_ids': purchase_line_min_price_ids,
                'purchase_line_min_date_ids': purchase_line_min_date_ids,
                }
