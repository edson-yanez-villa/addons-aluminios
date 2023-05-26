# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class EstadoResultadoReport(models.Model):
    _name = "estado.resultado.report"
    _description = "Estado de resultados"
    _auto = False
    # _rec_name = 'date'

    group0 = fields.Many2one('account.group', string='Nivel 0', readonly=True)
    group1 = fields.Many2one('account.group', string='Nivel 1', readonly=True)
    group2 = fields.Many2one('account.group', string='Nivel 2', readonly=True)
    group3 = fields.Many2one('account.group', string='Nivel 3', readonly=True)
    group4 = fields.Many2one('account.group', string='Nivel 4', readonly=True)
    account_id = fields.Many2one('account.account', string='Cuenta', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta Analítica', readonly=True)
    debit = fields.Float(string='Debito', readonly=True)
    credit = fields.Float(string='Credito', readonly=True)
    balance = fields.Float(string='Balance', readonly=True)
    date = fields.Date(string='Fecha', readonly=True)

    def _select(self):
        select_str = """
            select aml.id,
               l0.id   as group0,
               l1.id   as group1,
               l2.id   as group2,
               l3.id   as group3,
               ag.id   as group4,
               ag.parent_id,
               ag.level,
               ag.code_prefix,
               ag.name as nameg,
               aa.id as account_id,
               aml.analytic_account_id,
               aa.code as cuenta,
               aa.name as cuenta_nombre,
               aml.date,
               DATE_PART(
                       'month',
                       aml.date
                   )   AS mes,
               aml.debit,
               aml.credit,
               aml.balance
        """
        return select_str

    def _from(self):
        from_str = """
                from account_move_line aml
                         inner join account_move am on am.id = aml.move_id
                         inner join account_account aa on aa.id = aml.account_id
                         inner join account_group ag on ag.id = aa.group_id
                         left join account_group l3 on l3.id = ag.parent_id
                         left join account_group l2 on l2.id = l3.parent_id
                         left join account_group l1 on l1.id = l2.parent_id
                         left join account_group l0 on l0.id = l1.parent_id
                where aa.group_id is not null
                  and am.state in ('posted')
                  --and aml.account_id in (13038, 13039, 13040)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
                GROUP BY aml.id,
                           l0.id,
                           l1.id,
                           l2.id,
                           l3.id,
                           ag.id,
                           ag.parent_id,
                           ag.level,
                           ag.code_prefix,
                           ag.name,
                           aa.id,
                           aml.analytic_account_id,
                           aa.code,
                           aa.name,
                           aml.date
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
        )""" % (
            self._table, self._select(), self._from(), self._group_by()))
