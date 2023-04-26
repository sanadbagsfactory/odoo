# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    _description = 'RFQ'

    vendor_ids = fields.Many2many('res.partner', string='Vendors')
    tender_type = fields.Many2one('purchase.tender.type', string='Tender Type')
    email_ids = fields.Char('Email Ids', compute='_compute_email_ids')

    @api.depends('vendor_ids')
    def _compute_email_ids(self):
        for rec in self:
            if rec.vendor_ids:
                mails = [mail for mail in rec.vendor_ids.mapped('email') if mail != False]
                print(f"mails: {mails}")
                rec.email_ids = ','.join(mails)
                print(f"email_ids: {rec.email_ids}")
            else:
                rec.email_ids = None

    def send_email_btn(self):
        mails = [mail for mail in self.vendor_ids.mapped('email') if mail != False]
        print(f"mails: {mails}")
        final = ','.join(mails)
        print(f"email_ids: {final}")
        print('RFQ Email action called--------------------')
        '''
        This function opens a window to compose an email, with the edi RFQ template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        print(ir_model_data._xmlid_lookup('purchase_tender_management.email_template_rfq_custom'))
        try:
            template_id = ir_model_data._xmlid_lookup('purchase_tender_management.email_template_rfq_custom')[2]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.requisition',
            'active_model': 'purchase.requisition',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
            'force_email': True,
        })
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self.with_context(lang=lang)
        ctx['model_description'] = _('Request for Quotation')

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_in_progress(self):
        sup = super(PurchaseRequisition, self).action_in_progress()
        self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.rfq')
        return sup
