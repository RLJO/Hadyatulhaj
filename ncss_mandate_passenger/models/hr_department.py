# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime, timedelta


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    is_main_department = fields.Boolean('Main Department', default=True)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    description = fields.Char()

