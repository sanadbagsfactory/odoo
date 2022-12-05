# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    # payment_ref = fields.Char('Payment Reference')
    attendant = fields.Char('Attendant')
    project_name = fields.Char('Project Name')
    project_shipment = fields.Char('Project Shipment')
    location = fields.Char('Location')
    po_no = fields.Char('PO No')
    invoice_name = fields.Char('Invoice Name')
    invoice_arabic_name = fields.Char('Invoice Arabic Name')
    total_wd = fields.Char('Total work done')
    total_wd_arabic = fields.Char('Total work done Arabic')

    confirmation_date = fields.Datetime('Confirmation Date')
    sub_contractor = fields.Char('Sub-Contractor')
    works = fields.Char('WORKS')
    period = fields.Char('PERIOD')
    contract_order = fields.Char('Contract/Order')
    retention = fields.Float('Retention (%)')
    retention_amount = fields.Float('Retention Amount', compute='_compute_retention_amount')
    advance = fields.Float('Advance (%)')
    advance_amount = fields.Float('Advance Amount', compute='_compute_advance_amount')
    advance_vat = fields.Float('Advance Vat', compute='_compute_advance_vat')
    recoverable = fields.Char('Recoverable')

    # journal_id = fields.Many2one('account.journal', string='Journal')

    # @api.onchange('project_name')
    # def _onchange_project_name(self):
    #     print(self.move_type)
    #     # out_invoice

    @api.depends('retention')
    def _compute_retention_amount(self):
        for rec in self:
            if rec.retention:
                if rec.invoice_line_ids:
                    rec.retention_amount = rec.invoice_line_ids[0].price_subtotal * (rec.retention / 100)
                else:
                    rec.retention_amount = 0
            else:
                rec.retention_amount = 0

    @api.depends('advance')
    def _compute_advance_amount(self):
        for rec in self:
            if rec.advance:
                if rec.invoice_line_ids:
                    rec.advance_amount = rec.invoice_line_ids[0].price_subtotal * (rec.advance / 100)
                else:
                    rec.advance_amount = 0
            else:
                rec.advance_amount = 0

    @api.depends('advance_amount')
    def _compute_advance_vat(self):
        for rec in self:
            if rec.advance_amount:
                if rec.invoice_line_ids:
                    if rec.invoice_line_ids[0].tax_ids:
                        rec.advance_vat = rec.advance_amount * (rec.invoice_line_ids[0].tax_ids.amount / 100)
                    else:
                        rec.advance_vat = 0
                else:
                    rec.advance_vat = 0
            else:
                rec.advance_vat = 0
