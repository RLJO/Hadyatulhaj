# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime, timedelta


class BudgetAllocatedTraining(models.Model):
    _name = 'budget.allocated.training'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "department_id"

    department_id = fields.Many2one('hr.department')
    budget = fields.Float()
    expensed_from_budget = fields.Float()
    remaining_from_budget = fields.Float(compute="compute_remaining_from_budget")
    start_date = fields.Date()
    end_date = fields.Date()

    @api.depends('budget','expensed_from_budget')
    def compute_remaining_from_budget(self):
        for record in self:
            record.remaining_from_budget = record.budget - record.expensed_from_budget


class CoursePlace(models.Model):
    _name = 'course.place'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(translate=True)
    need_ticket = fields.Boolean(default=True)


class EmployeeDegreeValue(models.Model):
    _name = 'employee.degree.value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    internal_day_value = fields.Float()
    external_day_value = fields.Float()
    traveling_type = fields.Selection([('tourism', 'tourism'),
                                       ('first_class', 'First Class'),
                                       ('vip', 'VIP'),
                                       ])
    number_of_paid_courses_per_year = fields.Float()
    number_of_free_courses_per_year = fields.Float()
    allowed_period_between_courses = fields.Float()


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    employee_degree_id = fields.Many2one('employee.degree.value')


class TrainingCourse(models.Model):
    _name = 'training.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char()
    description = fields.Text()
    type = fields.Selection([('internal', 'Internal'), ('external', 'External')])
    price = fields.Float()
    number_of_days = fields.Float()
    start_date = fields.Date()
    end_date = fields.Date()
    is_free = fields.Boolean()
    is_private = fields.Boolean(string=_('Private'),default=False)
    employee_id = fields.Many2one('hr.employee', 'Employee')
    course_place_id = fields.Many2one('course.place',required=True)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_private_rel', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)

    @api.onchange('is_private')
    def onchange_rem_emp(self):
        if self.is_private ==False:
            self.employee_id=False

    @api.constrains('start_date', 'end_date')
    def constrains_start_end_date(self):
        for record in self:
            if record.end_date < record.start_date:
                raise UserError(_("End Date Must Be Greater Than Start Date"))

    @api.onchange('start_date', 'end_date')
    def onchange_start_end_date(self):
        if self.start_date and self.end_date:
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(str(self.start_date), date_format)
            end_date = datetime.strptime(str(self.end_date), date_format)
            self.number_of_days = float((end_date-start_date).days)


class MandatePassenger(models.Model):
    _name = 'mandate.passenger'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "employee_id"

    name = fields.Char()
    employee_id = fields.Many2one('hr.employee', 'Employee')
    employee_type = fields.Selection([('employee', 'Employee'),
                                      ('department_manager', 'Department Manager'),
                                      ('manager', 'Manager'),
                                      ])
    employee_degree_id = fields.Many2one('employee.degree.value')
    course_place_id = fields.Many2one('course.place',reuired=True)
    type = fields.Selection([('course', 'Course'),
                              ('mandate', 'Mandate'),
                              ('work_shop', 'work shop'),
                              ] ,default='course',tracking=True,)
    course_id = fields.Many2one('training.course', 'Course',required=True)
    course_type = fields.Selection([('internal', 'Internal'), ('external', 'External')])
    description = fields.Text()
    price = fields.Float()
    start_date = fields.Date()
    end_date = fields.Date()
    number_of_days = fields.Integer()
    total_value_without_ticket = fields.Float(compute='get_total_value_without_ticket', store=True)
    day_value = fields.Float(compute='get_total_value', store=True)
    housing_value = fields.Float(compute='get_total_value', store=True)
    transportation_value = fields.Float(compute='get_total_value', store=True)
    daily_expenses = fields.Float(compute='get_total_value')
    total = fields.Float(compute='get_total_expenses', store=True)
    Subsistence_rate = fields.Float()
    is_direct_manager = fields.Boolean(compute='get_direct_manager')
    is_department_manager = fields.Boolean(compute='compute_department_manager')
    traveling_type = fields.Selection([('tourism', 'tourism'),
                                       ('first_class', 'First Class'),
                                       ('vip', 'VIP'),
                                       ])
    reason = fields.Text()
    attach_file = fields.Many2many('ir.attachment', 'mandate_attach_rel', 'doc_id', 'attach_id4',
                                   string=_('Attachment File'),
                                          help='You can attach the copy of your document', copy=False)
    attach_file_ticket = fields.Many2many('ir.attachment', 'mandate_attach_rel', 'doc_id', 'attach_id4', string=_('Attachment ticket'),
                                      help='You can attach the copy of your document', copy=False)

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection([('draft', 'Draft'),
                               ('direct_manager_approve', 'Direct Manager Approved'),
                               ('department_manager_approve', 'Department Manager Approved'),
                               ('hr_approve', 'Hr Approvedd'),
                               ('accounting_approve', 'Accounting Approved'),
                               ('refuse', 'Refused'),
                               ], default='draft', tracking=True, group_expand='_expand_states')

    def _getdesc(self):
        value = dict(self.env['mandate.passenger'].fields_get(allfields=['type'])['type']['selection'])
        for rec in self:

            if rec.type:
                rec.type_desc = value[rec.type]
            else:
                rec.type_desc = ''

    def _getcoursetypedesc(self):
        value = dict(self.env['mandate.passenger'].fields_get(allfields=['course_type'])['course_type']['selection'])
        for rec in self:

            if rec.course_type:
                rec.course_type_desc = value[rec.course_type]
            else:
                rec.course_type_desc = ''

    def _get_state_desc(self):
        value = dict(self.env['mandate.passenger'].fields_get(allfields=['state'])['state']['selection'])

        for record in self:
            if record.state:
                record.state_desc = value[record.state]
            else:
                record.state_desc = ''

    state_desc = fields.Char(compute="_get_state_desc")
    type_desc = fields.Char(compute="_getdesc")
    course_type_desc= fields.Char(compute="_getcoursetypedesc")

    color = fields.Integer(compute="compute_color")

    department_id = fields.Many2one('hr.department')
    budget = fields.Float(compute="compute_budget_info")
    expensed_from_budget = fields.Float(compute="compute_budget_info")
    remaining_from_budget = fields.Float(compute="compute_budget_info")

    def return_main_department(self, department):
        if department and department.is_main_department:
            return department
        else:
            parent_department = department.parent_id
            return self.return_main_department(parent_department)

    def compute_budget_info(self):
        current_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        if current_employee_id and self.state == 'direct_manager_approve':
            for record in self:
                main_department = self.return_main_department(record.employee_id.department_id)
                if main_department:
                    budget_obj = self.env['budget.allocated.training'].search(
                        [('department_id.id', '=', main_department.id)], limit=1)
                    if budget_obj:
                        # record.department_id = budget_obj.department_id.id
                        record.budget = budget_obj.budget
                        record.expensed_from_budget = budget_obj.expensed_from_budget
                        record.remaining_from_budget = budget_obj.remaining_from_budget
                    else:
                        record.budget = 0.0
                        record.expensed_from_budget = 0.0
                        record.remaining_from_budget = 0.0
                else:
                    record.budget = 0.0
                    record.expensed_from_budget = 0.0
                    record.remaining_from_budget = 0.0
        else:
            self.budget = 0.0
            self.expensed_from_budget = 0.0
            self.remaining_from_budget = 0.0

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        employee = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_employee')
        direct_manager = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_direct_manager')
        department_manager = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_department_manager')
        accounting_manager = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_accounting_manager')
        center_manager = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_center_manager')
        hr_manager = self.env.user.has_group('ncss_mandate_passenger.mandate_passenger_hr_manager')
        order = "create_date desc"
        if center_manager or hr_manager:
            # current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
            # passenger_mandate_obj = self.search([])
            # for mandate in passenger_mandate_obj:
            #     lst.append(mandate.id)
            args += []
        if accounting_manager:
            current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
            # passenger_mandate_obj = self.search([('state', '=', 'department_manager_approve')])
            # for mandate in passenger_mandate_obj:
            #     lst.append(mandate.id)
            # print(self.create_uid)
            # print(":::LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL", self.is_department_manager)
            # main_department = self.return_main_department(self.employee_id.department_id)
            # print(":::::::::::::::::::", main_department)
            # print(":::::::::::::::::::", self.employee_id.department_id.name)
            # print(":::::::::::::::::::", self.employee_id.name)
            args += ['|', '|', ('create_uid.id', '=', self.env.user.id),
                     ('employee_id.parent_id.id', '=', current_user_id),
                     ('state', 'in', ['refuse', 'hr_approve', 'accounting_approve'])]

        # if department_manager:
        #     current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
        #     # passenger_mandate_obj = self.search(['|', ('employee_id.department_id.manager_id.id', '=', current_user_id),
        #     #                                      ('create_uid', '=', current_user_id)])
        #     # for mandate in passenger_mandate_obj:
        #     #     lst.append(mandate.id)
        #     args += ['|', '|', ('employee_id.department_id.manager_id.id', '=', current_user_id),
        #              ('employee_id.parent_id.id', '=', current_user_id),
        #              ('create_uid.id', '=', self.env.user.id)]

        if direct_manager:
            current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
            # passenger_mandate_obj = self.search(['|', ('employee_id.parent_id.id', '=', current_user_id), ('create_uid', '=', current_user_id)])
            # for mandate in passenger_mandate_obj:
            #     lst.append(mandate.id)
            # args += [('id', 'in', lst)]
            args += ['|', ('employee_id.parent_id.id', '=', current_user_id), ('create_uid.id', '=', self.env.user.id)]
        # else:
        if employee:
            args += [('create_uid', '=', self.env.user.id)]

        return super(MandatePassenger, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('mandate.passenger.sequence')
        res = super(MandatePassenger, self).create(values)
        user_ids = res.mapped('employee_id.parent_id.user_id').ids or [self.env.uid]
        res.make_activity(user_ids[0])
        message = 'تم انشاء طلب انتداب واركاب لك (%s)' % res['name']
        res.make_notification(message)
        return res

    def make_notification(self, message):
        now = datetime.now()
        start_date = now.date()
        end_date = start_date + timedelta(days=1)
        notify_id = self.env['hr.notification'].sudo().create({'notification_MSG': message,
                                                               'date_start': start_date,
                                                               'date_end': end_date,
                                                               'state': 'notify',
                                                               'employee_id': self.employee_id.id})
        print("notify_id", notify_id)

    def make_activity(self, user_ids):
        print("j...",user_ids)
        now = datetime.now()
        date_deadline = now.date()
        if self:
            if user_ids:
                actv_id=self.sudo().activity_schedule(
                    'mail.mail_activity_data_todo', date_deadline,
                    note=_(
                        '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for <a href="#" data-oe-model="%s" data-oe-id="%s">%s\'s</a> Review') % (
                             self._name, self.id, self.employee_id._name,
                             self.employee_id.id, self.employee_id.display_name),
                    user_id=user_ids,
                    res_id=self.id,

                    summary=_("Request Approve")
                    )
                print("active", actv_id)
                # now = datetime.now()
                # start_date = now.date()
                # end_date = start_date + timedelta(days=1)
                # notify_id = self.env['hr.notification'].sudo().create({'notification_MSG': message,
                #                                                        'date_start': start_date,
                #                                                        'date_end': end_date,
                #                                                        'state': 'notify',
                #                                                        'employee_id': self.employee_id.id})
                # print("notify_id", notify_id)

    @api.depends('state')
    def compute_color(self):
        for record in self:
            if record.state == 'draft':

                record.color = 2
            elif record.state == 'direct_manager_approve':
                # self.make_activity()
                record.color = 4
            elif record.state == 'department_manager_approve':
                record.color = 6
            elif record.state == 'accounting_approve':
                record.color = 8
            else:
                record.color = 10

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.employee_degree_id = self.employee_id.employee_degree_id.id
        self.traveling_type = self.employee_id.employee_degree_id.traveling_type

    @api.onchange('course_id')
    def onchange_company_id(self):
        for record in self:
            if record.course_id:
                if not record.employee_id:
                    raise UserError(_("Please Add Employee"))
                record.description = record.course_id.description
                record.course_type = record.course_id.type
                record.course_place_id = record.course_id.course_place_id.id
                record.price = record.course_id.price
                record.start_date = record.course_id.start_date
                record.end_date = record.course_id.end_date
                record.number_of_days = record.course_id.number_of_days
                record.description = record.course_id.description
                course_obj = self.search([('employee_id', '=', self.employee_id.id),
                                          ('state', '=', 'accounting_approve')], order='id desc')
                print("course_obj", course_obj)
                if course_obj:
                    print(">>>>>>>>>>>>>>>>.", course_obj[0])
                    start_year = date(self.course_id.end_date.year, 1, 1)
                    end_year = date(self.course_id.end_date.year, 12, 31)
                    print("course end_date", self.course_id.end_date)
                    print("start_year", start_year)
                    print("end_year", end_year)
                    courses_approved_within_year = self.search_count([('employee_id', '=', self.employee_id.id),
                                                                     ('state', '=', 'accounting_approve'),
                                                                     ('course_id.end_date', '>=', start_year),
                                                                     ('course_id.end_date', '<=', end_year),
                                                                     ('course_id.is_free', '=', self.course_id.is_free),
                                                                     ])
                    print("self.course_id.is_free", self.course_id.is_free)
                    print("courses_approved_within_year", courses_approved_within_year)
                    if self.course_id.is_free:
                        if courses_approved_within_year >= self.employee_degree_id.number_of_free_courses_per_year:
                            print("111111111111111111111")
                            raise UserError(_("You aren't allowed to Request Extra Free Courses "
                                              "The Number Of Courses "
                                              "Allowed For "
                                              "You Is"
                                              " %s" % self.employee_degree_id.number_of_free_courses_per_year))
                    else:
                        if courses_approved_within_year >= self.employee_degree_id.number_of_paid_courses_per_year:
                            print("2222222222222222222")
                            raise UserError(_("You aren't allowed to Request Extra Paid Courses "
                                              "The Number Of Courses "
                                              "Allowed For "
                                              "You Is"
                                              " %s" % self.employee_degree_id.number_of_paid_courses_per_year))
                    date_format = "%Y-%m-%d"
                    last_course_end_date = datetime.strptime(str(course_obj[0].course_id.end_date), date_format)
                    current_course_start_date = datetime.strptime(str(self.course_id.start_date), date_format)
                    difference_between_last_two_courses = float((current_course_start_date - last_course_end_date).days)

                    print("last_course_date", last_course_end_date)
                    print("current_course_date", current_course_start_date)
                    print("difference_between_last_two_courses", difference_between_last_two_courses)
                    print("allowed_period_between_courses", self.employee_degree_id.allowed_period_between_courses)
                    if difference_between_last_two_courses < self.employee_degree_id.allowed_period_between_courses:
                        raise UserError(_("You aren't allowed to Request Extra Course "
                                          "last course you take at %s" % course_obj[0].course_id.end_date))

    @api.depends('employee_degree_id', 'course_type', 'number_of_days')
    def get_total_value_without_ticket(self):
        for record in self:
            if record.course_type == 'internal':
                if record.employee_degree_id:
                   record.total_value_without_ticket = record.employee_degree_id.internal_day_value * record.number_of_days
            elif record.course_type == 'external':
                if record.employee_degree_id:
                    record.total_value_without_ticket = record.employee_degree_id.external_day_value * record.number_of_days
            else:
                record.total_value_without_ticket = 0.0

    @api.depends('total_value_without_ticket', 'number_of_days')
    def get_total_value(self):
        for record in self:
            if record.total_value_without_ticket > 0.0 and record.number_of_days > 0.0:
                record.day_value = record.total_value_without_ticket / record.number_of_days
                record.housing_value = (record.total_value_without_ticket*50)/100
                record.transportation_value = (record.total_value_without_ticket*25)/100
                record.daily_expenses = (record.total_value_without_ticket*25)/100
            else:
                record.day_value = 0.0
                record.housing_value = 0.0
                record.transportation_value = 0.0
                record.daily_expenses = 0.0

    @api.depends('total_value_without_ticket', 'price')
    def get_total_expenses(self):
        for record in self:
            record.total = record.total_value_without_ticket + record.price

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

    def compute_department_manager(self):
        current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
        for record in self:
            if record.employee_id.department_id:
                main_department = self.return_main_department(record.employee_id.department_id)
                if main_department and main_department.manager_id:
                    if main_department.manager_id.id == current_user_id:
                        budget_obj = self.env['budget.allocated.training'].search(
                            [('department_id.id', '=', main_department.id)], limit=1)
                            # [('department_id.id', '=', record.employee_id.department_id.id)], limit=1)
                        if budget_obj:
                            if budget_obj.remaining_from_budget > record.total:
                                self.is_department_manager = True
                            else:
                                self.is_department_manager = False
                        else:
                            self.is_department_manager = False
                    else:
                        self.is_department_manager = False
                else:
                    self.is_department_manager = False
            else:
                self.is_department_manager = False

    def action_direct_manager_approve(self):
        department_id = self.mapped('employee_id.department_id')
        if department_id:
            dep = self.return_main_department(department_id)
            user_ids = dep.mapped('manager_id.user_id').ids
            if user_ids:
                self.make_activity(user_ids[0])
        message = 'تمت موافقه المدير المباشر علي طلب الانتداب والاركاب الخاص بك (%s)' % self.name
        self.make_notification(message)
        self.state = 'direct_manager_approve'

    def get_users(self,groupidxml):
        myuserlist=[]
        groupid=self.env.ref(groupidxml).id
        groupObj = self.env['res.groups'].search([('id','=',groupid)])
        if groupObj:
              for rec in groupObj.users:
                  myuserlist.append(rec.id)

        return myuserlist

        #     for i in groupObj.users:
        #         userObj = self.env['res.users'].search([('id', '=', i.id)])

    def action_department_manager_approve(self):
        for record in self:
            budget_obj = self.env['budget.allocated.training'].search(
                [('department_id.id', '=', record.employee_id.department_id.id)], limit=1)
            if budget_obj:
                budget_obj.expensed_from_budget += record.total

            user_ids = list(self.get_users("ncss_mandate_passenger.mandate_passenger_hr_manager"))
            print (user_ids)
            if user_ids:
                for rec in user_ids:
                    self.make_activity(rec)
            message = 'تمت موافقه مدير القسم علي طلب الانتداب والاركاب الخاص بك (%s)' % self.name
            self.make_notification(message)
            record.state = 'department_manager_approve'

    def action_hr_manager_approve(self):
        user_ids = list(self.get_users("ncss_mandate_passenger.mandate_passenger_accounting_manager"))
        print(user_ids)
        if self.course_place_id.need_ticket:
            if not self.attach_file_ticket:
                raise UserError(_("Please Add Flight Ticket"))
        if user_ids:
            for rec in user_ids:
                self.make_activity(rec)
        message = 'تمت موافقه مدير الموارد البشريه علي طلب الانتداب والاركاب الخاص بك (%s)' % self.name
        self.make_notification(message)
        self.state = 'hr_approve'

    def action_accounting_approve(self):
        if self.course_place_id.need_ticket:
            if not self.attach_file_ticket:
                raise UserError(_("Please Add Flight Ticket"))
        message = 'تمت موافقه مدير الحسابات علي طلب الانتداب والاركاب الخاص بك (%s)' % self.name
        self.make_notification(message)
        hr_attendance = self.env['hr.attendance']
        start_date = self.start_date
        end_date = self.end_date
        num_of_days = (end_date - start_date).days
        i = 0
        string_to_date = start_date.strftime("%Y-%m-%d 08:00:00")
        string_to_end_date = start_date.strftime("%Y-%m-%d 15:00:00")
        date_with_time = datetime.strptime(string_to_date, '%Y-%m-%d %H:%M:%S')
        end_date_with_time = datetime.strptime(string_to_end_date, '%Y-%m-%d %H:%M:%S')
        for i in range(num_of_days+1):
            start_date_with_time = date_with_time + timedelta(days=i)
            end_date_time = end_date_with_time + timedelta(days=i)
            hr_attendance.sudo().create({
                'employee_id': self.employee_id.id,
                'check_in': start_date_with_time,
                'check_out': end_date_time,
                'description': self.name or 'حاضر بدوره',

            })
            i += 1
        self.state = 'accounting_approve'
        # employee_work_hours = self.employee_id.resource_calendar_id.attendance_ids
        # print(":::::::::employee_work_hours::::::::::", employee_work_hours[0].hour_from)
        # raise UserError(_(employee_work_hours[0].hour_from))
        # dt = datetime.combine(date.today(), datetime.min.time())
        # print(":::::::::::::::", dt)

    def refuse_action(self):
        for record in self:
            if not record.reason:
                raise UserError(_("Please Add the reason of Refuse"))
            else:
                message = 'تمت رفض طلب الانتداب والاركاب الخاص بك (%s)' % self.name
                self.make_notification(message)
                self.state = 'refuse'

    def set_to_draft(self):
        message = 'تمت اعاده طلب الانتداب والاركاب الخاص بك كجديد (%s)' % self.name
        self.make_notification(message)
        self.state = 'draft'
