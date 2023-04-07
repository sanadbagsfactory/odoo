from odoo import models, fields, api


class ConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    amount_limit = fields.Float(string='Amount Limit',
                                config_parameter='approval_workflow.amount_limit')
