# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # payment_ref = fields.Char('Payment Reference')
    attendant = fields.Many2one('res.partner', 'Attendant')
    project_name = fields.Many2one('project.project', 'Project Name')
    project_shipment = fields.Char('Project Shipment')
    project_code = fields.Char('Project Code')
    po_no = fields.Many2one('purchase.order', 'PO No')
    invoice_name = fields.Char('Invoice Name')
    invoice_arabic_name = fields.Char('Invoice Arabic Name')
    total_wd = fields.Char('Total work done')
    total_wd_arabic = fields.Char('Total work done Arabic')
    po_type = fields.Selection([
        ('project', 'Project'),
        ('other', 'Other')
    ], string='PO Type')

    confirmation_date = fields.Datetime('Confirmation Date')
    sub_contractor = fields.Many2one('res.partner', 'Sub-Contractor')
    works = fields.Char('WORKS')
    period = fields.Char('PERIOD')
    contract_order = fields.Char('Contract/Order')
    retention = fields.Float('Retention (%)')
    retention_amount = fields.Float('Retention Amount', compute='_compute_retention_amount')
    advance = fields.Float('Advance (%)')
    advance_amount = fields.Float('Advance Amount', compute='_compute_advance_amount')
    advance_vat = fields.Float('Advance Vat', compute='_compute_advance_vat')
    recoverable = fields.Float('Recoverable')

    # journal_id = fields.Many2one('account.journal', string='Journal')

    # @api.onchange('project_name')
    # def _onchange_project_name(self):
    #     print(self.move_type)
    #     # out_invoice

    @api.depends('retention')
    def _compute_retention_amount(self):
        for rec in self:
            if rec.retention:
                rec.retention_amount = rec.amount_untaxed * (rec.retention / 100)
            else:
                rec.retention_amount = 0

    @api.depends('advance')
    def _compute_advance_amount(self):
        for rec in self:
            if rec.advance:
                rec.advance_amount = rec.amount_untaxed * (rec.advance / 100)
            else:
                rec.advance_amount = 0

    @api.depends('advance_amount')
    def _compute_advance_vat(self):
        for rec in self:
            if rec.advance_amount:
                # rec.advance_vat = rec.amount_tax * rec.advance_amount
                rec.advance_vat = 0
            else:
                rec.advance_vat = 0

    @api.onchange('po_no')
    def _on_change_po_no(self):
        if self.po_no:
            self.purchase_id = self.po_no.id
        self.purchase_vendor_bill_id = False

        if not self.purchase_id:
            return

        # Copy data from PO
        invoice_vals = self.purchase_id.with_company(self.purchase_id.company_id)._prepare_invoice()
        invoice_vals['currency_id'] = self.invoice_line_ids and self.currency_id or invoice_vals.get('currency_id')
        del invoice_vals['ref']
        del invoice_vals['company_id']  # avoid recomputing the currency
        self.update(invoice_vals)

        # Copy purchase lines.
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        for line in po_lines.filtered(lambda l: not l.display_type):
            self.invoice_line_ids += self.env['account.move.line'].new(
                line._prepare_account_move_line(self)
            )

        # Compute invoice_origin.
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))

        # Compute ref.
        refs = self._get_invoice_reference()
        self.ref = ', '.join(refs)

        # Compute payment_reference.
        if len(refs) == 1:
            self.payment_reference = refs[0]

        self.purchase_id = False


class AccountMoveLines(models.Model):
    _inherit = 'account.move.line'

    contract_per_amount = fields.Char('Contract Amount (%)', compute='_compute_contract_per_amount')
    is_bill = fields.Boolean(compute='_compute_is_bill')
    is_project = fields.Boolean(compute='_compute_is_project')

    def _compute_is_bill(self):
        for rec in self:
            if rec.move_id.move_type == 'in_invoice':
                rec.is_bill = True
            else:
                rec.is_bill = False

    def _compute_is_project(self):
        for rec in self:
            if rec.move_id.po_type == 'project':
                rec.is_project = True
            else:
                rec.is_project = False

    @api.depends('price_unit')
    def _compute_contract_per_amount(self):
        for rec in self:
            if rec.price_unit:
                try:
                    rec.contract_per_amount = f'{round((rec.price_unit / rec.move_id.amount_untaxed) * 100, 2)}%'
                except:
                    rec.contract_per_amount = 0
            else:
                rec.contract_per_amount = 0
