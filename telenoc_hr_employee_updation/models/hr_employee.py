# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResCountry(models.Model):
    _inherit = 'res.country'

    is_default_country = fields.Boolean()


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def get_default_country(self):
        country = self.env['res.country'].search([('is_default_country', '=', True)], limit=1)
        return country

    country_id = fields.Many2one('res.country', 'Nationality (Country)', groups="hr.group_hr_user",
                                 tracking=True, default=get_default_country)
    is_default_country = fields.Boolean(related='country_id.is_default_country')
    date_of_issue = fields.Date('Date of Issue')
    date_of_expiry = fields.Date('Date of Expiry')
    iqama_number = fields.Char('Iqama Number')
    iqama_date_of_issue = fields.Date('Date of Issue')
    iqama_date_of_expiry = fields.Date('Date of Expiry')
    bank_name = fields.Char('Bank Name')
    account_number = fields.Char('Account Number')
    iban_number = fields.Char('IBAN Number')
    employee_code = fields.Char()

