from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        for rec in self:
            records = self.env['account.journal'].search(
                [('is_multi_branch', '=', False), ('id', '=', rec.journal_id.id)])
            if rec.branch_id:
                if records:
                    for line in rec.invoice_line_ids:
                        # h_percent = 100 - rec.branch_id.analytic_plan_id.id
                        line.branch_id = rec.branch_id.id
                        line.analytic_distribution = {
                            rec.branch_id.analytic_account_id.id: 100}

                    for line in rec.line_ids:
                        line.branch_id = rec.branch_id.id
                        line.analytic_distribution = {
                            rec.branch_id.analytic_account_id.id: 100}
                else:
                    for line in rec.invoice_line_ids:
                        if not line.branch_id:
                            line.branch_id = rec.branch_id.id
                            line.analytic_distribution = {
                                rec.branch_id.analytic_account_id.id: 100}
                    for line in rec.line_ids:
                        if not line.branch_id:
                            line.branch_id = rec.branch_id.id
                            line.analytic_distribution = {
                                rec.branch_id.analytic_account_id.id: 100}

    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        records = self.env['account.journal'].search(
            [('is_multi_branch', '=', False), ('id', '=', res.journal_id.id)])
        if res.branch_id:
            if records:
                for line in res.invoice_line_ids:
                    line.branch_id = res.branch_id
                    line.analytic_distribution = {
                        res.branch_id.analytic_account_id.id: 100}

                for line in res.line_ids:
                    line.branch_id = res.branch_id
                    line.analytic_distribution = {
                        res.branch_id.analytic_account_id.id: 100}
            else:
                print("else create called")
                for line in res.invoice_line_ids:
                    if not res.branch_id:
                        line.branch_id = res.branch_id
                        line.analytic_distribution = {
                            res.branch_id.analytic_account_id.id: 100}
                for line in res.line_ids:
                    if not line.branch_id:
                        line.branch_id = res.branch_id.id
                        line.analytic_distribution = {
                            res.branch_id.analytic_account_id.id: 100}
        return res

    def write(self, values):
        res = super(AccountMove, self).write(values)
        if values.get('invoice_line_ids'):
            records = self.env['account.journal'].search(
                [('is_multi_branch', '=', False), ('id', '=', self.journal_id.id)])
            if self.branch_id:
                if records:
                    for line in self.invoice_line_ids:
                        line.branch_id = self.branch_id.id
                        line.analytic_distribution = {
                            self.branch_id.analytic_account_id.id: 100}
                    for line in self.line_ids:
                        line.branch_id = self.branch_id.id
                        line.analytic_distribution = {
                            self.branch_id.analytic_account_id.id: 100}
                else:
                    print("else write called")
                    for line in self.invoice_line_ids:
                        if not line.branch_id:
                            line.branch_id = self.branch_id.id
                            line.analytic_distribution = {
                                self.branch_id.analytic_account_id.id: 100}
                        if not line.branch_id:
                            line.branch_id = self.branch_id.id
                            line.analytic_distribution = {
                                self.branch_id.analytic_account_id.id: 100}
        return res

    def action_register_payment(self):
        return {
            'name': _('Register Payment'),
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
                'default_branch_id': self.branch_id.id,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id)
    is_multi_branch = fields.Boolean(related='move_id.journal_id.is_multi_branch')

    @api.onchange('branch_id')
    def _on_branch_id_change(self):
        for rec in self:
            rec.analytic_distribution = {rec.branch_id.analytic_account_id.id: 100}
            print(rec.analytic_distribution)


class AccountAccountInherited(models.Model):
    _inherit = 'account.journal'
    is_multi_branch = fields.Boolean(string='Multi Branches')
