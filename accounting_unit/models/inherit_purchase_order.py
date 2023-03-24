from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class InheritedPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_ids = fields.Many2many('res.partner', compute="_compute_partner_ids")

    @api.depends('partner_id')
    def _compute_partner_ids(self):
        for rec in self:
            record = self.env['res.partner'].search([('supplier_rank', '>', 0)])
            if record:
                rec.partner_ids = record
            else:
                rec.partner_ids = False
