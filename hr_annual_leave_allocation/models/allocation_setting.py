import time
import datetime
from dateutil.relativedelta import relativedelta

import odoo
from odoo import SUPERUSER_ID
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    no_of_days_per_year = fields.Float('No Of Days Per Year', default=365)
    allocation_type = fields.Selection([('Daily', 'Daily'),
                                        ('Monthly', 'Monthly'),
                                        ('Yearly', 'Yearly'), ], default='Daily')
    leave_type_id = fields.Many2one('hr.leave.type',
                                    domain=[('allocation_type', '=', 'fixed')])
    leave_id = fields.Many2one('hr.leave.type')
    unpaid_type = fields.Selection([('Add', 'Add'),
                                    ('Ignore', 'Ignore')], default='Add'
                                   )
    first_period = fields.Float(default=5)
    deserve_first_period = fields.Float(default=21)
    second_period = fields.Float()
    deserve_second_period = fields.Float(default=30)
    next_call = fields.Datetime()


class AllocationConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    # sale_customer_rel = fields.Boolean(string='Allow the sales man to link with the customer',default=lambda self: self.env.user.company_id.sale_customer_rel)
    # allow_custom_commision = fields.Boolean(string="Allow Custom Commission",default=lambda self: self.env.user.company_id.allow_custom_commision)

    no_of_days_per_year = fields.Float('No Of Days Per Year', default=lambda self: self.env.user.company_id.no_of_days_per_year)
    allocation_type = fields.Selection([('Daily', 'Daily'),
                                        ('Monthly', 'Monthly'),
                                        ('Yearly', 'Yearly'), ],
                                       default=lambda self: self.env.user.company_id.allocation_type)
    leave_type_id = fields.Many2one('hr.leave.type', string='Annual Leave',
                                    default=lambda self: self.env.user.company_id.leave_type_id,
                                    domain=[('allocation_type', '=', 'fixed')])
    unpaid_type = fields.Selection([('Add', 'Add'),
                                    ('Ignore', 'Ignore')],
                                   default=lambda self: self.env.user.company_id.unpaid_type
                                   )
    leave_id = fields.Many2one('hr.leave.type', string='Unpaid Leave',
                               default=lambda self: self.env.user.company_id.leave_id)
    first_period = fields.Float(default=lambda self: self.env.user.company_id.first_period)
    deserve_first_period = fields.Float(default=lambda self: self.env.user.company_id.deserve_first_period)
    second_period = fields.Float(default=lambda self: self.env.user.company_id.second_period)
    deserve_second_period = fields.Float(default=lambda self: self.env.user.company_id.deserve_second_period)
    next_call = fields.Datetime(default=lambda self: self.env.user.company_id.next_call)

    # @api.onchange('sale_customer_rel')
    # def change_allow_rel(self):
    #     print "change companyyyyyyyyyyy",self.sale_customer_rel
    #     self.company_id.write({'sale_customer_rel':self.sale_customer_rel,'allow_custom_commision':self.allow_custom_commision})
    #     return {}

    @api.model
    def create(self, vals):
        # if 'nextcall' in vals:
        cron = self.env.ref('hr_annual_leave_allocation.employee_annual_allocation')
            # print("cron: ", cron)
            # cron_id = self.env['ir.cron'].search([('id', '=', cron.id)])
            # print(cron_id)
            # # cron.nextcall = vals['nextcall']
            # cron_id.write({
            #     'nextcall': vals['nextcall'],
            # })
        if 'company_id' in vals or 'no_of_days_per_year' in vals \
            or 'allocation_type' in vals or 'leave_type_id' in vals \
            or 'unpaid_type' in vals or 'first_period' in vals \
            or 'deserve_first_period' in vals or 'second_period' in vals \
            or 'deserve_second_period' in vals \
            or 'leave_id' in vals\
            or 'next_call' in vals:
            self.env.user.company_id.write({
                    'no_of_days_per_year': vals['no_of_days_per_year'],
                    'allocation_type': vals['allocation_type'],
                    'leave_type_id': vals['leave_type_id'],
                    'unpaid_type': vals['unpaid_type'],
                    'first_period': vals['first_period'],
                    'deserve_first_period': vals['deserve_first_period'],
                    'second_period': vals['second_period'],
                    'deserve_second_period': vals['deserve_second_period'],
                    'leave_id': vals['leave_id'],
                    'next_call': vals['next_call'],
                 })
            cron.sudo().write({
                'nextcall': vals['next_call'],
            })
            #print "in comp",self.env.user.company_id.sale_customer_rel
            #print "sallllllll",vals['sale_customer_rel']
        # else:
        #     self.env.user.company_id.write({'sale_customer_rel':self.sale_customer_rel,'allow_custom_commision':self.allow_custom_commision})
            #print "out comp"
        res = super(AllocationConfigSettings, self).create(vals)
        # res.company_id.write({'sale_customer_rel':vals['sale_customer_rel'],'allow_custom_commision':vals['allow_custom_commision']})
        res.company_id.write({
                    'no_of_days_per_year':vals['no_of_days_per_year'],
                    'allocation_type':vals['allocation_type'],
                    'leave_type_id':vals['leave_type_id'],
                    'unpaid_type':vals['unpaid_type'],
                    'first_period':vals['first_period'],
                    'deserve_first_period':vals['deserve_first_period'],
                    'second_period':vals['second_period'],
                    'deserve_second_period':vals['deserve_second_period'],
                    'leave_id':vals['leave_id'],
                    'next_call': vals['next_call'],
                 })
        # res['nextcall'] = vals['nextcall']
        return res
