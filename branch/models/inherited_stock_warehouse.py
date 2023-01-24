# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_id = fields.Many2one('res.branch')


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    branch_id = fields.Many2one('res.branch')
