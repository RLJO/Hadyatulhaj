# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AppraisalRecommendations(models.Model):
    _name = 'appraisal.recommendations'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    is_default = fields.Boolean('Default recommendations')


class AppraisalManagerRecommendations(models.Model):
    _name = 'appraisal.manager.recommendations'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    appraisal_manager_recommendations_id = fields.Many2one('hr.employee.appraisal')
    appraisal_recommendation_id = fields.Many2one('appraisal.recommendations')
    approve_recommendation = fields.Boolean('Yes')
    disagree_recommendation = fields.Boolean('No')


class StrongWeakPointLines(models.Model):
    _name = 'strong.weak.point.lines'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    strong_weak_point_lines_id = fields.Many2one('hr.employee.appraisal')
    strong_points = fields.Char()
    weak_points = fields.Char()


class AppraisalLevel(models.Model):
    _name = 'appraisal.level'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()


class AppraisalCriteria(models.Model):
    _name = 'appraisal.criteria'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    max_limit = fields.Float()
    is_default = fields.Boolean('Default Criteria')


class AppraisalItem(models.Model):
    _name = 'appraisal.item'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    hr_employee_appraisal_id = fields.Many2one('hr.employee.appraisal')
    appraisal_criteria_id = fields.Many2one('appraisal.criteria')
    max_limit = fields.Float()
    deserved_degree = fields.Float()
    appraisal_level = fields.Char(compute='compute_appraisal_level')
    appraisal_level_id = fields.Many2one('appraisal.level')

    @api.onchange('deserved_degree')
    def onchange_deserved_degree(self):
        for record in self:
            if record.deserved_degree > record.max_limit:
                raise UserError(_("Deserve degree must be less than maximum limit"))

    @api.onchange('deserved_degree', 'max_limit')
    def compute_appraisal_level(self):
        for record in self:
            if record.deserved_degree and record.max_limit:
                result = (record.deserved_degree / record.max_limit)*100
                print("::::::::::::::result : ", result)
                if result < 50:
                    record.appraisal_level = 'ضعيف'
                elif 50 < result <= 65:
                    record.appraisal_level = 'مقبول'
                elif 65 < result <= 75:
                    record.appraisal_level = 'جيد'
                elif 75 < result <= 89:
                    record.appraisal_level = 'عالي / جيد جداً'
                else:
                    record.appraisal_level = 'متميز / ممتاز'
            else:
                record.appraisal_level = ' '


class AdministrativeCommunication(models.Model):
    _name = 'hr.employee.appraisal'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee')
    manager_id = fields.Many2one('hr.employee')
    appraisal_id = fields.Many2one('hr.appraisal')
    appraisal_item_ids = fields.One2many('appraisal.item', 'hr_employee_appraisal_id', copy=True)
    strong_weak_point_ids = fields.One2many('strong.weak.point.lines', 'strong_weak_point_lines_id', copy=True)
    appraisal_manager_recommendations_ids = fields.One2many('appraisal.manager.recommendations',
                                                            'appraisal_manager_recommendations_id', copy=True)
    total_deserve_appraisal = fields.Float(compute='compute_total_deserve_appraisal')
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('completed', 'Completed'),
                                        ], default='draft')

    def action_complete_appraisal(self):
        self.state = 'completed'

    @api.depends('appraisal_item_ids')
    def compute_total_deserve_appraisal(self):
        for record in self:
            record.total_deserve_appraisal = sum([line.deserved_degree for line in record.appraisal_item_ids])


#     sequence = fields.Char()
#     treatment_type = fields.Selection([('in', 'Incoming'), ('out', 'Outgoing'), ('internal', 'Internal')])
#     administrative_communication_out_id = fields.Many2one('administrative.communication', 'Outgoing')
#     # change to selection
#     post_type = fields.Selection([('paper', 'Paper'), ('fax', 'Fax'), ('electronic', 'Electronic')])
#     category_name = fields.Char()
#     # post type
#
#     assign_to_id = fields.Many2one('administrative.communication.category', 'Assign To')
#     assign_to_department_id = fields.Many2one('administrative.communication.category', 'Assign To Department')
#
#     # new field
#     nature_of_transaction = fields.Selection([('personal', 'Personal'), ('public', 'Public'), ('secret', 'Secret')])
#     way_of_send = fields.Selection([('manual', 'manual'), ('email', 'email'), ('fax', 'Fax'), ('post', 'post')])
#     #
#     transactions_number = fields.Char()
#     years = fields.Many2one('administrative.communication.years')
#     reference_number = fields.Char()
#     transaction_date = fields.Date('Transaction Date', default=fields.Date.today())
#     hijri_date = fields.Char('Date', compute='_calculate_hijri_date', store=True)
#     # source_id = fields.Many2one('administrative.communication.source')
#     source_id = fields.Many2one('administrative.communication.category')
#     destination_id = fields.Many2one('administrative.communication.source')
#     transfer_to_id = fields.Many2one('administrative.communication.management')
#     user_id = fields.Many2one('res.users')
#
#     internal_source_department_id = fields.Many2one('administrative.communication.management')
#     internal_source_manager_id = fields.Many2one('res.users')
#
#     contact_id = fields.Many2one('administrative.communication.contact')
#     transfer_date = fields.Date('Receipt Date', default=fields.Date.today())
#     allow_transfer_date = fields.Boolean()
#     edit_transaction_date = fields.Boolean()
#     transfer_number = fields.Char()
#     attachments = fields.Integer()
#     subject = fields.Text()
#     file_number = fields.Char()
#     notes = fields.Char()
#     sender_type = fields.Many2one('administrative.communication.sender')
#     transaction_line_ids = fields.One2many('administrative.communication.line', 'administrative_communication_id',
#                                            copy=True)
#     transaction_attachment_line_ids = fields.One2many('administrative.communication.attachments',
#                                                       'administrative_communication_id', copy=True)
#     state = fields.Selection([('draft', 'Draft'),
#                               ('reviewed', 'sent to department'),
#                               ('assigned', 'Sent To Employee'),
#                               ('outgoing', 'Outgoing Sent'),
#                               ('barcode', 'Barcode'),
#                               ('instrument', 'Instrument'),
#                               ('done', 'Done'),
#                               ], default='draft')
#     state_in = fields.Selection(related='state')
#     state_out = fields.Selection(related='state')
#
#     # @api.model
#     # def search(self, args, offset=0, limit=None, order=None, count=False):
#     #     employee = self.env.user.has_group('ncss_administrative_communications.administrative_communication_employee')
#     #     department_manager = self.env.user.has_group('ncss_administrative_communications.administrative_communication_department_manager')
#     #     center_manager = self.env.user.has_group('ncss_administrative_communications.administrative_communication_center_manager')
#     #
#     #     if employee:
#     #         args += ['|', ('user_id', '=', self.env.user.id), ('create_uid', '=', self.env.user.id)]
#     #     if department_manager:
#     #         args += ['|', '|', '|', ('user_id', '=', self.env.user.id),
#     #                  ('create_uid.id', '=', self.env.user.id),
#     #                  ('transfer_to_id.id', '=', self.env.user.ncss_department_id.id),
#     #                  ('transfer_to_id.user_id.id', '=', self.env.user.id),
#     #                  ]
#     #     if center_manager:
#     #         args += []
#     #     return super(AdministrativeCommunication, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
#
#     def get_users(self, group_id):
#         user_list = []
#         group_obj = self.env.ref(group_id).id
#         group_ids = self.env['res.groups'].search([('id', '=', group_obj)])
#         if group_ids:
#             for rec in group_ids.users:
#                 if rec.id not in user_list:
#                     user_list.append(rec.id)
#         return user_list
#
#     def create_activity(self, user_id, message):
#         print(":::::::::::::::", user_id, message)
#         now = datetime.now()
#         date_deadline = now.date()
#         values = {
#             'res_id': self.id,
#             'res_model_id': self.env['ir.model'].search([('model', '=', 'administrative.communication')]).id,
#             'user_id': user_id,
#             'summary': message,
#             'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
#             'date_deadline': date_deadline
#         }
#         self.env['mail.activity'].sudo().create(values)
#
#     @api.model
#     def create(self, values):
#         if values['treatment_type'] == 'in':
#             values['sequence'] = self.env['ir.sequence'].next_by_code('administrative.communication.import')
#         elif values['treatment_type'] == 'out':
#             values['sequence'] = self.env['ir.sequence'].next_by_code('administrative.communication.export')
#         else:
#             values['sequence'] = self.env['ir.sequence'].next_by_code('administrative.communication.internal')
#         res = super(AdministrativeCommunication, self).create(values)
#
#         user_ids = res.get_users("ncss_administrative_communications.administrative_communication_assign_to_department_button")
#         message = 'معامله رقم %s ' % res['sequence']
#         if user_ids:
#             for rec in user_ids:
#                 res.create_activity(rec, message)
#         return res
#
#     @api.onchange('internal_source_department_id')
#     def onchange_internal_source_department_id(self):
#         self.internal_source_manager_id = self.internal_source_department_id.user_id.id
#
#     @api.onchange('transfer_to_id')
#     def onchange_transfer_to_id(self):
#         self.user_id = self.transfer_to_id.user_id.id
#
#     @api.onchange('assign_to_id')
#     def onchange_assign_to_id(self):
#         self.assign_to_department_id = self.assign_to_id.id
#
#     @api.depends('transaction_date')
#     def _calculate_hijri_date(self):
#         cal = calverter.Calverter()
#         for rec in self:
#             if rec.transaction_date:
#                 d = rec.transaction_date
#                 jd = cal.gregorian_to_jd(d.year, d.month, d.day)
#                 hj = cal.jd_to_islamic(jd)
#                 rec.hijri_date = str(hj[2]) + "/" + str(hj[1]) + "/" + str(hj[0])
#
#     def action_administrative_communication(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Assigned To My Department',
#             'res_model': 'administrative.communication',
#             'domain': [('user_id', '=', self.env.user.id)],
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#         }
#
#     def make_activity(self, user_ids):
#         print("j...", user_ids)
#         now = datetime.now()
#         date_deadline = now.date()
#
#         if self:
#
#             if user_ids:
#                 actv_id = self.sudo().activity_schedule(
#                     'mail.mail_activity_data_todo', date_deadline,
#                     note=_(
#                         '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for %s\'Review') % (
#                              self._name, self.id,
#                              self.user_id.display_name),
#                     user_id=user_ids,
#                     res_id=self.id,
#
#                     summary=_("Request Approve")
#                 )
#                 print("active", actv_id)
#
#     def assign_to_department_action(self):
#         if not self.transfer_to_id:
#             raise UserError(_('Please Add The Department.'))
#         if self.user_id:
#             message = 'معامله رقم %s ' % self.sequence
#             self.create_activity(self.user_id.id, message)
#         self.state = 'reviewed'
#
#     def assign_to_employee_action(self):
#         if not self.user_id:
#             raise UserError(_('Please Add The Specialized Employee.'))
#         self.state = 'assigned'
#
#     @api.returns('self', lambda value: value.id)
#     def copy(self, default=None):
#         self.ensure_one()
#         return super(AdministrativeCommunication, self).copy(default)
#
#     def outgoing_treatment_action(self):
#         self.state = 'outgoing'
#         default = {}
#         default['treatment_type'] = 'out'
#         # default['destination_id'] = self.source_id.id
#         default['transfer_to_id'] = False
#         # default['source_id'] = self.env.ref('ncss_administrative_communications.demo_contact_ncss').id
#         default['source_id'] = self.env.ref('ncss_administrative_communications.demo_source_direction').id
#         default['assign_to_id'] = self.source_id.id
#         y = self.copy(default)
#         y.administrative_communication_in_id = self.id
#         self.administrative_communication_out_id = y.id
#
#         user_ids = self.get_users("ncss_administrative_communications.administrative_communication_done_button")
#         message = 'معامله صادره رقم %s ' % y.sequence
#         if user_ids:
#             for rec in user_ids:
#                 self.create_activity(rec, message)
#
#         barcode_user_ids = self.get_users("ncss_administrative_communications.administrative_communication_print_barcode_button")
#         barcode_message = 'معامله صادره رقم %s يمكنك طباعه الباركود الان' % y.sequence
#         if barcode_user_ids:
#             for code in barcode_user_ids:
#                 # self.create_activity(code, barcode_message)
#                 now = datetime.now()
#                 date_deadline = now.date()
#                 values = {
#                     'res_id': y.id,
#                     'res_model_id': self.env['ir.model'].search([('model', '=', 'administrative.communication')]).id,
#                     'user_id': code,
#                     'summary': barcode_message,
#                     'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
#                     'date_deadline': date_deadline
#                 }
#                 self.env['mail.activity'].sudo().create(values)
#
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Administrative Communication',
#             'res_model': 'administrative.communication',
#             'res_id': y.id,
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'current',
#         }
#
#     def action_assign_to(self):
#         ncss_department_id = self.env.user.ncss_department_id
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'administrative communication wizard',
#             'res_model': 'administrative.communication.wizard',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'context': {
#                 'default_ncss_department_id': ncss_department_id.id if ncss_department_id else False,
#                 'default_position': self.env.user.position,
#             },
#             'target': 'new',
#         }
#
#     def outgoing_barcode_action(self):
#         self.state = 'barcode'
#         user_ids = self.get_users("ncss_administrative_communications.administrative_communication_print_instrument_button")
#         message = 'معامله صادره رقم %s يمكنك طباعه السند الان' % self.sequence
#         if user_ids:
#             for rec in user_ids:
#                 self.create_activity(rec, message)
#         return self.env.ref('ncss_administrative_communications.barcode_report').report_action(self)
#
#     def outgoing_instrument_action(self):
#         self.state = 'instrument'
#         user_ids = self.get_users(
#             "ncss_administrative_communications.administrative_communication_done_button")
#         message = 'معامله صادره رقم %s يمكنك اكمالها الان' % self.sequence
#         if user_ids:
#             for rec in user_ids:
#                 self.create_activity(rec, message)
#         return self.env.ref('ncss_administrative_communications.report_administrative_communication').\
#             report_action(self)
#
#     def action_done(self):
#         self.state = 'done'
#
#     def set_to_draft(self):
#         self.state = 'draft'
#
#
# class AdministrativeCommunicationWizard(models.TransientModel):
#     _name = 'administrative.communication.wizard'
#
#     user_id = fields.Many2one('res.users')
#     procedure_id = fields.Many2one('administrative.communication.procedures')
#     sender_notes = fields.Char()
#     # receipt_notes = fields.Char()
#     ncss_department_id = fields.Many2one('administrative.communication.management')
#     position = fields.Selection([('regular', 'Regular'),
#                                  ('center_manager', 'Center Manager'),
#                                  ('department_manager', 'Manager'),
#                                  ])
#     no_of_days = fields.Integer()
#     due_date = fields.Date(default=fields.date.today())
#
#     @api.onchange('procedure_id')
#     def onchange_procedure_id(self):
#         self.no_of_days = self.procedure_id.no_of_days
#
#     @api.onchange('no_of_days')
#     def onchange_no_of_days(self):
#         self.due_date = fields.date.today() + timedelta(days=self.no_of_days)
#
#     @api.onchange('position', 'ncss_department_id')
#     def onchange_position(self):
#         users = []
#         user_obj = self.env['res.users']
#         if self.position == 'regular':
#             user_ids = user_obj.search([('position', '=', 'regular'),
#                                         ('ncss_department_id', '=', self.ncss_department_id.id)])
#             for user in user_ids:
#                 users.append(user.id)
#
#         elif self.position == 'center_manager':
#             user_ids = user_obj.search([('position', '=', 'department_manager')])
#             for user in user_ids:
#                 users.append(user.id)
#
#         elif self.position == 'department_manager':
#             user_ids = user_obj.search([])
#             for user in user_ids:
#                 users.append(user.id)
#         else:
#             users = []
#         domain = {'user_id': [('id', 'in', users)]}
#         return {'domain': domain}
#
#     def make_activity(self, user_ids):
#         print("j...", user_ids)
#         now = datetime.now()
#         date_deadline = now.date()
#
#         if self:
#
#             if user_ids:
#                 actv_id = self.sudo().activity_schedule(
#                     'mail.mail_activity_data_todo', date_deadline,
#                     note=_(
#                         '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for %s\'Review') % (
#                              self._name, self.id,
#                              self.user_id.display_name),
#                     user_id=user_ids,
#                     res_id=self.id,
#
#                     summary=_("Request Approve")
#                 )
#                 print("active", actv_id)
#
#     def get_users(self, group_id):
#         user_list = []
#         group_obj = self.env.ref(group_id).id
#         group_ids = self.env['res.groups'].search([('id', '=', group_obj)])
#         if group_ids:
#             for rec in group_ids.users:
#                 if rec.id not in user_list:
#                     user_list.append(rec.id)
#         return user_list
#
#     def create_activity(self, user_id, message):
#         print(":::::::::::::::", user_id, message)
#         now = datetime.now()
#         date_deadline = now.date()
#         values = {
#             'res_id': self.env.context.get('active_ids')[0],
#             'res_model_id': self.env['ir.model'].search([('model', '=', 'administrative.communication')]).id,
#             'user_id': user_id,
#             'summary': message,
#             'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
#             'date_deadline': date_deadline
#         }
#         self.env['mail.activity'].sudo().create(values)
#
#     def action_assign_to(self):
#         print(self.env.context.get('active_ids')[0])
#         communication_id = self.env['administrative.communication'].sudo().browse(self.env.context.get('active_ids')[0])
#         communication_lines = self.env['administrative.communication.line']
#         communication_line_obj = communication_lines.sudo().create({
#             'administrative_communication_id': self.env.context.get('active_ids')[0],
#             'user_attached_id': self.env.user.id,
#             'user_id': self.user_id.id,
#             'procedure_id': self.procedure_id.id,
#             'due_date': self.due_date,
#             'sender_notes': self.sender_notes,
#         })
#
#         user_ids = self.get_users("ncss_administrative_communications.administrative_communication_outgoing_button")
#         message = 'معامله رقم %s ' % communication_id.sequence
#         if user_ids:
#             for rec in user_ids:
#                 self.create_activity(rec, message)
#
#         if self.user_id:
#             # communication_lines.make_activity(self.user_id.id)
#             now = datetime.now()
#             date_deadline = now.date()
#             values = {
#                 'res_id': communication_line_obj.id,
#                 'res_model_id': self.env['ir.model'].search([('model', '=', 'administrative.communication.line')]).id,
#                 'user_id': self.user_id.id,
#                 'summary': 'معامله محاله اليك',
#                 'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
#                 'date_deadline': date_deadline
#             }
#             self.env['mail.activity'].create(values)
#         if communication_id.state == 'reviewed':
#             communication_id.state = 'assigned'
#
#
# class AdministrativeCommunicationLine(models.Model):
#     _name = 'administrative.communication.line'
#     _rec_name = "administrative_communication_id"
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#
#     administrative_communication_id = fields.Many2one('administrative.communication')
#     attached_by_id = fields.Many2one('administrative.communication.contact')
#     recipient_by_id = fields.Many2one('administrative.communication.contact')
#     user_attached_id = fields.Many2one('res.users')
#     user_id = fields.Many2one('res.users')
#     source_id = fields.Many2one('administrative.communication.source')
#     transfer_to_id = fields.Many2one('administrative.communication.management')
#     procedure_id = fields.Many2one('administrative.communication.procedures')
#     sender_type = fields.Many2one('administrative.communication.sender')
#     date_and_time = fields.Datetime('Date And Time', default=datetime.now())
#     notes = fields.Char()
#     sender_notes = fields.Char()
#     receipt_notes = fields.Char()
#     due_date = fields.Date()
#     subject = fields.Text(related="administrative_communication_id.subject")
#
#     # @api.model
#     # def search(self, args, offset=0, limit=None, order=None, count=False):
#     #     employee = self.env.user.has_group('ncss_administrative_communications.administrative_communication_employee')
#     #     department_manager = self.env.user.has_group('ncss_administrative_communications.administrative_communication_department_manager')
#     #     center_manager = self.env.user.has_group('ncss_administrative_communications.administrative_communication_center_manager')
#     #
#     #     if employee:
#     #         args += ['|', ('user_id', '=', self.env.user.id), '|',
#     #                  ('create_uid', '=', self.env.user.id),
#     #                  ('user_attached_id', '=', self.env.user.id),
#     #                  ]
#     #     # if department_manager:
#     #     #     args += ['|', '|','|', '|', ('user_id', '=', self.env.user.id),
#     #     #              ('create_uid', '=', self.env.user.id),
#     #     #              ('user_attached_id', '=', self.env.user.id),
#     #     #              ('user_id', '=', self.env.user.id),
#     #     #              ('user_id.ncss_department_id.id', '=', self.env.user.ncss_department_id.id),
#     #     #              ]
#     #     # if center_manager:
#     #     #     args += []
#     #     return super(AdministrativeCommunicationLine, self).search(args=args, offset=offset, limit=limit, order=order,count=count)
#
#     @api.onchange('source_id', 'transfer_to_id')
#     def onchange_source_id(self):
#         contacts = []
#         transfers = []
#         for record in self:
#             for c in record.source_id.contact_line_ids:
#                 contacts.append(c.contact_id.id)
#             for t in record.transfer_to_id.contact_line_ids:
#                 transfers.append(t.contact_id.id)
#         domain = {'attached_by_id': [('id', 'in', contacts)], 'recipient_by_id': [('id', 'in', transfers)]}
#         return {'domain': domain}
#
#
# class AdministrativeCommunicationAttachments(models.Model):
#     _name = 'administrative.communication.attachments'
#
#     administrative_communication_id = fields.Many2one('administrative.communication')
#     attachments = fields.Binary()
#     attachment_ids = fields.Many2many('ir.attachment', 'admin_attach_rel', 'doc_id', 'attach_id4',
#                                       string=_('Attachment ticket'),
#                                       help='You can attach the copy of your document', copy=False)
#
#     description = fields.Char()
#
#
# # class HrEmployeeAttachment(models.Model):
# #     _inherit = 'ir.attachment'
# #
# #     doc_attach_rel = fields.Many2many('administrative.communication.attachments', 'doc_attachment_id',
# #                                       'attach_id8', 'doc_id8',
# #                                       string="Attachment", invisible=1)
