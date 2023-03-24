from odoo import fields, models, api, _, tools
from odoo.tools import formatLang


class InheritedPurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'

    def name_get(self):
        result = []
        for doc in self:
            name = doc.name or ''
            result.append((doc.id, name))
        return result
