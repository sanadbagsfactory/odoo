# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class SNDPettyCash(models.Model):
    _name = 'snd.petty.cash'

    name = fields.Char(
        string='Name',
        index=True,
        default=lambda self: _('New')
    )
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Payment',
                                 domain='[("type", "in", ["bank", "cash"])]')
    account_id = fields.Many2one(comodel_name='account.account', string='Account')
    # domain='[("account_type", "=", "expense")]'
    amount = fields.Float(string='Amount')
    tax_ids = fields.Many2many(comodel_name='account.tax', string='Taxes')
    description = fields.Text(string='Description')
    move_id = fields.Many2one('account.move', 'Bill')
    ref = fields.Char(string='Vendor Invoice Number')
    bill_state = fields.Selection(related='move_id.state', string='Bill Status')
    payment_state = fields.Selection(related='move_id.payment_state', string='Payment State')
    payment_id = fields.Many2one('account.payment', 'Payment')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)

    def action_confirm(self):
        self.write({
            'state': 'confirm'
        })
        if self.payment_id:
            self.payment_id.unlink()
        if self.move_id:
            self.move_id.unlink()
        self.create_bill()

    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })
        if self.payment_id:
            self.payment_id.action_cancel()
        if self.move_id:
            self.move_id.button_cancel()

    def action_draft(self):
        self.write({
            'state': 'draft'
        })
        if self.payment_id:
            self.payment_id.action_draft()
        if self.move_id:
            self.move_id.button_draft()

    def create_bill(self):
        for rec in self:
            bill = {
                'petty_cash_id': rec.id,
                'ref': rec.ref,
                'invoice_line_ids': [(0, 0, {
                    'product_id': False,
                    'name': rec.description,
                    'price_unit': rec.amount,
                    'quantity': 1.0,
                    'tax_ids': rec.tax_ids.ids,
                    'account_id': rec.account_id.id,
                })],
                'partner_id': rec.vendor_id.id,
                'branch_id': rec.branch_id.id,
                'invoice_date': date.today(),
                'date': date.today(),
                'state': 'draft',
                'move_type': 'in_invoice'
            }
            record = self.env['account.move'].create(bill)
            rec.move_id = record.id
            record.action_post()
            if rec.move_id:
                payment = {
                    'date': date.today(),
                    'amount': rec.move_id.amount_residual,
                    'payment_type': 'outbound',
                    'partner_type': 'supplier',
                    'ref': rec.move_id.name,
                    'journal_id': rec.journal_id.id,
                    'currency_id': 148,
                    'partner_id': rec.move_id.partner_id.id,
                    'partner_bank_id': False,
                    # 'destination_account_id': rec.account_id.id,
                    'branch_id': rec.move_id.branch_id.id,
                    'state': 'draft',
                    'petty_cash_id': rec.id,
                }
                record = self.env['account.payment'].create(payment)
                rec.payment_id = record.id
                record.action_post()
                rec.move_id.payment_id = record.id
                print(f'{record} Payment is created')

    # def create_payment(self):
    #     for rec in self:
    #         payment = {
    #             'partner_id': rec.vendor_id.id,
    #             'branch_id': rec.branch_id.id,
    #             'date': date.today(),
    #             'state': 'draft',
    #             'journal_id': rec.journal_id.id,
    #             'payment_type': 'outbound',
    #             'amount': rec.amount,
    #             'ref': rec.move_id.name,
    #             'invoice_vendor_bill_id': rec.move_id.id,
    #         }
    #         record = self.env['account.payment'].create(payment)
    #         print(f'{record} Payment is created')
    moves_count = fields.Integer('Moves', compute='_compute_moves_count')

    def _compute_moves_count(self):
        for rec in self:
            order_count = self.env['account.move'].search_count(
                [('petty_cash_id.id', '=', rec.id), ('move_type', '=', 'in_invoice')])
            rec.moves_count = order_count if order_count >= 1 else 0

    def show_moves(self):
        return {
            'name': _('Bills'),
            'view_mode': "tree,form",
            'res_model': 'account.move',
            'domain': [('petty_cash_id', '=', self.id), ('move_type', '=', 'in_invoice')],
            'context': "{'create': False,'edit': False}",
            'type': 'ir.actions.act_window',
        }

    payments_count = fields.Integer('Moves', compute='_compute_payments_count')

    def _compute_payments_count(self):
        for rec in self:
            count = self.env['account.payment'].search_count([('petty_cash_id', '=', self.id)])
            rec.payments_count = count if count >= 1 else 0

    def show_payments(self):
        return {
            'name': _('Payment'),
            'view_mode': "tree,form",
            'res_model': 'account.payment',
            'domain': [('petty_cash_id', '=', self.id)],
            'context': "{'create': False,'edit': False}",
            'type': 'ir.actions.act_window',
        }

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('snd.petty.cash.seq') or _('New')
        return super(SNDPettyCash, self).create(vals)

    @api.model
    def unlink(self):
        for rec in self:
            if rec.payment_id or rec.move_id:
                rec.payment_id.unlink()
                rec.move_id.unlink()
            return super(SNDPettyCash, self).unlink()


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    petty_cash_id = fields.Many2one('snd.petty.cash')


class AccountPaymentInherited(models.Model):
    _inherit = 'account.payment'

    petty_cash_id = fields.Many2one('snd.petty.cash')

    @api.model
    def create(self, vals):
        print(vals)
        return super(AccountPaymentInherited, self).create(vals)
