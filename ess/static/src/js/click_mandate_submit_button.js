odoo.define('ess.click_submit_button', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')

    publicWidget.registry.submit_button = publicWidget.Widget.extend({
        selector: '#contactForm2',
        events: {'click #submit_mandate_button_id': 'RestrictMandateSubmit',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        RestrictMandateSubmit: function () {
           var self = this;
           var type = document.getElementById("type").value;
           var course_id = document.getElementById("course_id").value;
           var place_id = document.getElementById("place_id").value;
           var course_type = document.getElementById("course_type").value;
           var start_date = document.getElementById("start_date").value;
           var end_date = document.getElementById("end_date").value;
           var description = document.getElementById("description").value;
           self._rpc({
                    route: '/course_restriction',
                    params: {
                        type: type,
                        course_id : course_id,
                        place_id : place_id,
                        course_type : course_type,
                        start_date : start_date,
                        end_date : end_date,
                        description : description,
                    },
           }).then(function (result) {
               if (result['val'] == 'No Extra Free Courses'){
                   alert("You aren't allowed to Request Extra Free Courses The Number Of Courses Allowed For You Is"+result['no_of_allowed_free_courses']);
                   return false;
               }
               else if (result['val'] == 'No Extra Paid Courses') {
                    alert("You aren't allowed to Request Extra Paid Courses The Number Of Courses Allowed For You Is"+result['no_of_allowed_paid_courses']);
                   return false;
               }
               else if (result['val'] == 'No Extra Course') {
                    alert("You aren't allowed to Request Extra Course last course you take at "+result['course_end_date']);
                   return false;
               }
               else {
                   alert("تم ارسال طلبكم بنجاح");
//                   parent.window.location.href='my/courses_and_mandate';
                }
           });
        },
    });
});


