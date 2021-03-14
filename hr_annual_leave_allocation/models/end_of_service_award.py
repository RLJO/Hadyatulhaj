# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import datetime


class EndOfServiceAward(models.Model):
    _name = 'end.of.service.award'
    _description = 'End of Service Award'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, index=True, tracking=True,
                                  track_visibility='onchange')
    contract_id = fields.Many2one('hr.contract', string='Contract', domain="[('employee_id', '=', employee_id)]",
                                  tracking=True, copy=False, related='employee_id.contract_id')
    join_date = fields.Date(string="Join Date", related='employee_id.join_date', tracking=True)
    last_work_date = fields.Date(tracking=True)
    contact_end_type = fields.Selection([('end_period', 'End of Contract Period'),
                                         ('immediate_resignation', 'Immediate resignation'),
                                         ('resignation_after_month', 'Resignation After Month'),
                                         ('law_80', 'Law 80'),
                                         ('law_77_by_employee', 'Law 77 By Employee'),
                                         ('law_77_by_company', 'Law 77 By Company'),
                                         ],
                                        default='end_period', tracking=True)

    number_of_days_from_join_date = fields.Float(string="Number of Days From Join Date",
                                                   compute='_compute_number_of_days_from_join_date', tracking=True)
    first_period_days = fields.Float(compute='_compute_number_of_days_from_join_date', tracking=True)
    second_period_days = fields.Float(compute='_compute_number_of_days_from_join_date', tracking=True)
    total_unpaid_days = fields.Float(string='Total Unpaid Days First Period', compute='_compute_total_unpaid_days')
    total_unpaid_days_second_period = fields.Float(compute='_compute_total_unpaid_days')
    net_period = fields.Float(compute='_compute_all_net_period')
    net_first_period = fields.Float(compute='_compute_all_net_period')
    net_second_period = fields.Float(compute='_compute_all_net_period')
    total_days_before = fields.Float(string="Total Years Before Five Years")
    total_days_after = fields.Float(string="Total Years After Five Years")
    net_period_before_5year = fields.Float(string="Deserve First Period", compute='_compute_total_years')
    net_period_after_5year = fields.Float(string="Deserve Second Period", compute='_compute_total_years')
    total_deserve = fields.Float(string="Total Deserve", compute='_compute_total_years')
    total_deserved_per_contract_end_type = fields.Float(compute='_compute_final_deserving')
    final_deserving = fields.Float(string="Final Deserving", compute='_compute_final_deserving')
    eos_computation_dependency = fields.Html()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], string='Status', readonly=True, tracking=True, copy=False, default='draft')

    def get_employee_end_of_service(self, employee_id, last_work_date, contact_end_type):
        employee_id = employee_id
        last_work_date = last_work_date
        contact_end_type = contact_end_type
        join_date = employee_id.join_date
        wage = employee_id.contract_id.wage
        leave = 0.0
        total_unpaid_days = 0.0
        number_of_days_from_join_date = 0.0
        net_period = 0.0
        total_years = 0.0
        total_days_before = 0.0
        net_period_before_5year = 0.0
        total_days_after = 0.0
        net_period_after_5year = 0.0
        final_deserving = 0.0
        # for rec in self:
        leave_ids = self.env['hr.leave']
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        leave_id = company.leave_id
        no_of_days_per_year = company.no_of_days_per_year
        first_period = company.first_period
        leave_obj_id = leave_ids.search([('employee_id', '=', employee_id.id),
                                         ('state', '=', 'validate'),
                                         ('holiday_status_id', '=', leave_id.id),
                                         ])
        if leave_obj_id:
            for l in leave_obj_id:
                leave += l.number_of_days
            total_unpaid_days = leave
        print("total_unpaid_days", total_unpaid_days)
        if last_work_date and join_date:
            difference_between_days = last_work_date - join_date
            number_of_days_from_join_date = difference_between_days.days
        print("number_of_days_from_join_date", number_of_days_from_join_date)
        net_period = number_of_days_from_join_date - total_unpaid_days
        print("net_period", net_period)
        total_years = net_period / no_of_days_per_year
        if total_years <= first_period:
            total_days_before = total_years
            net_period_before_5year = total_years * 15
            total_days_after = 0.0
            net_period_after_5year = 0.0
        else:
            total_days_before = first_period
            net_period_before_5year = first_period * 15
            total_days_after = total_years - first_period
            net_period_after_5year = self.total_days_after * 30
        print("total_days_before", total_days_before)
        print("net_period_before_5year", net_period_before_5year)
        print("total_days_after", total_days_after)
        print("net_period_after_5year", net_period_after_5year)
        total = 0.0
        if contact_end_type == 'end_period':
            total = net_period_before_5year + net_period_after_5year
        elif contact_end_type in ['immediate_resignation', 'resignation_after_month']:
            if total_years < 2:
                total = 0.0
            elif 2 <= total_years < 5:
                total = (net_period_before_5year + net_period_after_5year) / 3
            elif 5 <= total_years < 10:
                total = (net_period_before_5year + net_period_after_5year) * (2 / 3)
            else:
                total = (net_period_before_5year + net_period_after_5year)
        else:
            total = 0.0
        final_deserving = total

        total_involved_items = 0.0
        contract = self.env['hr.contract'].sudo().browse(self.contract_id.id)
        for i in self.env.user.company_id.eos_involved_item_id:
            total_involved_items += contract[i.field_name]
        deserving = (final_deserving * total_involved_items) / 30
        # deserving = final_deserving * wage / 30
        vals= {
            'join_date': join_date,
            'total_unpaid_days': total_unpaid_days,
            'number_of_days_from_join_date': number_of_days_from_join_date,
            'net_period': net_period,
            'total_days_before': total_days_before,
            'net_period_before_5year': net_period_before_5year,
            'total_days_after': total_days_after,
            'net_period_after_5year': net_period_after_5year,
            'final_deserving': final_deserving,
            'wage': wage,
            'deserving': deserving,
        }
        print("vals", vals)
        return vals

    @api.depends('employee_id')
    def _compute_total_unpaid_days(self):
        leave = 0.0
        leave_first_period = 0.0
        leave_second_period = 0.0
        for rec in self:
            if rec.employee_id:
                leave_ids = self.env['hr.leave']
                company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
                no_of_days_in_first_period = company.first_period * company.no_of_days_per_year
                end_date_first_period = self.join_date + timedelta(days=no_of_days_in_first_period)
                leave_id = company.leave_id
                leave_obj_id = leave_ids.search([('employee_id', '=', rec.employee_id.id),
                                                 ('state', '=', 'validate'),
                                                 ('holiday_status_id', '=', leave_id.id)])
                if leave_obj_id:
                    for l in leave_obj_id:
                        if l.request_date_to <= end_date_first_period:
                            leave_first_period += l.number_of_days
                        else:
                            leave_second_period += l.number_of_days
        self.total_unpaid_days = leave_first_period
        self.total_unpaid_days_second_period = leave_second_period

    @api.depends('join_date', 'last_work_date')
    def _compute_number_of_days_from_join_date(self):
        for record in self:
            record.number_of_days_from_join_date = 0
            record.first_period_days = 0
            record.second_period_days = 0
            if record.last_work_date and record.join_date:
                number_of_days_from_join_date = record.last_work_date - record.join_date

                company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
                no_of_days_in_first_period = company.first_period * company.no_of_days_per_year

                if number_of_days_from_join_date.days > no_of_days_in_first_period:
                    first_period_days = no_of_days_in_first_period
                    second_period_days = number_of_days_from_join_date.days - no_of_days_in_first_period
                else:
                    first_period_days = number_of_days_from_join_date.days
                    second_period_days = 0.0
                record.first_period_days = first_period_days
                record.second_period_days = second_period_days
                record.number_of_days_from_join_date = number_of_days_from_join_date.days

    @api.depends('number_of_days_from_join_date', 'total_unpaid_days')
    def _compute_all_net_period(self):
        for record in self:
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            record.net_first_period = (record.first_period_days - record.total_unpaid_days) / company.no_of_days_per_year
            record.net_second_period = (record.second_period_days - record.total_unpaid_days_second_period) / company.no_of_days_per_year
            record.net_period = record.net_first_period + record.net_second_period

    @api.depends('net_first_period', 'net_second_period')
    def _compute_total_years(self):
        for record in self:
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            no_of_days_per_year = company.no_of_days_per_year
            first_period = company.first_period
            deserve_first_period = record.net_first_period * 15
            deserve_second_period = record.net_second_period * 30
            self.net_period_before_5year = deserve_first_period
            self.net_period_after_5year = deserve_second_period
            record.total_deserve = deserve_first_period + deserve_second_period

    @api.depends('total_deserve', 'contact_end_type', 'number_of_days_from_join_date')
    def _compute_final_deserving(self):
        self.eos_computation_dependency = False
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        no_of_days_per_year = company.no_of_days_per_year
        total_years = self.number_of_days_from_join_date / no_of_days_per_year
        total_deserved_per_contract_end_type = 0.0
        for record in self:
            if record.contact_end_type == 'end_period':
                total_deserved_per_contract_end_type = record.total_deserve
            elif record.contact_end_type in ['immediate_resignation', 'resignation_after_month']:
                if total_years < 2:
                    total_deserved_per_contract_end_type = 0.0
                elif 2 <= total_years < 5:
                    total_deserved_per_contract_end_type = record.total_deserve/3
                elif 5 <= total_years < 10:
                    total_deserved_per_contract_end_type = (record.total_deserve) * (2/3)
                else:
                    total_deserved_per_contract_end_type = record.total_deserve
            else:
                total_deserved_per_contract_end_type = 0.0
        total_involved_items = 0.0
        contract = self.env['hr.contract'].browse(self.contract_id.id)
        index = 0
        for i in self.env.user.company_id.eos_involved_item_id:
            index += 1
            if self.eos_computation_dependency:
                self.eos_computation_dependency += str(index) + " - " + i.name + " = " + str(contract[i.field_name])+"<br/>"
            else:
                self.eos_computation_dependency = str(index) + " - " + i.name + " = " + str(contract[i.field_name])
            total_involved_items += contract[i.field_name]
        self.total_deserved_per_contract_end_type = total_deserved_per_contract_end_type
        self.final_deserving = total_deserved_per_contract_end_type * (total_involved_items / 30)

    def action_approve(self):
        self.get_employee_end_of_service(self.employee_id, self.last_work_date, self.contact_end_type)
        self.state = "approved"

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_('You Can Not Delete a Request Which Is Not Draft.'))
            res = super(EndOfServiceAward, record).unlink()
            return res

    def get_day_name_from_date(self, contract_day):
        contract_day = str(contract_day)
        year, month, day = contract_day.split('-')
        day_name = datetime.date(int(year), int(month), int(day))
        e_name = day_name.strftime("%A")
        if e_name == 'Saturday':
            ar_name = 'السبت'
        elif e_name == 'Sunday':
            ar_name = 'الاحد'
        elif e_name == 'Monday':
            ar_name = 'الاثنين'
        elif e_name == 'Tuesday':
            ar_name = 'الثلاثاء'
        elif e_name == 'Wednesday':
            ar_name = 'الاربعاء'
        elif e_name == 'Thursday':
            ar_name = 'الخميس'
        else:
            ar_name = 'الجمعه'
        return ar_name
