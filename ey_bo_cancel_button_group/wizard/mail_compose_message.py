from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class MailComposerInherith(models.TransientModel):
    _inherit = 'mail.compose.message'
    
    @api.multi
    def send_mail_action(self):
        context = dict(self.env.context)
        if self.env.user.has_group('ey_bo_cancel_button_group.group_create_button_sale'):
            context['come_create_order'] = True
        return super(MailComposerInherith, self.with_context(context)).send_mail()
