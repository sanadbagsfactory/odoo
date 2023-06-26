from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'



class MaterialReceiving(models.AbstractModel):
    _name = 'report.inventory_material_report.voucher_temp_id'


    def _get_report_values(self, docids, data=None):

        return {
            'document_type': self.env['department.document.type'].search([('department_type', '=', 'whu'),('document_type', '=', '4')]),
            'docs': self.env['stock.picking'].browse(docids)
        }