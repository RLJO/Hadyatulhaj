# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HealthHealth(models.Model):
    _name = 'health.health'

    name = fields.Char()


class BloodBlood(models.Model):
    _name = 'blood.blood'

    name = fields.Char()


class ReligionReligion(models.Model):
    _name = 'religion.religion'

    name = fields.Char()


class CertificateLevel(models.Model):
    _name = 'certificate.level'

    name = fields.Char()


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    certificate = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctorate', 'doctorate'),
        ('diploma', 'diploma'),
        ('High School', 'High School'),
        ('Intermediate education', 'Intermediate education'),
    ], 'Certificate Level', default='bachelor', groups="hr.group_hr_user", tracking=True)

    certificate_id = fields.Many2one('certificate.level', 'Certificate Level')
    job_history_ids = fields.One2many('hr.history.line', 'hr_employee_id')
    sub_agency_id = fields.Char('Sub Agency Id')
    employee_number = fields.Char('Employee Id')
    personal_identifier = fields.Char('Personal Identifier')
    personal_identifier_place = fields.Char()
    personal_identifier_date = fields.Date()
    passport_number = fields.Char()
    national_id = fields.Char('National Id')
    iqama_no = fields.Char('Iqama Number')

    first_name = fields.Char()
    second_name = fields.Char()
    Third_name = fields.Char()
    last_name = fields.Char()

    first_name_e = fields.Char('First Name')
    second_name_e = fields.Char('Second Name')
    Third_name_e = fields.Char('Third Name')
    last_name_e = fields.Char('Last Name')
    religion_id = fields.Many2one('religion.religion', 'Religion Type')
    blood_id = fields.Many2one('blood.blood', 'Blood Type')
    health_id = fields.Many2one('health.health', 'health status Type')
    employee_status_code = fields.Char()

    job_number = fields.Char()
    job_class_code = fields.Char()
    job_class_description = fields.Char()
    job_cat_chain = fields.Char()
    job_name_code = fields.Char()
    job_name_description = fields.Char()
    employee_type_code = fields.Char()
    employee_type_description = fields.Char()
    rank_code = fields.Char()
    step_id = fields.Char()
    step_date = fields.Date()
    first_grade_date = fields.Date()
    actual_job_name_code = fields.Char()
    actual_job_name_description = fields.Char()
    job_organization_name = fields.Char()
    actual_organization_id = fields.Char()
    actual_organization_name = fields.Char()
    next_promotion_date = fields.Date()
    government_hire_date = fields.Date()
    location_code = fields.Char()
    ministry_hire_date = fields.Date()
    remaining_business_balance = fields.Char()
    transaction_code = fields.Char()

    termination_reason_code = fields.Char()
    termination_date = fields.Date()
    last_update_date = fields.Date()

    first_related_person_name = fields.Char()
    first_related_person_relation = fields.Char()
    first_related_person_phone = fields.Char()

    second_related_person_name = fields.Char()
    second_related_person_relation = fields.Char()
    second_related_person_phone = fields.Char()

    # @api.constrains('national_id')
    # def _check_national_id(self):
    #     if len(self.national_id) > 10:
    #         raise UserError(_('Number Of Characters In National ID Must Not Exceed 10'))


class HrHistoryLine(models.Model):
    _name = 'hr.history.line'

    hr_employee_id = fields.Many2one('hr.employee')
    hr_job_id = fields.Many2one('hr.job.history', 'Decision')
    description = fields.Char()

    def action_done(self):
        for record in self:
            # print(record.hr_job_id)
            # print(record.description)
            # print(record.hr_employee_id.name)
            record.hr_employee_id.job_number = record.hr_job_id.job_number
            record.hr_employee_id.job_class_code = record.hr_job_id.job_class_code
            record.hr_employee_id.job_class_description = record.hr_job_id.job_class_description
            record.hr_employee_id.job_cat_chain = record.hr_job_id.job_cat_chain
            record.hr_employee_id.job_name_code = record.hr_job_id.job_name_code
            record.hr_employee_id.job_name_description = record.hr_job_id.job_name_description
            record.hr_employee_id.employee_type_code = record.hr_job_id.employee_type_code
            record.hr_employee_id.employee_type_description = record.hr_job_id.employee_type_description
            record.hr_employee_id.rank_code = record.hr_job_id.rank_code
            record.hr_employee_id.step_id = record.hr_job_id.step_id
            record.hr_employee_id.step_date = record.hr_job_id.step_date
            record.hr_employee_id.first_grade_date = record.hr_job_id.first_grade_date
            record.hr_employee_id.actual_job_name_code = record.hr_job_id.actual_job_name_code
            record.hr_employee_id.actual_job_name_description = record.hr_job_id.actual_job_name_description
            record.hr_employee_id.job_organization_name = record.hr_job_id.job_organization_name
            record.hr_employee_id.actual_organization_id = record.hr_job_id.actual_organization_id
            record.hr_employee_id.actual_organization_name = record.hr_job_id.actual_organization_name
            record.hr_employee_id.next_promotion_date = record.hr_job_id.next_promotion_date
            record.hr_employee_id.government_hire_date = record.hr_job_id.government_hire_date
            record.hr_employee_id.location_code = record.hr_job_id.location_code
            record.hr_employee_id.ministry_hire_date = record.hr_job_id.ministry_hire_date
            record.hr_employee_id.remaining_business_balance = record.hr_job_id.remaining_business_balance
            record.hr_employee_id.transaction_code = record.hr_job_id.transaction_code

            contract_id = self.env['hr.contract'].search([('employee_id', '=', record.hr_employee_id.id),
                                                          ('state', '=', 'open'),
                                                          ])
            if contract_id:
                contract_id.wage = record.hr_job_id.wage


class HrJobHistory(models.Model):
    _name = 'hr.job.history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'job_number'

    # hr_employee_id = fields.Many2one('hr.employee')
    job_number = fields.Char()
    job_class_code = fields.Char()
    job_class_description = fields.Char()
    job_cat_chain = fields.Char()
    job_name_code = fields.Char()
    job_name_description = fields.Char()
    employee_type_code = fields.Char()
    employee_type_description = fields.Char()
    rank_code = fields.Char()
    step_id = fields.Char()
    step_date = fields.Date()
    first_grade_date = fields.Date()
    wage = fields.Float()
    actual_job_name_code = fields.Char()
    actual_job_name_description = fields.Char()
    job_organization_name = fields.Char()
    actual_organization_id = fields.Char()
    actual_organization_name = fields.Char()
    next_promotion_date = fields.Date()
    government_hire_date = fields.Date()
    location_code = fields.Char()
    ministry_hire_date = fields.Date()
    remaining_business_balance = fields.Char()
    transaction_code = fields.Char()
    transaction_description = fields.Char()
    transaction_start_date = fields.Date()
    transaction_end_date = fields.Date()
    last_update_date = fields.Date()
