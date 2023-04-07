# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class InheritedAccountMoveDiscount(models.Model):
    _inherit = 'account.move'

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     default=False)
    discount_rate = fields.Float('Discount Rate', digits=(16, 2))
    amount_discount = fields.Monetary(string='Discount', compute='_compute_discount_amount',
                                      track_visibility='always')
    is_lines = fields.Boolean(default=False, compute='_compute_is_lines')

    @api.depends('invoice_line_ids')
    def _compute_is_lines(self):
        for rec in self:
            rec.is_lines = bool(rec.invoice_line_ids)

    def apply_discount(self):
        for rec in self:
            print('Btn Clicked')
            print(rec.move_type)
            inv_product_id = int(
                self.env['ir.config_parameter'].sudo().get_param('cognitive_discount_solution.inv_product_id'))
            bill_product_id = int(
                self.env['ir.config_parameter'].sudo().get_param('cognitive_discount_solution.bill_product_id'))
            for line in self.invoice_line_ids:
                if line.product_id.id in [inv_product_id, bill_product_id]:
                    line.unlink()
            if rec.move_type == 'out_invoice':
                if not inv_product_id:
                    raise UserError('Please Map Discount Product')
                invoice_line_vals = {
                    'product_id': inv_product_id,
                    'name': 'Discount',
                    'quantity': 1,
                    'price_unit': rec.amount_discount,
                    'tax_ids': False,
                    'partner_id': rec.partner_id.id,
                    'currency_id': rec.currency_id.id,
                    'move_id': rec.id,
                }
                print(invoice_line_vals)
                rec.write({
                    'invoice_line_ids': [(0, 0, invoice_line_vals)]
                })
                print(rec.invoice_line_ids)
                # # rec.invoice_line_ids += rec.invoice_line_ids.new(invoice_line_vals)
                # invoice_line = self.env['account.move.line'].new(invoice_line_vals)
                # rec.invoice_line_ids = [(6, 0, [invoice_line.id])]
            if rec.move_type == 'in_invoice':
                if not bill_product_id:
                    raise UserError('Please Map Discount Product')
                print('Invoiced ')
                invoice_line_vals = {
                    'product_id': bill_product_id,
                    'name': 'Discount',
                    'quantity': 1,
                    'price_unit': rec.amount_discount,
                    'tax_ids': False,
                    'partner_id': rec.partner_id.id,
                    'currency_id': rec.currency_id.id,
                    'move_id': rec.id,
                }
                print(invoice_line_vals)
                rec.write({
                    'invoice_line_ids': [(0, 0, invoice_line_vals)]
                })
                print(rec.invoice_line_ids)
                # invoice_line = self.env['account.move.line'].new(invoice_line_vals)
                # rec.invoice_line_ids = [(6, 0, [invoice_line.id])]

    @api.depends('discount_rate')
    def _compute_discount_amount(self):
        for rec in self:
            if rec.discount_type == 'percent':
                amount_discount = rec.amount_untaxed * (rec.discount_rate / 100)
                rec.update({
                    'amount_discount': -amount_discount,
                })
            elif rec.discount_type == 'amount':
                rec.update({
                    'amount_discount': -rec.discount_rate,
                })
            else:
                rec.update({
                    'amount_discount': 0.0,
                })
