# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    def action_post(self):
        self.write({
            'state': 'approve'
        })

    @api.model
    def mark_activity_done(self, user_id):
        activity = self.env['mail.activity'].search(
            [('user_id', '=', user_id), ('res_model', '=', 'account.payment'), ('res_id', '=', self.id)])
        activity.action_done()

    def button_approved(self):
        self.write({
            'state': 'posted'
        })
        self.mark_activity_done(self.env.user.id)
        return super(AccountPaymentInh, self).action_post()

    def action_draft(self):
        self.write({
            'state': 'draft'
        })
        return super(AccountPaymentInh, self).action_draft()

    @api.model
    def create(self, vals):
        res = super(AccountPaymentInh, self).create(vals)
        if self.env.user.has_group('approval_workflow.group_limit_payment'):
            limited_amount = self.env['ir.config_parameter'].sudo().get_param('approval_workflow.amount_limit')
            if float(res.amount) > float(limited_amount):
                raise UserError(f'You are allowed to created a payment only: {limited_amount}')
            todos = {
                'res_id': res.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'account.payment')]).id,
                'user_id': self.env.user.search([('login', '=', 'hisham@sanadbags.com')]).id,
                'summary': f'Please Approve the Amount {res.amount}',
                'note': 'Amount Approval',
                'date_deadline': datetime.now(),
            }
            if self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id:
                self.env['mail.activity'].sudo().create(todos)
            else:
                raise ValidationError('This email does not exist (baashar.mohammed@sanadbags.com)')
        return res

    def write(self, values):
        res = super(AccountPaymentInh, self).write(values)
        if values and self.env.user.has_group(
                'approval_workflow.group_limit_payment'
        ):
            limited_amount = self.env['ir.config_parameter'].sudo().get_param('approval_workflow.amount_limit')
            print(f'Limit Amount: {limited_amount}')
            print(f'Limit Amount type: {type(limited_amount)}')
            print(f'amount: {type(values.get("amount"))}')
            print(values)
            print(f'amount: {values.get("amount")}')
            if float(values.get('amount')) > float(limited_amount):
                raise UserError(f'You are allowed to created a payment only: {limited_amount}')
            print(self.env.user.has_group('approval_workflow.group_limit_payment'))
        return res
