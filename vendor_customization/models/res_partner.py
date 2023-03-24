import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_rank = fields.Integer(default=0, copy=False)
    customer_rank = fields.Integer(default=0, copy=False)

    #     Vendor Custom Fields
    name_arabic = fields.Char('Arabic Name')
    vcode_start = fields.Integer('5', default=5)
    vcode_input = fields.Char(size=4)
    vendor_code = fields.Char('Vendor Code', compute='_compute_vendor_code')

    @api.depends('vcode_input')
    def _compute_vendor_code(self):
        for rec in self:
            if rec.vcode_input:
                rec.vendor_code = str(rec.vcode_start) + str(rec.vcode_input)
            else:
                rec.vendor_code = f'{str(rec.vcode_start)}XXXX'

    # Customer Fields
    ccode_start = fields.Integer('3', default=3)
    ccode_input = fields.Char(size=4)
    customer_code = fields.Char('Customer Code', compute='_compute_customer_code')

    @api.depends('ccode_input')
    def _compute_customer_code(self):
        for rec in self:
            if rec.ccode_input:
                rec.customer_code = str(rec.ccode_start) + str(rec.ccode_input)
            else:
                rec.customer_code = f'{str(rec.ccode_start)}XXXX'

    focus_gl = fields.Char('Focus G/L')
    loc = fields.Selection([
        ('international', 'International'),
        ('domestic', 'Domestic')
    ], string='Location')

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
    Comm_reg_no = fields.Char('CR Number')
    cr_no = fields.Char('CR Number')
    cr_expiry_date = fields.Date('CR Expiry Date')
    # Phone
    country_code_phone = fields.Char('Country Code', size=3)
    phone_number = fields.Char('Phone Number', size=10)

    @api.onchange('country_code_phone', 'phone_number')
    def _on_phone_change(self):
        for rec in self:
            if rec.country_code_phone or rec.phone_number:
                rec.phone = str(rec.country_code_phone) + str(rec.phone_number)
                if rec.name == self.env.company.partner_id.name:
                    self.env.company.country_code_phone = str(rec.country_code_phone)
                    self.env.company.phone_number = str(rec.phone_number)

    # CR Expiry Msg Display to Account & Purchase users

    def cr_expiry_msg(self):
        print('clicked cr_expiry')
        if (
                self.env.user.has_group('account.group_account_manager')
                or self.env.user.has_group('account.group_account_user')
        ):
            for rec in self.env['res.partner'].search([]):
                if rec.cr_expiry_date <= datetime.date.today():
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': ('CR Date Expired'),
                            'message': f'CR date has been expired of User\nID: {rec.id}\nName: {rec.name}',
                            'type': 'danger',  # types: success,warning,danger,info
                            'sticky': True,  # True/False will display for few seconds if false
                        },
                    }

    # new fields
    is_vat = fields.Boolean('VAT', default=False)
    vat_certificate_id = fields.Many2many(comodel_name="ir.attachment",
                                          relation="m2m_ir_vat_certificate_rel",
                                          column1="m2m_id",
                                          column2="attachment_id",
                                          )
    cr_attachment_id = fields.Many2many(comodel_name="ir.attachment",
                                        relation="m2m_ir_cr_attachment_rel",
                                        column1="m2m_id",
                                        column2="attachment_id",
                                        )
    ntc_attachment_id = fields.Many2many(comodel_name="ir.attachment",
                                         relation="m2m_ir_ntc_attachment_rel",
                                         column1="m2m_id",
                                         column2="attachment_id",
                                         )

    # Approvals
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    def action_confirm(self):
        self.write({
            'state': 'confirm'
        })

    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })

    def action_draft(self):
        self.write({
            'state': 'draft'
        })


class InheritedResCompany(models.Model):
    _inherit = 'res.company'

    country_code_phone = fields.Char('Country Code', size=3)
    phone_number = fields.Char('Phone Number', size=10)

    @api.onchange('country_code_phone', 'phone_number')
    def _on_phone_change(self):
        for rec in self:
            if rec.country_code_phone or rec.phone_number:
                rec.phone = str(rec.country_code_phone) + str(rec.phone_number)
                rec.partner_id.country_code_phone = str(rec.country_code_phone)
                rec.partner_id.phone_number = str(rec.phone_number)

    @api.constrains('phone_number')
    def _verify_phone_number(self):
        for rec in self:
            if rec.phone_number and not rec.phone_number.isdigit():
                raise ValidationError(_("The Phone Number must be a sequence of digits."))

