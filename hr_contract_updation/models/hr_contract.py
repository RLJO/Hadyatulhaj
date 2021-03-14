from odoo import api, fields, models, _


class HrContractType(models.Model):
    _name = 'hr.contract.type'

    name = fields.Char()


class Contract(models.Model):
    _inherit = 'hr.contract'

    contract_period = fields.Selection([('one_year', 'One Year'),
                                        ('two_year', 'Two Year'),
                                        ('temp', 'Temporary'),
                                        ], string='Contract Period', default='one_year')
    number_of_months = fields.Char('Number Of Months')
    contract_type = fields.Many2one('hr.contract.type')
    home_allowance = fields.Float(compute='compute_total_allowance', store=True)
    transportation_allowance = fields.Float(compute='compute_total_allowance', store=True)
    mobile_allowance = fields.Float()
    other_allowance = fields.Float()
    deduct_tamenat = fields.Boolean()
    tameenat_deduction = fields.Float(compute='get_tameenat_deduction', store=True)
    total_salary = fields.Float(compute='get_total_salary', store=True)
    net_contract_salary = fields.Float(compute='get_net_contract_salary', store=True)

    @api.depends('wage', 'home_allowance', 'transportation_allowance', 'mobile_allowance', 'other_allowance')
    def get_total_salary(self):
        for record in self:
            allowances = record.home_allowance+record.transportation_allowance+record.mobile_allowance+record.other_allowance
            record.total_salary = record.wage+allowances

    @api.depends('deduct_tamenat', 'wage', 'home_allowance')
    def get_tameenat_deduction(self):
        for record in self:
            if record.deduct_tamenat:
                record.tameenat_deduction = ((record.wage + record.home_allowance)*10)/100
            else:
                record.tameenat_deduction = 0.0

    @api.depends('total_salary', 'tameenat_deduction')
    def get_net_contract_salary(self):
        for record in self:
            record.net_contract_salary = record.total_salary - record.tameenat_deduction

    @api.depends('wage')
    def compute_total_allowance(self):
        for record in self:
            if record.wage:
                if self.env.user.company_id.home_allowance:
                    record.home_allowance = (self.env.user.company_id.home_allowance/100) * record.wage
                if self.env.user.company_id.transportation_allowance:
                    record.transportation_allowance = (self.env.user.company_id.transportation_allowance/100) * record.wage


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    join_date = fields.Date()
