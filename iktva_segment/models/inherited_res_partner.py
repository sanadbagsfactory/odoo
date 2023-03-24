from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_rank = fields.Integer(default=0, copy=False)
    customer_rank = fields.Integer(default=0, copy=False)

    iktva_segment_id = fields.Many2one('iktva.segment','IKTVA Segment')
    iktva_description = fields.Text(related='iktva_segment_id.description')
    iktva_scoring = fields.Char(related='iktva_segment_id.score')
