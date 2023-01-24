from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DepartmentDocumentType(models.Model):
    _name = 'department.document.type'
    _rec_name = 'department_type'

    department_type = fields.Selection([
        ('ops', 'Operations'),
        ('prd', 'Production'),
        ('pur', 'Procurement'),
        ('whu', 'Warehousing'),
        ('mtn', 'Maintenance'),
        ('qlt', 'Quality'),
        ('qau', 'Quality Assurance'),
        ('qcu', 'Quality Control'),
        ('hse', 'HSE'),
        ('ssd', 'Support Services'),
        ('acc', 'Accounting'),
        ('hru', 'Human Resources'),
        ('gau', 'Government Affairs'),
        ('cru', 'Customer Relations'),
        ('itu', 'Information Technology'),
        ('cpl', 'Compliance'),
    ], string='Department')
    dept_short_form = fields.Char('Short Form', compute='_compute_dept_short_form')
    document_type = fields.Selection([
        ('1', 'Policy'),
        ('2', 'Procedure'),
        ('3', 'Work Instructions'),
        ('3', 'Work Instructions'),
        ('4', 'Forms'),
        ('5', 'Other'),
    ], string='Document Type')
    doc_short_form = fields.Char('Short Form', compute='_compute_doc_short_form')
    doc_no = fields.Char('Doc No', compute='_compute_doc_no')
    approved_on = fields.Date('Approved On')
    revision = fields.Char('Revision')
    notes = fields.Char('Note', size=50)

    @api.depends('department_type')
    def _compute_dept_short_form(self):
        for rec in self:
            if rec.department_type:
                rec.dept_short_form = rec.department_type.upper()
            else:
                rec.dept_short_form = ''

    @api.depends('document_type')
    def _compute_doc_short_form(self):
        for rec in self:
            if rec.document_type:
                rec.doc_short_form = rec.document_type
            else:
                rec.doc_short_form = ''

    @api.depends('dept_short_form', 'doc_short_form')
    def _compute_doc_no(self):
        for rec in self:
            if rec.dept_short_form and rec.doc_short_form:
                rec.doc_no = f'{rec.dept_short_form}-{rec.doc_short_form}001'
            else:
                rec.doc_no = ''

    @api.model
    def create(self, vals):
        res = super(DepartmentDocumentType, self).create(vals)
        if res.department_type and res.document_type:
            records = self.env['department.document.type'].search(
                [('department_type', '=', res.department_type), ('document_type', '=', res.document_type)])
            if len(records) > 1:
                raise UserError('This Type of Document Already Exists')
        return res

    @api.constrains('document_type', 'doc_no', 'department_type')
    def check_duplicate_document(self):
        for rec in self:
            if rec.document_type or rec.department_type or rec.doc_no:
                records = self.env['department.document.type'].search(
                    [('department_type', '=', rec.department_type), ('document_type', '=', rec.document_type)])
                print(records)
                if len(records) > 1:
                    raise UserError('This Type of Document Already Exists')
