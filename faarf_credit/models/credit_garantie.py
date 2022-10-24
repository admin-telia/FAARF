from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditClientGarantie(models.Model):
    """Definition de la table credit"""

    _name = 'credit_client_garantie'
    cliente_id = fields.Many2one('credit_clients', string='Cliente', required=True)
    credit_id = fields.Many2one('credit_credit', string='Crédit', required=True)

    montant = fields.Float(string='Montant ', required=False, digits=(16, 0))
    date = fields.Date(string='Date', required=True, )
    piece_comptable = fields.Char(string='Pièce comptable', required=False)

    is_rembourse = fields.Boolean(
        string='Remboursé ?',
        default=0,
        required=False)


class CreditGarantie(models.Model):
    """Definition de la table credit"""

    _name = 'credit_garantie'
    name = fields.Char(string='N°', required=False, default="-")
    date = fields.Date(string='Date', required=False)

    cliente_id = fields.Many2one('credit_clients', string='Bénéficiaire', required=True)
    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    gestionnaire = fields.Char(string='Gestionnaire', required=False, related="cliente_id.gestionnaire_id.name")
    province = fields.Char(string='Province', required=False, related="cliente_id.province_id.name")
    departement = fields.Char(string='Departement', required=False, related="cliente_id.departement_id.name")
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    montant = fields.Float(string="Montant", required=False, digits=(16, 0), compute="calcul_montant", store=True)
    line_ids = fields.One2many('credit_garantie_line', inverse_name='garantie_id', string='Credit_ids')
    ligne_ids = fields.Many2many('credit_client_garantie', string='Crédits')

    credit_ids = fields.Many2many(comodel_name='credit_credit', string='Credit_ids')

    state = fields.Selection([('N', 'N'), ('A', 'A'),
                              ('P', 'P')],
                             string='Etat', readonly=True, default="N", )

    def set_calculer(self):
        # credits = self.env['credit_credit'].search([
        #     ('cliente_id', '=', self.cliente_id.id),
        # ], order='id asc')
        credits = self.credit_ids
        self.line_ids.unlink()
        for c in credits:
            rembours = self.env['credit_credit_remboursement_line'].search([('credit_id.id', '=', c.id)])
            montant_p_paye = 0
            interet_paye = 0
            garantie_paye = 0
            penalite = 0
            capital = c.montant_accorde
            interet = c.montant_interet
            for l in rembours:
                montant_p_paye += l['montant_p']
                interet_paye += l['interet_p']
                garantie_paye += l['garantie_p']
            montant_a_rembourser = c.montant_accorde + c.montant_interet + c.montant_garantie
            montant_rembourser = montant_p_paye + interet_paye + garantie_paye
            montant_reste = montant_a_rembourser - montant_rembourser
            montant_fa_reverser = montant_rembourser - capital - interet - penalite

            self.env['credit_garantie_line'].create({
                'num_pret': c.name,
                'montant_capital': capital,
                'montant_a_rembourser': montant_a_rembourser,
                'montant_rembourser': montant_rembourser,
                'montant_reste': montant_reste,
                'montant_fa': garantie_paye,
                'montant_penalite': 0,
                'montant_fa_reverser': montant_fa_reverser,
                'garantie_id': self.id
            })

    def set_valider(self):
        if self.montant < 0:
            raise ValidationError("Vous ne pouvez pas valider cet odre de restitution")
        else:
            compteur = self.env['credit_compt_client_garantie'].search([])
            nombre = 1
            if compteur:
                c = compteur[0]
                nombre = c.nombre + 1
                compteur.nombre = nombre
                nombre = str(nombre).zfill(9)
            else:
                self.env['credit_compt_client_garantie'].create({
                    'nombre': 1,
                })
                nombre = str(nombre).zfill(9)

            self.name = nombre
            self.state = 'A'

            for l in self.line_ids:
                credit = self.env['credit_credit'].search([('name', '=', l.num_pret)])
                credit.fa_state = '2'

    @api.depends('line_ids')
    def calcul_montant(self):
        for val in self:
            montant = 0
            for l in val.line_ids:
                montant = montant + l.montant_fa_reverser
            val.montant = montant


class CreditGarantieLine(models.Model):
    """Definition de la table credit"""

    _name = 'credit_garantie_line'
    _order = 'num_pret'

    num_pret = fields.Char(string='Numéro du prêts', required=False, readonly='1')
    montant_capital = fields.Float(string='Capital ', required=False, digits=(16, 0))
    montant_a_rembourser = fields.Float(string='Montant à rembourser', required=False, digits=(16, 0))
    montant_rembourser = fields.Float(string='Montant remboursé', required=False, digits=(16, 0))
    montant_reste = fields.Float(string='Reste à payer ', required=False, digits=(16, 0))
    montant_fa = fields.Float(string='F.A constitué', required=False, digits=(16, 0))
    montant_penalite = fields.Float(string='Pénalité ', required=False, digits=(16, 0))
    montant_fa_reverser = fields.Float(string='F.A à reverser', required=False, digits=(16, 0))

    garantie_id = fields.Many2one('credit_garantie', string='Odoo', required=False)


class CreditRemboursementFA(models.Model):
    """Definition rouboursement d'echeance ou arriere avec FA"""

    _name = 'credit_remboursement_fa'

class CreditRemboursementFALine(models.Model):
    """Definition rouboursement d'echeance ou arriere avec FA"""

    _name = 'credit_remboursement_fa_line'

    credit_id = fields.Many2one(comodel_name='credit', string='Credit_id', required=False)
    cliente_id = fields.Many2one('credit_clients', string='Cliente', required=True)
    montant_credit = fields.Float(string='Montant crédit ', required=False, digits=(16, 0))
    montant_du = fields.Float(string='Dû ', required=False, digits=(16, 0))
    montant_fa = fields.Float(string='Fa ', required=False, digits=(16, 0))