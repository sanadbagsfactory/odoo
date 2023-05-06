from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('posted', 'Posted'),
    #     ('cancel', 'Cancel'),
    #     ('approve', 'Approve'),
    #     ('reject', 'Reject'),
    # ])

    # @api.depends('date', 'auto_post')
    # def _compute_hide_post_button(self):
    #     for record in self:
    #         if record.state not in ['reject', 'approve']:
    #             record.hide_post_button = record.state != 'draft' \
    #                                       or record.auto_post != 'no' and record.date > fields.Date.today()
    #         else:
    #             record.hide_post_button = False

    is_auditor = fields.Boolean(compute='_compute_is_auditor')
    is_bill_jv = fields.Boolean(compute='_compute_approve_reject_jv')
    bill_id = fields.Many2one('account.move')

    def _compute_is_auditor(self):
        if self.env.user.has_group(
                'account.group_account_readonly') and self.move_type == 'in_invoice' and self.state == 'posted' and self.amount_tax:
            self.is_auditor = True
        else:
            self.is_auditor = False

    def _compute_approve_reject_jv(self):
        for rec in self:
            counter = self.env['account.move'].search_count([('bill_id', '=', rec.id)])
            if counter:
                rec.is_bill_jv = True
            else:
                rec.is_bill_jv = False

    def action_approve(self):
        for rec in self:
            debit_account = int(
                self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.vat_account_id'))
            credit_account = int(
                self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.clearing_account_id'))
            journal = int(self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.journal_id'))
            if self.env['account.move'].search([('bill_id', '=', rec.id)]):
                raise UserError('Already Approved and JV is Attached on this Bill')
            else:
                lines = []
                move_dict = {
                    'ref': rec.name,
                    'branch_id': rec.branch_id.id,
                    'move_type': 'entry',
                    'journal_id': journal,
                    'partner_id': rec.partner_id.id,
                    'date': rec.date,
                    'state': 'draft',
                    'bill_id': rec.id
                }
                debit_line = (0, 0, {
                    'name': 'Advance Payment',
                    'debit': rec.amount_tax,
                    'credit': 0.0,
                    'partner_id': rec.partner_id.id,
                    'account_id': debit_account,
                })
                lines.append(debit_line)
                credit_line = (0, 0, {
                    'name': 'Advance Payment',
                    'debit': 0.0,
                    'partner_id': rec.partner_id.id,
                    'credit': rec.amount_tax,
                    'account_id': credit_account,
                })
                lines.append(credit_line)
                move_dict['line_ids'] = lines
                move = self.env['account.move'].sudo().create(move_dict)
                print('JV Created')

    def action_reject(self):
        for rec in self:
            credit_account = int(
                self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.clearing_account_id'))
            debit_account = int(
                self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.expense_account_id'))
            journal = int(self.env['ir.config_parameter'].sudo().get_param('auditor_approval_workflow.journal_id'))
            if self.env['account.move'].search([('bill_id', '=', rec.id)]):
                raise UserError('Already Approved and JV is Attached on this Bill')
            else:
                lines = []
                move_dict = {
                    'ref': rec.name,
                    'branch_id': rec.branch_id.id,
                    'move_type': 'entry',
                    'journal_id': journal,
                    'partner_id': rec.partner_id.id,
                    'date': rec.date,
                    'state': 'draft',
                    'bill_id': rec.id
                }
                debit_line = (0, 0, {
                    'name': 'Advance Payment',
                    'debit': rec.amount_tax,
                    'credit': 0.0,
                    'partner_id': rec.partner_id.id,
                    'account_id': debit_account,
                })
                lines.append(debit_line)
                credit_line = (0, 0, {
                    'name': 'Advance Payment',
                    'debit': 0.0,
                    'partner_id': rec.partner_id.id,
                    'credit': rec.amount_tax,
                    'account_id': credit_account,
                })
                lines.append(credit_line)
                move_dict['line_ids'] = lines
                move = self.env['account.move'].sudo().create(move_dict)
                print('JV Created')

    def go_to_jv(self):
        return {
            'name': _('Journal Entries'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('bill_id', '=', self.id), ('move_type', '=', 'entry')],
            'context': {
                'default_bill_id': self.id,
                'create': False
            },
            'type': 'ir.actions.act_window',
        }
