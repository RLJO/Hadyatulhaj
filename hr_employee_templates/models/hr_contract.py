from odoo import api, fields, models, _
import datetime


class Contract(models.Model):
    _inherit = 'hr.contract'

    contract_type = fields.Selection([('saudi_contract', 'Saudi Contract'),
                                        ('foreign_saudi_contract', 'Foreign Saudi Contract'),
                                        ('advisor_contract', 'Advisor Contract'),
                                        ('cooperation_contract', 'Cooperation Contract'),
                                        ], string='Contract Type', default='saudi_contract')

    def get_day_name_from_date(self, contract_day):
        contract_day = str(contract_day)
        year, month, day = contract_day.split('-')
        day_name = datetime.date(int(year), int(month), int(day))
        e_name = day_name.strftime("%A")
        if e_name == 'Saturday':
            ar_name = 'السبت'
        elif e_name == 'Sunday':
            ar_name = 'الاحد'
        elif e_name == 'Monday':
            ar_name = 'الاثنين'
        elif e_name == 'Tuesday':
            ar_name = 'الثلاثاء'
        elif e_name == 'Wednesday':
            ar_name = 'الاربعاء'
        elif e_name == 'Thursday':
            ar_name = 'الخميس'
        else:
            ar_name = 'الجمعه'
        return ar_name
