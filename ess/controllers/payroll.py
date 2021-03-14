# -*- coding: utf-8 -*-

import base64

from odoo.http import content_disposition, Controller, request, route
import odoo.addons.portal.controllers.portal as PortalController
from datetime import date, datetime
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

from . import main as mainController



class ESSPortalPayRoll(Controller):

    @route(['/my/statement'], type='http', auth='user', website=True)
    def statement(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        values = mainController.ESSPortal.check_modules(self)


        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            openbal, dat = request.env['res.partner'].sudo().get_data(partner, post['from_date'], post['to_date'])

            values.update({
                'openbal': openbal,
                'dat': dat,
                'date_to': post['to_date'],
                'date_from': post['from_date'],
            })

        values.update({
            'partner': partner,
            'employee': emb_obj,
        })
        
        response = request.render("ess.ess_statement", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/payslip_correction_request'], type='http', auth='user', website=True)
    def payslipCorrection(self, redirect=None, **post):
        values = {}
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        payslip_obj = request.env['hr.payslip'].sudo().search([('employee_id','=',emb_obj.id)])

        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            #error, error_message = self.details_form_validate(post)

            if 'payslip_id' in post:
                post.update({
                    'payslip_id': int(post['payslip_id']),
                })

            post.update({
                'employee_id': emb_obj.id,
                'employee_note': post['employee_note'],
            })
            aa = request.env['hr.payslip.correction'].sudo().create(post)
            print(aa)


        values.update({
            'partner': partner,
            'employee': emb_obj,
            'payslip_obj': payslip_obj,
        })
        
        response = request.render("ess.ess_payslip_correction", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/payslip_correction_track'], type='http', auth='user', website=True)
    def payslipCorrectionTrack(self, redirect=None, **post):
        values = {}
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        payslip_correction_obj = request.env['hr.payslip.correction'].sudo().search([('employee_id','=',emb_obj.id)])

        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        values.update({
            'partner': partner,
            'employee': emb_obj,
            'payslip_correction_obj': payslip_correction_obj,
        })
        
        response = request.render("ess.ess_payslip_correction_track", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/payslip'], type='http', auth='user', website=True)
    def payslip(self, redirect=None, **post):
        values = {}
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        payslip_obj = request.env['hr.payslip'].sudo().search([('employee_id','=',emb_obj.id)])

        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        values.update({
            'partner': partner,
            'employee': emb_obj,
            'payslip_obj': payslip_obj,
        })
        
        response = request.render("ess.ess_payslip", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/eos'], type='http', auth='user', website=True)
    def eos(self, redirect=None, **post):
        values = {}
        eos_value = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            eos_value = request.env['end.of.service.award'].sudo().get_employee_end_of_service(emb_obj,
                                                                                               datetime.strptime(str(post['date']),DEFAULT_SERVER_DATE_FORMAT).date(),
                                                                                               post['type'])

        values.update({
            'partner': partner,
            'employee': emb_obj,
            'eos_value' : eos_value,
        })
        

            
        response = request.render("ess.ess_eos", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route('/print/statment', methods=['POST', 'GET'], csrf=False, type='http', auth="user", website=True)
    def print_statment(self, **post):

        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        ddd = request.env['report.de_partner_statement.de_partner_ledger_pdf_report']._get_report_values(data=post)

        pdf = request.env.ref('ess.partner_ledger_pdf').sudo().render_qweb_pdf([ddd])[0]


        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
   
    @route('/print/payslip', methods=['POST', 'GET'], csrf=False, type='http', auth="user", website=True)
    def print_payslip(self, **post):

        pdf = request.env.ref('hr_payroll.action_report_payslip').sudo().render_qweb_pdf([int(post['id'])])[0]


        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    