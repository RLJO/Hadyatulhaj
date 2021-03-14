from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_level_approve = fields.Boolean(default=True)
    level_one_amount = fields.Float(default=0.0)
    level_two_amount = fields.Float(default=0.0)
    level_three_amount = fields.Float(default=0.0)


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    is_level_approve = fields.Boolean(default=lambda self: self.env.user.company_id.is_level_approve)
    level_one_amount = fields.Float(default=lambda self: self.env.user.company_id.level_one_amount)
    level_two_amount = fields.Float(default=lambda self: self.env.user.company_id.level_two_amount)
    level_three_amount = fields.Float(default=lambda self: self.env.user.company_id.level_three_amount)

    @api.constrains('level_two_amount', 'level_three_amount')
    def constrains_level_two_amount(self):
        if self.level_one_amount and self.level_two_amount:
            if self.level_one_amount > self.level_two_amount:
                raise UserError(_("Level Two Amount Must Be Greater Than "
                                  "Or Equal To Level One Amount"))
        if self.level_three_amount and self.level_two_amount:
            if self.level_two_amount > self.level_three_amount:
                raise UserError(_("Level Three Amount Must Be Greater Than "
                                  "Or Equal To Level One Amount"))

    @api.model
    def create(self, values):
        if 'company_id' in values \
                or 'is_level_approve' in values \
                or 'level_one_amount' in values \
                or 'level_two_amount' in values \
                or 'level_three_amount' in values:
            self.env.user.company_id.write({
                    'is_level_approve': values['is_level_approve'],
                    'level_one_amount': values['level_one_amount'],
                    'level_two_amount': values['level_two_amount'],
                    'level_three_amount': values['level_three_amount'],
                 })
        res = super(PurchaseConfigSettings, self).create(values)
        return res
