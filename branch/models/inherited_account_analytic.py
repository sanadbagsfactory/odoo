from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    branch_id = fields.Many2one('res.branch', string='Branch')


class AccountAnalyticPlan(models.Model):
    _inherit = 'account.analytic.plan'

    branch_id = fields.Many2one('res.branch', string='Branch')
