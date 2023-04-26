from odoo import models, fields, api, _


class PurchaseTenderType(models.Model):
    _name = 'purchase.tender.type'
    _description = 'Purchase Tender Type'

    name = fields.Char('Name')
