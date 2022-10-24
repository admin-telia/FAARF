from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _inherit = 'credit_credit'

    def set_acc_projet_programme(self):
        self.write({
            'state': 'BEN',
        })

    def set_val_projet_programme(self):
        # self.calcul_tableau_amortissement()
        name = self.env['ir.sequence'].next_by_code('credit.sequence.code') or 'New'
        self.sudo().write({
            'state': 'DA',
            'name': name
        })

    # pour notation
    def set_env_notation(self):
        self.write({
            'state': 'RC',
        })

    #pour choix benef
    def set_env_choix_benef(self):
        self.write({
            'state': 'NOT',
        })

class CreditProjetChoixBenef(models.TransientModel):
    """ """
    _name = "credit_projet_ch_benef"
    _description = ""

    def _default_name(self):
        return "Comité regional"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    zone_id = fields.Many2one("ref_zone", "Zone", required=False)
    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)


    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_benef = fields.Integer(string=' Nombre de bénéficiare', required=False, compute="calcul_montant")
    montant = fields.Float(string='Montant', required=False, digits=(16, 0), compute="calcul_montant")

    @api.depends('credit_ids')
    def calcul_montant(self):
        for val in self:
            val.nbr_benef = len(val.credit_ids)
            montant = 0
            for c in self.credit_ids:
                montant = montant + c.montant_accorde
            val.montant = montant

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        credit_ids = self.env['credit_credit'].search([
            ('state', '=', 'NOT'),
            ('bailleur_id', '=', self.bailleur_id.id),
            ('produit_credit', '=', self.produit_credit.id),
        ], order="note_notation")
        if self.superviseur_id:
            credit_ids = credit_ids.search([
                ('superviseur_id', '=', self.superviseur_id.id)])

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})
        self.credit_ids = credit_ids

    def set_accorde_r(self):
        for val in self.credit_ids:
            val.set_acc_projet_programme()



class CreditProjetRabottage(models.TransientModel):
    """ """
    _name = "credit_projet_rabo"
    _description = ""

    def _default_name(self):
        return "Comité regional"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    zone_id = fields.Many2one("ref_zone", "Zone", required=False)
    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)


    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_benef = fields.Integer(string=' Nombre de bénéficiare', required=False, compute="calcul_montant")
    montant = fields.Float(string='Montant', required=False, digits=(16, 0), compute="calcul_montant")

    @api.depends('credit_ids')
    def calcul_montant(self):
        for val in self:
            val.nbr_benef = len(val.credit_ids)
            montant = 0
            for c in self.credit_ids:
                montant = montant + c.montant_accorde
            val.montant = montant

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        credit_ids = self.env['credit_credit'].search([
            ('state', '=', 'BEN'),
            ('bailleur_id', '=', self.bailleur_id.id),
            ('produit_credit', '=', self.produit_credit.id),
        ], order="note_notation")
        if self.superviseur_id:
            credit_ids = credit_ids.search([
                ('superviseur_id', '=', self.superviseur_id.id)])

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})
        self.credit_ids = credit_ids

    def set_accorde_r(self):
        for val in self.credit_ids:
            val.set_val_projet_programme()