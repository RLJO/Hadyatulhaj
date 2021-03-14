from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


import logging
_logger = logging.getLogger(__name__)
grey = "\x1b[38;21m"
yellow = "\x1b[33;21m"
red = "\x1b[31;21m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
green = "\x1b[32m"
blue = "\x1b[34m"


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    def unlink(self):
        leave_type_id = self.env.user.company_id.leave_type_id
        for record in self:
            if leave_type_id.id == record.id:
                raise UserError(_("You are not allowed to delete This record!!"))
        return super(HrLeaveType, self).unlink()


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_validate(self):
        res = super(HrLeave, self).action_validate()
        for record in self:
            contract_id = self.env['hr.contract'].search([('employee_id', '=', record.employee_id.id),
                                                          ('state', '=', 'open'),
                                                          ])
            if contract_id:
                contract_id.state = 'Partial Stop'
        return res

    @api.model
    def create(self, values):
        res = super(HrLeave, self).create(values)
        allocation_id = self.env['hr.leave.allocation'].search([('employee_id', '=', values['employee_id']),
                                                                ('state', '=', 'validate')
                                                                ], order='id desc', limit=1)
        if allocation_id:
            if allocation_id.available_from:
                request_date_from = datetime.strptime(values['request_date_from'], '%Y-%m-%d')
                date_from = request_date_from.date()
                if date_from < allocation_id.available_from or\
                   date_from > allocation_id.expiry_date:
                    raise UserError(_("You Aren't Allowed To Make This Leave "
                                      "You Can Make Between %s and %s"
                                      % (allocation_id.available_from, allocation_id.expiry_date)))
        return res

    def write(self, values):
        res = super(HrLeave, self).write(values)
        allocation_id = self.env['hr.leave.allocation'].search([('employee_id', '=', self.employee_id.id),
                                                                ('state', '=', 'validate')
                                                                ], order='id desc', limit=1)
        if allocation_id:
            if allocation_id.available_from:
                if allocation_id.available_from > self.request_date_from or\
                   self.request_date_from > allocation_id.expiry_date:
                    raise UserError(_("You Aren't Allowed To Make This Leave "
                                      "You Can Make Between %s and %s"
                                      % (allocation_id.available_from, allocation_id.expiry_date)))
        return res


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    @api.model
    def _get_expiry_date(self):
        return self.get_expiry_date()

    def get_expiry_date_states(self, ex_date, employee_id):
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        no_of_days_per_year = company.no_of_days_per_year
        contract_id = self.env['hr.contract'].search([('employee_id', '=', employee_id),
                                                      ('state', '=', 'open')
                                                      ], order='id desc', limit=1)
        if contract_id:
            if contract_id.deserved_leave:
                if contract_id.deserved_leave == 'one_year':
                    years = ex_date + timedelta(days=no_of_days_per_year)
                else:
                    years = ex_date + timedelta(days=2 * no_of_days_per_year)
        return years

    @api.onchange('employee_id')
    def get_expiry_date(self):
        if self.employee_id:
            years = False
            if self.employee_id.working_date:
                years = self.get_expiry_date_states(self.employee_id.working_date, self.employee_id.id)
            elif self.employee_id.join_date:
                years = self.get_expiry_date_states(self.employee_id.join_date, self.employee_id.id)
            self.expiry_date = years

    @api.model
    def _get_available_from(self):
        return self.get_available_from_date()

    @api.onchange('expiry_date')
    def get_available_from_date(self):
        if self.expiry_date:
            company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
            no_of_days_per_year = company.no_of_days_per_year
            month_per_year = no_of_days_per_year/12
            available_from_date = self.expiry_date - timedelta(days=month_per_year)
            self.available_from = available_from_date

    last_allocation_date = fields.Date()
    allocated_until = fields.Date()
    expiry_date = fields.Date(default=_get_expiry_date)
    available_from = fields.Date(default=_get_available_from)


class Contract(models.Model):
    _inherit = 'hr.contract'

    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('Partial Stop', 'Partial Stop'),
        ('close', 'Expired'),
        ('cancel', 'Cancelled')
    ], string='Status', group_expand='_expand_states', copy=False,
        tracking=True, help='Status of the contract', default='draft')

    contract_period = fields.Selection([('one_year', 'One Year'),
                                        ('two_year', 'Two Year'),
                                        ], string='Contract Period', default='one_year')
    deserved_leave = fields.Selection([('one_year', 'One Year'),
                                        ('two_year', 'Two Year'),
                                        ], string='Deserved Leave', default='one_year')

    @api.model
    def create(self, values):
        res = super(Contract, self).create(values)
        contract_id = self.search([('employee_id', '=', values['employee_id']), '|',
                                   ('state', '=', 'close'), ('state', '=', 'open')
                                   ], order='id asc', limit=1)
        if contract_id:
            contract_id.employee_id.join_date = contract_id.date_start
        return res

    def write(self, values):
        res = super(Contract, self).write(values)
        contract_id = self.search([('employee_id', '=', self.employee_id.id), '|',
                                   ('state', '=', 'close'), ('state', '=', 'open')
                                   ], order='id asc', limit=1)
        if contract_id:
            contract_id.employee_id.join_date = contract_id.date_start
        return res


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _get_join_date(self):
        contract_id = self.env['hr.contract'].search([('employee_id', '=', self.id), '|',
                                                      ('state', '=', 'close'),
                                                      ('state', '=', 'open')
                                                      ], order='id asc', limit=1)
        if contract_id:
            self.join_date = contract_id.date_start

    join_date = fields.Date(default=_get_join_date)
    working_date = fields.Date("Rejoin Date")
    last_allocation_date = fields.Date()
    allocation_ids = fields.One2many('hr.leave.allocation', 'employee_id')

    def get_employee_allocation(self, employee):
        employee = employee
        _logger.info(blue)
        _logger.info('employee ' + str(employee) + reset)
        _logger.info(yellow)
        _logger.info('employee.join_date ' + str(employee.join_date) + reset)

        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        allocation_obj = self.env['hr.leave.allocation']
        no_of_days_per_year = company.no_of_days_per_year
        leave_type_id = company.leave_type_id
        leave_id = company.leave_id
        unpaid_type = company.unpaid_type
        first_period = company.first_period
        deserve_first_period = company.deserve_first_period
        deserve_second_period = company.deserve_second_period
        leave_ids = self.env['hr.leave']
        if employee.join_date:
            leave = 0.0
            total_days = (fields.date.today() - employee.join_date).days
            leave_obj_id = leave_ids.search([('employee_id', '=', employee.id),
                                             ('holiday_status_id', '=', leave_id.id)])
            if leave_obj_id:
                for l in leave_obj_id:
                    leave += l.number_of_days

            if unpaid_type == 'Add':
                total_work_days = total_days - leave
            else:
                total_work_days = total_days
            no_of_years = total_work_days / no_of_days_per_year
            if no_of_years <= first_period:  # less than 5 years
                no_of_deserved_days = (fields.date.today() - employee.working_date).days
                no_of_years_deserved = no_of_deserved_days / no_of_days_per_year  # 1.3 year
                deserve_period = no_of_years_deserved * deserve_first_period

            else: # no_of_years > first_period   this is number of years from joining date
                no_of_deserved_days = (fields.date.today() - employee.working_date).days
                no_of_years_deserved = no_of_deserved_days / no_of_days_per_year  # 1.3 year
                period_after_5_years = no_of_years - first_period  # No of period after 5 years .3 month
                period_before_5_years = no_of_years_deserved - period_after_5_years  # No of period before 5 years 1 year


                if period_before_5_years <= 0:  # get allocation with 30 days
                    deserve_period = no_of_years_deserved * deserve_second_period

                else:  # get allocation with 30 days and 21 days
                    deserved_before_5_years = period_before_5_years * deserve_first_period
                    deserved_after_5_years= period_after_5_years * deserve_second_period
                    deserve_period=deserved_before_5_years+deserved_after_5_years


            final_period = deserve_period

            a = allocation_obj.create({
                'name': 'Annual Allocation',
                'holiday_status_id': leave_type_id.id,
                'number_of_days': final_period,
                'employee_id': employee.id,
                'last_allocation_date': fields.Date.today(),
                'allocated_until': fields.Date.today(),
            })
            employee.last_allocation_date = fields.Date.today()
            print(a.id)

    @api.model
    def cron_employee_annual_allocation(self):

        _logger.info(blue)
        _logger.info('cron_employee_annual_allocation ' + reset)
        company = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
        no_of_days_per_year = company.no_of_days_per_year
        allocation_type = company.allocation_type
        employee_ids = self.env['hr.employee'].search([])
        contract_obj = self.env['hr.contract']
        _logger.info(yellow)
        _logger.info('employee_ids ' + str(employee_ids) + reset)
        for employee in employee_ids:
            contract_id = contract_obj.search([('employee_id', '=', employee.id),
                                               ('state', '=', 'open')])
            if contract_id:
                _logger.info('contract_id ' + str(contract_id) + reset)
                if employee.last_allocation_date:
                    _logger.info(blue)
                    _logger.info('employee.last_allocation_date '+ str(employee.last_allocation_date) + reset)
                    allocation_per_days = (fields.date.today() - employee.last_allocation_date).days
                    allocation_per_year = allocation_per_days / no_of_days_per_year
                    allocation_per_month = allocation_per_year / 12
                    if allocation_type == 'Yearly':
                        if allocation_per_year >= 1:
                            self.get_employee_allocation(employee)
                    elif allocation_type == 'Monthly':
                        if allocation_per_month >= 1:
                            self.get_employee_allocation(employee)
                    elif allocation_type == 'Daily':
                        if allocation_per_days >= 1:
                            self.get_employee_allocation(employee)
                else:
                    self.get_employee_allocation(employee)
