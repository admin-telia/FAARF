from math import floor

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCreditTransfert(models.Model):
    """Definition de la table credit"""

    _name = 'credit_credit_transfert'
    _rec_name = 'motif'

    motif = fields.Char(string='Motif', required=True)
    gestionnaire_de_id = fields.Many2one('res.users', string='Gestionnaire', required=True, )
    gestionnaire_a_id = fields.Many2one('res.users', string='Gestionnaire', required=True, )
    date_transf = fields.Date(string='Date transfert', required=False)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    state = fields.Selection(string='Etat', readonly=True, default="B",
                             selection=[('B', 'Brouillon'), ('T', 'Transféré')], )

    credit_ids = fields.Many2many(comodel_name='credit_credit', string='Credit_ids')

    def set_validate(self):
        for rec in self.credit_ids:
            if rec.gestionnaire_id.id == self.gestionnaire_de_id.id:
                rec.gestionnaire_id = self.gestionnaire_a_id
                rec.superviseur_id = self.gestionnaire_a_id.x_superviseur_id

        self.state = 'T'
        self.date_transf = fields.Date.context_today(self)