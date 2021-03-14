from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    administrative_decisions_ids = fields.One2many('hr.administrative.decisions', 'employee_id')
