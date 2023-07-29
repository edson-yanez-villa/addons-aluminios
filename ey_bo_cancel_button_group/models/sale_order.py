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
                record.can_cancel = self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_sale')
            else:
                record.can_cancel = record.state in ['sale', 'draft', 'sent'] and len(pickings) == 0

    @api.multi
    def action_sale_ok(self):
        context = dict(self.env.context)
        context['come_sale'] = True
        return super(SaleOrder, self.with_context(context)).action_sale_ok()

    @api.multi
    def write(self, vals):
        context = dict(self.env.context)
        come_sale = context.get('come_sale', False)
        if not come_sale and not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_sale') and self.state in ['sale']:
            raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
        else:
            if come_sale:
                context.pop('come_sale')
            return super(SaleOrder, self.with_context(context)).write(vals)
    