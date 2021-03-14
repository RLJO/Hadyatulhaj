# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AdministrativeDecisionsType(models.Model):
    _name = 'administrative.decisions.type'
    _description = 'Administrative Decisions Type'

    name = fields.Char(required=1)


class HrAdministrativeDecisions(models.Model):
    _name = 'hr.administrative.decisions'
    _description = 'Administrative Decisions'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,
                                  track_visibility='onchange')
    decision_type_id = fields.Many2one('administrative.decisions.type', string='Type Of Decision')
    date = fields.Date(string="Date")
    description = fields.Text(string="Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('first_approve', 'First Approve'),
        ('second_approve', 'Second Approve')
    ], string='Status', readonly=True, tracking=True, copy=False, default='draft')

    def action_draft(self):
        self.state = "draft"

    def action_first_approve(self):
        self.state = "first_approve"

    def action_second_approve(self):
        self.state = "second_approve"

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_('You Can Not Delete a Record Which Is Not Draft.'))
            res = super(HrAdministrativeDecisions, record).unlink()
            return res
