# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    employee = fields.Many2one('hr.employee', string='Employee')
    employee_id = fields.Char('Employee ID')
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    is_required = fields.Boolean('Is Required', related='account_id.is_required')

    @api.onchange('employee')
    def on_employee_change(self):
        for rec in self:
            if rec.employee:
                rec.employee_id = rec.employee.barcode
            else:
                rec.employee_id = ''
