from odoo.http import request
from odoo import models, api, fields,_


class CourseSchedule(models.AbstractModel):
    _inherit = 'course.schedule'

    @api.model
    def get_course_obj(self, data):
        if data and data['id']:
            cou_obj = self.env['course.schedule'].sudo().browse(int(data['id']))
            for emb in cou_obj.registered_employees:
                if emb.employee_id.id == int(data['employee_id']):
                    return {
                        'duration' : cou_obj.duration,
                        'f_date' : cou_obj.f_date,
                        'to_date' : cou_obj.to_date,
                        'price' : cou_obj.price,
                        'trainer_id' : cou_obj.trainer_id.partner_name.name,
                        'capacity' : cou_obj.capacity,
                        'state' : "enrolled",
                    }
            return {
                'duration' : cou_obj.duration,
                'f_date' : cou_obj.f_date,
                'to_date' : cou_obj.to_date,
                'price' : cou_obj.price,
                'trainer_id' : cou_obj.trainer_id.partner_name.name,
                'capacity' : cou_obj.capacity,
                'state' : "not_yet",
            }
