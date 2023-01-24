from odoo import fields, models, api, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    length = fields.Float('Length')
    width = fields.Float('Width')

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        print(vals)
        print(vals.get('length'))
        print(vals.get('width'))
        if vals.get('length'):
            self.product_tmpl_id.length = vals.get('length')
        if vals.get('width'):
            self.product_tmpl_id.width = vals.get('width')
        return res

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        print(res.product_tmpl_id)
        if res.product_tmpl_id:
            res.product_tmpl_id.length = res.length
            res.product_tmpl_id.width = res.width
        return res

    def _prepare_variant_values(self, combination):
        print('_prepare_variant_values')
        variant_dict = super()._prepare_variant_values(combination)
        variant_dict['width'] = self.width
        variant_dict['length'] = self.length
        return variant_dict


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float('Length')
    width = fields.Float('Width')

    @api.onchange('length', 'width')
    def _onchange_length_width_size(self):
        for rec in self:
            if rec.length:
                rec.product_variant_id.length = rec.length
            if rec.width:
                rec.product_variant_id.width = rec.width


    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        print(res.product_variant_id)
        if res.product_variant_id:
            res.product_variant_id.length = res.length
            res.product_variant_id.width = res.width
        return res

    def _prepare_variant_values(self, combination):
        print('_prepare_variant_values')
        variant_dict = super()._prepare_variant_values(combination)
        variant_dict['width'] = self.width
        variant_dict['length'] = self.length
        return variant_dict
