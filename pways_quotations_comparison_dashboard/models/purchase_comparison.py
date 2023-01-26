# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta

class ResCompany(models.Model):
    _inherit = 'res.company'

    is_remaing_cancel = fields.Boolean(string="Cancel Non Selected RFQ")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_remaing_cancel = fields.Boolean(related="company_id.is_remaing_cancel", string="Cancel Non Selected RFQ", readonly=False)


class PurchaseComparison(models.Model):
    _name = 'purchase.comparison'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Comparion'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, help="Name", default="NEW")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    comparison_line_ids = fields.One2many('purchase.comparison.line', 'comparison_id', string="Comparison")
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    ordering_date = fields.Date(string="Start Date",default=fields.Date.today())
    end_date = fields.Date(string="End Date")
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Set To Approve'), ('approved', 'Approved'), ('inprogress', 'In progress'), ('done', 'Done'), ('cancel', 'Cancel'),], default='draft')

    def action_set_confirm(self):
        self.write({'state': 'inprogress'})

    def action_set_approve(self):
        self.write({'state': 'approved'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def open_purchase_order(self):
        view_id = self.env.ref('pways_quotations_comparison_dashboard.purchase_comparison_tree_view_new_inherit').id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_id': view_id,
            'view_mode': 'tree',
            'res_model': 'purchase.order',
            'target': 'new',
            'domain': [('state', 'in', ['draft', 'sent'])],
            "context": {"create": False},
        }

    def close_action_window(self):
        print("hahahaha")

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
        
        
        tendor_id = self.env['purchase.comparison'].search([('id', '=', reqisition_id)], limit=1)
        purchase_ids = tendor_id.comparison_line_ids.mapped('purchase_id')
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

    @api.model
    def confirm_order_action(self, purchase_id=None, reqisition_id=None):
        purchase_orders = self.env['purchase.order'].search([('id', '=', purchase_id)])
        comparison_id = self.env['purchase.comparison'].browse(reqisition_id)
        confirm_purchase_id = self.env['purchase.order'].browse(purchase_id)
        if comparison_id.env.company.is_remaing_cancel:
            cancel_purchase_ids = comparison_id.comparison_line_ids.mapped('purchase_id').filtered(lambda x:x.id != confirm_purchase_id.id)
            for cancel in cancel_purchase_ids:
                cancel.button_cancel()
        comparison_id.write({'state': 'done'})
        today_date = datetime.now()
        display_msg = """ RFQ """ + str(confirm_purchase_id.name) + """
                                      is confirmed from vendor """ + confirm_purchase_id.partner_id.name + """
                                      with amount of """ + str(confirm_purchase_id.amount_total) + """ on date """ + today_date.strftime("%Y-%m-%d")
        comparison_id.message_post(body=display_msg)
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

    @api.model
    def create(self,vals):
        res = super(PurchaseComparison, self).create(vals)
        res['name'] = self.env['ir.sequence'].next_by_code('purchase.comparison') or '/'
        return res

class PurchaseComparisonLine(models.Model):
    _name = 'purchase.comparison.line'

    comparison_id = fields.Many2one('purchase.comparison', string="Comparison Id")
    purchase_id = fields.Many2one('purchase.order', string="References")
    partner_id = fields.Many2one('res.partner', string="Vendor", related="purchase_id.partner_id")
    user_id = fields.Many2one('res.users', string="Buyer", related="purchase_id.user_id")
    date = fields.Datetime(string="Order Date", related="purchase_id.date_order")
    state = fields.Selection(related="purchase_id.state")

class PurchaseOrder(models.Model):
    _inherit='purchase.order'

    def action_open_dashboard(self):
        lines = []
        purchase_comp = self.env['purchase.comparison'].browse(self.env.context.get('active_id'))
        for line in self:
            line_purchase_id = self.env['purchase.comparison.line'].create({
                    'purchase_id': line.id,
                })
            lines.append(line_purchase_id.id)
        purchase_comp.comparison_line_ids = [[6, 0, lines]]
        purchase_comp.write({'state': 'approve'})
        return True