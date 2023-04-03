# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    employee_id = fields.Many2one('hr.employee', string='Employee')

    @api.onchange('employee_id')
    def _on_employee_id_change(self):
        for rec in self:
            if rec.employee_id:
                for line in rec.line_ids:
                    line.employee = rec.employee_id


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    employee = fields.Many2one('hr.employee', string='Employee')
    employee_id = fields.Char('Employee ID', related='employee.barcode')
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    is_required = fields.Boolean('Is Required', related='account_id.is_required')
