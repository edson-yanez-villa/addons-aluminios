from odoo.tools import config
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def _post_validate(self):
        for move in self:
            if move.line_ids:
                for line in move.line_ids:
                    if line.company_id.id != move.company_id.id:
                        query = 'UPDATE account_move_line SET company_id = %s WHERE id = %s' % (move.company_id.id, line.id)
                        self.env.cr.execute(query)
                        self.env.cr.commit()
                if not all([x.company_id.id == move.company_id.id for x in move.line_ids]):
                    raise UserError(_("Cannot create moves for different companies."))
        self.assert_balanced()
        return self._check_lock_date()
