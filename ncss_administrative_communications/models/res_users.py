# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'
    # transfer_to_ids = fields.Many2many('administrative.communication.management')
    ncss_department_id = fields.Many2one('administrative.communication.management', 'Department')
    position = fields.Selection([('regular', 'Regular'),
                                 ('center_manager', 'Center Manager'),
                                 ('department_manager', 'Manager'),
                                 ], default='regular')
