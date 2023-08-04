from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    user_can_cancel = fields.Boolean("Puede cancelar", compute='_can_cancel_button')

    def _can_cancel_button(self):
        for record in self:
            if record.state == 'open':
                record.user_can_cancel = self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice')
            elif record.state in ['draft', 'proforma2']:
                record.user_can_cancel = True
            else:
                record.user_can_cancel = False

    # @api.model
    # def get_count_as(self):
    #     context = dict(self.env.context)
    #     context['come_sale'] = True
    #     return super(AccountInvoice, self.with_context(context)).get_count_as()
    
    # @api.multi
    # def action_invoice_open(self):
    #     context = dict(self.env.context)
    #     context['come_sale'] = self.origin and self.state in ['draft']
    #     return super(AccountInvoice, self.with_context(context)).action_invoice_open()

    @api.multi
    def write(self, vals):
        # write_invoice = not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice') and self.state in ['paid']
        # order = self.env['sale.order'].search([('name', '=', self.origin)])
        # has_origin_sale = self.origin and (order.state in ['sale'] if order else False)
        # context = dict(self.env.context)
        # come_sale = context.get('come_sale', False)
        invoice_line_ids = vals.get('invoice_line_ids', False)
        if invoice_line_ids and not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice'):
            raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
        else:
            return super(AccountInvoice, self).write(vals)
    
    
# class AccountInvoiceLineInherit(models.Model):
#     _inherit = 'account.invoice.line'
    
#     # @api.onchange('product_id', 'name', 'account_id', 'account_analytic_id', 'analytic_tag_ids', 'quantity', 'uom_id', 'price_unit', 'discount', 'invoice_line_tax_ids', 'price_subtotal')
#     # def _onchange_items_line(self):
#     #     if not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice'):
#     #         raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
    
#     @api.multi
#     def write(self, vals):
#         if not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice'):
#             raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
#         else:
#             return super(AccountInvoiceLineInherit, self).write(vals)
