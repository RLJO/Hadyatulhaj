from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('Accounting Approve', 'Accounting Approved'),
        ('Administrative and Financial Affairs', 'Administrative and Financial Affairs Approved'),
        ('Financial auditor', 'Financial Auditor Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    def action_accounting_approve(self):
        self.state = 'Accounting Approve'

    def action_financial_affairs(self):
        self.state = 'Administrative and Financial Affairs'

    def action_financial_auditor(self):
        self.state = 'Financial auditor'
