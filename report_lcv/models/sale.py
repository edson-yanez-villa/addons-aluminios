# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float('Precio Unitario', required=True, digits=dp.get_precision('Product Price'),
                              change_default=True, default=0.0, store=True)

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        price_product = line.product_id.lst_price * (1 - (line.discount or 0.0) / 100.0)
        total1 = price * line.product_uom_qty
        total2 = price_product * line.product_uom_qty
        if round(total1, 2) != round(total2, 2):
            user = self.env.user
            if not user.has_group('report_lcv.group_sale_price_unit'):
                raise UserError(_('No puede editar el precio del producto'))

        return line

    @api.multi
    def write(self, values):
        result = super(SaleOrderLine, self).write(values)
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_product = line.product_id.lst_price * (1 - (line.discount or 0.0) / 100.0)
            total1 = price * line.product_uom_qty
            total2 = price_product * line.product_uom_qty
            if round(total1, 2) != round(total2, 2):
                user = self.env.user
                if not user.has_group('report_lcv.group_sale_price_unit'):
                    raise UserError(_('No puede editar el precio del producto'))
        return result

    @api.multi
    @api.onchange('price_unit', 'discount')
    def onchange_price_unit_valid(self):
        for line in self:
            if line.product_id:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                price_product = line.product_id.lst_price * (1 - (line.discount or 0.0) / 100.0)
                total1 = price * line.product_uom_qty
                total2 = price_product * line.product_uom_qty
                if round(total1, 2) != round(total2, 2):
                    user = self.env.user
                    if not user.has_group('report_lcv.group_sale_price_unit'):
                        raise UserError(_('No puede editar el precio del producto'))
