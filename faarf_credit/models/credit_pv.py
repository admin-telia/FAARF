from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class CreditCreditPv(models.Model):
    """Definition de la table credit"""
    _name = 'credit_credit_pv'

    _description = "Faarf proces verbal"

    name = fields.Char(string='Numéro', required=False)

    credit_count = fields.Integer(string='Dossiers analysés', compute="calcul_count")
    credit_count_montant = fields.Float(string="Montant", compute="calcul_count", digits=(16, 0))
    credit_accorde = fields.Integer(string='Dossiers accordés', compute="calcul_count")
    credit_accorde_montant = fields.Float(string="Montant", compute="calcul_count", digits=(16, 0))
    credit_ajourne = fields.Integer(string='Dossiers ajournés', compute="calcul_count")
    credit_ajourne_montant = fields.Float(string="Montant", compute="calcul_count", digits=(16, 0))
    credit_refuse = fields.Integer(string='Dossiers refusés', compute="calcul_count")
    credit_refuse_montant = fields.Float(string="Montant", compute="calcul_count", digits=(16, 0))

    date = fields.Datetime(string='Date', required=False)

    membre_ids = fields.One2many(
        comodel_name='credit_credit_pv_commite',
        inverse_name='credit_pv_id',
        string='Membres',
        required=False)

    credit_line_ids = fields.One2many(
        comodel_name='credit_credit_pv_credit',
        inverse_name='credit_pv_id',
        string='Membres',
        required=False)

    credit_ids = fields.One2many(
        comodel_name='credit_credit',
        inverse_name='credit_pv_id',
        string='Crédits',
        required=False)

    state = fields.Selection(string='Etat', readonly=True, default="B",
                             selection=[('B', 'Brouillon'), ('A', 'Approuvée'),
                                        ('S', 'Signé')], )

    @api.depends('credit_line_ids')
    def calcul_count(self):
        for val in self:
            val.credit_accorde = self.env['credit_credit_pv_credit'].search_count([
                ('credit_pv_id', '=', val.id),
                ('state', '=', 'A'),
            ])

            val.credit_ajourne = self.env['credit_credit_pv_credit'].search_count([
                ('credit_pv_id', '=', val.id),
                ('state', '=', 'AJ'),
            ])
            val.credit_refuse = self.env['credit_credit_pv_credit'].search_count([
                ('credit_pv_id', '=', val.id),
                ('state', '=', 'R'),
            ])

            val.credit_count = val.credit_accorde + val.credit_ajourne + val.credit_refuse

            credit_accorde_montant = 0
            credit_ajourne_montant = 0
            credit_refuse_montant = 0

            for l in val.credit_line_ids:
                if l.state == 'A':
                    credit_accorde_montant = credit_accorde_montant + l.credit_id.montant_accorde
                elif l.state == 'AJ':
                    credit_ajourne_montant = credit_ajourne_montant + l.credit_id.montant_accorde
                elif l.state == 'R':
                    credit_refuse_montant = credit_refuse_montant + l.credit_id.montant_accorde

            val.credit_accorde_montant = credit_accorde_montant
            val.credit_ajourne_montant = credit_ajourne_montant
            val.credit_refuse_montant = credit_refuse_montant
            val.credit_count_montant = credit_accorde_montant + credit_ajourne_montant + credit_refuse_montant

    def add_credit_line(self, credit_id, state):
        self.env['credit_credit_pv_credit'].create({
            'credit_id': credit_id,
            'state': state,
            'date': datetime.now(),
            'credit_pv_id': self.id
        })

    def set_validate(self):
        credit_compteur = self.env['credit_compteur_pv'].search([])
        nombre = 1
        if credit_compteur:
            nombre = credit_compteur.nombre + 1
            credit_compteur.nombre = nombre
            nombre = str(nombre).zfill(6)
        else:
            self.env['credit_compteur_pv'].create({
                'nombre': 1,
            })
            nombre = str(nombre).zfill(6)

        self.name = nombre
        self.date = datetime.now()
        self.state = 'A'


class CreditCreditPvCommite(models.Model):
    """Definition de la table credit"""
    _name = 'credit_credit_pv_commite'

    user_id = fields.Many2one('res.users', string='Membre', required=False)
    signature = fields.Datetime(string='Signature', required=False)

    credit_pv_id = fields.Many2one(
        comodel_name='credit_credit_pv',
        string='Credit_pv_id',
        required=False)


class CreditCreditPvCredit(models.Model):
    """Definition de la table credit"""
    _name = 'credit_credit_pv_credit'

    credit_id = fields.Many2one(
        comodel_name='credit_credit',
        string='Crédit',
        required=False)

    date = fields.Datetime(string='Date', required=False)

    state = fields.Selection(string='Etat', readonly=True, default="B",
                             selection=[('A', 'Accordé'), ('AJ', 'Ajourné'),
                                        ('R', 'Rejeté')], )

    credit_pv_id = fields.Many2one(
        comodel_name='credit_credit_pv',
        string='Credit_pv_id',
        required=False)
