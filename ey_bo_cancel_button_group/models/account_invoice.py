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

    @api.multi
    def write(self, vals):
        invoice_line_ids = vals.get('invoice_line_ids', False)
        journal_id = vals.get('journal_id', False)
        date_invoice = vals.get('date_invoice', False)
        if not date_invoice and not journal_id and invoice_line_ids and not self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_edit_button_invoice'):
            raise UserError('Usted no tiene los permisos necesarios para realizar esta accion')
        return super(AccountInvoice, self).write(vals)
    