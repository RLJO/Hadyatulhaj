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

from . import main as mainController


class ESSPortalProfile(Controller):

    @route(['/my/information'], type='http', auth='user', website=True)
    def information(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':

            if 'image_1920' in post:
                image_1920 = post.get('image_1920')
                if image_1920:
                    image_1920 = image_1920.read()
                    image_1920 = base64.b64encode(image_1920)
                    emb_obj.sudo().write({
                        'image_1920': image_1920
                    })
                post.pop('image_1920')

    @route(['/my/myProfile'], type='http', auth='user', website=True)
    def myProfile(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })
        
        values.update({
            'partner': partner,
            'employee': emb_obj,
        })
        

        print(values)
        response = request.render("ess.ess_myorofile", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    @route(['/my/contracts'], type='http', auth='user', website=True)
    def my_contracts(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        contract_obj = request.env['hr.contract'].sudo().search([('employee_id','=',emb_obj.id)])

        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })

        values.update({
            'partner': partner,
            'employee': emb_obj,
            'contract_obj': contract_obj,
        })
        
        response = request.render("ess.ess_contract", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/myExperians'], type='http', auth='user', website=True)
    def myExperians(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })
        
        values.update({
            'partner': partner,
            'employee': emb_obj,
        })
        

        print(values)
        response = request.render("ess.ess_myexperians", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    @route(['/my/myEducational'], type='http', auth='user', website=True)
    def myEducational(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })
        
        values.update({
            'partner': partner,
            'employee': emb_obj,
        })
        

        print(values)
        response = request.render("ess.ess_myeducational", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @route(['/my/myskills'], type='http', auth='user', website=True)
    def myskills(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })
        
        values.update({
            'partner': partner,
            'employee': emb_obj,
        })
        

        print(values)
        response = request.render("ess.ess_myskills", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    @route(['/my/network'], type='http', auth='user', website=True)
    def network(self, redirect=None, **post):
        values = {}
        
        partner = request.env.user.partner_id
        emb_obj = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])
        emb_objs = request.env['hr.employee'].sudo().search([('id','!=',emb_obj.id)])

        values = mainController.ESSPortal.check_modules(self)

        values.update({
            'error': {},
            'error_message': [],
        })
        
        values.update({
            'partner': partner,
            'employee': emb_obj,
            'emb_objs' : emb_objs,
        })
        

        print(values)
        response = request.render("ess.ess_network", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    