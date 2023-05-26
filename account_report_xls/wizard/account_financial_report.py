# -*- coding: utf-8 -*-

from odoo import api, fields, models
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    excel_file = fields.Binary('Excel File')

    @api.multi
    def get_style(self):
        main_header_style = easyxf('font:height 300;'
                                   'align: horiz center;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz center;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        left_header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                                   'align: horiz left;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        text_left = easyxf('font:height 200; align: horiz left;'
                           "borders: top thin,left thin,right thin,bottom thin")

        text_right = easyxf('font:height 200; align: horiz right;'
                            "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')

        text_left_bold = easyxf('font:height 200; align: horiz right;font:bold True;'
                                "borders: top thin,left thin,right thin,bottom thin")

        text_right_bold = easyxf('font:height 200; align: horiz right;font:bold True;'
                                 "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')
        text_center = easyxf('font:height 200; align: horiz center;'
                             "borders: top thin,left thin,right thin,bottom thin")

        return [main_header_style, left_header_style, header_style, text_left, text_right, text_left_bold,
                text_right_bold, text_center]

    @api.multi
    def check_report_excel(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(
            ['date_from', 'date_to', 'journal_ids', 'target_move', 'date_from_cmp', 'debit_credit', 'date_to_cmp',
             'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter', 'target_move', 'comparison_context'])[
            0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        comparison_context = self._build_comparison_context(data)
        data['form']['comparison_context'] = comparison_context
        rep_data = self.env['report.account.report_financial']
        lines = rep_data.get_account_lines(data.get('form'))

        excel_style = self.get_style()
        main_header_style = excel_style[0]
        left_header_style = excel_style[1]
        header_style = excel_style[2]
        text_left = excel_style[3]
        text_right = excel_style[4]
        text_left_bold = excel_style[5]
        text_right_bold = excel_style[6]
        text_center = excel_style[7]
        # ====================================

        # Define Wookbook and add sheet
        workbook = xlwt.Workbook()
        filename = 'Perdida Ganancia.xls'
        worksheet = workbook.add_sheet('Perdida y Ganancia')
        worksheet.col(0).width = 130 * 150
        worksheet.col(1).width = 130 * 40
        worksheet.write_merge(0, 0, 0, 1, 'Ganancia y Perdida', main_header_style)
        worksheet.write(1, 0, 'Desde', text_left_bold)
        worksheet.write(1, 1, self.date_from, text_left)
        worksheet.write(2, 0, 'Hasta', text_left_bold)
        worksheet.write(2, 1, self.date_to, text_left)
        row = 4
        col = 0
        for line in lines:
            if line['account_type'] == 'sum':
                worksheet.write(row, col, 'Nombre', left_header_style)
                worksheet.write(row, col + 1, 'Saldo', text_right_bold)
                if 'balance_cmp' in line:
                    worksheet.write(row, col + 2, data['form']['label_filter'], text_right)
            elif line['account_type'] == 'account_type':
                worksheet.write(row, col, line['name'], text_left_bold)
                worksheet.write(row, col + 1, line['balance'], text_right_bold)
                if 'balance_cmp' in line:
                    worksheet.write(row, col + 2, line['balance_cmp'], text_right)
            elif line['account_type'] == 'other':
                worksheet.write(row, col, line['name'], text_left)
                worksheet.write(row, col + 1, line['balance'], text_right)
                if 'balance_cmp' in line:
                    worksheet.write(row, col + 2, line['balance_cmp'], text_right)
            row += 1

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})

        if self.excel_file:
            active_id = self.ids[0]
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=accounting.report&download=true&field=excel_file&id=%s&filename=%s' % (
                    active_id, filename),
                'target': 'new',
            }
