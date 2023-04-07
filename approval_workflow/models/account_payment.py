# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approval'),
        ('posted', 'Approved'),
        ('reject', 'Rejected'),
    ], string='Approval Status', default='draft', compute='_compute_approval_state')

    def _compute_approval_state(self):
        for rec in self:
            if rec.state == 'approve':
                rec.approval_state = 'approve'
            elif rec.state == 'reject':
                rec.approval_state = 'reject'
            elif rec.state == 'posted':
                rec.approval_state = 'posted'
            else:
                rec.approval_state = 'draft'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')
    is_amount_limit = fields.Boolean(default=False)

    def action_post(self):
        if self.is_amount_limit:
            self.write({
                'state': 'approve'
            })
        else:
            self.write({
                'state': 'posted'
            })
            return super(AccountPaymentInh, self).action_post()

    @api.model
    def mark_activity_done(self, user_id):
        activity = self.env['mail.activity'].search(
            [('user_id', '=', user_id), ('res_model', '=', 'account.payment'), ('res_id', '=', self.id)])
        activity.action_done()

    @api.model
    def create_approval_activity(self, res_id, user, amount):
        if user.has_group('approval_workflow.group_approve_payment'):
            todos = {
                'res_id': res_id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'account.payment')]).id,
                'user_id': user.id,
                'summary': f'Please Approve the Amount {amount}',
                'note': 'Amount Approval',
                'date_deadline': datetime.now(),
            }
            if user.id:
                activity = self.env['mail.activity'].sudo().create(todos)
            else:
                raise ValidationError(f'This email does not exist ({user.login})')

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

    def action_rejected(self):
        self.write({
            'state': 'reject'
        })
        todos = {
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'account.payment')]).id,
            'user_id': self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id,
            'summary': f'Your Payment has been Rejected',
            'note': self.ref,
            'date_deadline': datetime.now(),
        }
        if self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id:
            activity = self.env['mail.activity'].sudo().create(todos)
        else:
            raise ValidationError(f'This email does not exist (baashar.mohammed@sanadbags.com)')

    def action_draft(self):
        self.write({
            'state': 'draft'
        })
        rec = super(AccountPaymentInh, self).action_draft()
        return rec

    @api.model
    def create(self, vals):
        res = super(AccountPaymentInh, self).create(vals)
        if self.env.user.has_group('approval_workflow.group_limit_payment'):
            limited_amount = self.env['ir.config_parameter'].sudo().get_param('approval_workflow.amount_limit')
            if float(res.amount) > float(limited_amount):
                res.is_amount_limit = True
                users = self.env['res.users'].search([])
                for user in users:
                    res.create_approval_activity(res.id, user, res.amount)
        return res

    # def write(self, values):
    #     res = super(AccountPaymentInh, self).write(values)
    #     if values and self.env.user.has_group(
    #             'approval_workflow.group_limit_payment'
    #     ):
    #         limited_amount = self.env['ir.config_parameter'].sudo().get_param('approval_workflow.amount_limit')
    #         print(f'Limit Amount: {limited_amount}')
    #         print(f'Limit Amount type: {type(limited_amount)}')
    #         print(f'amount: {type(values.get("amount"))}')
    #         print(values)
    #         print(f'amount: {values.get("amount")}')
    #         if float(values.get('amount')) > float(limited_amount):
    #             raise UserError(f'You are allowed to created a payment only: {limited_amount}')
    #         print(self.env.user.has_group('approval_workflow.group_limit_payment'))
    #     return res
