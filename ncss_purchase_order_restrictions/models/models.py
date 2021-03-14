from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('Accounting Approve', 'Accounting Approved'),
        ('Administrative and Financial Affairs', 'Administrative and Financial Affairs Approved'),
        ('Financial auditor', 'Financial auditor Approved'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def action_accounting_approve(self):
        self.state = 'Accounting Approve'

    def action_financial_affairs(self):
        self.state = 'Administrative and Financial Affairs'

    def action_financial_auditor(self):
        self.state = 'Financial auditor'

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'Financial auditor']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.sudo().button_approve()
            else:
                order.write({'state': 'to approve'})
        return True
