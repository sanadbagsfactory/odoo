# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Branch'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')
    division_id = fields.Char(string='Division')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_plan_id = fields.Many2one('account.analytic.plan', string='Analytic Plan')

    @api.model
    def create(self, vals):
        res = super(ResBranch, self).create(vals)
        print(vals)
        plan = self.env['account.analytic.plan'].create(
            {
                'name': vals.get('name'),
                'branch_id': res.id,
            })
        print(plan)
        res.analytic_plan_id = plan.id

        result = self.env['account.analytic.account'].create(
            {
                'name': vals.get('name'),
                'plan_id': plan.id,
                'branch_id': res.id,
            })
        res.analytic_account_id = result.id
        return res

    def write(self, vals):
        res = super(ResBranch, self).write(vals)
        if vals.get('name'):
            self.analytic_account_id.update({'name': vals.get('name')})
            self.analytic_plan_id.update({'name': vals.get('name')})
            # res.analytic_account_id = result.id
        return res

    def unlink(self):
        if self.analytic_account_id:
            self.analytic_account_id.unlink()
        if self.analytic_plan_id:
            self.analytic_plan_id.unlink()
        return super(ResBranch, self).unlink()
