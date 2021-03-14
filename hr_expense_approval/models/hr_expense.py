from odoo import api, fields, models, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    state = fields.Selection(selection_add=[('direct_manager_approve', 'Direct Manager Approve'),
                                            ('center_manager_approve', 'Center Manager Approve'),
                                            ])
    is_direct_manager = fields.Boolean(compute='get_direct_manager')

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

    def direct_manager_approve(self):
        if self.total_amount > self.env.user.company_id.expense_limit_amount:
            self.write({'state': 'direct_manager_approve'})
        else:
            self.approve_expense_sheets()

    def center_manager_approve(self):
        self.approve_expense_sheets()


class ResCompany(models.Model):
    _inherit = 'res.company'

    expense_limit_amount = fields.Float()


class RequisitionConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    expense_limit_amount = fields.Float(default=lambda self: self.env.user.company_id.expense_limit_amount)

    @api.model
    def create(self, values):
        if 'company_id' in values\
                or 'expense_limit_amount' in values:
            self.env.user.company_id.write({
                    'expense_limit_amount': values['expense_limit_amount'],
                 })
        res = super(RequisitionConfigSettings, self).create(values)
        return res
