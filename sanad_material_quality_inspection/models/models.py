from odoo import api, fields, models

class QualityControl(models.Model):
    _inherit = 'quality.point'

    section2b_id = fields.One2many('section2b.inspection', 'quality_id')
    section2c_id = fields.One2many('section2c.inspection', 'quality_id', string='Section 2 D')
    section2d_id = fields.One2many('section2d.inspection', 'quality_id',string='Section 2 C')



class Section2BInspection(models.Model):
    _name = 'section2b.inspection'

    quality_id = fields.Many2one('quality.point')
    product_id = fields.Many2one('product.product', 'Product')
    gsm_type = fields.Selection([
        ('1300gsm', '1300 GSM'),
        ('950gsm', '950 GSM'),
        ('700gsm', '700 GSM'),
    ])
    sepecification = fields.Float('Specification')
    actual = fields.Float('Actual')
    accepted = fields.Boolean(default=False, string='Accepted')
    rejected = fields.Boolean(default=False, string='Rejected')
    reference = fields.Boolean(default=False, string='Reference')


class Section2CInspection(models.Model):
    _name = 'section2c.inspection'

    quality_id = fields.Many2one('quality.point')
    product_id = fields.Many2one('product.product', 'Product')
    gsm_type = fields.Selection([
        ('1300gsm', '1300 GSM'),
        ('950gsm', '950 GSM'),
        ('700gsm', '700 GSM'),
    ])
    sepecification = fields.Float('Specification')
    actual = fields.Float('Actual')
    accepted = fields.Boolean(default=False, string='Accepted')
    rejected = fields.Boolean(default=False, string='Rejected')
    reference = fields.Boolean(default=False, string='Reference')


class Section2DInspection(models.Model):
    _name = 'section2d.inspection'

    quality_id = fields.Many2one('quality.point')
    product_id = fields.Many2one('product.product', 'Product')
    gsm_type = fields.Selection([
        ('1300gsm', '1300 GSM'),
        ('950gsm', '950 GSM'),
        ('700gsm', '700 GSM'),
    ])
    sepecification = fields.Float('Specification')
    actual = fields.Float('Actual')
    accepted = fields.Boolean(default=False, string='Accepted')
    rejected = fields.Boolean(default=False, string='Rejected')
    reference = fields.Boolean(default=False, string='Reference')

