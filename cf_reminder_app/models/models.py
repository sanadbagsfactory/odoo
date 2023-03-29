# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class CfReminderApp(models.Model):
    _name = 'cf.reminder.app'
    _description = 'cf_reminder_app.cf_reminder_app'

    @api.model
    def send_reminder_emails(self):
        print('send_reminder_emails')
        today = datetime.now().date()
        print(today)
        partners = self.env['res.partner'].search([])
        if expired_partners := partners.filtered(
                lambda p: p.cr_expiry_date <= today if p.cr_expiry_date else None
        ):
            subject = 'Your CR date has expired'
            print(subject)
            print(expired_partners)
            data_dict = {}
            for partner in expired_partners:
                data_dict[partner.id] = partner.name
                body = f'Dear {partner.name},\n\nYour CR date has expired. Please renew your CR status as soon as possible.\n\nBest regards,\n\nThe Odoo team'
                mail_values = {
                    'subject': subject,
                    'body_html': body,
                    'email_to': partner.email,
                }
                if mail := self.env['mail.mail'].create(mail_values):
                    mail.send()
            if (
                    self.env.user.has_group('account.group_account_manager')
                    or self.env.user.has_group('account.group_account_user')
            ):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('CR Expired'),
                        'message': f'Following users CR date has been expired:\n {data_dict}',
                        'type': 'danger',  # types: success,warning,danger,info
                        'sticky': True,  # True/False will display for few seconds if false
                    },
                }
