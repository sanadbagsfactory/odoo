# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_ids = fields.Many2many('res.partner', compute="_compute_partner_ids")
    po_number = fields.Char(string='PO Number')
    pa_number = fields.Char(string='PA Number')
    pl_number = fields.Char(string='PL Number')
    supply_date = fields.Date(string='Date of Supply')

    @api.depends('partner_id')
    def _compute_partner_ids(self):
        for rec in self:
            if rec.move_type in ['out_invoice', 'out_invoice', 'out_refund', 'out_receipt']:
                record = self.env['res.partner'].search([('customer_rank', '>', 0)])
                if record:
                    rec.partner_ids = record
                else:
                    rec.partner_ids = False
            elif rec.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
                record = self.env['res.partner'].search([('supplier_rank', '>', 0)])
                if record:
                    rec.partner_ids = record
                else:
                    rec.partner_ids = False
            else:
                rec.partner_ids = self.env['res.partner'].search([])

    def unlink(self):
        for rec in self:
            print(rec.partner_id.supplier_rank)
            print(rec.partner_id.customer_rank)
            if rec.move_type == 'out_invoice' and rec.state == 'posted':
                raise UserError("Post entry can't be deleted!")
        rec = super(AccountMove, self).unlink()
        return rec
