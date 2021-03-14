# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LetterLetter(models.Model):
    _name = 'letter.letter'
    _inherit = ['mail.thread', 'mail.activity.mixin'  ]

    name  = fields.Char()
    template_id = fields.Html('Template',translate=True, sanitize=False)


    model_id = fields.Many2one('ir.model', 'Applies to', help="The type of document this template can be used with")
    model = fields.Char('Related Document Model', related='model_id.model', index=True, store=True, readonly=True)


class LetterRequest(models.Model):
    _name = 'letter.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    Date = fields.Date()
    letter_type_id = fields.Many2one('letter.letter')
    request_id = fields.Many2one('hr.employee', 'Requester')
    employee_id = fields.Many2one('hr.employee', 'Approval')
    note = fields.Text()
    state = fields.Selection(selection=[('Draft', 'Draft'),
                                        ('Approve', 'Approve'),
                                        ('Cancel', 'Cancel'),
                                        ], default='Draft')

    def action_draft(self):
        for record in self:
            record.state = 'Draft'

    def action_approve(self):
        for record in self:
            record.state = 'Approve'

    def action_cancel(self):
        for record in self:
            record.state = 'Cancel'
