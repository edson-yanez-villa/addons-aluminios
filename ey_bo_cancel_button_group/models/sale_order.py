from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    can_cancel = fields.Boolean('Puede cancelar', compute='_can_cancel_button')

    def _can_cancel_button(self):
        for record in self:
            pickings = record.picking_ids.filtered(lambda picking: picking.state == 'done' )
            invoices = record.invoice_ids.filtered(lambda invoice: invoice.state in ['open', 'paid'])
            if record.state == 'sale' and (len(pickings) > 0 or len(invoices) > 0):
                record.can_cancel = self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_button')
            else:
                record.can_cancel = record.state in ['sale', 'draft', 'sent'] and len(pickings) == 0

    @api.model
    def create(self, vals):
        if self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_button'):
            return super(SaleOrder, self).create(vals)
        else:
            raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')

    @api.multi
    def write(self, vals):
        if self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_button'):
            return super(SaleOrder, self).write(vals)
        else:
            raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
    