from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_ids = fields.Many2many('res.branch', string="Allowed Branch")
    branch_id = fields.Many2one('res.branch', string='Branch')
