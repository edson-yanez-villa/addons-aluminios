from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class SaleAdvancePaymentInvInherith(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    
    @api.multi
    def create_invoices(self):
        context = dict(self.env.context)
        context['come_sale'] = True
        return super(SaleAdvancePaymentInvInherith, self.with_context(context)).create_invoices()
