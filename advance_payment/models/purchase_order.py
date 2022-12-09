from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Left Side
    payment_ref = fields.Char('Payment Reference')
    attendant = fields.Many2one('res.partner', 'Attendant')
    project_name = fields.Many2one('project.project', 'Project Name')
    project_shipment = fields.Char('Project Shipment')
    project_code = fields.Char('Project Code')
    po_no = fields.Char(string='PO No', compute='compute_po_no')
    po_type = fields.Selection([
        ('project', 'Project'),
        ('other', 'Other')
    ], string='PO Type')
    # Right Side
    sub_contractor = fields.Many2one('res.partner', 'Sub-Contractor')
    contract_order = fields.Char('Contract/Order')

    def _prepare_invoice(self, ):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals.update({
            'payment_reference': self.payment_ref,
            'attendant': self.attendant.id,
            'project_name': self.project_name.id,
            'project_shipment': self.project_shipment,
            'project_code': self.project_code,
            'po_no': self.id,
            'po_type': self.po_type,

            'confirmation_date': self.date_approve,
            'sub_contractor': self.sub_contractor.id,
            'contract_order': self.contract_order,
        })
        return invoice_vals

    @api.depends('order_line.invoice_lines.move_id')
    def compute_po_no(self):
        for order in self:
            invoices = order.mapped('order_line.invoice_lines.move_id')
            temp = ''
            for inv in invoices:
                temp += inv.name
                temp += ','
            order.po_no = temp.rstrip(',')


class PurchaseOrderLines(models.Model):
    _inherit = 'purchase.order.line'

    contract_per_amount = fields.Char('% Contract Amount', compute='_compute_contract_per_amount')
    # previous_percentage = fields.Char('Previous')
    # this_month_percentage = fields.Char('This Month')
    # total_percentage = fields.Char('Total')
    # percentage_total_amount = fields.Char('% Total Amount')

    @api.depends('price_unit', 'product_qty')
    def _compute_contract_per_amount(self):
        for rec in self:
            # print(rec.invoice_lines)
            # temp = [float(line.contract_per_amount.replace('%', '')) for line in rec.invoice_lines]
            # temp = sum(temp)
            # print(temp)
            if rec.price_unit or rec.product_qty or rec.order_id.amount_untaxed:
                try:
                    rec.contract_per_amount = f'{round((rec.price_unit / rec.order_id.amount_untaxed) * 100, 2)}%'
                    # rec.contract_per_amount = f'{round((rec.product_qty / rec.order_id.amount_untaxed) * 100, 2)}%'
                except:
                    rec.contract_per_amount = f'0.00%'
            else:
                rec.contract_per_amount = f'0.00%'
