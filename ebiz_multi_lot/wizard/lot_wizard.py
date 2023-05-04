# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LotWizard(models.TransientModel):
    _name = "lot.wizard"

    lot_id = fields.Many2many('stock.production.lot', string='Lot/Serial Number')
    check = fields.Boolean(default=False)

    @api.onchange('check')
    def _onchange_check(self):
            for line in self.lot_id:
                if self.check:
                   line.is_active_line = True
                else:
                    line.is_active_line = False


    @api.model
    def default_get(self, fields):
        vals = super(LotWizard, self).default_get(fields)
        if self.env.context.get('active_model') == 'stock.move.line':
            item_line = self.env['stock.move.line'].browse([('id', '=', self._context.get('active_id')), ('check_product', '=', False)])
            picking_ids = self.env['stock.picking'].browse(self.env['stock.move.line'].browse(self._context.get('active_id')).picking_id.id)
            product_ids = picking_ids.mapped('move_ids_without_package').mapped('product_id').ids
            if product_ids and picking_ids and picking_ids.location_id:
                stock_ids = self.env['stock.production.lot'].search(
                    [('product_id', 'in', product_ids), ('location_ids', '=', picking_ids.location_id.id)])
                if stock_ids:
                    vals['lot_id'] = [(6, 0, stock_ids.ids)]
        return vals

    def add_lot_lines(self):
        vals = []
        picking_ids = self.env['stock.picking'].browse(self.env['stock.move.line'].browse(self.env.context['active_id']).picking_id.id)
        line_ids = self.lot_id.filtered(lambda x: x.is_active_line == True)
        stock_move_line = self.env['stock.move.line']
        for picking in line_ids:
            move_line_id = picking_ids.mapped('move_line_ids_without_package').filtered(
                lambda x: x.product_id == picking.product_id)
            vals_list = {'product_id': move_line_id.product_id.id,
                         'company_id': move_line_id.company_id.id if move_line_id.company_id else None,
                         'product_uom_id': move_line_id.product_uom_id.id if move_line_id.product_uom_id else None,
                         'location_id': move_line_id.location_id.id if move_line_id.location_id else None,
                         'location_dest_id': move_line_id.location_dest_id.id if move_line_id.location_dest_id else None,
                         # 'product_uom_id': move_line_id.product_uom_id.id if move_line_id.product_uom_id else None,
                         'qty_done': picking.available_quantity,
                         'picking_id': move_line_id.picking_id.id if move_line_id.picking_id else None,
                         'lot_id': picking.id}
            mv_line_id = stock_move_line.create(vals_list)
            picking_ids.move_line_ids_without_package = [(4, mv_line_id.id)]
        line_ids.is_active_line = False