# -*- coding: utf-8 -*-

import base64

from odoo.http import content_disposition, Controller, request, route
import odoo.addons.portal.controllers.portal as PortalController
from datetime import date, datetime ,timedelta
import base64
import io
from werkzeug.utils import redirect
from odoo import http
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo.tools.translate import _
import pytz
import time
from odoo.tools import formataddr


from .main import ESSPortal
# from odoo.addons.ess.controllers.main import ESSPortal


class EssAsset(Controller):

    # def check_modules(self):
    #     values = {}
    #     if request.env['ir.module.module'].sudo().search([('name', '=', 'hr_announcement')]).state == 'installed':
    #         values.update({
    #             'announcement': True,
    #         })
    #     else:
    #         values.update({
    #             'announcement': False,
    #         })
    #     return values

    @route(['/request/asset'], type='http', auth='user', website=True)
    def asset(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        if post and request.httprequest.method == 'POST':
            post.update({
                'employee_id': emb_obj.id,
                'asset_request_description': post['description'],
                'asset_request_Reason': post['asset_request_Reason'],
                'asset_request_startDate': post['asset_request_startDate'],
                'asset_request_deliveryDate': post['asset_request_deliveryDate'],
            })
            print("post assest ",post)
            asset_obj = request.env['asset.account.request'].sudo().create(post)
            asset_obj.sudo().action_submit()
            print("post Id ", asset_obj.id)

            emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
            asset_assignation_obj = request.env['asset.account.request'].sudo().search(
                [('employee_id', '=', emb_obj.id)])

            values.update({
                'partner': request.env.user.partner_id,
                'employee': emb_obj,
                'asset_assignation_obj': asset_assignation_obj,
            })
            return request.render("ess.ess_view_asset_assignation", values)
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
        })
        print(" heloo ", values)
        response = request.render("ess.ess_asset_assignation", values)
        return response

    @route(['/my/asset_assignation'], type='http', auth='user', website=True)
    def asset_assignation(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        asset_assignation_obj = request.env['asset.account.request'].sudo().search([('employee_id', '=', emb_obj.id)])
        for rec in asset_assignation_obj:
            print(rec.state)
            if rec['type_of_disclaimer_desc']:
                assest_list = rec['type_of_disclaimer_desc']
                print(assest_list)
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'asset_assignation_obj': asset_assignation_obj,
        })
        response = request.render("ess.ess_view_asset_assignation2", values)
        return response

    @route(['/custody/request'], type='http', auth='user', website=True)
    def custody(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        if post and request.httprequest.method == 'POST':
            post.update({
                'employee_id': emb_obj.id,
                'date': post['date'],
                'amount': post['amount'],
                'description': post['description'],
            })
            print(post)
            request.env['custody.request'].sudo().create(post)
            emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
            custody_obj = request.env['custody.request'].sudo().search([('employee_id', '=', emb_obj.id)])

            values.update({
                'partner': request.env.user.partner_id,
                'employee': emb_obj,
                'custody_obj': custody_obj,
            })
            return request.render("ess.ess_view_custody", values)
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
        })
        response = request.render("ess.ess_custody_request", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/custody'], type='http', auth='user', website=True)
    def view_custody(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        custody_obj = request.env['custody.request'].sudo().search([('employee_id', '=', emb_obj.id)])

        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'custody_obj': custody_obj,
        })
        response = request.render("ess.ess_view_custody", values)
        return response

    @route(['/my/custody/in_progress'], type='http', auth='user', website=True)
    def view_custody_in_progress(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        custody_obj = request.env['custody.request'].sudo().search([('employee_id', '=', emb_obj.id)])

        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'custody_obj': custody_obj,
        })
        response = request.render("ess.ess_custody_in_progress", values)
        return response

    @route(['/custody/warning'], type='http', auth='user', website=True)
    def custody_warning(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])

        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
        })
        response = request.render("ess.custody_warning_message", values)
        return response

    @route(['/add_custody_line'], type='http', auth='user', website=True)
    def add_custody_line(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        custody_description_obj = request.env['custody.description'].sudo().search([])
        if post and request.httprequest.method == 'POST':
            if float(post['amount']) > float(post['get_remaining_amount']):
                values.update({
                    'partner': request.env.user.partner_id,
                    'employee': emb_obj,
                    'remain_amount': post['get_remaining_amount'],
                })
                return request.render("ess.custody_warning_message", values)
            else:
                print(post)
                name = post.get('doc_attachment_id').filename
                file = post.get('doc_attachment_id')
                # print(file)
                # file = post['doc_attachment_id']
                # print(">>>>>>>>>>>>>>>>>", type(file))
                # print(">>>>>>>>>>>>>>>>>", type(base64.b64encode(file.encode())))
                docid=request.env['custody.request.line'].sudo().create({
                    'custody_id': int(post['get_id']),
                    'custody_description_id': post['custody_description_id'],
                    'date': post['date'],
                    'amount': post['amount'],
                    #'attach_invoice': base64.b64encode(file.encode()),
                    # 'attach_invoice': io.BytesIO(base64.b64encode(file.read())),
                    'description': post['description'],
                })

                Attachments = request.env['ir.attachment']

                attachment_id = Attachments.sudo().create({
                    'name': name,
                    'type': 'binary',
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'custody.request.line',
                    'res_id': docid.id
                })
                print(docid)
                docid.sudo().update({
                    'attach_invoice': [(4, attachment_id.id)],
                })
                custody_obj = request.env['custody.request'].sudo().search([('employee_id', '=', emb_obj.id)])

                values.update({
                    'partner': request.env.user.partner_id,
                    'employee': emb_obj,
                    'custody_obj': custody_obj,

                })
                return request.render("ess.ess_custody_in_progress", values)
        custody_line_obj = request.env['custody.request.line'].sudo().search([('custody_id.id', '=', int(post['id']))])
        print(">>>>>>>>>>>>>>>custody_line_obj", custody_line_obj)
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'custody_description_obj': custody_description_obj,
            'custody_id': post.get('id'),
            'custody_line_obj': custody_line_obj,

        })
        response = request.render("ess.ess_add_custody_line", values)
        return response


    @route(['/request/passenger_mandate'], type='http', auth='user', website=True)
    def passenger_mandate(self, redirect=None, **post):
        print("hi passenger_mandate2")
        values = {}
        courses = []
        now = datetime.now()
        date_start = now.date()
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])

        course_obj = request.env['training.course'].sudo().search([ '&',('start_date','>=',date_start),'|',('is_private','=' ,False),'&', ('is_private','=', True) ,('employee_id','=',emb_obj.id)  ])
        for rec in course_obj:
            print(rec)
        course_place_obj = request.env['course.place'].sudo().search([])
        for cour in course_obj:
            courses.append({
                'course': cour.id,
                'place': cour.course_place_id.id
            })
        if post and request.httprequest.method == 'POST':
            print(post)
            private_start_date = post['start_date']
            private_end_date = post['end_date']

            if post['type'] == 'دوره':
                type = 'course'
            elif post['type'] == 'انتداب':
                type = 'mandate'
            elif post['type'] == 'ورشه عمل':
                type = 'work_shop'
            else:
                type = post['type']


            if post['course_type'] == 'داخلي':
                course_type = 'internal'
            elif post['course_type'] == 'خارجي':
                course_type = 'external'
            elif post['course_type'] == 'خاصة':
                course_type = 'private'

            else:
                course_type = post['course_type']
            post.update({
                'employee_id': emb_obj.id,
                'employee_degree_id': emb_obj.employee_degree_id.id,
                'type': type,
                'course_type': course_type,
                'course_id': post['course_id'],
                'price': request.env['training.course'].sudo().browse(int(post['course_id'])).price,

                'number_of_days': request.env['training.course'].sudo().browse( int(post['course_id'])).number_of_days,
                'course_place_id': post['course_place_id'],
                'description': post['description'],
                'state': 'draft',
            })


            # if course_type != 'private' :
            post.update({ 'start_date': request.env['training.course'].sudo().browse(int(post['course_id'])).start_date,
            'end_date': request.env['training.course'].sudo().browse(int(post['course_id'])).end_date
                          })
            # elif course_type == 'private' :
            #     post.update(
            #         {'start_date':  private_start_date,
            #          'end_date': private_end_date
            #          })
            print("befor create shaliby ",post)
            # obj_id =request.env['mandate.passenger'].sudo().create(post)
            # emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
            # courses_and_mandate_obj = request.env['mandate.passenger'].sudo().search([('employee_id', '=', emb_obj.id)])
            # # print("LLLLLLLLLLLL", courses_and_mandate_obj)
            # values.update({
            #     'partner': request.env.user.partner_id,
            #     'employee': emb_obj,
            #     'courses_and_mandate_obj': courses_and_mandate_obj,
            # })
            # response = request.render("ess.ess_view_courses_and_mandate", values)
            # return response
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'course_obj': course_obj,
            'course_place_obj': course_place_obj,
            'course_and_place_obj': courses,
            'msg':_('Your Request has been Sent Successfully')
        })
        print(values)
        response = request.render("ess.ess_passenger_mandate", values)
        return response

    @route(['/course_restriction'], type='json', auth="public", methods=['GET', 'POST'], csrf=False)
    def course_restriction(self, **args):
        print(args)
        print(int(args['course_id']))
        training_course_obj = request.env['training.course'].sudo().browse(int(args['course_id']))
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        course_obj = request.env['mandate.passenger'].sudo().\
            search([('employee_id', '=', emb_obj.id),
                    ('state', '=', 'accounting_approve')], order='id desc')
        print("course_obj", course_obj)
        values = {}
        create_course = False
        if course_obj:
            start_year = date(training_course_obj.end_date.year, 1, 1)
            end_year = date(training_course_obj.end_date.year, 12, 31)
            print("course end_date", training_course_obj.end_date)
            print("start_year", start_year)
            print("end_year", end_year)
            courses_approved_within_year = request.env['mandate.passenger'].search_count([('employee_id', '=', emb_obj.id),
                                                              ('state', '=', 'accounting_approve'),
                                                              ('course_id.end_date', '>=', start_year),
                                                              ('course_id.end_date', '<=', end_year),
                                                              ('course_id.is_free', '=', training_course_obj.is_free),
                                                              ])
            print("training_course_obj.is_free", training_course_obj.is_free)
            print("courses_approved_within_year", courses_approved_within_year)
            if training_course_obj.is_free:
                if courses_approved_within_year >= emb_obj.employee_degree_id.number_of_free_courses_per_year:
                    create_course = False
                    values.update({
                        'val': 'No Extra Free Courses',
                        'no_of_allowed_free_courses': emb_obj.employee_degree_id.number_of_free_courses_per_year,
                    })
            else:
                if courses_approved_within_year >= emb_obj.employee_degree_id.number_of_paid_courses_per_year:
                    create_course = False
                    values.update({
                        'val': 'No Extra Paid Courses',
                        'no_of_allowed_paid_courses': emb_obj.employee_degree_id.number_of_paid_courses_per_year,
                    })
            date_format = "%Y-%m-%d"
            last_course_end_date = datetime.strptime(str(course_obj[0].course_id.end_date), date_format)
            current_course_start_date = datetime.strptime(str(training_course_obj.start_date), date_format)
            difference_between_last_two_courses = float((current_course_start_date - last_course_end_date).days)
            print("last_course_date", last_course_end_date)
            print("current_course_date", current_course_start_date)
            print("difference_between_last_two_courses", difference_between_last_two_courses)
            print("allowed_period_between_courses", emb_obj.employee_degree_id.allowed_period_between_courses)
            if difference_between_last_two_courses < emb_obj.employee_degree_id.allowed_period_between_courses:
                create_course = False
                values.update({
                    'val': 'No Extra Course',
                    'course_end_date': course_obj[0].course_id.end_date,
                })
            else:
                create_course = True
        if create_course:
            mandate_obj = request.env['mandate.passenger']
            if args['type'] == 'دوره':
                type = 'course'
            elif args['type'] == 'انتداب':
                type = 'mandate'
            elif args['type'] == 'ورشه عمل':
                type = 'work_shop'
            else:
                type = args['type']

            if args['course_type'] == 'داخلي':
                course_type = 'internal'
            elif args['course_type'] == 'خارجي':
                course_type = 'external'
            elif args['course_type'] == 'خاصة':
                course_type = 'private'
            else:
                course_type = args['course_type']

            mandate_obj.sudo().create({
                'employee_id': emb_obj.id,
                'employee_degree_id': emb_obj.employee_degree_id.id,
                'type': type,
                'course_type': course_type,
                'course_id': int(args['course_id']),
                'price': training_course_obj.price,
                'start_date': training_course_obj.start_date,
                'end_date': training_course_obj.end_date,
                'number_of_days': training_course_obj.number_of_days,
                'course_place_id': int(args['place_id']),
                'description': args['description'],
                'state': 'draft',
            })

            values.update({
                'val': 'done',
            })
        print("VVVVVVVVVVVVVV", values)
        return values


    @route(['/request/passenger_mandate_private'], type='http', auth='user', website=True)
    def passenger_mandate_private(self, redirect=None, **post):


        now = datetime.now()
        date_start = now.date()
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])

        # course_obj = request.env['training.course'].sudo().search( [ '&',('start_date','>=',date_start),'|',('is_private','=' ,False),'&', ('is_private','=', True) ,('employee_id','=',emb_obj.id) ])
        course_place_obj = request.env['course.place'].sudo().search([])
        if post and request.httprequest.method == 'POST':
            print(post)
            print(post)
            name = post.get('doc_attachment_id').filename
            file = post.get('doc_attachment_id')
            # private_start_date = post['start_date']
            # private_end_date = post['end_date']

            # if post['type'] == 'دوره':
            #     type = 'course'
            # elif post['type'] == 'انتداب':
            #     type = 'mandate'
            # elif post['type'] == 'ورشه عمل':
            #     type = 'work_shop'
            # else:
            #     type = post['type']


            if post['type'] == 'داخلي':
                course_type = 'internal'
            elif post['type'] == 'خارجي':
                course_type = 'external'

            else:
                course_type = post['type']

            post.update({
                'name':post['name'],
                'description': post['description'],
                'type': course_type,
                'price':post['price'],
                'start_date':post['start_date'],
                'end_date':post['end_date'],
                'number_of_days':post['number_of_days'],
                'is_private':True,
                'employee_id': emb_obj.id,
                    })


            # if course_type != 'private' :
            #     post.update({ 'start_date': request.env['training.course'].sudo().browse(int(post['course_id'])).start_date,
            #     'end_date': request.env['training.course'].sudo().browse(int(post['course_id'])).end_date
            #                   })
            # elif course_type == 'private' :
            #     post.update(
            #         {'start_date':  private_start_date,
            #          'end_date': private_end_date
            #          })

            print("befor create",post)
            Attachments = request.env['ir.attachment']

            attachment_id = Attachments.sudo().create({
                'name': name,
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
                'res_model': 'custody.request.line',
                'res_id': 1
            })

            post ['doc_attachment_id']= [(4, attachment_id.id)]
            print("Private shaliby ",post)
            obj_id =request.env['training.course'].sudo().create(post)
            # Update mypost
            mypost = post.copy()
            mypost['course_type']=post['type']
            mypost['type'] ='course'
            mypost['course_id'] =obj_id.id
            mypost['employee_degree_id']= emb_obj.employee_degree_id.id
            mypost['state'] = 'draft'
            del mypost['doc_attachment_id']
            del mypost['is_private']
            del mypost['name']
            del mypost['message_follower_ids']
            # = request.env['training.course'].sudo().create(post)
            print("shaliby2 mypost",mypost)
            mand_id= request.env['mandate.passenger'].sudo().create(mypost)
            print(mand_id.id)
            attachment_id.update({

                'res_id': obj_id.id
            })

            # print(obj_id)
            # docid.sudo().update({
            #     'doc_attachment_id': [(4, attachment_id.id)],
            # })

        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            # 'course_obj': course_obj,
            'course_place_obj': course_place_obj,
            'msg':_('Your Request has been Sent Successfully')
        })
        print(values)
        response = request.render("ess.ess_passenger_mandate_private", values)
        return response

    @route(['/my/courses_and_mandate'], type='http', auth='user', website=True)
    def view_courses_and_mandate(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        courses_and_mandate_obj = request.env['mandate.passenger'].sudo().search([('employee_id', '=', emb_obj.id)])

        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'courses_and_mandate_obj': courses_and_mandate_obj,
        })
        response = request.render("ess.ess_view_courses_and_mandate", values)
        return response

    @route(['/get/course_place'], type='json', auth="public", methods=['GET', 'POST'], csrf=False)
    def get_country(self, **args):
        course_obj = request.env['training.course'].sudo().browse(int(args['course_id']))
        values = {}
        for place in course_obj:
            values.update({
                'val': place.course_place_id.id,
            })
        return values

    @route(['/change/notification'], type='json', auth="public", methods=['GET', 'POST'], csrf=False)
    def change_notification_color(self, **args):
        notification_id = int(args['course_id'].split("#")[1])
        notification_obj = request.env['hr.notification'].sudo().browse(int(args['course_id'].split("#")[1]))
        if notification_obj:
            for notify in notification_obj:
                notify.is_read = 1

        value = {
            'result': notification_id
        }
        return value

    @route(['/change/announcement_color'], type='json', auth="public", methods=['GET', 'POST'], csrf=False)
    def change_announcement_color(self, **args):
        announcement_id = int(args['url'].split("#")[1])
        announcement_obj = request.env['hr.announcement'].sudo().browse(int(args['url'].split("#")[1]))
        if announcement_obj:
            for announcement in announcement_obj:
                announcement.is_read = 1
        value = {
            'result': announcement_id
        }
        return value

    @route(['/all/notification'], type='http', auth='user', website=True)
    def all_notification(self, redirect=None, **post):
        values = {}
        values = ESSPortal.check_modules(self)
        emb_obj = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        notification_obj = request.env['hr.notification'].sudo().search([('employee_id', '=', emb_obj.id)],order='id desc')
        values.update({
            'partner': request.env.user.partner_id,
            'employee': emb_obj,
            'notification_obj': notification_obj,
        })

        response = request.render("ess.ess_all_notification", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
