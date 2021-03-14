from odoo import models, fields, api, _

class Wizard(models.TransientModel):
    _name = 'assests.wizard'
    _description = "Wizard: Reason of refuse Request"

    Reason = fields.Char(string=_("Reason Refuse"))

    def create_reason(self):
        vals = {
            'asset_request_Refuse_reason': self.Reason,
            'state': 'refuse',
            'refuse_boolean': True
        }
        print(self.env.context.get('active_ids')[0])
        asset_id = self.env['asset.account.request'].browse(self.env.context.get('active_ids')[0])

        asset_id.update(vals)
        message = 'تم رفض طلب العهده الخاص بك'
        asset_id.make_notification(message)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'asset.account.request',
                'res_id': asset_id.id,
                'context': context
                }