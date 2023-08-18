from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class UsersInherith(models.Model):
    _inherit = 'res.users'
    
    stock_location_ids = fields.Many2many('stock.location', string='Ubicaciones permitidas')
