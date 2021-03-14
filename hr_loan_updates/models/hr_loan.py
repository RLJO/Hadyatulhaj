# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrLoan(models.Model):
    _inherit = 'hr.loan'
    guarantor_employee_id = fields.Many2one('hr.employee')
    guarantor_employee_position_id = fields.Many2one('hr.job')
    guarantor_employee_salary = fields.Float()
    state = fields.Selection(selection_add=[('guarantor_employee_approve', 'Guarantor Employee Approve'),
                                            ('direct_manager_approve', 'Direct Manager Approve'),
                                            ('hr_approve', 'Hr Approve'),
                                            ])
    is_direct_manager = fields.Boolean(compute='get_direct_manager')

    def get_direct_manager(self):
        current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
        for record in self:
            if record.employee_id and record.employee_id.parent_id:
                if record.employee_id.parent_id.id == current_user_id:
                    self.is_direct_manager = True
                else:
                    self.is_direct_manager = False
            else:
                self.is_direct_manager = False

    @api.onchange('guarantor_employee_id')
    def onchange_guarantor_employee_id(self):
        for record in self:
            employee_contract_id = self.env['hr.contract'].search([('employee_id', '=', record.guarantor_employee_id.id),
                                                          ('state', '=', 'open')
                                                          ], order='id desc', limit=1)
            record.guarantor_employee_position_id = record.guarantor_employee_id.job_id.id
            record.guarantor_employee_salary = employee_contract_id.wage if employee_contract_id else 0.0

    def action_guarantor_employee_approve(self):
        self.write({'state': 'guarantor_employee_approve'})

    def action_direct_manager_approve(self):
        self.write({'state': 'direct_manager_approve'})

    def action_hr_approve(self):
        self.write({'state': 'hr_approve'})

    def action_accounting_approve(self):
        self.action_approve()
