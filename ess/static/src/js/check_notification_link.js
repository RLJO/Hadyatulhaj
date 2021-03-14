odoo.define('ess.check_notification_link', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc')

    publicWidget.registry.notification = publicWidget.Widget.extend({
        selector: '.newselector',
        events: {'click .visitedlink': '_getNotification',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _getNotification: function () {
           var self = this;
           $(window).bind('hashchange', function() {
                self._rpc({
                    route: '/change/notification',
                    params: {
                        course_id: decodeURI(window.location.href),
                    },
                }).then(function (result) {
                    $('#notify'+result['result']).css({"color":"black"});
                });
            });
        },
    });

    publicWidget.registry.announcement = publicWidget.Widget.extend({
        selector: '.announcement_selector',
        events: {'click .visitedlink': '_ChangeAnnouncementColor',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _ChangeAnnouncementColor: function () {
           var self = this;
           $(window).bind('hashchange', function() {
                self._rpc({
                    route: '/change/announcement_color',
                    params: {
                        url: decodeURI(window.location.href),
                    },
                }).then(function (result) {
                $('td').find('#announcement'+result['result']).css({"color":"black"});
                parent.window.location.href='/my/announcement#by_job_position';
                $('#by_department2').addClass("active");
                });
            });
        },
    });

    publicWidget.registry.public_announcement = publicWidget.Widget.extend({
        selector: '.public_announcement_selector',
        events: {'click .visitedlink': '_ChangePublicAnnouncementColor',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _ChangePublicAnnouncementColor: function () {
           var self = this;
           $(window).bind('hashchange', function() {
                self._rpc({
                    route: '/change/announcement_color',
                    params: {
                        url: decodeURI(window.location.href),
                    },
                }).then(function (result) {
//                $('#announcement'+result['result']).css({"background_color":"black"});
$('td').find('#announcement'+result['result']).css({"color":"black"});
$('li').find('#by_department').css({"class":"active"});
//$('#by_department2').addClass("active");
parent.window.location.href='/my/announcement#by_job_position';
//parent.window.location.href='/add/achievement_lines?id='+result['id']+'&'+'work_order='+result['name'];
                });
            });
        },
    });

    publicWidget.registry.mandate = publicWidget.Widget.extend({
        selector: '.mandate_visited',
        events: {'click .mandate_visited_link': '_MandatePassengerClick',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _MandatePassengerClick: function () {
           var self = this;
           parent.window.location.href='/my/courses_and_mandate';
        },
    });

    publicWidget.registry.custody = publicWidget.Widget.extend({
        selector: '.custody_visited',
        events: {'click .custody_visited_link': '_CustodyClick',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _CustodyClick: function () {
           parent.window.location.href='/my/custody';
        },
    });

    publicWidget.registry.asset = publicWidget.Widget.extend({
        selector: '.asset_visited',
        events: {'click .asset_visited_link': '_AssetAssignationClick',},

        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;
            return def;
        },

        _AssetAssignationClick: function () {
           var self = this;
           parent.window.location.href='/my/asset_assignation';
        },
    });

});


