from odoo.http import request
from odoo import models, api, fields,_


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def website_go_to(self):
        self.website_id._force()
        return {
            'type': 'ir.actions.act_url',
            'url': 'my/dashboard',
            'target': 'self',
        }


class ResPartner(models.AbstractModel):
    _inherit = 'res.partner'

    def get_data(self, partner, from_date, to_date):
        cr = self._cr
        query = """select sum(l.debit - l.credit) as opening_bal
            from account_move_line l
            join account_move m on l.move_id = m.id
            join account_account a on l.account_id = a.id
            where a.reconcile = True
        and l.partner_id = %s and l.date < %s
        """ 
        cr.execute(query, [partner.id, from_date])
        openbal = cr.dictfetchall()

        cr = self._cr
        query = """
        select m.ref,m.name as doc_no, m.date, m.narration, j.name as journal, p.name as partner_name, 
            l.name as line_desc, a.name as gl_account, m.currency_id, l.debit, l.credit
            from account_move_line l
            join account_move m on l.move_id = m.id
            join res_partner p on l.partner_id = p.id
            join account_account a on l.account_id = a.id
            join account_journal j on m.journal_id = j.id
            where a.reconcile = True
        and l.partner_id = %s and (m.date between %s and %s)
        order by m.date
        """ 
        cr.execute(query, [partner.id, from_date, to_date])
        dat = cr.dictfetchall()

        return openbal, dat

    @api.model
    def print_report(self, data):
        data = {'partner_id': int(data['partner_id']),'start_date': data['start_date'], 'end_date': data['end_date']}
        self.env.ref('ess.partner_ledger_pdf').report_action(self, data=data)