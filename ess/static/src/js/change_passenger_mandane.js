odoo.define('ess.uom_portal', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')

    publicWidget.registry.place = publicWidget.Widget.extend({
        selector: '#contactForm2',
        events: {
            'change select[name="course_id"]': '_adaptCityForm',
        },
        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
//            var elem = document.getElementById(elmId);
            var elem = document.getElementById("course_id");
            if(typeof elem !== 'undefined' && elem !== null) {
               self._rpc({
                    route: '/get/course_place',
                    params: {
                        course_id: document.getElementById("course_id").value,
                    },
                }).then(function (result) {
                    document.getElementById('place_id').value = result['val'];
                });
            }
//            if(document.getElementById("course_id").value != ''){
//                self._rpc({
//                    route: '/get/course_place',
//                    params: {
//                        course_id: document.getElementById("course_id").value,
//                    },
//                }).then(function (result) {
//                    document.getElementById('place_id').value = result['val'];
//                });
//            }
            return def;
        },

        _adaptCityForm: function () {
//            debugger;
            var self = this;
//            if(document.getElementById("course_id").value != ''){
            var elem = document.getElementById("course_id");
            if(typeof elem !== 'undefined' && elem !== null){
                self._rpc({
                    route: '/get/course_place',
                    params: {
                        course_id: document.getElementById("course_id").value,
                    },
                }).then(function (result) {
                    document.getElementById('place_id').value = result['val'];
                });
            }

        },
    });


});
