# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError
from lxml import etree
from odoo.tools.float_utils import float_compare

from odoo.exceptions import UserError


# from doc._extensions.pyjsparser.parser import true

class MaterialPurchaseRequisition(models.Model):
    _name = 'material.purchase.requisition'
    _description = 'Purchase Requisition'
    # _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']  # odoo11
    _order = 'id desc'

    # @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel', 'reject'):
                raise UserError(
                    _('You can not delete Purchase Requisition which is not in draft or cancelled or rejected state.'))
        return super(MaterialPurchaseRequisition, self).unlink()

    name = fields.Char(
        string='Number',
        index=True,
        readonly=1,
    )
    state = fields.Selection([
        ('draft', 'New'),
        ('dept_confirm', 'Waiting Department Approval'),
        ('ir_approve', 'Waiting Finance Approval'),
        ('approve', 'Approved'),
        ('stock', 'RFQ Created'),
        ('picking', 'Internal Picking Created'),
        ('po_pick', 'RFQ/IP Created'),
        ('receive', 'Received'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected')],
        default='draft',
        track_visibility='onchange',
    )
    request_date = fields.Date(
        string='Requisition Date',
        default=fields.Date.today(),
        required=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        copy=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        copy=True,
    )
    approve_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager',
        readonly=True,
        copy=False,
    )
    reject_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager Reject',
        readonly=True,
    )
    approve_employee_id = fields.Many2one(
        'hr.employee',
        string='Approved by',
        readonly=True,
        copy=False,
    )
    reject_employee_id = fields.Many2one(
        'hr.employee',
        string='Rejected by',
        readonly=True,
        copy=False,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True,
        copy=True,
    )
    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        copy=True,
    )
    requisition_line_ids = fields.One2many(
        'material.purchase.requisition.line',
        'requisition_id',
        string='Purchase Requisitions Line',
        copy=True,
    )
    date_end = fields.Date(
        string='Requisition Deadline',
        readonly=True,
        help='Last date for the product to be needed',
        copy=True,
    )
    date_done = fields.Date(
        string='Date Done',
        readonly=True,
        help='Date of Completion of Purchase Requisition',
    )
    managerapp_date = fields.Date(
        string='Department Approval Date',
        readonly=True,
        copy=False,
    )
    manareject_date = fields.Date(
        string='Department Manager Reject Date',
        readonly=True,
    )
    userreject_date = fields.Date(
        string='Rejected Date',
        readonly=True,
        copy=False,
    )
    userrapp_date = fields.Date(
        string='Approved Date',
        readonly=True,
        copy=False,
    )
    receive_date = fields.Date(
        string='Received Date',
        readonly=True,
        copy=False,
    )
    reason = fields.Text(
        string='Reason for Requisitions',
        required=False,
        copy=True,
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        copy=True,
    )
    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=False,
        copy=True,
    )
    delivery_picking_id = fields.Many2one(
        'stock.picking',
        string='Internal Picking',
        readonly=True,
        copy=False,
    )
    requisiton_responsible_id = fields.Many2one(
        'hr.employee',
        string='Requisition Responsible',
        copy=True,
    )
    employee_confirm_id = fields.Many2one(
        'hr.employee',
        string='Confirmed by',
        readonly=True,
        copy=False,
    )
    confirm_date = fields.Date(
        string='Confirmed Date',
        readonly=True,
        copy=False,
    )

    dept_manager = fields.Boolean(string="dept manager", default=True, compute="allow_edit_line")
    aprove_state_edit_check = fields.Boolean(string="Approve state edit", default=True)
    edit_pick_detail = fields.Boolean(string="edit picking details at draft and approve state", default=True)

    purchase_order_ids = fields.One2many(
        'purchase.order',
        'custom_requisition_id',
        string='Purchase Ordes',
    )
    custom_picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Picking Type',
        copy=False,
    )

    picking_count = fields.Integer(compute='compute_pick_count')
    po_count = fields.Integer(compute='compute_po_count')
    po_confirmed = fields.Boolean(compute='get_po_status', default=False)
    pick_confirmed = fields.Boolean(compute='get_pick_status', default=False)
    requi_act_po = fields.Boolean('requisition action po', default=False, compute="onchange_requistion_type_action")
    requi_act_ip = fields.Boolean('requisition action ip', default=False)

    requi_act_ip_po = fields.Boolean('requisition action ip/po', default=False)

    # @api.depends('requisition_line_ids.requisition_type')
    def onchange_requistion_type_action(self):
        for rec in self:
            rec.requi_act_po = False
            rec.requi_act_ip = False
            if rec.requisition_line_ids:
                requi_type_in_line = rec.requisition_line_ids.mapped('requisition_type')
                if 'internal' in rec.requisition_line_ids.mapped(
                        'requisition_type') and 'purchase' in rec.requisition_line_ids.mapped('requisition_type'):
                    rec.requi_act_ip_po = True
                else:
                    if rec.requisition_line_ids[0].requisition_type:
                        if rec.requisition_line_ids[0].requisition_type == 'purchase':
                            rec.requi_act_po = True
                        #
                        if rec.requisition_line_ids[0].requisition_type == 'internal':
                            rec.requi_act_ip = True

    #
    #                 for line in rec.requisition_line_ids:
    #                     if line.requisition_type:
    #                         if line.requisition_type == 'purchase':
    #                             rec.requi_act_po = True
    #                         elif line.requisition_type == 'internal':
    #                             rec.requi_act_ip = True

    def get_po_status(self):
        for rec in self:

            requi_po = rec.env['purchase.order'].search([('origin', '=', rec.name)])
            requi_po_state = requi_po.filtered(lambda r: r.state == 'purchase')
            if ((rec.env.user.has_group('material_purchase_requisitions.group_create_requisition')) and not (
                    rec.env.user.has_group(
                        'material_purchase_requisitions.group_purchase_requisition_manager') or rec.env.user.has_group(
                'material_purchase_requisitions.group_purchase_requisition_user') or rec.env.user.has_group(
                'material_purchase_requisitions.group_purchase_requisition_department')) and (
                    rec.state == 'stock' or rec.state == 'picking' or rec.state == 'po_pick')):
                if len(requi_po) >= 1:
                    if len(requi_po) == len(requi_po_state):
                        rec.po_confirmed = True
                    else:
                        rec.po_confirmed = False
                else:
                    rec.po_confirmed = False
            else:
                rec.po_confirmed = False

    def get_pick_status(self):
        try:
            for rec in self:
                requi_pick = rec.env['stock.picking'].search([('origin', '=', rec.name)])
                requi_pick_state = requi_pick.filtered(lambda r: r.state == 'done')
                if ((rec.env.user.has_group('material_purchase_requisitions.group_create_requisition')) and not (
                        rec.env.user.has_group(
                            'material_purchase_requisitions.group_purchase_requisition_manager') or rec.env.user.has_group(
                    'material_purchase_requisitions.group_purchase_requisition_user') or rec.env.user.has_group(
                    'material_purchase_requisitions.group_purchase_requisition_department') or rec.env.user.has_group(
                    'material_purchase_requisitions.group_store_keeper')) and (
                        rec.state == 'stock' or rec.state == 'picking' or rec.state == 'po_pick')):
                    if len(requi_pick) >= 1:
                        if len(requi_pick) == len(requi_pick_state):
                            rec.pick_confirmed = True
                        else:
                            rec.pick_confirmed = False
                    else:
                        rec.pick_confirmed = False
                else:
                    rec.pick_confirmed = False
        except Exception as e:
            print(e)
            raise e

    def compute_pick_count(self):
        for rec in self:
            order_count = self.env['stock.picking'].search_count([('custom_requisition_id.id', '=', rec.id)])
            if order_count >= 1:
                rec.picking_count = order_count
            else:
                rec.picking_count = 0

    def compute_po_count(self):
        for rec in self:
            order_count = self.env['purchase.order'].search_count([('custom_requisition_id.id', '=', rec.id)])
            rec.po_count = order_count

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('purchase.requisition.seq')
        vals.update({
            'name': name
        })
        res = super(MaterialPurchaseRequisition, self).create(vals)
        return res

    # @api.multi
    def requisition_confirm(self):
        for rec in self:
            manager_mail_template = self.env.ref(
                'material_purchase_requisitions.email_confirm_material_purchase_requistion')
            rec.employee_confirm_id = rec.employee_id.id
            rec.confirm_date = fields.Date.today()
            rec.state = 'dept_confirm'
            if rec.env.user.has_group(
                    'material_purchase_requisitions.group_create_requisition') and not rec.env.user.has_group(
                'material_purchase_requisitions.group_purchase_requisition_department'):
                rec.aprove_state_edit_check = False
            if manager_mail_template:
                manager_mail_template.send_mail(self.id)

    # @api.multi
    def requisition_reject(self):
        for rec in self:
            rec.state = 'reject'
            rec.reject_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.userreject_date = fields.Date.today()

    # @api.multi
    def manager_approve(self):
        # for rec in self:
        requis = self.requisition_line_ids.filtered(lambda r: r.requisition_type == False)
        if requis:
            raise UserError(_('please select requisition action!'))
        else:
            self.managerapp_date = fields.Date.today()
            self.approve_manager_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            employee_mail_template = self.env.ref(
                'material_purchase_requisitions.email_purchase_requisition_iruser_custom')
            email_iruser_template = self.env.ref('material_purchase_requisitions.email_purchase_requisition')
            employee_mail_template.sudo().send_mail(self.id)
            email_iruser_template.sudo().send_mail(self.id)
            # flag = False
            # for line in rec.requisition_line_ids:
            #     if line.requisition_type == 'purchase':
            #         flag = True
            # if flag:
            #     rec.state = 'ir_approve'
            # else:
            self.state = 'approve'

    #                 if rec.requisition_line_ids[0].requisition_type:
    #                     if rec.requisition_line_ids[0].requisition_type == 'internal':
    #                         rec.state = 'approve'
    #                     else:
    #                         rec.state = 'ir_approve'

    # @api.multi
    def user_approve(self):
        for rec in self:
            rec.userrapp_date = fields.Date.today()
            rec.approve_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.state = 'approve'

    def user_not_approve(self):
        for rec in self:
            #             rec.userrapp_date = fields.Date.today()
            #             rec.approve_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.state = 'dept_confirm'

    # @api.multi
    def reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def _prepare_pick_vals(self, line=False, stock_id=False):
        pick_vals = {
            'product_id': line.product_id.id,
            'product_uom_qty': line.qty,
            'product_uom': line.uom.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.dest_location_id.id,
            'name': line.product_id.name,
            'picking_type_id': self.custom_picking_type_id.id,
            'picking_id': stock_id.id,
            'custom_requisition_line_id': line.id,
            'company_id': line.requisition_id.company_id.id,
        }
        return pick_vals

    @api.model
    def _prepare_po_line(self, line=False, purchase_order=False):
        po_line_vals = {
            'product_id': line.product_id.id,
            'name': line.product_id.name,
            'product_qty': line.qty / line.product_id.uom_po_id.factor_inv,
            'product_uom': line.product_id.uom_po_id.id,
            'date_planned': fields.Date.today(),
            'price_unit': line.product_id.standard_price,
            'order_id': purchase_order.id,
            # 'account_analytic_id': self.analytic_account_id.id,
            'custom_requisition_line_id': line.id
        }
        return po_line_vals

    def request_stock1(self):
        for rec in self:
            rec.request_stock()
            rec.state = 'picking'

    # @api.multi
    def request_stock(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        # internal_obj = self.env['stock.picking.type'].search([('code','=', 'internal')], limit=1)
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        #         if not internal_obj:
        #             raise UserError(_('Please Specified Internal Picking Type.'))
        pur = -1
        for rec in self:
            if not rec.requisition_line_ids:
                raise UserError(_('Please create some requisition lines.'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                    raise UserError(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                    raise UserError(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise UserError(_('Select Destination location under the picking details.'))
                #                 if not rec.employee_id.dest_location_id.id or not rec.employee_id.department_id.dest_location_id.id:
                #                     raise UserError(_('Select Destination location under the picking details.'))
                picking_vals = {
                    'partner_id': rec.employee_id.sudo().address_home_id.id,
                    # 'min_date' : fields.Date.today(),
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                    'picking_type_id': rec.custom_picking_type_id.id,
                    'note': rec.reason,
                    'custom_requisition_id': rec.id,
                    'origin': rec.name,
                    'company_id': rec.company_id.id,
                }
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {
                    'delivery_picking_id': stock_id.id,
                }
                rec.write(delivery_vals)

            po_dict = {}
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'internal':
                    pick_vals = rec._prepare_pick_vals(line, stock_id)
                    move_id = move_obj.sudo().create(pick_vals)
                # else:
                if line.requisition_type == 'purchase':  # 10/12/2019
                    if not line.partner_id:
                        raise UserError(
                            _('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
                    for partner in line.partner_id:
                        if partner not in po_dict:
                            po_vals = {
                                'partner_id': partner.id,
                                'currency_id': rec.env.user.company_id.currency_id.id,
                                'date_order': fields.Date.today(),
                                #                                'company_id':rec.env.user.company_id.id,
                                'company_id': rec.company_id.id,
                                'custom_requisition_id': rec.id,
                                'origin': rec.name,
                                'user_id': self.env.user.id,
                            }
                            purchase_order = purchase_obj.create(po_vals)
                            # pur = purchase_order
                            po_dict.update({partner: purchase_order})
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            #                            {
                            #                                     'product_id': line.product_id.id,
                            #                                     'name':line.product_id.name,
                            #                                     'product_qty': line.qty,
                            #                                     'product_uom': line.uom.id,
                            #                                     'date_planned': fields.Date.today(),
                            #                                     'price_unit': line.product_id.lst_price,
                            #                                     'order_id': purchase_order.id,
                            #                                     'account_analytic_id': rec.analytic_account_id.id,
                            #                            }
                            purchase_line_obj.sudo().create(po_line_vals)
                            pur = purchase_line_obj
                        else:
                            purchase_order = po_dict.get(partner)
                            pur = purchase_order
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            #                            po_line_vals =  {
                            #                                 'product_id': line.product_id.id,
                            #                                 'name':line.product_id.name,
                            #                                 'product_qty': line.qty,
                            #                                 'product_uom': line.uom.id,
                            #                                 'date_planned': fields.Date.today(),
                            #                                 'price_unit': line.product_id.lst_price,
                            #                                 'order_id': purchase_order.id,
                            #                                 'account_analytic_id': rec.analytic_account_id.id,
                            #
                            #                            }
                            check = False
                            for p_line in purchase_order.order_line:
                                if p_line.product_id.id == line.product_id.id:
                                    p_line.product_qty = (
                                                                     line.qty / line.product_id.uom_po_id.factor_inv) + p_line.product_qty
                                    check = True
                            if not check:
                                purchase_line_obj.sudo().create(po_line_vals)
            if rec.requi_act_ip_po == True:
                rec.state = 'po_pick'
            else:
                rec.state = 'stock'
        if pur != -1:
            if pur:
                for u_rec in pur.order_line:
                    u_rec.product_qty = math.ceil(round(u_rec.product_qty, 2))

    # @api.multi
    def action_received(self):
        for rec in self:
            rec.receive_date = fields.Date.today()
            rec.state = 'receive'

    #             rec.po_confirmed= False
    #             rec.pick_confirmed= False
    # @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.onchange('employee_id')
    def set_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.sudo().department_id.id
            rec.dest_location_id = rec.employee_id.sudo().dest_location_id.id or rec.employee_id.sudo().department_id.dest_location_id.id

            # @api.multi

    def show_picking(self):
        for rec in self:
            res = self.env.ref('stock.action_picking_tree_all')
            res = res.read()[0]
            res['domain'] = str([('custom_requisition_id', '=', rec.id)])
            res['context'] = "{'create': False}"
        return res

    # @api.multi
    def action_show_po(self):
        for rec in self:
            purchase_action = self.env.ref('purchase.purchase_rfq')
            purchase_action = purchase_action.read()[0]
            purchase_action['domain'] = str([('custom_requisition_id', '=', rec.id)])
            #             purchase_action['context']= "{'create': False, 'edit':False}"
            purchase_action['context'] = "{'create': False}"
        return purchase_action

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(MaterialPurchaseRequisition, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                                          toolbar=toolbar,
                                                                          submenu=submenu)
        if not self.env.user.has_group('material_purchase_requisitions.group_create_requisition'):
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('edit', '0')
            result['arch'] = etree.tostring(temp)
        #         if self.env.user.has_group('approval_so_po.group_contact_user'):
        #             temp = etree.fromstring(result['arch'])
        #             temp.set('delete', '0')
        #             temp.set('edit', '0')
        #             temp.set('duplicate', '0')
        #             result['arch'] = etree.tostring(temp)
        #         doc = etree.XML(result['arch'])
        #         for node in doc.xpath("//field[@name='requisition_line_ids']"):
        #             #             if self._context['type'] in ('in_invoice', 'in_refund'):
        #             #                 # Hack to fix the stable version 8.0 -> saas-12
        #             #                 # purchase_ok will be moved from purchase to product in master #13271
        #             #                 if 'purchase_ok' in self.env['product.template']._fields:
        #             #                     node.set('domain', "[('purchase_ok', '=', True)]")
        #             #             else:
        #             # node.set('domain', "[('company_id', '=', compny_a)]")
        #             if self.env.user.has_group('material_purchase_requisitions.group_purchase_requisition_department'):
        #                 node.set('readonly', '1')
        #
        #
        #                 result['arch'] = etree.tostring(doc)
        # return res
        return result

    def allow_edit_line(self):
        #         for rec in self:
        #             if rec.state == 'dept_confirm':
        #                 if rec.env.user.has_group('material_purchase_requisitions.group_purchase_requisition_department') and rec.state == 'dept_confirm':
        #                     rec.dept_manager =True
        #                 else:
        #                     rec.dept_manager =False
        #
        #             elif rec.state == 'draft':
        #                     rec.dept_manager = True
        #             elif rec.state == 'approve':
        #                 rec.dept_manager = True
        #
        #             else:
        #                 rec.dept_manager = False

        for rec in self:
            if rec.state == 'dept_confirm':
                if rec.env.user.has_group(
                        'material_purchase_requisitions.group_purchase_requisition_department') and rec.state == 'dept_confirm':
                    rec.dept_manager = True
                    rec.edit_pick_detail = False
                else:
                    rec.dept_manager = False
                    rec.edit_pick_detail = False

            elif rec.state == 'draft':
                rec.dept_manager = True
                rec.edit_pick_detail = False
            elif rec.state == 'approve':
                if rec.env.user.has_group(
                        'material_purchase_requisitions.group_purchase_requisition_manager') or rec.env.user.has_group(
                    'material_purchase_requisitions.group_store_keeper'):
                    rec.dept_manager = True
                    rec.aprove_state_edit_check = True

                    if rec.env.user.has_group('material_purchase_requisitions.group_store_keeper'):
                        if rec.requi_act_ip == True or rec.requi_act_ip_po == True:
                            rec.edit_pick_detail = True
                        else:
                            rec.edit_pick_detail = False
                else:
                    rec.dept_manager = False
                    rec.aprove_state_edit_check = False
                    rec.edit_pick_detail = False

            else:
                rec.dept_manager = False
                rec.aprove_state_edit_check = False
                rec.edit_pick_detail = False
