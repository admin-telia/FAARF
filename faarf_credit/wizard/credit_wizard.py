from odoo import fields, models, api


class CreditCreditValider(models.TransientModel):
    _name = 'wiz_credit_credit_com_valider'
    _description = 'credit_credit_com_valider'

    name = fields.Char(string='Name', required=False)
    montant_demande = fields.Float(string='Montant demandé ', required=False, digits=(16, 0))
    montant_accorde = fields.Float(string='Montant accordé ', required=False, digits=(16, 0))
    date_demande = fields.Date(string="Date d'approbation ", required=True, default=fields.Date.context_today)
    avis_commite_antenne = fields.Text(string="Avis du comité régional", required=False)

    credit_id = fields.Many2one("credit_credit", string="", required=False, )

    def valider(self):
        pass
