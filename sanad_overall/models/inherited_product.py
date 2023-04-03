from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float('Length')
    width = fields.Float('Width')
    barcode_type = fields.Selection([
        ('tools', 'Tools'),
        ('fg', 'FG'),
        ('rw', 'RW'),
        ('wip', 'WIP'),
    ], string='Type')
    barcode_type_value = fields.Char(compute="_compute_barcode_type_values")
    barcode_sequence = fields.Char()

    def generate_barcode(self):
        for rec in self:
            if rec.barcode_type == 'tools':
                seq = self.env['ir.sequence'].next_by_code('product.template.tools.seq')
                rec.update({
                    'barcode_sequence': seq,
                    'barcode': rec.barcode_type_value + seq
                })
            elif rec.barcode_type == 'fg':
                seq = self.env['ir.sequence'].next_by_code('product.template.fg.seq')
                rec.update({
                    'barcode_sequence': seq,
                    'barcode': rec.barcode_type_value + seq
                })
            elif rec.barcode_type == 'rw':
                seq = self.env['ir.sequence'].next_by_code('product.template.rw.seq')
                rec.update({
                    'barcode_sequence': seq,
                    'barcode': rec.barcode_type_value + seq
                })
            elif rec.barcode_type == 'wip':
                seq = self.env['ir.sequence'].next_by_code('product.template.wip.seq')
                rec.update({
                    'barcode_sequence': seq,
                    'barcode': rec.barcode_type_value + seq
                })

    # @api.onchange('barcode_type')
    # def _onchange_barcode_type(self):
    #     for rec in self:
    #         if rec.barcode_type == 'tools':
    #             seq = self.env['ir.sequence'].search(
    #                 [('name', '=', 'Type Tools')])
    #             self.env['ir.sequence'].next_by_code(seq.code)
    #             number = 0
    #             if len(str(seq.number_next_actual)) == 1:
    #                 number = f'00000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 2:
    #                 number = f'0000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 3:
    #                 number = f'000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 4:
    #                 number = f'00{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 5:
    #                 number = f'0{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 6:
    #                 number = str(seq.number_next_actual)
    #             if number:
    #                 rec.barcode_sequence = number
    #         elif rec.barcode_type == 'fg':
    #             seq = self.env['ir.sequence'].search(
    #                 [('name', '=', 'Type FG')])
    #             self.env['ir.sequence'].next_by_code(seq.code)
    #             number = 0
    #             if len(str(seq.number_next_actual)) == 1:
    #                 number = f'00000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 2:
    #                 number = f'0000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 3:
    #                 number = f'000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 4:
    #                 number = f'00{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 5:
    #                 number = f'0{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 6:
    #                 number = str(seq.number_next_actual)
    #             if number:
    #                 rec.barcode_sequence = number
    #         elif rec.barcode_type == 'wr':
    #             seq = self.env['ir.sequence'].search(
    #                 [('name', '=', 'Type WR')])
    #             self.env['ir.sequence'].next_by_code(seq.code)
    #             number = 0
    #             if len(str(seq.number_next_actual)) == 1:
    #                 number = f'00000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 2:
    #                 number = f'0000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 3:
    #                 number = f'000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 4:
    #                 number = f'00{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 5:
    #                 number = f'0{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 6:
    #                 number = str(seq.number_next_actual)
    #             if number:
    #                 rec.barcode_sequence = number
    #         elif rec.barcode_type == 'wip':
    #             seq = self.env['ir.sequence'].search(
    #                 [('name', '=', 'Type WIP')])
    #             self.env['ir.sequence'].next_by_code(seq.code)
    #             number = 0
    #             if len(str(seq.number_next_actual)) == 1:
    #                 number = f'00000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 2:
    #                 number = f'0000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 3:
    #                 number = f'000{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 4:
    #                 number = f'00{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 5:
    #                 number = f'0{str(seq.number_next_actual)}'
    #             elif len(str(seq.number_next_actual)) == 6:
    #                 number = str(seq.number_next_actual)
    #             if number:
    #                 rec.barcode_sequence = number

    @api.depends('barcode_type')
    def _compute_barcode_type_values(self):
        for rec in self:
            if rec.barcode_type == 'tools':
                rec.barcode_type_value = '20'
            elif rec.barcode_type == 'fg':
                rec.barcode_type_value = '6'
            elif rec.barcode_type == 'rw':
                rec.barcode_type_value = '18'
            elif rec.barcode_type == 'wip':
                rec.barcode_type_value = '23'
            else:
                rec.barcode_type_value = ''
