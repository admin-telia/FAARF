from datetime import datetime, date
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class HrSaisieInformation(models.Model):
    _name = "hr_saisie_infos"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    _rec_name = 'employee_id'
    name = fields.Char(string='Code stage', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Choisir Employé', required=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_mnts = fields.Float(string='Coût')
    x_service_id = fields.Integer(string='id')
    service = fields.Char(string='Service', readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_eng = fields.Date(string="Date opération", default=date.today(), readonly=True)
    domaine_id = fields.Many2one('hr_domaine', string='Domaine', required=True)
    type_stage_id = fields.Many2one('hr_type_stage', string='Type stage', required=True)
    organisme_id = fields.Many2one('hr_organisme', string='Organisme', required=True)
    lieu_id = fields.Many2one('hr_lieu', string='Lieu', required=True)
    x_date_debut = fields.Date('Date debut', required=True)
    x_date_fin = fields.Date('Date fin', required=True)
    observations = fields.Text('Observations')
    active = fields.Boolean(string="Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Annuler'),
        ('R', 'Reporter'),
        ('CL', 'Clôturer'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    x_date_debut_report = fields.Date(string='Date debut report')
    x_date_fin_report = fields.Date(string='Date fin report')
    x_line_ids = fields.One2many('hr_frais', 'x_stage_id', string="Frais Annexes")
    fichier_joint = fields.Binary(string='Joindre Fichier(pdf,word,etc.)', attachment=True)

    @api.constrains('x_date_debut', 'x_date_fin', 'x_mnts')
    def CtrlDate(self):
        for val in self:
            if val.x_date_debut > val.x_date_fin or val.x_mnts < 0:
                raise ValidationError(
                    _("Enregistrement impossible. La date de début doit être inférieure à la date de fin ou le "
                      "montant ne peut pas être à zéro"))

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_annuler(self):
        self.write({'state': 'A'})

    def action_reporter(self):
        self.write({'state': 'R'})

    def action_cloturer(self):
        self.write({'state': 'CL'})
        ddbut = str(self.x_date_debut.strftime("%Y-%m-%d"))
        ddfin = str(self.x_date_fin.strftime("%Y-%m-%d"))
        x_struct_id = int(self.company_id)
        val_id = int(self.id)
        self.env.cr.execute(
            """UPDATE hr_saisie_infos SET x_date_debut_report = %s, x_date_fin_report = %s WHERE company_id = %s and id = %s""",
            (ddbut, ddfin, x_struct_id, val_id))

    @api.onchange('employee_id')
    def remplir_service(self):
        if self.employee_id:
            self.x_service_id = self.employee_id.hr_service.id
            self.service = self.employee_id.hr_service.name


class HrFraisAnnexes(models.Model):
    _name = 'hr_frais'
    x_stage_id = fields.Many2one('hr_saisie_infos')
    obj = fields.Char(string='Objet', required=True)
    mnt_annex = fields.Integer('Montant', required=True)
    observation = fields.Text('Observations')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# classe de saisie des informations sur le stagiaire interne
class HrSaisieInformationStage(models.Model):
    _name = "hr_saisie_infos_stage"
    _order = 'sequence, id'
    _rec_name = 'nom_stagiaire'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    name = fields.Char(string='Code stage', readonly=True, states={'CL': [('readonly', True)]})
    nom_stagiaire = fields.Char(string='Nom', required=True, states={'CL': [('readonly', True)]})
    prenom_stagiaire = fields.Char(string='Prénom(s)', required=True, states={'CL': [('readonly', True)]})
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    states={'CL': [('readonly', True)]})
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 states={'CL': [('readonly', True)]})
    x_service_id = fields.Many2one('hr_service', string='Service', states={'CL': [('readonly', True)]})
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user,
                                   states={'CL': [('readonly', True)]})
    date_eng = fields.Date(string="Date opération", default=date.today(), readonly=True)
    domaine_id = fields.Many2one('hr_domaine', string='Domaine', required=True, states={'CL': [('readonly', True)]})
    type_stage_id = fields.Many2one('hr_type_stage', string='Type stage', required=True,
                                    states={'CL': [('readonly', True)]})
    sexe = fields.Selection([
        ('masculin', 'Masculin'),
        ('feminin', 'Feminin'),
    ], 'Sexe', default='masculin', states={'CL': [('readonly', True)]})

    maitre_sage_id = fields.Many2one('hr.employee', string='Maitre de stage', required=True,
                                     states={'CL': [('readonly', True)]})
    nom_dm = fields.Char('Nom DM', states={'CL': [('readonly', True)]})
    # etb = fields.Many2one('hr_etablsmt', string='Etablissement', states={'CL': [('readonly', True)]})
    nationalite = fields.Many2one('ref_nationalite', string='Nationalité', states={'CL': [('readonly', True)]})
    date_naissance = fields.Date('Date de naissance', required=True, states={'CL': [('readonly', True)]})
    tel = fields.Char(string='Telephone', states={'CL': [('readonly', True)]})
    mail = fields.Char(string='Email', states={'CL': [('readonly', True)]})
    etblsment = fields.Char(string='Etablissement', states={'CL': [('readonly', True)]})
    diplome = fields.Many2one('hr_diplome', string='Diplôme', states={'CL': [('readonly', True)]})
    situation_id = fields.Many2one('hr_situationfamille', string='Situation de famille',
                                   states={'CL': [('readonly', True)]})
    x_date_debut = fields.Date('Date debut', required=True, states={'CL': [('readonly', True)]})
    x_date_fin = fields.Date('Date fin', required=True, states={'CL': [('readonly', True)]})
    observations = fields.Text('Observations', states={'CL': [('readonly', True)]})
    theme = fields.Char('Thème', states={'CL': [('readonly', True)]})
    active = fields.Boolean(string="Etat", default=True, states={'CL': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Annuler'),
        ('R', 'Reporter'),
        ('CL', 'Clôturer'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    x_line_d_ids = fields.One2many('hr_demandestage', 'x_stage_interne_id', string="Liste des demandes de stage",
                                   states={'CL': [('readonly', True)]})
    x_line_a_ids = fields.One2many('hr_autorisationstage', 'x_stage_interne_id',
                                   string="Liste des autorisations de stage", states={'CL': [('readonly', True)]})

    x_titre = fields.Char(string='Titre', default='ATTESTATION DE STAGE', states={'CL': [('readonly', True)]})
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ', states={'CL': [('readonly', True)]})
    p2 = fields.Char(string='Phrase 2', default='atteste que M./Mme/Mlle', states={'CL': [('readonly', True)]})
    p3 = fields.Char(string='Phrase 3', default='a effectué un stage au  ', states={'CL': [('readonly', True)]})
    p4 = fields.Char(string='Phrase 4', default='durant la période du ', states={'CL': [('readonly', True)]})
    p5 = fields.Char(string='Phrase 5', default='Au ', states={'CL': [('readonly', True)]})
    p6 = fields.Char(string='Phrase 6', default='sur le thème ', states={'CL': [('readonly', True)]})
    p7 = fields.Char(string='Phrase 7',
                     default='En foi de quoi, la présente attestation lui est délivrée pour servir et valoir ce que de droit',
                     states={'CL': [('readonly', True)]})
    responsale = fields.Many2one('hr.employee', string='Responsable', states={'CL': [('readonly', True)]})
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', states={'CL': [('readonly', True)]})
    date_attest = fields.Date(string="Date", default=date.today())
    fichier_joint = fields.Binary(string='Joindre Rapport stage(fichier pdf,word,etc.)', attachment=True,
                                  states={'CL': [('readonly', True)]})
    fichier_joint_fic = fields.Binary(string="Joindre Fiche d'evaluation(fichier pdf,word,etc.)", attachment=True,
                                      states={'CL': [('readonly', True)]})

    @api.constrains('x_date_debut', 'x_date_limite')
    def CtrlDate(self):

        for val in self:
            if val.x_date_debut > val.x_date_fin:
                raise ValidationError(
                    _("Enregistrement impossible. La date de début doit être inférieure à la date de fin."))

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_annuler(self):
        self.write({'state': 'A'})

    def action_reporter(self):
        self.write({'state': 'R'})

    def action_cloturer(self):
        self.write({'state': 'CL'})


# class permettant de mettre en place les demande de stage
class HrDemandeStage(models.Model):
    _name = "hr_demandestage"
    x_stage_interne_id = fields.Many2one('hr_saisie_infos_stage')
    name = fields.Char(string='Objet', required=True)
    fichier_joint = fields.Binary(string='Pièce jointe', attachment=True, required=True)
    date_op = fields.Datetime('Date Opération', default=datetime.today(), readonly=True)


# class permettant de mettre en place les autorisations de stage
class HrAutorisationStage(models.Model):
    _name = "hr_autorisationstage"
    x_stage_interne_id = fields.Many2one('hr_saisie_infos_stage')
    name = fields.Char(string='Objet', required=True)
    fichier_joint = fields.Binary(string='Pièce jointe', attachment=True, required=True)
    date_op = fields.Datetime('Date Opération', default=datetime.today(), readonly=True)
