# -*- coding: utf-8 -*-
###################################################################################
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Jesni Banu (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrnotificationTable(models.Model):
    _name = 'hr.notification'
    _description = 'HR Notification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    notification_MSG = fields.Char(string='Notification ', help="Notification")

    state = fields.Selection([ ('notify', 'Notification') , ('expired', 'Expired')],
                             string='Status',  default='notify',
                             track_visibility='always')

    date_start = fields.Date(string='Start Date', default=fields.Date.today(), required=True, help="Start date of "
                                                                                                   "Notification want"
                                                                                                   " to see")
    date_end = fields.Date(string='End Date', default=fields.Date.today(), required=True, help="End date of "
                                                                                               "Notification want too")
    employee_id = fields.Many2one('hr.employee', 'Employee')
    is_read = fields.Boolean()
    # res_id =fields.Integer(string="Model id")

    @api.constrains('date_start', 'date_end')
    def validation(self):
        if self.date_start > self.date_end:
            raise ValidationError("Start date must be less than End Date")


    def _get_state_desc(self):
        value = dict(self.env['hr.notification'].fields_get(allfields=['state'])['state']['selection'])

        for record in self:
            if record.state:
                record.state_desc = value[record.state]
            else:
                record.state_desc = ''

    state_desc = fields.Char(compute="_get_state_desc")


    def get_expiry_state(self):
        """
        Function is used for Expiring Announcement based on expiry date
        it activate from the crone job.

        """
        now = datetime.now()
        now_date = now.date()
        ann_obj = self.search([('state', '!=', 'expired')])
        for recd in ann_obj:
            if recd.date_end < now_date:
                recd.write({
                    'state': 'expired'
                })
