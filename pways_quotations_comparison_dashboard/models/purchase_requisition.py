# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from calendar import monthrange
from datetime import date, timedelta
import datetime, calendar
import pytz

class PurchaseOrder(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def get_purchase_line_data(self, option, reqisition_id=None):
        min_price_total = []
        min_delivery_date = []
        
        record = []
        total = []
        partner_ids = []
        price_order_line_ids = []
        date_order_line_ids = []

        min_total_vendor = 0
        min_delivery_vendor = 0
        
        
        tendor_id = self.env['purchase.requisition'].search([('id', '=', reqisition_id)], limit=1)
        purchase_ids = self.env['purchase.order'].search([('requisition_id', '=', tendor_id.id)]).filtered(lambda x: len(x.order_line.ids) > 0)
        product_ids = self.env['purchase.order.line'].search([('order_id', 'in', purchase_ids.ids)]).mapped('product_id')
        
        for purchase_id in purchase_ids:
            min_price_total.append(sum(purchase_id.order_line.mapped('price_unit')))
            min_delivery_date.append(min(purchase_id.order_line.mapped('date_planned')).date())

        for order in purchase_ids:
            if min(min_price_total) == sum(order.order_line.mapped('price_unit')):
                min_total_vendor = order.partner_id
            if (min(min_delivery_date)) == min(order.order_line.mapped('date_planned')).date():
                min_delivery_vendor = order.partner_id

        order_line_ids = purchase_ids.mapped('order_line')
        product_ids = order_line_ids.mapped('product_id')
        for product in product_ids:
            order_lines = order_line_ids.filtered(lambda x: x.product_id and x.product_id.id == product.id)
            min_price_order_line = min(order_lines.mapped('price_unit'))
            min_date_order_line = min(order_lines.mapped('date_planned'))
            min_price_order_line_id = order_lines.filtered(lambda x: x.price_unit and x.price_unit == min_price_order_line)
            min_date_order_line_id = order_lines.filtered(lambda x: x.date_planned and x.date_planned == min_date_order_line)
            for price_order_line in min_price_order_line_id:
                price_order_line_ids.append(price_order_line.id)
            for date_order_line in min_date_order_line_id:
                date_order_line_ids.append(date_order_line.id)

        for order in purchase_ids:
            if option =='by_price' and min_total_vendor == order.partner_id:
                partner_ids.append({
                    'option': 'by_price',
                    'id': order.partner_id.id,
                    'name': order.partner_id.name,
                })
                total.append({
                    'state': order.state,
                    'option': 'by_price',
                    'id': order.id,
                    'partner_id':order.partner_id.id,
                    'total': order.amount_total,
                    'subtotal': sum(order.order_line.mapped('price_unit')),
                    'tax': order.amount_tax,
                    'delivery_date': min(order.order_line.mapped('date_planned')).date().strftime("%d/%m/%Y"),
                })
            elif option =='by_date' and min_delivery_vendor == order.partner_id:
                partner_ids.append({
                    'option': 'by_date',
                    'id': order.partner_id.id,
                    'name': order.partner_id.name,
                })
                total.append({
                    'state': order.state,
                    'option': 'by_date',
                    'id': order.id,
                    'partner_id':order.partner_id.id,
                    'total': order.amount_total,
                    'subtotal': sum(order.order_line.mapped('price_unit')),
                    'tax': order.amount_tax,
                    'delivery_date': min(order.order_line.mapped('date_planned')).date().strftime("%d/%m/%Y"),
                })
            else:
                partner_ids.append({
                    'option': '',
                    'id': order.partner_id.id,
                    'name': order.partner_id.name,
                })
                total.append({
                    'state': order.state,
                    'option': '',
                    'id': order.id,
                    'partner_id':order.partner_id.id,
                    'total': order.amount_total,
                    'subtotal': sum(order.order_line.mapped('price_unit')),
                    'tax': order.amount_tax,
                    'delivery_date': min(order.order_line.mapped('date_planned')).date().strftime("%d/%m/%Y"),
                })

        for product_id in product_ids:
            lines=[]
            min_prize = min(self.env['purchase.order.line'].search([
                ('order_id', 'in', purchase_ids.ids), 
                ('product_id', '=', product_id.id)]).mapped('price_unit'))
            min_prize_vendor = self.env['purchase.order'].search([
                ('order_line', '=', self.env['purchase.order.line'].search([
                    ('order_id', 'in', purchase_ids.ids), 
                    ('product_id', '=', product_id.id), 
                    ('price_unit', '=', min_prize)
                    ], limit=1).id)
                ]).partner_id
            min_date = min(self.env['purchase.order.line'].search([
                ('order_id', 'in', purchase_ids.ids), 
                ('product_id', '=', product_id.id)]).mapped('date_planned'))
            min_date_vendor = self.env['purchase.order'].search([
                ('order_line', '=', self.env['purchase.order.line'].search([
                    ('order_id', 'in', purchase_ids.ids), 
                    ('product_id', '=', product_id.id), 
                    ('date_planned', '=', min_date)
                    ], limit=1).id)
                ]).partner_id
            for vendor_id in purchase_ids:
                if product_id.id in vendor_id.order_line.mapped('product_id').ids:
                    for order_line in vendor_id.order_line:
                        if order_line.product_id.id == product_id.id:
                            if option =='by_price' and min_total_vendor == vendor_id.partner_id:
                                lines.append({
                                    'option': 'by_price',
                                    'message': ('Delivery Date :' + str(order_line.date_planned)),
                                    'vendor_id': vendor_id.partner_id.id,
                                    'line_id': order_line.id,
                                    'product_id': order_line.product_id.id,
                                    'vendor_name': vendor_id.partner_id.name,
                                    'unit_price': order_line.price_unit,
                                    'qty': order_line.product_qty,
                                    'delivery_date': order_line.date_planned.date().strftime("%d/%m/%Y"),
                                    })
                            
                            elif option =='by_date' and min_delivery_vendor == vendor_id.partner_id:
                                lines.append({
                                    'option': 'by_date',
                                    'vendor_id': vendor_id.partner_id.id,
                                    'message': ('Delivery Date :' + str(order_line.date_planned)),
                                    'line_id': order_line.id,
                                    'product_id': order_line.product_id.id,
                                    'vendor_name': vendor_id.partner_id.name,
                                    'unit_price': order_line.price_unit,
                                    'qty': order_line.product_qty,
                                    'delivery_date': order_line.date_planned.date().strftime("%d/%m/%Y"),
                                    })
                            elif option =='by_line_price':
                                lines.append({
                                    'option': 'by_line_price',
                                    'vendor_id': vendor_id.partner_id.id,
                                    'message': ('Delivery Date :' + str(order_line.date_planned)),
                                    'line_id': order_line.id,
                                    'product_id': order_line.product_id.id,
                                    'vendor_name': vendor_id.partner_id.name,
                                    'unit_price': order_line.price_unit,
                                    'qty': order_line.product_qty,
                                    'delivery_date': order_line.date_planned.date().strftime("%d/%m/%Y"),
                                    })
                            elif option =='by_line_date':
                                lines.append({
                                    'option': 'by_line_date',
                                    'vendor_id': vendor_id.partner_id.id,
                                    'message': ('Delivery Date :' + str(order_line.date_planned)),
                                    'line_id': order_line.id,
                                    'product_id': order_line.product_id.id,
                                    'vendor_name': vendor_id.partner_id.name,
                                    'unit_price': order_line.price_unit,
                                    'qty': order_line.product_qty,
                                    'delivery_date': order_line.date_planned.date().strftime("%d/%m/%Y"),
                                    })
                            else:
                                lines.append({
                                    'option': '',
                                    'vendor_id': vendor_id.partner_id.id,
                                    'message': ('Delivery Date :' + str(order_line.date_planned)),
                                    'line_id': order_line.id,
                                    'product_id': order_line.product_id.id,
                                    'vendor_name': vendor_id.partner_id.name,
                                    'unit_price': order_line.price_unit,
                                    'qty': order_line.product_qty,
                                    'delivery_date': order_line.date_planned.date().strftime("%d/%m/%Y"),
                                    })
                else:
                    lines.append({
                        'option': '',
                        'vendor_id': 0,
                        'line_id': 0,
                        'product_id': product_id.id,
                        'vendor_name': 0,
                        'unit_price': 0,
                        'qty': 0,
                        })


            record.append({
                'min_date_vendor': min_date_vendor.name,
                'min_date': min_date.date().strftime("%d/%m/%Y"),
                'product_id': product_id.id,
                'product_name': product_id.name,
                'description': self.env['purchase.order.line'].search([('order_id', 'in', purchase_ids.ids), ('product_id', '=', product_id.id)], limit=1).name,
                'min_prize': min_prize,
                'min_prize_vendor': min_prize_vendor.name,
                'message': ("Vendor Name: " + min_prize_vendor.name + " ,Min Prize: " + str(min_prize)),
                'record_lines': lines,
                })

        return {
            'record_line_ids': record, 
            'partner_ids': partner_ids, 
            'total': total, 
            'length': len(purchase_ids.ids), 
            'option': option, 
            'min_total_vendor': min_total_vendor, 
            'min_delivery_vendor': min_delivery_vendor,
            'reqisition_name': tendor_id.name,
            'price_order_line_ids': price_order_line_ids,
            'date_order_line_ids': date_order_line_ids,
        }

    def action_open_dashboard(self):
        active_id = self.env.context.get('active_id')
        return {
            'name': 'Dashboard',
            'type': 'ir.actions.client',
            'tag': 'compare_dashboard',
            'context': "{'reqisition_id': active_id}",
        }

    @api.model
    def remove_line_action(self, line_id=None, active_id=None):
        lines = self.env['purchase.order.line'].search([('id', '=', line_id)])
        if lines:
            lines.unlink()
        return True

    def confirm_order_action(self, purchase_id=None):
        purchase_orders = self.env['purchase.order'].search([('id', '=', self.id)])
        for order in purchase_orders:
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
            return True
            