from odoo import api, fields, models


class RespartnerInheritModel(models.Model):
    _inherit = 'res.partner'

    check_ktva = fields.Boolean(default=False)
    check_vat_cr = fields.Boolean(default=False)

    @api.onchange('country_id')
    def _onchange_country(self):
        if self.country_id.name == 'Saudi Arabia':
            self.loc = 'domestic'
            self.check_ktva = True
        else:
            self.loc = 'international'
            self.check_ktva = False

    @api.onchange('loc')
    def _onchange_loc(self):
        if self.loc == 'domestic':
            self.check_ktva = True
        else:
            self.check_ktva = False

    @api.onchange('company_type', 'country_id', 'loc')
    def _onchange_company(self):
        if self.loc == 'international' and self.company_type == 'person':
            self.check_vat_cr = True
        else:
            self.check_vat_cr = False
