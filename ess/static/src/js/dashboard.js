odoo.define('ess.dashboard', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')

    var x = document.getElementsByClassName("sid_dashboard");

    publicWidget.registry.portalDashboard = publicWidget.Widget.extend({
        selector: '#side_menu_class',
        events: {
            'click .edit-pic': '_onClickEditPic',
            'change .input-edit-pic': '_onInputUploadChange',
        },
    
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            
            
            return def;
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _onClickEditPic: function (ev) {
            ev.preventDefault();
            $(ev.currentTarget).closest('form').find('.input-edit-pic').trigger('click');
        },

        _onInputUploadChange: function (ev) {
            if (!ev.currentTarget.files.length) {
                return;
            }
            var $form = $(ev.currentTarget).closest('form');
            var reader = new window.FileReader();
            reader.readAsDataURL(ev.currentTarget.files[0]);
            reader.onload = function (ev) {
                $form.find('.emp_img').attr('src', ev.target.result);
                $form.find('.emp_img').attr('style', 'border-radius: 50%; width: 100%; height: 170px;')
                
            };

            $(ev.currentTarget.form).find('.upload-btn').trigger('click');
        },

    });


    
    });
    