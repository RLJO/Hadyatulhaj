# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    first_note = fields.Text('Reason One')
    second_note = fields.Text('Reason Two')
    third_note = fields.Text('Reason Three')
    is_confirm = fields.Boolean(default=True)
    is_level1_approve = fields.Boolean(default=False)
    is_level2_approve = fields.Boolean(default=False)
    is_level3_approve = fields.Boolean(default=False)
    is_request_approve = fields.Boolean(default=False)
    is_level_approve = fields.Boolean(default=lambda self: self.env.user.company_id.is_level_approve)
    level_one_amount = fields.Float(default=lambda self: self.env.user.company_id.level_one_amount)
    level_two_amount = fields.Float(default=lambda self: self.env.user.company_id.level_two_amount)
    level_three_amount = fields.Float(default=lambda self: self.env.user.company_id.level_three_amount)
    approved_by1_id = fields.Many2one('res.users', string="Approved By")
    approved_by2_id = fields.Many2one('res.users', string="Approved By")
    approved_by3_id = fields.Many2one('res.users', string="Approved By")
    level_one_approved_date = fields.Date('Date')
    level_two_approved_date = fields.Date('Date')
    level_third_approved_date = fields.Date('Date')
    state = fields.Selection(selection_add=[
        ('waiting approve1', 'waiting First approve'),
        ('waiting approve2', 'waiting second approve'),
        ('waiting approve3', 'waiting third approve'),
        ('waiting special approve', 'waiting special approve'),
        ('approve', 'Approved'),
        ('refuse1', 'Refuse'),
        ('refuse2', 'Refuse'),
        ('refuse3', 'Refuse'),
    ])

    def make_activity(self, user_ids):
        print("user_ids...", user_ids)
        now = datetime.now()
        date_deadline = now.date()
        values = {
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'purchase.order')]).id,
            'user_id': user_ids,
            'summary': 'Purchase Request',
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'date_deadline': date_deadline
        }
        self.env['mail.activity'].create(values)

    def get_users(self, group_id_xml):
        user_list = []
        group_id = self.env.ref(group_id_xml).id
        group_obj = self.env['res.groups'].search([('id', '=', group_id)])
        if group_obj:
            for rec in group_obj.users:
                user_list.append(rec.id)
        return user_list

    @api.model
    def create(self, values):
        res = super(PurchaseOrder, self).create(values)
        now = datetime.now()
        date_deadline = now.date()
        data = {
            'res_id': res.id,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'purchase.order')]).id,
            'user_id': self.env.uid,
            'summary': 'Purchase Request',
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'date_deadline': date_deadline
        }
        self.env['mail.activity'].create(data)
        if res.is_level_approve:
            if res.amount_total >= res.level_one_amount:
                res.is_request_approve = True
                res.is_confirm = True
            res.request_approval()
        return res

    def write(self, values):
        res = super(PurchaseOrder, self).write(values)
        print(values)
        if 'order_line' in values:
            if self.is_level_approve:
                if self.amount_total >= self.level_one_amount:
                    self.is_request_approve = True
                    self.is_confirm = True
        return res

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'approve']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.sudo().button_approve()
            else:
                order.sudo().write({'state': 'to approve'})
            order.is_confirm = True
        return True

    def request_approval(self):
        if self.amount_total >= self.level_one_amount:
            self.state = 'waiting approve1'
            self.is_level1_approve = True
            self.is_request_approve = False

            user_ids = list(self.get_users("ncss_purchase_level_approval.group_purchase_first_approval"))
            if user_ids:
                for rec in user_ids:
                    print("user first approve", rec)
                    self.make_activity(rec)

    def request_approval1(self):
        if self.amount_total >= self.level_two_amount:
            self.state = 'waiting approve2'
            self.is_level1_approve = False
            self.is_level2_approve = True
            user_ids = list(self.get_users("ncss_purchase_level_approval.group_purchase_second_approval"))
            if user_ids:
                for rec in user_ids:
                    print("user second approve", rec)
                    self.make_activity(rec)
        else:
            self.state = 'approve'
            self.is_level1_approve = False
            user_ids = list(self.get_users("ncss_purchase_level_approval.group_button_confirm"))
            if user_ids:
                for rec in user_ids:
                    print("user confirm order approve", rec)
                    self.make_activity(rec)
        self.approved_by1_id = self.env.user.id
        self.level_one_approved_date = fields.Date.today()

    def request_approval2(self):
        if self.amount_total >= self.level_three_amount:
            self.state = 'waiting approve3'
            self.is_level1_approve = False
            self.is_level2_approve = False
            self.is_level3_approve = True
            user_ids = list(self.get_users("ncss_purchase_level_approval.group_purchase_third_approval"))
            if user_ids:
                for rec in user_ids:
                    print("user third approve", rec)
                    self.make_activity(rec)

        else:
            self.state = 'approve'
            self.is_level1_approve = False
            self.is_level2_approve = False
            user_ids = list(self.get_users("ncss_purchase_level_approval.group_button_confirm"))
            if user_ids:
                for rec in user_ids:
                    print("user confirm order approve", rec)
                    self.make_activity(rec)
        self.approved_by2_id = self.env.user.id
        self.level_two_approved_date = fields.Date.today()

        # self.state = 'approve'
        # self.is_level2_approve = False
        # self.approved_by2_id = self.env.user.id
        # self.level_two_approved_date = fields.Date.today()

    def request_approval3(self):
        self.state = 'approve'
        self.is_level3_approve = False
        self.approved_by3_id = self.env.user.id
        self.level_third_approved_date = fields.Date.today()
        user_ids = list(self.get_users("ncss_purchase_level_approval.group_button_confirm"))
        if user_ids:
            for rec in user_ids:
                print("user confirm order approve", rec)
                self.make_activity(rec)

    def refuse_to_approve(self):
        if self.state == 'waiting approve1':
            if not self.first_note:
                raise UserError(_("Please Add The Reason Of Refuse"))
            self.state = 'refuse1'
            self.is_level1_approve = False
        elif self.state == 'waiting approve2':
            if not self.second_note:
                raise UserError(_("Please Add The Reason Of Refuse"))
            self.state = 'refuse2'
            self.is_level2_approve = False
        else:
            if not self.third_note:
                raise UserError(_("Please Add The Reason Of Refuse"))
            self.state = 'refuse3'
            self.is_level3_approve = False

    def request_special_approval(self):
        self.state = 'waiting special approve'

    def special_approve_action(self):
        self.state = 'approve'
