from odoo import fields, models, api, _


class ResPartnerBankInherited(models.Model):
    _inherit = 'res.partner.bank'

    iban_number = fields.Char('IBAN Number')