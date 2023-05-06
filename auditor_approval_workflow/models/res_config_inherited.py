from odoo import fields, models, api, _


class ResConfigInherited(models.TransientModel):
    _inherit = 'res.config.settings'

    clearing_account_id = fields.Many2one('account.account', string='Clearing Account',
                                          config_parameter='auditor_approval_workflow.clearing_account_id')
    expense_account_id = fields.Many2one('account.account', string='Expense Account',
                                         config_parameter='auditor_approval_workflow.expense_account_id')
    vat_account_id = fields.Many2one('account.account', string='Vat Account',
                                     config_parameter='auditor_approval_workflow.vat_account_id')
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 config_parameter='auditor_approval_workflow.journal_id')
