from odoo import models, fields, api


class ConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    inv_product_id = fields.Many2one('product.product', string='Invoice Product',
                                        config_parameter='cognitive_discount_solution.inv_product_id')
    bill_product_id = fields.Many2one('product.product', string='Bill Product',
                                         config_parameter='cognitive_discount_solution.bill_product_id')
