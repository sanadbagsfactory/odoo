# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.department'

    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


# class User_rec_rules(models.Model):
#     _inherit="res.users"
#     
#     department_ids= fields.Many2many('hr.department', string="Allowed Departments")