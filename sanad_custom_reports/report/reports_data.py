from odoo import models, api, fields


class InsuranceClaimWizardReport(models.AbstractModel):
    _name = 'report.sanad_custom_reports.report_purchase_quote_temp'
    _description = 'Quotation / Purchase'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        print(docs)
        print(self.env.context)
        print(docs.company_id)
        header_data = self.env['department.document.type'].search(
            [('department_type', '=', 'pur'), ('document_type', '=', '4')])
        print(header_data)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'header_data': header_data
        }
