from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"
    
    
    @api.model
    def _get_locations_domain(self):
        ids = self.env.user.stock_location_ids.ids
        return [('id', 'in', ids)]

    @api.model
    def _get_default_location(self):
        ids = self.env.user.stock_location_ids.ids
        if ids:
            return ids[0]
        return False
    
    location_id = fields.Many2one(
        'stock.location', "Source Location Zone",
        default=lambda self:self._get_default_location(),
        readonly=True, 
        required=True,
        domain=lambda self:self._get_locations_domain(),
        states={'draft': [('readonly', False)]})
    