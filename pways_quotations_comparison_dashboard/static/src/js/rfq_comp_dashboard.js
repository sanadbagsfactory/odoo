odoo.define('pways_quotations_comparison_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var session = require('web.session');
var utils = require('web.utils');
var _t = core._t;
var time = require('web.time');
var QWeb = core.qweb;
var Widget = require('web.Widget');
const { loadBundle } = require('@web/core/assets');
const {setCookie} = require('web.utils.cookies');
const {getCookie} = require('web.utils.cookies');
var rpc = require('web.rpc');

var RFQDashboard = AbstractAction.extend({
    template: 'RFQDashboard',
    events: {
        'click  .remove_line': '_remove_line',
/*        'click  .show_product': '_show_product',*/
        'click  .conform_order': '_conform_order',
        'change #selection_type': 'onChangeSelectionType',
        'click  .back_button': '_back_button',
    },
    init: function(parent, options) {
        this._super(parent, options);
        this.reqisition_id = options.context.reqisition_id;
        this.purchase_ids = [];
        this.select_type = "";
        if (!this.reqisition_id)
        {
            this.reqisition_id = parseInt(getCookie('id'));
        }
    },

    willStart: function() {
        var self = this;
        return Promise.all([loadBundle(this), this._super()]).then(function() {
            return self.fetch_data();
        });
    },
    fetch_data: function () {
        var self = this;
        var def1 =  this._rpc({
            model: 'purchase.comparison',
            method: 'get_purchase_line_data',
            args: [this.select_type, this.reqisition_id],
        }).then(function(result) {
            self.purchase_ids = result
        });
        return $.when(def1);
    },
    onChangeSelectionType: function(events) {
        var self = this;
        var option = $(events.target).val();
        this.select_type = option
        var def1 =  this._rpc({
            model: 'purchase.comparison',
            method: 'get_purchase_line_data',
            args: [option, self.reqisition_id],
            }).then(function(result) {
                self.purchase_ids = result;
                self.render_dashboards(
                    result, 
                    result.record_line_ids, 
                    result.partner_ids, 
                    result.total, 
                    result.length, 
                    result.option, 
                    result.min_total_vendor, 
                    result.min_delivery_vendor,
                    result.reqisition_name,
                    result.price_order_line_ids,
                    result.date_order_line_ids,
                );
            });
        return $.when(def1);
    },
    _conform_order:function () {
        var self = this;
        var id = $(event.target).attr("data-id");
        return rpc.query({
            model: 'purchase.comparison',
            method: 'confirm_order_action',
            args: [parseInt(id), self.reqisition_id],
        }).then(function(result) {
            var action = {
                'name': 'Dashboard',
                'type': 'ir.actions.client',
                'tag': 'compare_dashboard',
                'context': {'reqisition_id': self.reqisition_id},
            };

            return self.do_action(action);
        });
    },
    _back_button: function () {
        var self = this;
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: 'purchase.comparison',
            res_id: parseInt(self.reqisition_id),
            views: [[false, 'form']],
            target: 'current'
        });
    },
    _remove_line: function () {
        var self = this;
        $(".remove_line").click(function() {
            var gen = $(this).attr("data-id");
            return rpc.query({
                model: 'purchase.comparison',
                method: 'remove_line_action',
                args: [gen, self.reqisition_id],
            }).then(function(result) {
                var action = {
                    'name': 'Dashboard',
                    'type': 'ir.actions.client',
                    'tag': 'compare_dashboard',
                    'context': {'reqisition_id': self.reqisition_id},
                };
                return self.do_action(action);
            });
        });
    },
    start: function() {
        setCookie("id", this.reqisition_id);
        var self = this;  
        return this._super().then(function() {
            self.render_dashboards(
                self.purchase_ids, 
                self.purchase_ids.record_line_ids, 
                self.purchase_ids.partner_ids, 
                self.purchase_ids.total, 
                self.purchase_ids.length, 
                self.purchase_ids.option, 
                self.purchase_ids.min_total_vendor, 
                self.purchase_ids.min_delivery_vendor, 
                self.purchase_ids.reqisition_name,
                self.purchase_ids.price_order_line_ids,
                self.purchase_ids.date_order_line_ids,
            );
        });
    },

    render_dashboards: function (res, record_line_ids, partner_ids, total, length, option, min_total_vendor, min_delivery_vendor, reqisition_name, price_order_line_ids, date_order_line_ids) {
        this.$('.o_rfq_dashboard').html(QWeb.render('RFQCompareTable', {
            widget: res, 
            'record_line_ids': record_line_ids, 
            'partner_ids': partner_ids, 
            'total': total, 
            'length': length, 
            'option': option, 
            'min_total_vendor': min_total_vendor, 
            'min_delivery_vendor': min_delivery_vendor, 
            'reqisition_name': reqisition_name,
            'price_order_line_ids': price_order_line_ids,
            'date_order_line_ids': date_order_line_ids,
        }));
    },
});

core.action_registry.add('compare_dashboard', RFQDashboard);

return RFQDashboard;

});
