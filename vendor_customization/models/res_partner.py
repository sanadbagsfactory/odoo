from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_rank = fields.Integer(default=0, copy=False)
    customer_rank = fields.Integer(default=0, copy=False)

    @api.onchange('vat')
    def _onchange_vat(self):
        print(self.supplier_type)
        print(self.customer_rank)
        print(self.supplier_rank)

    #     Vendor Custom Fields
    name_arabic = fields.Char('Arabic Name')
    new_gl = fields.Char('New G/L')
    focus_gl = fields.Char('Focus G/L')
    loc = fields.Selection([
        ('international', 'International'),
        ('domestic', 'Domestic')
    ], string='Location')
    Comm_reg_no = fields.Char('Commercial Registration Number')

    supplier_type = fields.Selection([
        ('manufacturing', 'Manufacturing'),
        ('trading', 'Trading'),
        ('services', 'Services')
    ], string='Supplier Type')

    # Customer Custom Fields
    customer_type = fields.Selection([
        ('xyz', 'XYZ'),
    ])
    primary_contact = fields.Char('Primary Contact')
    company_name = fields.Char('Company Name')
    text_treatment = fields.Char('Text Treatment')
    cr_no = fields.Char('CR Number')
    trn = fields.Char('TRN')
    place_of_supply = fields.Many2one(string="Place of Supply", comodel_name='res.country')
    bsn_leg_info = fields.Char('Business Legal Information')
    cus_currency_id = fields.Many2one('res.currency', string='Currency')
    company_country_id = fields.Many2one(string="Company Country", comodel_name='res.country')
    # Company Address ------------------------------------
    com_street = fields.Char()
    com_street2 = fields.Char()
    com_city = fields.Char()
    com_state_id = fields.Many2one(comodel_name='res.country.state', string='State')
    com_zip = fields.Char()
    com_country_id = fields.Many2one(string="Company Country", comodel_name='res.country')
    # -----------------------------------------
    facebook_acc = fields.Char('Facebook')
    twitter_acc = fields.Char('Twitter')

    # same fields
    cr_expiry_date = fields.Date('CR Expiry Date')
    iktiva_segment = fields.Char('IKTIVA Segment')
    iktiva_scoring = fields.Char('IKTIVA Scoring')
