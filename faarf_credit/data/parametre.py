from odoo import fields, models, api


class FaarfParamProduit(models.Model):
    """Definir un type de client."""

    _name = "credit_param_produit"
    _description = ""

    name = fields.Char(string='Libellé', required=False)
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=False)
    #individuelle
    taux_int_annuel = fields.Float(string="Taux d'intérêt annuel", required=False)
    taux_int_annuel_psh = fields.Float(string="Taux d'intérêt annuel PSH", required=False)
    taux_frais_dossier = fields.Float(string="Taux frais de dossier", required=False)
    taux_garantie = fields.Float(string="Taux de fonds d'autonomisation", required=False)

    #GS
    taux_int_annuel_gs = fields.Float(string="Taux d'intérêt annuel", required=False)
    taux_frais_dossier_gs = fields.Float(string="Taux frais de dossier", required=False)
    taux_garantie_gs = fields.Float(string="Taux de fonds d'autonomisation", required=False)

    #ASS/GR
    taux_int_annuel_ass = fields.Float(string="Taux d'intérêt annuel", required=False)
    taux_frais_dossier_ass = fields.Float(string="Taux frais de dossier", required=False)
    taux_garantie_ass = fields.Float(string="Taux de fonds d'autonomisation", required=False)

    montant_max_antenne = fields.Float(string='Montant max. antenne régionale', required=False, digits=(16, 0))
    montant_max_com_credit = fields.Float(string='Montant max. comité crédit', required=False, digits=(16, 0))
    montant_max_dg = fields.Float(string='Montant max. directrice', required=False, digits=(16, 0))

    #compte
    cpte_membr_ind = fields.Many2one(comodel_name='compta_plan_lines', string='Compte de principal', required=False)
    cpte_int_ind = fields.Many2one(comodel_name='compta_plan_lines', string='Compte de principal', required=False)

    cpte_membr_gs = fields.Many2one(comodel_name='compta_plan_lines', string='Compte de principal', required=False)
    cpte_int_gs = fields.Many2one(comodel_name='compta_plan_lines', string='Compte de principal', required=False)

    cpte_membr_ass = fields.Many2one('compta_plan_lines', string='Compte de principal', required=False)
    cpte_int_ass = fields.Many2one('compta_plan_lines', string='Compte de principal', required=False)

    cpte_frais = fields.Many2one(comodel_name='compta_plan_lines', string='Frais', required=False)
    cpte_penalite = fields.Many2one(comodel_name='compta_plan_lines', string='Pénalité', required=False)
    cpte_fa = fields.Many2one(comodel_name='compta_plan_lines', string='FA', required=False)
    capital = fields.Many2one(comodel_name='compta_plan_lines', string='Capital', required=False)

    active = fields.Boolean('Actif', default=True,)