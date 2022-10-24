from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class FaarfParamProduit(models.Model):
    """Definir un type de client."""

    _name = "credit_param_financement"
    _description = ""

    name = fields.Char(string='Libellé', required=True)
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    montant = fields.Float(string='Montant ', required=False, digits=(16, 0))
    reste_est = fields.Float(string='Montant ', required=False, digits=(16, 0))
    reste_reel = fields.Float(string='Montant ', required=False, digits=(16, 0))

    line_ids = fields.One2many(
        comodel_name='credit_param_financement_line',
        inverse_name='financement_id',
        string='Ligne',
        required=False)


class FaarfParamProduit(models.Model):
    """Definir un type de client."""

    _name = "credit_param_financement_line"
    _description = ""

    date = fields.Date(string='Date', required=False)
    montant = fields.Float(string='Montant ', required=False, digits=(16, 0))
    current_user = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    financement_id = fields.Many2one('credit_param_financement', string='Financement_id', required=False)


class FaarfParamProduit(models.Model):
    """Definir un type de client."""

    _name = "credit_param_produit"
    _description = ""

    name = fields.Char(string='Libellé', required=True)
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    type_produit = fields.Selection(string='Type produit',
                                    selection=[('CREDIT', 'CREDIT'),
                                               ('PROJET', 'Projet/Programme'), ],
                                    required=True)
    ordre_remboursment = fields.Selection(string='Ordre de remboursement',
                                          selection=[('1', 'Garantie -> Capital -> Intérêt'),
                                                     ('2', 'Garantie -> Intérêt -> Capital'),
                                                     ('3', 'Capital -> Intérêt -> Garantie'),
                                                     ('4', 'Capital -> Garantie -> Intérêt'),
                                                     ('5', 'Intérêt -> Capital -> Garantie'),
                                                     ('6', 'Intérêt -> Garantie -> Capital'), ],
                                          required=True, default='1')

    # individuelle
    taux_int_annuel = fields.Float(string="Taux d'intérêt annuel", required=True)
    taux_int_annuel_psh = fields.Float(string="Taux d'intérêt annuel PVH", required=True)
    taux_frais_dossier = fields.Float(string="Taux frais de dossier", required=True)
    taux_garantie = fields.Float(string="Taux de fonds d'autonomisation", required=True)

    # GS
    taux_int_annuel_gs = fields.Float(string="Taux d'intérêt annuel", required=True)
    taux_int_annuel_psh_gs = fields.Float(string="Taux d'intérêt annuel PVH", required=True)
    taux_frais_dossier_gs = fields.Float(string="Taux frais de dossier", required=True)
    taux_garantie_gs = fields.Float(string="Taux de fonds d'autonomisation", required=True)

    n_min_membre_gs = fields.Integer(string='Nombre min. de membre', required=True)
    n_max_membre_gs = fields.Integer(string='Nombre max. de membre', required=True)

    # ASS/GR
    taux_int_annuel_ass = fields.Float(string="Taux d'intérêt annuel", required=True)
    taux_int_annuel_psh_ass = fields.Float(string="Taux d'intérêt annuel PVH", required=True)
    taux_frais_dossier_ass = fields.Float(string="Taux frais de dossier", required=True)
    taux_garantie_ass = fields.Float(string="Taux de fonds d'autonomisation", required=True)

    n_min_membre_ass = fields.Integer(string='Nombre min. de membre', required=True)
    n_max_membre_ass = fields.Integer(string='Nombre max. de membre', required=True)

    montant_max_antenne = fields.Float(string='Montant max. antenne régionale', required=True, digits=(16, 0))
    montant_max_com_credit = fields.Float(string='Montant max. comité crédit', required=True, digits=(16, 0))
    montant_max_dg = fields.Float(string='Montant max. DG', required=True, digits=(16, 0))
    montant_max_cca = fields.Float(string='Comité CA', required=True, digits=(16, 0))

    document_ids = fields.One2many(
        comodel_name='credit_prod_document',
        inverse_name='produit_id',
        string='documents',
        required=False)

    crit_fondamentaux = fields.One2many(
        comodel_name='credit_prod_crit_fond',
        inverse_name='produit_id',
        string='Critères fondamentaux',
        required=False)

    crit_complementaires = fields.One2many(
        comodel_name='credit_prod_crit_compl',
        inverse_name='produit_id',
        string='Critères Complémentaires',
        required=False)

    # compte
    cpte_membr = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Client', required=False)
    cpte_int = fields.Many2one(comodel_name='compta_plan_lines', string="Compte Intêret", required=False)

    cpte_frais = fields.Many2one(comodel_name='compta_plan_lines', string="Compte Frais dossier", required=False)
    cpte_penalite = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Pénalité', required=False)
    cpte_fa = fields.Many2one(comodel_name='compta_plan_lines', string="Compte FA (Garantie)", required=False)
    cpte_assurance = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Assurance', required=False)
    capital = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Principal', required=False)

    active = fields.Boolean('Actif', default=True, )


# Parametre critere
class CreditProduitDocument(models.Model):
    """Definir un type de client."""

    _name = "credit_prod_document"
    _description = ""

    name = fields.Char(string='Libellé', required=True)
    est_obligatoire = fields.Boolean(string='Obligatoire ?', required=False)

    sc = fields.Boolean(string='S/C', required=False)
    ef = fields.Boolean(string='Entreprise formelle', required=False)
    grp = fields.Boolean(string='Groupement', required=False)
    ass = fields.Boolean(string='Association', required=False)
    gs = fields.Boolean(string='Groupe solidaire', required=False)
    ind = fields.Boolean(string='Individuelle', required=False)

    produit_id = fields.Many2one(
        comodel_name='credit_param_produit',
        string='Produit_id',
        required=False)


# Parametre critere
class CreditProduitCritereFond(models.Model):
    """Definir un type de client."""

    _name = "credit_prod_crit_fond"
    _description = ""

    name = fields.Char(string="Eléments d'analyse", required=True)
    borne_sup = fields.Integer(string='Borne supérieure', required=True)
    borne_inf = fields.Integer(string='Borne inférieure', required=True)

    sequence = fields.Integer(string='Séquence', required=True)

    produit_id = fields.Many2one(
        comodel_name='credit_param_produit',
        string='Produit_id',
        required=False)


class CreditProduitCritereComp(models.Model):
    """Definir un type de client."""

    _name = "credit_prod_crit_compl"
    _description = ""

    name = fields.Char(string="Eléments d'analyse", required=True)
    borne_sup = fields.Integer(string='Borne supérieure', required=True)
    borne_inf = fields.Integer(string='Borne inférieure', required=True)

    sequence = fields.Integer(string='Séquence', required=True)

    produit_id = fields.Many2one(
        comodel_name='credit_param_produit',
        string='Produit_id',
        required=False)


# param assur
class CreditAssureur(models.Model):
    """ Credit Assureurs """
    _name = 'credit_param_assureur'
    _description = "Credit Assureurs"

    assureur_id = fields.Many2one('credit_assureur', string='Assureur', required=True)
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)

    taux_assureur = fields.Float(string='Taux Assureur', required=True)
    taux_bailleur = fields.Float(string='Taux Bailleur', required=True)
    taux_gestionnaire = fields.Float(string='Taux Gestionnaire', required=True)

    cpte_assureur = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Assureur', required=False)
    cpte_produit = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Produit', required=False)

    @api.constrains('assureur_id', 'bailleur_id')
    def _check_assur_baill(self):
        for rec in self:
            r = self.env['credit_param_assureur'].search([('assureur_id', '=', rec.assureur_id.id),
                                                          ('bailleur_id', '=', rec.bailleur_id.id),
                                                          ('id', '!=', rec.id)])
            if r:
                raise ValidationError("Le paramétrage de l'Assureur doit etre unique par bailleur")
