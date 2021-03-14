import time
import datetime
from dateutil.relativedelta import relativedelta

import odoo
from odoo import SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    home_allowance = fields.Float()
    transportation_allowance = fields.Float()


class AllocationConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    home_allowance = fields.Float(default=lambda self: self.env.user.company_id.home_allowance)
    transportation_allowance = fields.Float(default=lambda self: self.env.user.company_id.transportation_allowance)

    @api.model
    def create(self, values):
        if 'company_id' in values or \
                'home_allowance' in values \
                or 'transportation_allowance' in values:
            self.env.user.company_id.write({
                    'home_allowance': values['home_allowance'],
                    'transportation_allowance': values['transportation_allowance'],
                 })
        res = super(AllocationConfigSettings, self).create(values)
        res.company_id.write({
            'home_allowance': values['home_allowance'],
            'transportation_allowance': values['transportation_allowance'],
        })
        return res
