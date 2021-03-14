# -*- coding: utf-8 -*-
###################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Jesni Banu (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from datetime import datetime, timedelta, date

from . import  calverter
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


GENDER_SELECTION = [('male', 'Male'),
                    ('female', 'Female'),
                    ('other', 'Other')]


class HrEmployeeContractName(models.Model):
    """This class is to add emergency contact table"""

    _name = 'hr.emergency.contact'
    _description = 'HR Emergency Contact'

    number = fields.Char(string='Number', help='Contact Number')
    relation = fields.Char(string='Contact', help='Relation with employee')
    employee_obj = fields.Many2one('hr.employee', invisible=1)


class HrEmployeeFamilyInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.family'
    _description = 'HR Employee Family'


    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)

    member_name = fields.Char(string='Name')
    relation = fields.Selection([('father', 'Father'),
                                 ('mother', 'Mother'),
                                 ('daughter', 'Daughter'),
                                 ('son', 'Son'),
                                 ('wife', 'Wife')], string='Relationship', help='Relation with employee')
    member_contact = fields.Char(string='Contact No')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    arabic_name = fields.Char(string="Arabic Name")


    def mail_reminder(self):
        """Sending expiry date notification for ID and Passport"""

        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.id_expiry_date:
                exp_date = fields.Date.from_string(i.id_expiry_date) - timedelta(days=14)
                if date_now >= exp_date:
                    mail_content = "  Hello  " + i.name + ",<br>Your ID " + i.identification_id + "is going to expire on " + \
                                   str(i.id_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('ID-%s Expired On %s') % (i.identification_id, i.id_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()
        match1 = self.search([])
        for i in match1:
            if i.passport_expiry_date:
                exp_date1 = fields.Date.from_string(i.passport_expiry_date) - timedelta(days=180)
                if date_now >= exp_date1:
                    mail_content = "  Hello  " + i.name + ",<br>Your Passport " + i.passport_id + "is going to expire on " + \
                                   str(i.passport_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('Passport-%s Expired On %s') % (i.passport_id, i.passport_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }

                    self.env['mail.mail'].sudo().create(main_content).send()


    personal_mobile = fields.Char(string='Mobile', related='address_home_id.mobile', store=True)
    joining_date = fields.Date(string='Joining Date')
    id_expiry_date = fields.Date(string='ID Expiry Date', help='Expiry date of Identification ID')
    id_expiry_date_hajri = fields.Char(string='Expiry Date Hajri',compute='_calculate_id_hajri', store=True, help='Expiry date of Identification ID')

    passport_expiry_date = fields.Date(string='Passport Expiry Date', help='Expiry date of Passport ID')
    passport_expiry_date_hajri = fields.Char(string='Expiry Date Hajri',compute='_calculate_passport_hajri', store=True, help='Expiry date of Passport ID')

    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", help='You can attach the copy of your Id')
    passport_attachment_id = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                              string="Attachment",
                                              help='You can attach the copy of Passport')
    fam_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family', help='Family Information')
    emergency_contacts = fields.One2many('hr.emergency.contact', 'employee_obj', string='Emergency Contact')
    ticket_ids = fields.One2many('hr.employee.tickets', 'employee_id', string='Tickets', help='Tickets Information')

    @api.depends('id_expiry_date')
    def _calculate_id_hajri(self):
        cal = calverter.Calverter()
        for rec in self:
            if rec.id_expiry_date:
                d = rec.id_expiry_date

                jd = cal.gregorian_to_jd(d.year, d.month, d.day)
                # print(jd)
                # print(cal.jd_to_islamic(jd))

                hj = cal.jd_to_islamic(jd)
                # print(hj[0], "/", hj[1], "/", hj[2])
                rec.id_expiry_date_hajri =str( hj[2])+ "/"+ str(hj[1])+ "/"+str(hj[0])

    @api.depends('passport_expiry_date')
    def _calculate_passport_hajri(self):
        cal = calverter.Calverter()
        for rec in self:
            if rec.passport_expiry_date:
                d = rec.passport_expiry_date

                jd = cal.gregorian_to_jd(d.year, d.month, d.day)
                # print(jd)
                # print(cal.jd_to_islamic(jd))

                hj = cal.jd_to_islamic(jd)
                # print(hj[0], "/", hj[1], "/", hj[2])
                rec.passport_expiry_date_hajri = str(hj[2]) + "/" + str(hj[1])+ "/" + str(hj[0])
			



class hr_employee_tickets(models.Model):
    _name = "hr.employee.tickets"
    _description = "Table For Employee Tickets data"
    ticket_type = fields.Selection([('single', 'Single'), ('family', 'Family')], string="Ticket Type")
    ticket_reg_date = fields.Datetime(string="Date Of Register", default=datetime.now())
    ticket_airline = fields.Char("Ticket Airline")
    ticket_class = fields.Selection([('economy', 'Economy'), ('first', 'First Class'),
                                     ('business', 'Business Class'), ('Guest', 'Guest')],
                                    default='economy', string="Ticket Class")
    ticket_number = fields.Integer("Ticket Number")

    # @api.one
    @api.constrains("ticket_number")
    def _change_num(self):
        if self.ticket_type == 'single' and self.ticket_number > 1:
            raise ValidationError("Ticket Number Must Be 1")

    ticket_price = fields.Float("Price For One Ticket")
    ticket_cost = fields.Float("Total Cost For Tickets", store=True, readonly=True, compute="_calc_tickets_cost")

    # @api.one
    @api.depends("ticket_price", "ticket_number")
    def _calc_tickets_cost(self):
        if self.ticket_number or self.ticket_price:
            self.ticket_cost = self.ticket_price * self.ticket_number

    employee_id = fields.Many2one('hr.employee', string="Employees")




