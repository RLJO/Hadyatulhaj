odoo.define('ess.portals', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.portalExpenses = publicWidget.Widget.extend({
        selector: '.o_portal_expense',
        events: {
            'change select[name="product_id"]': '_onProductChange',
        },
    
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);

            // this.call('notification', 'notify', {
            //     title: "zzzzzzzzzz",
            //     message: "data.message",
            //     sticky: false
            // });

            rpc.query({
                model: 'product.product',
                method: 'get_product_obj',
                args: [{
                    'id': this.$('select[name="product_id"]').val(),
                }]
            }).then(function (result) {
                $("#unit_amount").val(result);
            });
    
            return def;
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _adaptAddressForm: function () {
            // this.connectionNotificationID = this.displayNotification({
            //     type: 'info',
            //     title: _t('Connection lost'),
            //     message: _t('Trying to reconnect...'),
            //     sticky: false
            // });
            var self = this
            rpc.query({
                model: 'product.product',
                method: 'get_product_obj',
                args: [{
                    'id': this.$('select[name="product_id"]').val(),
                }]
            }).then(function (result) {
                $("#unit_amount").val(result);
            }); 
        },
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _onProductChange: function () {
            this._adaptAddressForm();
        },
    });
    

    publicWidget.registry.portalTraining = publicWidget.Widget.extend({
        selector: '.o_portal_trainingt',
        events: {
            'change select[name="course_name"]': '_onCourseChange',
        },
    
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);  
            
            rpc.query({
                model: 'course.schedule',
                method: 'get_course_obj',
                args: [{
                    'id': this.$('select[name="course_name"]').val(),
                    'employee_id': document.getElementById("employee_id").value,
                }]
            }).then(function (result) {
            if (result){
                $("#duration").val(result.duration);
                $("#f_date").val(result.f_date);
                $("#to_date").val(result.to_date);
                $("#trainer_id").val(result.trainer_id);
                $("#capacity").val(result.capacity);
                $("#price").val(result.price);

                if (result.state == 'enrolled'){
                    $(".enrool_btn").hide();
                }else{
                    $(".enrool_btn").show();
                }
                }
            });


            return def;
        },
    

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _onCourseChange: function (ev) {
            rpc.query({
                model: 'course.schedule',
                method: 'get_course_obj',
                args: [{
                    'id': this.$('select[name="course_name"]').val(),
                    'employee_id': document.getElementById("employee_id").value,
                }]
            }).then(function (result) {
                if (result){
                $("#duration").val(result.duration);
                $("#f_date").val(result.f_date);
                $("#to_date").val(result.to_date);
                $("#trainer_id").val(result.trainer_id);
                $("#capacity").val(result.capacity);
                $("#price").val(result.price);

                if (result.state == 'enrolled'){
                    $(".enrool_btn").hide();
                }else{
                    $(".enrool_btn").show();
                }
                }
            });
        },
    });

    publicWidget.registry.portalCOMPANYDOC = publicWidget.Widget.extend({
        selector: '.o_portal_company_doc',
        events: {
            'change .attach': '_onChange',
        },
    
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);  
            
            
           


            return def;
        },
    

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _onChange: function (ev) {
            $("._save_buttone").show();
            $(".attach").hide();
        },
    });
    
    });
    