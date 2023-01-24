# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
