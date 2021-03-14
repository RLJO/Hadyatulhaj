# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################

import time

from odoo import fields,api,models

class PartnerLedger(models.TransientModel):

    _name = 'partner.ledger'

    start_date = fields.Date(string='From Date', required=True)
    end_date = fields.Date(string='To Date', required=True)

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, help='Select Partner for movement')
    

    def print_report(self):
        data = {'partner_id': self.partner_id.id,'start_date': self.start_date, 'end_date': self.end_date}
        return self.env.ref('ess.partner_ledger_pdf').report_action(self, data=data)
