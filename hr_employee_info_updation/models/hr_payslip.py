# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    sub_agency_id = fields.Char('Sub Agency Id')
    employee_number = fields.Char('Employee Id')
    personal_identifier = fields.Char('Personal Identifier')
    national_id = fields.Char('National Id')
    iqama_no = fields.Char('Iqama Number')

    start_date = fields.Date()
    appraisal_d = fields.Char('Appraisal ID')
    appraisal_type_code = fields.Char()
    rating_result = fields.Selection([('bad', 'bad'), ('usual', 'usual'), ('good', 'good'), ('excellent', 'excellent')], "Result")
    rating_code = fields.Selection([('bad', 'bad'), ('usual', 'usual'), ('good', 'good'), ('excellent', 'excellent')])

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.sub_agency_id = self.employee_id.sub_agency_id
            self.employee_number = self.employee_id.employee_number
            self.personal_identifier = self.employee_id.personal_identifier
            self.national_id = self.employee_id.national_id
            self.iqama_no = self.employee_id.iqama_no


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    sub_agency_id = fields.Char('Sub Agency Id')
    employee_number = fields.Char('Employee Id')
    personal_identifier = fields.Char('Personal Identifier')
    national_id = fields.Char('National Id')
    iqama_no = fields.Char('Iqama Number')
    vacation_code = fields.Char()
    decision_number = fields.Char()
    decision_date = fields.Date()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.sub_agency_id = self.employee_id.sub_agency_id
            self.employee_number = self.employee_id.employee_number
            self.personal_identifier = self.employee_id.personal_identifier
            self.national_id = self.employee_id.national_id
            self.iqama_no = self.employee_id.iqama_no


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    sub_agency_id = fields.Char('Sub Agency Id')
    employee_number = fields.Char('Employee Id')
    personal_identifier = fields.Char('Personal Identifier')
    national_id = fields.Char('National Id')
    iqama_no = fields.Char('Iqama Number')
    rank_code = fields.Char()
    step_id = fields.Char()
    step_date = fields.Date()
    consolidation_set_id = fields.Char()
    consolidation_set_description = fields.Char()
    element_code = fields.Char()
    element_classification = fields.Char()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.sub_agency_id= self.employee_id.sub_agency_id
            self.employee_number= self.employee_id.employee_number
            self.personal_identifier= self.employee_id.personal_identifier
            self.national_id= self.employee_id.national_id
            self.iqama_no= self.employee_id.iqama_no
            self.rank_code= self.employee_id.rank_code
            self.step_id= self.employee_id.step_id
            self.step_date= self.employee_id.step_date
            # self.consolidation_set_id= self.employee_id.consolidation_set_id
            # self.consolidation_set_description= self.employee_id.consolidation_set_description
            # self.element_code= self.employee_id.element_code
            # self.element_classification = self.employee_id.element_classification
