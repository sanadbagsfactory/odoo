from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    is_locked = fields.Boolean('Control Account')
    is_required = fields.Boolean('Employee is required')
