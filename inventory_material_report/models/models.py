from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'



# class MaterialReceiving(models.AbstractModel):
#     _name = 'report.inventory_material_report.voucher_temp_id'
#
#
#     def _get_report_values(self, docids, data=None):
#
#         doc = self.env['department.document.type'].search([('department_type', '=', 'whu'),('document_type', '=', '4')])
#
#         return {
#             'document_type': 'Forms' if doc.document_type == '4' else None,
#             'approved_on': doc.approved_on if doc.approved_on else None,
#             'department_type': 'Warehousing' if doc.department_type == 'whu' else None,
#             'revision': doc.revision if doc.revision else None,
#             'notes': doc.notes if doc.notes else None,
#
#             'docs': self.env['stock.picking'].browse(docids)
#         }