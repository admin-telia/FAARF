from odoo import fields, models, api

#classe type formation
class TypeFormation(models.Model):
    _name = 'hr_type_formation'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of formation.", default=10)
    name = fields.Char(string = "Libéllé court", required = True)
    lib_long = fields.Char(string = "Libellé long", size = 35, required = True)
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string = "Etat", default=True)

#classe type session
class TypeSession(models.Model):
    _name = 'hr_type_session'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string = "Libéllé court", required = True)
    lib_long = fields.Char(string = "Libellé long", size = 35, required = True)
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string = "Etat", default=True)

# Formation
class HrThemeForm(models.Model):
    _name = "hr_theme"
    _order = 'sequence, id'
    _rec_name = 'lib_long'
    sequence = fields.Integer(help="", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_domaine_id = fields.Many2one(comodel_name='hr_domaine', string='Domaine', required=False)
    active = fields.Boolean(string="Etat", default=True)

#classe mode de paiement
class HrModePaiement(models.Model):
    _name = 'hr_modepaiement'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string = "Libéllé court", required = True)
    lib_long = fields.Char(string = "Libellé long", size = 35, required = True)
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string = "Etat", default=True)

#classe etablissement des stagiaires
class HrEtablissement(models.Model):
    _name = 'hr_etablsmt'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string = "Libéllé court", required = True)
    lib_long = fields.Char(string = "Libellé long", required = True)
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string = "Etat", default=True)

#Evaluation

class HrCritereEvalaution(models.Model):
    _name = "hr_critere_evaluation"
    _order = 'sequence, id'
    name = fields.Char(string="Libellé", required=True)
    sequence = fields.Integer(help="", required=True)
    active = fields.Boolean(string="Etat", default=True)
    description = fields.Text(string="Description", size="1000")

class HrSousCritereEvaluation(models.Model):
    _name = 'hr_sous_critere_evaluation'
    _order = 'crit_seq, sequence'
    sequence = fields.Integer(help="", required=True)
    name = fields.Char(string="Libellé", required=True)
    born_sup = fields.Char(string="Borne supérieure", required=True)
    born_inf = fields.Char(string="Borne inférieure", required=True)
    crit_seq = fields.Integer(string='Crit_seq', related='x_critere_evaluation_id.sequence', store=True)
    x_critere_evaluation_id = fields.Many2one('hr_critere_evaluation', string='Critère', required=True)
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)

# Creation de la classe titre avec ses attributs
class HrTitreEvaluation(models.Model):
    _name = "hr_titreevaluation"
    _order = 'sequence, id'
    _rec_name = 'lib_long'
    sequence = fields.Integer(help="", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
