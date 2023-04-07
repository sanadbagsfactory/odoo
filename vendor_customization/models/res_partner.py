import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_rank = fields.Integer(default=0, copy=False)
    customer_rank = fields.Integer(default=0, copy=False)

    #     Vendor Custom Fields
    name_arabic = fields.Char('Arabic Name')
    vendor_code = fields.Char('Vendor Code')

    def generate_vendor_code(self):
        for rec in self:
            seq = self.env['ir.sequence'].next_by_code('res.partner.vendor.seq')
            rec.update({
                'vendor_code': seq,
            })

    # Customer Fields
    customer_code = fields.Char('Customer Code')

    def generate_customer_code(self):
        for rec in self:
            seq = self.env['ir.sequence'].next_by_code('res.partner.customer.seq')
            rec.update({
                'customer_code': seq,
            })

    focus_gl = fields.Char('Focus G/L')
    new_gl = fields.Char('new G/L')
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
    # extra------------------------------------------------------
    iktiva_segment = fields.Char('IKTIVA Segment', invisible=1)
    iktiva_scoring = fields.Char('IKTIVA Scoring', invisible=1)
    # Extraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
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
            data_dict = {}
            for rec in self.env['res.partner'].search([]):
                if (
                        rec.cr_expiry_date
                        and rec.cr_expiry_date <= datetime.date.today()
                ):
                    print(f'record found: Id: {rec.id} Name: {rec.name}')
                    data_dict[rec.id] = rec.name
            print(f'Last Login time: {self.env.user.login_date.time()}')
            print(f'Last Login time: {self.env.user.login_date}')
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('CR Date Expired'),
                    'message': f'Following users CR date has been expired:\n {data_dict}',
                    'type': 'danger',  # types: success,warning,danger,info
                    'sticky': True,  # True/False will display for few seconds if false
                },
            }

    def send_reminder_emails(self):
        print('send_reminder_emails')
        today = datetime.now().date()
        print(today)
        partners = self.env['res.partner'].search([])
        if expired_partners := partners.filtered(
                lambda p: p.cr_expiry_date <= today
        ):
            subject = 'Your CR date has expired'
            print(subject)
            print(expired_partners)
            for partner in expired_partners:
                body = f'Dear {partner.name},\n\nYour CR date has expired. Please renew your CR status as soon as possible.\n\nBest regards,\n\nThe Odoo team'
                mail_values = {
                    'subject': subject,
                    'body_html': body,
                    'email_to': partner.email,
                }
                if mail := self.env['mail.mail'].create(mail_values):
                    mail.send()

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

    #     Validations
    @api.constrains('cr_no')
    def cr_no_uniqueness(self):
        for rec in self:
            if (
                    rec.cr_no
                    and len(
                self.env['res.partner'].search([('cr_no', '=', rec.cr_no)])
            )
                    > 1
            ):
                raise UserError("A CR Number is already exists with this number . CR Number must be unique!")

    @api.constrains('vat', 'cr_no', 'phone_number')
    def vat_uniqueness_and_validations(self):
        for rec in self:
            if rec.vat and not rec.vat.isdigit():
                raise ValidationError(_("The VAT Number must be a sequence of digits."))
            if rec.cr_no and not rec.cr_no.isdigit():
                raise ValidationError(_("The CR Number must be a sequence of digits."))
            if rec.phone_number and not rec.phone_number.isdigit():
                raise ValidationError(_("The Phone Number must be a sequence of digits."))


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

    @api.constrains('vat', 'company_registry', 'phone_number')
    def uniqueness_and_validations(self):
        for rec in self:
            if rec.vat and not rec.vat.isdigit():
                raise ValidationError(_("The VAT Number must be a sequence of digits."))
            if rec.company_registry and not rec.company_registry.isdigit():
                raise ValidationError(_("The Company Registry must be a sequence of digits."))
            if rec.phone_number and not rec.phone_number.isdigit():
                raise ValidationError(_("The Phone Number must be a sequence of digits."))
