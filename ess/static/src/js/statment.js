odoo.define('ess.statment', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')


    publicWidget.registry.portalStatment = publicWidget.Widget.extend({
        selector: '.o_portal_statment',
        events: {
            'click .print_button': '_onClickPrint',
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
        _onClickPrint: function () {
            alert("PPPPPPPPPPPPPPPPP")

            var self = this
            rpc.query({
                model: 'res.partner',
                method: 'print_report',
                args: [{
                    'partner_id': 3,
                    'start_date': '2020-05-01',
                    'end_date': '2020-05-20',
                }]
            }).then(function (result) {
                console.log("====================")
            }); 
        },
    
        
    });
    

    // publicWidget.registry.portalDocuments = publicWidget.Widget.extend({
    //     selector: '.o_portal_document',
    //     events: {
    //         'change input[name="doc_attachment_id"]': '_onChange',
    //     },
    
    //     /**
    //      * @override
    //      */
    //     start: function () {
    //         var def = this._super.apply(this, arguments);    
    //         return def;
    //     },
    

    //     //--------------------------------------------------------------------------
    //     // Handlers
    //     //--------------------------------------------------------------------------
    
    //     /**
    //      * @private
    //      */
    //     _onChange: function (ev) {
    //         console.log(ev)
    //         if (!ev.currentTarget.files.length) {
    //             return;
    //         }
    //         var $form = $(ev.currentTarget).closest('form');
    //         var reader = new window.FileReader();
    //         reader.readAsDataURL(ev.currentTarget.files[0]);
    //         reader.onload = function (ev) {
    //             console.log(ev.target.result)
    //             //$form.find('.attachment').attr('src', ev.target.result);

    //             ev.preventDefault();
    //             var num_A = $( ".num_A" ).val();


    //             // $form.find('.s2u_portal_avatar_img').attr('style', 'border-radius: 50%; width: 128px; height: 128px;')
    //         };
    //     },
    // });


    
    });
    