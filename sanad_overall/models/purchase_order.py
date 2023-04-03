from odoo import fields, models, api, _
from datetime import datetime, date


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('purchase.order.rfq.seq') or 'New'
        print(name)
        vals.update({
            'name': name
        })
        # current_year = date.today().year
        # print(f'current_year: {current_year}')
        # seq = self.env['ir.sequence'].search(
        #     [('name', '=', 'Purchase Order')])
        # self.env['ir.sequence'].next_by_code(seq.code)
        # number = 0
        # if len(str(seq.number_next_actual)) == 1:
        #     number = '00000' + str(seq.number_next_actual)
        # elif len(str(seq.number_next_actual)) == 2:
        #     number = '0000' + str(seq.number_next_actual)
        # elif len(str(seq.number_next_actual)) == 3:
        #     number = '000' + str(seq.number_next_actual)
        # elif len(str(seq.number_next_actual)) == 4:
        #     number = '00' + str(seq.number_next_actual)
        # elif len(str(seq.number_next_actual)) == 5:
        #     number = '0' + str(seq.number_next_actual)
        # elif len(str(seq.number_next_actual)) == 6:
        #     number = str(seq.number_next_actual)
        # if self.env.user.department_ids:
        #     code = self.env.user.department_ids[-1].seq_code
        #     if code:
        #         vals['name'] = str(current_year) + str(code) + str(number) or _(
        #       'New')
        #     else:
        #         vals['name'] = str(current_year) + str('UUU') + str(number) or _(
        #             'New')
        # else:
        #     vals['name'] = str(current_year) + str('UUU') + str(number) or _(
        #         'New')
        return super(PurchaseOrder, self).create(vals)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        current_year = date.today().year
        print(f'current_year: {current_year}')
        seq = self.env['ir.sequence'].search(
            [('name', '=', 'Purchase Order')])
        self.env['ir.sequence'].next_by_code(seq.code)
        number = 0
        if len(str(seq.number_next_actual)) == 1:
            number = '00000' + str(seq.number_next_actual)
        elif len(str(seq.number_next_actual)) == 2:
            number = '0000' + str(seq.number_next_actual)
        elif len(str(seq.number_next_actual)) == 3:
            number = '000' + str(seq.number_next_actual)
        elif len(str(seq.number_next_actual)) == 4:
            number = '00' + str(seq.number_next_actual)
        elif len(str(seq.number_next_actual)) == 5:
            number = '0' + str(seq.number_next_actual)
        elif len(str(seq.number_next_actual)) == 6:
            number = str(seq.number_next_actual)
        if self.env.user.department_ids:
            code = self.env.user.department_ids[-1].seq_code
            if code:
                self.name = str(current_year) + str(code) + str(number) or _(
                    'New')
            else:
                self.name = str(current_year) + str('UUU') + str(number) or _(
                    'New')
        else:
            self.name = str(current_year) + str('UUU') + str(number) or _(
                'New')
        return res