from odoo import models, api, fields, _


class IktvaSegment(models.Model):
    _name = 'iktva.segment'
    _description = 'IKTVA Segment'

    name = fields.Char('Name')
    description = fields.Text('Description')
    score = fields.Char('Score')
