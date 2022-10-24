from odoo import fields, models, api
from datetime import datetime, date


class HrEvaluation(models.Model):
    _name = "hr_evaluation"
    x_titre_id = fields.Many2one('hr_titreevaluation', string='Titre', required=True)
    # Identification de l’agent
    employee_id = fields.Many2one('hr.employee', string='Agent', required=True)
    contract_id = fields.Many2one("hr.contract", string="Contrat", required=True)
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie agent", required=True)
    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type agent", required=True)
    x_classees = fields.Char(string="Classe", readonly=True, force_save=True)
    x_categorie = fields.Char(string="Catégorie", readonly=True, force_save=True)
    x_echelle = fields.Char(string="Echelle", readonly=True, force_save=True)
    x_echellon = fields.Char(string="Echelon", readonly=True, force_save=True)
    x_service = fields.Char(string="Service", readonly=True, force_save=True)
    x_emploi = fields.Char(string="Emploi", readonly=True, force_save=True)
    x_fonction = fields.Char(string="Fonction", readonly=True, force_save=True)
    x_matricule = fields.Char(string="Mle Contractuel ", readonly=True, force_save=True)

    # dentification superieur
    employee_h_id = fields.Many2one('hr.employee', string='supérieur', required=True)
    contract_h_id = fields.Many2one("hr.contract", string="Contrat", required=True)
    x_categorie_employe_h_id = fields.Many2one("hr_catemp", string="Catégorie agent", required=True)
    x_type_employe_h_id = fields.Many2one("hr.payroll.structure", string="Type agent", required=True)
    x_classees_h = fields.Char(string="Classe", readonly=True, force_save=True)
    x_categorie_h = fields.Char(string="Catégorie", readonly=True, force_save=True)
    x_echelle_h = fields.Char(string="Echelle", readonly=True, force_save=True)
    x_echellon_h = fields.Char(string="Echelon", readonly=True, force_save=True)
    x_service_h = fields.Char(string="Service", readonly=True, force_save=True)
    x_emploi_h = fields.Char(string="Emploi", readonly=True, force_save=True)
    x_fonction_h = fields.Char(string="Fonction", readonly=True, force_save=True)
    x_matricule_h = fields.Char(string="Mle Contractuel ", readonly=True, force_save=True)

    x_sous_criteres_ids = fields.One2many(comodel_name='hr_sous_critere',
                                          inverse_name='x_evaluations_id',
                                          string=' sous criteres',
                                          required=False)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    observation_sup_imm = fields.Text()
    contrainte_realisation = fields.Text()
    point_divergence = fields.Text()
    observation_amelioration = fields.Text()

    def action_rechercher(self):
        if not self.x_categorie_employe_id:
            return
        elements = self.env["hr_sous_critere_evaluation"].search([
            ('x_categorie_employe_id', '=', self.x_categorie_employe_id.id)], order="crit_seq, sequence")
        x_lines_ids = []
        # delete old payslip lines
        self.x_sous_criteres_ids.unlink()
        for e in elements:
            x_lines_ids.append((0, 0,
                                {'x_critere': e.x_critere_evaluation_id.name, 'x_sous_critere': e.name,
                                 'born_sup': e.born_sup, 'born_inf': e.born_inf, 'x_note': e.born_inf,
                                 'crit_seq': e.crit_seq, 's_crit_seq': e.sequence,
                                 }))
        self.x_sous_criteres_ids = x_lines_ids

    def action_confrimer(self):
        pass

    @api.onchange("employee_id")
    def onchange_employee(self):
        if not self.employee_id:
            return
        self.contract_id = self.env["hr.contract"].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'open')])

    @api.onchange("contract_id")
    def onchange_contract(self):
        if not self.contract_id:
            self.vider()
            return
        self.x_categorie_employe_id = self.contract_id.x_categorie_employe_id
        self.x_type_employe_id = self.contract_id.struct_id
        self.x_service = self.contract_id.hr_service.name
        self.x_emploi = self.contract_id.x_emploi_id.name
        self.x_fonction = self.contract_id.x_fonction_id.name
        self.x_matricule = self.employee_id.matricule
        if self.x_type_employe_id.code == 'FCT_MD':
            self.x_classees = self.contract_id.x_classees_id.name
            self.x_categorie = self.contract_id.x_categorie_id.name
            self.x_echelle = self.contract_id.x_echelle_id.name
            self.x_echellon = self.contract_id.x_echellon_id.name
        if self.x_type_employe_id.code in ('CTRCT', 'FCT_DETACH'):
            self.x_categorie = self.contract_id.x_categorie_c_id.name
            self.x_echelle = self.contract_id.x_echelle_c_id.name
            self.x_echellon = self.contract_id.x_echellon_c_id.name

    @api.onchange("employee_h_id")
    def onchange_employee_h(self):
        self.contract_h_id = []
        if not self.employee_h_id:
            return
        self.contract_h_id = self.env["hr.contract"].search([
            ('employee_id', '=', self.employee_h_id.id),
            ('state', '=', 'open')])

    @api.onchange("contract_h_id")
    def onchange_contract_h(self):
        if not self.contract_h_id:
            self.vider_h()
            return
        self.x_categorie_employe_h_id = self.contract_h_id.x_categorie_employe_id
        self.x_type_employe_h_id = self.contract_h_id.struct_id
        self.x_service_h = self.contract_h_id.hr_service.name
        self.x_emploi_h = self.contract_h_id.x_emploi_id.name
        self.x_fonction_h = self.contract_h_id.x_fonction_id.name
        self.x_matricule_h = self.employee_h_id.matricule
        if self.x_type_employe_h_id.code == 'FCT_MD':
            self.x_classees_h = self.contract_h_id.x_classees_id.name
            self.x_categorie_h = self.contract_h_id.x_categorie_id.name
            self.x_echelle_h = self.contract_h_id.x_echelle_id.name
            self.x_echellon_h = self.contract_h_id.x_echellon_id.name
        if self.x_type_employe_h_id.code in ('CTRCT', 'FCT_DETACH'):
            self.x_categorie_h = self.contract_h_id.x_categorie_c_id.name
            self.x_echelle_h = self.contract_h_id.x_echelle_c_id.name
            self.x_echellon_h = self.contract_h_id.x_echellon_c_id.name

    def vider(self):
        self.x_categorie_employe_id = []
        self.x_type_employe_id = []
        self.x_service = ''
        self.x_emploi = ''
        self.x_fonction = ''
        self.x_matricule = ''
        self.x_classees = ''
        self.x_categorie = ''
        self.x_echelle = ''
        self.x_echellon = ''

    def vider_h(self):
        self.x_categorie_employe_h_id = []
        self.x_type_employe_h_id = []
        self.x_service_h = ''
        self.x_emploi_h = ''
        self.x_fonction_h = ''
        self.x_matricule_h = ''
        self.x_classees_h = ''
        self.x_categorie_h = ''
        self.x_echelle_h = ''
        self.x_echellon_h = ''


class HrSousCritere(models.Model):
    _name = 'hr_sous_critere'
    # name = fields.Char(string="Libellé", required=True)
    x_critere = fields.Char(string="Critère",)
    x_sous_critere = fields.Char(string="Sous Critère",)
    born_sup = fields.Integer(string="Borne supérieure",)
    born_inf = fields.Integer(string="Borne inférieure",)
    crit_seq = fields.Integer(string='Crit_seq')
    s_crit_seq = fields.Integer(string='Crit_seq')
    x_note = fields.Integer(string="Note", required=True)

    x_evaluations_id = fields.Many2one(comodel_name='hr_evaluation', string='', required=False)


# classe de la fiche d'attente
class HrFicheAttente(models.Model):
    _name = 'hr_ficheattente'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of ministere.", default=10)

    name = fields.Many2one('hr.employee', string='Employé', required=True)
    x_drh_id = fields.Many2one('hr.employee', string='DRH', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_op = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_ficheattente_line', 'name', string='Liste Des Objectifs',
                                 states={'A': [('readonly', True)]})
    active = fields.Boolean(string="Etat", default=True)
    fichier_joint = fields.Binary(string="Joindre Contrat d'objectif", attachment=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Soumettre'),
        ('NV', 'Annuler'),
        ('C', 'Valider'),
        ('NC', 'Rejetter'),
        ('A', 'Approuver'),
        ('NA', 'Rejetter'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_non_valider(self):
        self.write({'state': 'NV'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_non_confirmer(self):
        self.write({'state': 'NC'})

    def action_appr(self):
        self.write({'state': 'A'})

    def action_non_appr(self):
        self.write({'state': 'NA'})

# classe de la fiche d'attente line
class HrFicheAttenteLine(models.Model):
    _name = 'hr_ficheattente_line'
    name = fields.Many2one('hr_ficheattente')
    objectif = fields.Text(string='Objectifs')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)