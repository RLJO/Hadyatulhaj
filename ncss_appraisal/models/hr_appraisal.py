# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime


class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    appraisal_count = fields.Float(compute='compute_appraisal_count')
    total_deserve_appraisal = fields.Float(compute='compute_total_deserve_appraisal')
    appraisal_level = fields.Char(compute='compute_appraisal_level')

    def compute_total_deserve_appraisal(self):
        hr_employee_appraisal = self.env['hr.employee.appraisal'].\
            search([('appraisal_id', '=', self.id), ('state', '=', 'completed')])
        total_appraisal_value = 0.0
        count = 0.0
        if hr_employee_appraisal:
            for appraisal in hr_employee_appraisal:
                count += 1
                total_appraisal_value += appraisal.total_deserve_appraisal
            if total_appraisal_value and count:
                self.total_deserve_appraisal = total_appraisal_value / count
            else:
                self.total_deserve_appraisal = 0.0
        else:
            self.total_deserve_appraisal = 0.0

    @api.onchange('total_deserve_appraisal')
    def compute_appraisal_level(self):
        for record in self:
            if record.total_deserve_appraisal:
                if record.total_deserve_appraisal < 50:
                    record.appraisal_level = 'ضعيف'
                elif 50 < record.total_deserve_appraisal <= 65:
                    record.appraisal_level = 'مقبول'
                elif 65 < record.total_deserve_appraisal <= 75:
                    record.appraisal_level = 'جيد'
                elif 75 < record.total_deserve_appraisal <= 89:
                    record.appraisal_level = 'عالي / جيد جداً'
                else:
                    record.appraisal_level = 'متميز / ممتاز'
            else:
                record.appraisal_level = ' '

    def compute_appraisal_count(self):
        hr_employee_appraisal = self.env['hr.employee.appraisal'].search_count([('appraisal_id', '=', self.id)])
        if hr_employee_appraisal:
            self.appraisal_count = hr_employee_appraisal
        else:
            self.appraisal_count = 0.0

    def action_open_employee_appraisal(self):
        return {
            'name': 'HR Employee Appraisal',
            'res_model': 'hr.employee.appraisal',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('appraisal_id', '=', self.id)],
        }

    def create_activity(self, user_id, appraisal_id):
        employee_id = self.env['hr.employee'].browse(user_id)
        if employee_id.user_id:
            print(employee_id.user_id)
            now = datetime.now()
            date_deadline = now.date()
            values = {
                'res_id': appraisal_id.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee.appraisal')]).id,
                'user_id': employee_id.user_id.id,
                'summary': 'Appraisal need approval',
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'date_deadline': date_deadline
            }
            self.env['mail.activity'].sudo().create(values)

    def button_send_appraisal(self):
        res = super(HrAppraisal, self).button_send_appraisal()
        employee_lst = []
        if self.manager_ids:
            for manager in self.manager_ids:
                if manager.id not in employee_lst:
                    employee_lst.append(manager.id)
        if self.collaborators_ids:
            for collaborators in self.collaborators_ids:
                if collaborators.id not in employee_lst:
                    employee_lst.append(collaborators.id)
        if self.colleagues_ids:
            for colleagues in self.colleagues_ids:
                if colleagues.id not in employee_lst:
                    employee_lst.append(colleagues.id)
        hr_employee_appraisal_obj = self.env['hr.employee.appraisal']
        appraisal_criteria_obj = self.env['appraisal.criteria'].search([('is_default', '=', True)])
        appraisal_recommendations_obj = self.env['appraisal.recommendations'].search([('is_default', '=', True)])

        for employee in employee_lst:
            appraisal_id = hr_employee_appraisal_obj.create({
                'employee_id': self.employee_id.id,
                'manager_id': employee,
                'appraisal_id': self.id,
                'appraisal_item_ids': [(0, 0, {
                    'appraisal_criteria_id': criteria.id,
                    'max_limit': criteria.max_limit})for criteria in appraisal_criteria_obj],
                'appraisal_manager_recommendations_ids': [(0, 0, {
                    'appraisal_recommendation_id': recommendations.id
                })for recommendations in appraisal_recommendations_obj],
            })

            self.create_activity(employee, appraisal_id)
        return res
