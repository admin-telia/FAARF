from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _inherit = 'credit_credit'

    note_notation = fields.Integer(string='Note', required=False, compute="calcul_note_notation")

    @api.depends('crit_fondamentaux_ids', 'crit_complementaires_ids')
    def calcul_note_notation(self):
        for val in self:
            note = 0
            for crit in val.crit_fondamentaux_ids:
                note = note + crit.score

            for crit in val.crit_complementaires_ids:
                note = note + crit.score

            val.note_notation = note

    #affichage des criteres de notation
    def action_rechercher(self):
        if not self.produit_credit:
            return
        elements = self.env["credit_prod_crit_fond"].search([
            ('produit_id', '=', self.produit_credit.id)], order="sequence")
        x_lines_ids = []
        # delete old payslip lines
        self.crit_fondamentaux_ids.unlink()
        for e in elements:
            x_lines_ids.append((0, 0,
                                {'name': e.name, 'borne_sup': e.borne_sup, 'borne_inf': e.borne_inf,
                                 'bareme': e.borne_sup,
                                 'score': 0, 'sequence': e.sequence,
                                 }))
        self.crit_fondamentaux_ids = x_lines_ids

        elements = self.env["credit_prod_crit_compl"].search([
            ('produit_id', '=', self.produit_credit.id)], order="sequence")
        x_lines_ids = []
        # delete old payslip lines
        self.crit_complementaires_ids.unlink()
        for e in elements:
            x_lines_ids.append((0, 0,
                                {'name': e.name, 'borne_sup': e.borne_sup, 'borne_inf': e.borne_inf,
                                 'bareme': e.borne_sup,
                                 'score': 0, 'sequence': e.sequence,
                                 }))
        self.crit_complementaires_ids = x_lines_ids