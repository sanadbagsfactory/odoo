from odoo import models, fields, api, _


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    seq_code = fields.Char('Code')


class ResUser(models.Model):
    _inherit = 'res.users'
    department_ids = fields.Many2many('hr.department')
