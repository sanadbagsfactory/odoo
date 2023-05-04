from odoo import models, fields, api, _

class ProductionLotInherit(models.Model):
    _inherit = 'stock.picking'


    def action_lot_assign(self):
        product_ids = self.move_ids_without_package.mapped('product_id').ids
        print("self.move_ids_without_package.mapped('product_id')",product_ids)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign Lots'),
            'res_model': 'lot.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {'search_default_group_by_product': 1, 'display_complete': True, 'picking_id': self.id, 'product_ids':product_ids},
        }


class ProductionLotInherit(models.Model):
    _inherit = 'stock.production.lot'

    available_quantity = fields.Float('Available Quantity', compute='_product_virtual_qty')
    is_active_line = fields.Boolean('Selected',default=False)

    @api.constrains('name', 'product_id', 'company_id')
    def _check_unique_lot(self):
        return

    @api.depends('quant_ids', 'quant_ids.available_quantity')
    def _product_virtual_qty(self):
        for lot in self:
            # We only care for the quants in internal or transit locations.
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' or (q.location_id.usage == 'transit' and q.location_id.company_id))
            lot.available_quantity = sum(quants.mapped('available_quantity'))


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    check_product = fields.Boolean(default=False)


    def assign_lot_number(self):
        product_ids = self.picking_id.move_ids_without_package.mapped('product_id').ids
        print("self.move_ids_without_package.mapped('product_id')", product_ids)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign Lots'),
            'res_model': 'lot.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {'search_default_group_by_product': 1, 'display_complete': True, 'picking_id': self.id,
                        'product_ids': product_ids},
        }