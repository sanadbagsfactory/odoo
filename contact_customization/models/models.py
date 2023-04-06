from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RespartnerInheritModel(models.Model):
    _inherit = 'res.partner'

    check_ktva = fields.Boolean(default=False)
    check_vat_cr = fields.Boolean(default=False)
    state = fields.Selection([
        ('create', 'Create'),
        ('confirm', 'Confirm'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
    ], default='create')

    def action_create(self):
        self.state = 'create'

    def action_confirm(self):
        self.state = 'confirm'
        if self.state == 'confirm':
            todos = {
                'res_id': self.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'res.partner')]).id,
                'user_id': self.env.user.search([('login', '=', 'azeem.anwar@sanadbags.com')]).id,
                'summary': f'New Vendor is confirmed {self.name}',
                'note': 'New Vendor is confirmed',
                # 'activity_type_id': 4,
                'date_deadline': datetime.now(),
            }
            if self.env.user.search([('login', '=', 'azeem.anwar@sanadbags.com')]).id:
                self.env['mail.activity'].sudo().create(todos)
            else:
                raise ValidationError('This email does not exist (azeem.anwar@sanadbags.com)')
    def action_cancel(self):
        self.state = 'cancel'
        todos = {
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'res.partner')]).id,
            'user_id': self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id,
            'summary': f'New vendor approval is rejected {self.name}',
            'note': 'New vendor approval is Rejected',
            # 'activity_type_id': 4,
            'date_deadline': datetime.now(),
        }
        if self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id:
            self.env['mail.activity'].sudo().create(todos)
        else:
            raise ValidationError('This email does not exist (baashar.mohammed@sanadbags.com)')
        self.env['mail.activity'].sudo().create(todos)

    def action_approve(self):
        self.state = 'approve'
        if self.state == 'approve':
            todos = {
                'res_id': self.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'res.partner')]).id,
                'user_id': self.env.user.search([('login', '=', 'asif.javaed@sanadbags.com')]).id,
                'summary': f'New Vendor is Approved {self.name}',
                'note': 'New Vendor is Approved',
                # 'activity_type_id': 4,
                'date_deadline': datetime.now(),
            }
            if self.env.user.search([('login', '=', 'asif.javaed@sanadbags.com')]).id:
                self.env['mail.activity'].sudo().create(todos)
            else:
                raise ValidationError('This email does not exist (asif.javaed@sanadbags.com)')

            self.env['mail.activity'].sudo().create(todos)


    @api.onchange('country_id')
    def _onchange_country(self):
        if self.country_id.name == 'Saudi Arabia':
            self.loc = 'domestic'
            self.check_ktva = True
        else:
            self.loc = 'international'
            self.check_ktva = False

    @api.onchange('loc')
    def _onchange_loc(self):
        if self.loc == 'domestic':
            self.check_ktva = True
        else:
            self.check_ktva = False

    @api.onchange('company_type', 'country_id', 'loc')
    def _onchange_company(self):
        if self.loc == 'international' and self.company_type == 'person':
            self.check_vat_cr = True
        else:
            self.check_vat_cr = False


    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if self.env.user.has_group('contact_customization.view_security_group'):
            raise ValidationError('Your are not allowed to create contact !')
        if res:
            todos = {
                'res_id': res.id,
                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'res.partner')]).id,
                'user_id': self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id,
                'summary': f'New Vendor is confirmed {res.name}',
                'note': 'New Vendor is confirmed',
                'date_deadline': datetime.now(),
            }
            if self.env.user.search([('login', '=', 'baashar.mohammed@sanadbags.com')]).id:
                self.env['mail.activity'].sudo().create(todos)
            else:
                raise ValidationError('This email does not exist (baashar.mohammed@sanadbags.com)')

            self.env['mail.activity'].sudo().create(todos)
        return res


    def write(self, vals_list):
        res = super().write(vals_list)
        if self.env.user.has_group('contact_customization.view_security_group'):
            raise ValidationError('Your are not allowed to create contact !')
        return res
