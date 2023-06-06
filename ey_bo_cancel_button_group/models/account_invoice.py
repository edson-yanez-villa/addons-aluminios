from odoo import models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    user_can_cancel = fields.Boolean("Puede cancelar", compute='_can_cancel_button')

    def _can_cancel_button(self):
        for record in self:
            if record.state == 'open':
                record.user_can_cancel = self.env.user.has_group('ey_bo_cancel_button_group.group_cancel_button')
            elif record.state in ['draft', 'proforma2']:
                record.user_can_cancel = True
            else:
                record.user_can_cancel = False
                