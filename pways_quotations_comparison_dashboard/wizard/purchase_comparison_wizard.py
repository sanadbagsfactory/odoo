from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class PurchaseComparisonWizards(models.TransientModel):
    _name = 'purchase.comparison.wizard'
    _description = "Purchase Comparison Wizard"

    user_id = fields.Many2one('res.users', string='Purchase Representative', default=lambda self: self.env.user)
    purchase_line_ids = fields.One2many('purchase.comparison.line.wizard', 'comparison_id', string="Comparison Id")

    @api.model
    def default_get(self, vals):
        lines = []
        vals = super(PurchaseComparisonWizards, self).default_get(vals)
        active_id = self.env.context.get('active_id')
        comparison_id = self.env['purchase.comparison'].browse(active_id)
        purchase_ids = self.env['purchase.order'].search([('state', '=', 'draft')])
        for purchase in purchase_ids:
                line_purchase_id = self.env['purchase.comparison.line.wizard'].create({
                    'purchase_id': purchase.id,
                })
                lines.append(line_purchase_id.id)
        vals['purchase_line_ids'] = [[6, 0, lines]]
        return vals

    def action_add_rfq(self):
        lines = []
        active_id = self.env.context.get('active_id')
        comparison_id = self.env['purchase.comparison'].browse(active_id)
        for line in self.purchase_line_ids.filtered(lambda x:x.check == True):
            line_purchase_id = self.env['purchase.comparison.line'].create({
                    'purchase_id': line.purchase_id.id,
                })
            lines.append(line_purchase_id.id)
        comparison_id.comparison_line_ids = [[6, 0, lines]]
        comparison_id.write({'state': 'approve'})
    

class PurchaseComparisonLineWizard(models.TransientModel):
    _name = 'purchase.comparison.line.wizard'
    _description = "Purchase Comparison Line Wizard"

    comparison_id = fields.Many2one('purchase.comparison.wizard', string="Order")
    check = fields.Boolean(string="Check")
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order")
    partner_id = fields.Many2one('res.partner', string="Vendor", related="purchase_id.partner_id")
    user_id = fields.Many2one('res.users', string="Buyer", related="purchase_id.user_id")
