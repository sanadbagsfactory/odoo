from odoo import fields, models


class Journal(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one('res.branch', default=lambda r: r.env.user.branch_id.id)
