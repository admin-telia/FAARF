from math import floor

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCreditTransfert(models.Model):
    """Definition de la table credit"""

    _name = 'credit_annulation_acc'
    _rec_name = 'motif'

    motif = fields.Char(string='Motif', required=True)
    date_annul = fields.Date(string='Date annulation', required=False)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    state = fields.Selection(string='Etat', readonly=True, default="B",
                             selection=[('B', 'Brouillon'), ('A', 'Annuler')], )

    credit_ids = fields.Many2many(comodel_name='credit_credit', string='Credit_ids')

    def set_annuler(self):
        for rec in self.credit_ids:
            if rec.state == 'DA':
                rec.state = 'AN'

        self.state = 'A'
        self.date_annul = fields.Date.context_today(self)