# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, timedelta
import calendar

from io import BytesIO
import xlwt
from xlwt import easyxf
import base64


class EstadoResultado(models.TransientModel):
    _name = "estado.resultado"

    @api.model
    def _get_from_date(self):
        date = datetime.now()
        date = str(date.year) + '-01' + '-01'
        return date

    @api.model
    def _get_to_date(self):
        date = datetime.now()
        m_range = calendar.monthrange(date.year, date.month)
        month = date.month
        if date.month < 10:
            month = '0' + str(date.month)
        date = str(date.year) + '-' + str(month) + '-' + str(m_range[1])
        return date

    account_ids = fields.Many2many('account.account', 'rel_wizard_account',
                                   'wizard_id', 'account_id', string=u'Cuentas')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta analitica')
    start_date = fields.Date(string='Fecha Inicial', required="1", default=_get_from_date)
    end_date = fields.Date(string='Fecha Final', required="1", default=_get_to_date)
    company_id = fields.Many2one('res.company', 'Compañia', default=lambda self: self.env.user.company_id)
    excel_file = fields.Binary('Excel File')
    default_Boolean=fields.Boolean(string="Cuentas por defecto")

    @api.multi
    def open_table(self):
        context_report = {}
        domain_report = []
        if self.start_date and self.end_date:
            domain_report.append(('date', '>=', self.start_date))
            domain_report.append(('date', '<=', self.end_date))
        if self.analytic_account_id:
            domain_report.append(('analytic_account_id', '=', self.analytic_account_id.id))
        if self.account_ids:
            domain_report.append(('account_id', 'in', self.account_ids.ids))

        name_context = ""
        name_context += " Desde: %s | " % str(self.start_date)
        name_context += " Hasta: %s " % str(self.end_date)

        return {
            'name': "REPORTE FINANCIERO:" + name_context,
            'view_mode': 'pivot',
            'res_model': 'estado.resultado.report',
            'type': 'ir.actions.act_window',
            'context': context_report,
            'domain': domain_report,
        }

    @api.multi
    def get_default_accounts(self):
        for record in self:
            account_ids = self.env['account.account'].search([
                ("company_id", "=" , self.company_id.id),
                ("user_type_id.name", "in", ['Ingreso', 'Gastos', 'Coste directo de la ventas'])
                ]).ids
            record.account_ids = [(6, 0, account_ids)]
        return {
            "type": "ir.actions.do_nothing",
        }
