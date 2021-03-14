from odoo import api, fields, models, _


class EosConfiguredFields(models.Model):
    _name = 'eos.configured.fields'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    field_name = fields.Char()


class ResCompany(models.Model):
    _inherit = 'res.company'

    eos_involved_item_id = fields.Many2many('eos.configured.fields')
    absent_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields_rel1', 'res_company_rel')
    penalty_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields_rel2', 'res_company_rel')
    extra_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields_rel3', 'res_company_rel')
    deduct_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields_rel4', 'res_company_rel')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    eos_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields_rel', 'res_config_settings_rel',
                                          default=lambda self: self.env.user.company_id.eos_involved_item_id)
    absent_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields2_rel', 'res_config_settings_rel',
                                             default=lambda self: self.env.user.company_id.absent_involved_item_id)
    penalty_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields3_rel', 'res_config_settings_rel',
                                              default=lambda self: self.env.user.company_id.penalty_involved_item_id)
    extra_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields4_rel', 'res_config_settings_rel',
                                            default=lambda self: self.env.user.company_id.extra_involved_item_id)
    deduct_involved_item_id = fields.Many2many('eos.configured.fields', 'eos_configured_fields5_rel', 'res_config_settings_rel',
                                             default=lambda self: self.env.user.company_id.deduct_involved_item_id)

    @api.model
    def create(self, values):
        if 'company_id' in values\
                or 'eos_involved_item_id' in values \
                or 'absent_involved_item_id' in values \
                or 'penalty_involved_item_id' in values \
                or 'extra_involved_item_id' in values \
                or 'deduct_involved_item_id' in values:
            self.env.user.company_id.write({
                    'eos_involved_item_id': values['eos_involved_item_id'],
                    'absent_involved_item_id': values['absent_involved_item_id'],
                    'penalty_involved_item_id': values['penalty_involved_item_id'],
                    'extra_involved_item_id': values['extra_involved_item_id'],
                    'deduct_involved_item_id': values['deduct_involved_item_id'],
                 })
        res = super(ResConfigSettings, self).create(values)
        return res
