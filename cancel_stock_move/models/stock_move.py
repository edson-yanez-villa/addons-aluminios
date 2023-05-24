
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def cancel_stock_move(self):
        for record in self:
            record.write({
                'state': 'draft'
            })
            record.action_cancel()
            record.unlink()
        