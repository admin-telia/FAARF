from odoo import fields, models, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


# classe  plan recrutement
class HrPlanRecrutement(models.Model):
    _name = 'hr_plan_recrutement'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of ministere.", default=10)
    name = fields.Char(string="Code", readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_plan = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_plan_recrutement_line', 'x_plan_id', string='Liste Des Compétences',
                                 states={'A': [('readonly', True)]})
    # x_line_p_ids = fields.One2many('hr_autorisationrecrut','x_recrut_id', string = 'Autorisation Recrutement')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('Ap', 'Approuver'),
        ('Ann', 'Annuler'),
        ('E', "En cours d'\'exécution"),
        ('ET', 'Exécution terminée'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    code = fields.Char(string='Code', default='DELIBERATION N°2017-019 /FNPSL/CA')
    p1 = fields.Char(string='Phrase 1',
                     default="Portant autorisation de recrutement de deux (02) chauffeurs pour le compte du Fonds national pour la promotion du sport et des loisirs")
    p2 = fields.Char(string='Phrase 2', default='LE CONSEIL D’ADMINISTRATION')
    espace = fields.Char(string='Pointillé', default='----------------------')
    visa = fields.Text('Visa')
    fichier_joint = fields.Binary(string="Joindre demande d'autorisation", attachment=True)

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select name from hr_param_visa where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        self.visa = lo and lo[0] or 0
        self.write({'state': 'V'})

    def action_confirmer(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select no_code from hr_cpte_plan_gpec where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'PGPEC' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_plan_gpec(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # Plan gpec
            self.name = 'PGPEC' + '/' + ok
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_cpte_plan_gpec SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'C'})

    def action_appr(self):
        self.write({'state': 'Ap'})

    def action_ann(self):
        self.write({'state': 'Ann'})

    def action_en_cours_exe(self):
        self.write({'state': 'E'})

    def action_exe_term(self):
        for record in self.x_line_ids:
            if record.etat == True:
                self.write({'state': 'ET'})
            else:
                raise ValidationError(
                    _("Bien vouloir vérifier que toutes les recrutements ont été exécutés avant de terminer l'\'exécution svp"))


# classe  PLAN line recrutement
class HrPlanRecrutementLine(models.Model):
    _name = 'hr_plan_recrutement_line'
    _order = 'sequence, id'
    _rec_name = 'x_emploi_id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of plan.", default=10)
    x_plan_id = fields.Many2one('hr_plan_recrutement')
    name = fields.Char('code')
    direction_id = fields.Many2one('ref_direction', string='Direction')
    x_service_id = fields.Many2one('ref_service', string='Service')
    x_emploi_id = fields.Many2one('hr_previsioncompetences_line', string='Emploi')
    x_diplome = fields.Char(string='Diplôme', readonly=True)
    x_nb_poste = fields.Integer(string='Nbre Poste')
    x_experience = fields.Text(string='Expériences réquises')
    x_competence = fields.Text(string='Compétences réquises')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    etat = fields.Boolean('Exécuté', default=False)

    @api.onchange('x_emploi_id')
    def remplir_liste(self):
        self.x_diplome = self.x_emploi_id.x_diplome_id.name
        self.x_nb_poste = self.x_emploi_id.nbre_employe
        self.x_experience = self.x_emploi_id.x_experience
        self.x_competence = self.x_emploi_id.competences
        self.company_id = self.x_emploi_id.company_id
        self.x_exercice_id = self.x_emploi_id.x_exercice_id


class PrevisionCompetences(models.Model):
    _name = "hr_previsioncompetences"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of type previsions.", default=10)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    name = fields.Char('Code', readonly=True)
    date_enreg = fields.Datetime(string='Date', default=datetime.today(), readonly=True)
    x_lines_ids = fields.One2many('hr_previsioncompetences_line', 'prevision_id',
                                  string='Ajouter les compétences réquises ')
    x_direction_id = fields.Many2one("ref_direction", string="Direction", required=True)
    x_service_id = fields.Many2one('ref_service', string='Service', required=True)
    x_observation = fields.Text('Observations')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('C', 'Confirmé'),
        ('Ap', 'Approuvé'),
        ('An', 'Annulé'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_eng_confirmer(self):
        x_struct_id = int(self.company_id)

        self.env.cr.execute("select no_code from hr_cpte_gpec where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'BRA' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_gpec(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # BESOIN RECRUTEMENT ANNUEL
            self.name = 'BRA' + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE hr_cpte_gpec SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'C'})

    def action_eng_approuver(self):
        self.write({'state': 'Ap'})

    def action_eng_annuler(self):
        self.write({'state': 'An'})


class PrevisionCompetenceLines(models.Model):
    _name = "hr_previsioncompetences_line"
    prevision_id = fields.Many2one('hr_previsioncompetences')
    _rec_name = 'x_emploi_id'
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_diplome_id = fields.Many2one('hr_diplome', string='Diplôme', required=True)
    x_experience = fields.Text(string='Expériences réquises', required=True)
    competences = fields.Text(string='Compétences', required=True)
    nbre_employe = fields.Integer(string='Nombre de poste à pourvoir')
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)


# Classe pour gerer le compteur pour l'EXPRESSION des besoins gpec
class Compteur_Besoins_gpec(models.Model):
    _name = "hr_cpte_gpec"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# Class pour gerer la centralisation des besoins en gpec de chaque service de chaque EPE
class HrCentralisationBesoinGPEC(models.Model):
    _name = "hr_central_gpec"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins gpec.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string="Code", size=50, readonly=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année',
                                     default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_central_gpec_line', 'x_besoin_central_id',
                                 string='Liste Des emplois et compétences', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('F', 'Fait'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_centralisation = fields.Date(string="Date", default=date.today())
    service_traiteur = fields.Char(string='Service Traiteur', readonly=True)

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # fonction de remplissage du tableau
    def centraliser(self):
        if self.annee_en_cours:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            for vals in self:
                vals.env.cr.execute(
                    """select (E.name) as emploi,(D.name) as diplome, (L.competences) as competence, (L.x_experience) as experience,(L.nbre_employe) as nbre,(P.x_direction_id) as id_direction,(P.x_service_id) as id_service,(L.x_emploi_id) as id_emploi,(L.x_diplome_id) as id_diplome, (DR.name) as direction, (S.name) as service from hr_previsioncompetences_line L, hr_emploi E, hr_diplome D, hr_previsioncompetences P, ref_direction DR, ref_service S where L.prevision_id = P.id and L.x_diplome_id = D.id and L.x_emploi_id = E.id and P.x_direction_id = DR.id and P.x_service_id = S.id and L.company_id = %d and L.x_exercice_id = %d and P.state = 'Ap' """ % (
                        x_struct_id, annee))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'direction_id': line['id_direction'], 'direction': line['direction'],
                                          'x_service_id': line['id_service'], 'x_service': line['service'],
                                          'x_emploi_id': line['id_emploi'], 'x_emploi': line['emploi'],
                                          'x_diplome_id': line['id_diplome'], 'x_diplome': line['diplome'],
                                          'x_nb_poste': line['nbre'], 'x_experience': line['experience'],
                                          'x_competence': line['competence']}))
                self.x_line_ids = result

            x_user_id = int(self.current_user)
            self.env.cr.execute(
                """select (R.id) AS id, (R.name) AS service, (R.code) AS code From ref_service R, res_users U where R.id = U.x_service_id and U.id = %s and U.company_id = %s""",
                (x_user_id, x_struct_id))
            rows = self.env.cr.dictfetchall()
            self.service_traiteur = rows and rows[0]['service']

            self.env.cr.execute("select no_code from hr_cpte_central_gpec where company_id = %d" % (x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'CGPEC' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO hr_cpte_central_gpec(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
            else:

                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                self.name = 'CGPEC' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE hr_cpte_central_gpec SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'F'})


# class pour gerer les lignes de centralisation des besoins gpec annuels en emploi et competence
class HrCentralisationBesoinGPECLine(models.Model):
    _name = "hr_central_gpec_line"
    x_besoin_central_id = fields.Many2one('hr_central_gpec')
    direction_id = fields.Integer(string='Id direction')
    direction = fields.Char(string='Direction', readonly=True)
    x_service_id = fields.Integer(string='id_Service')
    x_service = fields.Char(string='Service')
    x_emploi_id = fields.Integer(string='id_emploi')
    x_emploi = fields.Char(string='Emploi')
    x_diplome_id = fields.Integer(string='id diplome', readonly=True)
    x_diplome = fields.Char(string='Diplôme', readonly=True)
    x_nb_poste = fields.Integer(string='Nbre Poste')
    x_experience = fields.Text(string='Expériences réquises')
    x_competence = fields.Text(string='Compétences réquises')


# Classe pour gerer le compteur pour la centralisation des besoins gpec annuels
class Compteur_Central_gpec(models.Model):
    _name = "hr_cpte_central_gpec"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe de consultation des plans de recrutement adoptés
class HrConsultationPlanRecrutement(models.Model):
    _name = "hr_consultation_plan_recrutement"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of consultation.", default=10)
    name = fields.Char(string="Code", readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Choisir l'\'année")
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_consult_plan = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_consultation_plan_recrutement_line', 'x_plan_consult_id',
                                 string='Liste Des Compétences', readonly=True)

    # fonction de remplissage du tableau
    def remplissage(self):
        if self.x_exercice_id:
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)
            for vals in self:
                vals.env.cr.execute(
                    """select (D.name) as direction,(S.name) as service,(E.name) as emploi,(L.x_diplome) as diplome,(L.x_nb_poste) as nbre,(L.x_experience) as experience,(L.x_competence) as competence,(P.name) as code,(P.state) as etat  from hr_plan_recrutement_line L, ref_direction D, ref_service S, hr_emploi E, hr_plan_recrutement P, hr_previsioncompetences_line PL where P.id = L.x_plan_id  and L.direction_id = D.id and L.x_service_id = S.id and L.x_emploi_id = PL.id AND PL.x_emploi_id = E.id AND P.state = 'ET' and P.company_id = %d and P.x_exercice_id = %d""" % (
                        x_struct_id, x_exo_id))
                rows = vals.env.cr.dictfetchall()
                result = []
                # vals.name = rows and rows['code']
                # print('code',rows and rows['code'])
                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'direction': line['direction'], 'x_service': line['service'],
                                          'x_emploi': line['emploi'], 'x_diplome': line['diplome'],
                                          'x_nb_poste': line['nbre'], 'x_experience': line['experience'],
                                          'x_competence': line['competence'], 'x_etat': line['etat']}))
                self.x_line_ids = result


# class permettant de recueillir les lignes de la requête
class HrConsultationPlanRecrutementLine(models.Model):
    _name = "hr_consultation_plan_recrutement_line"
    x_plan_consult_id = fields.Many2one('hr_consultation_plan_recrutement')

    direction = fields.Char(string='Direction')
    x_service = fields.Char(string='Service')
    x_emploi = fields.Char(string='Emploi')
    x_diplome = fields.Char(string='Diplôme')
    x_nb_poste = fields.Integer(string='Nbre Poste')
    x_experience = fields.Text(string='Expériences réquises')
    x_competence = fields.Text(string='Compétences réquises')
    x_etat = fields.Char(string='Etat')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# Classe d'avis de recrutement
class HrAvisRecrutement(models.Model):
    _name = 'hr_avis_recrutement'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of avis de recrutement.", default=10)

    name = fields.Char(string='Code', readonly=True)
    x_ordonnateur_id = fields.Many2one('ref_service', string='Ordonnateur', required=True)
    x_libelle_avis = fields.Char(string='Libellé Avis', required=True)
    x_diplome_id = fields.Many2one('hr_diplome', string='Diplôme', required=True)
    x_profil_id = fields.Many2one('hr_emploi', string='Profil', required=True)
    x_context = fields.Text(string='Contexte', required=True)
    x_mission = fields.Text(string='Mission', required=True)
    x_condition = fields.Text(string='Condition', required=True)
    x_date_debut = fields.Date('Date debut', required=True)
    x_date_limite = fields.Date('Date limite', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_enreg = fields.Date(string="Date Opération", default=date.today())
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Approuver'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Fonction pour contrôler les dates
    @api.constrains('x_date_debut', 'x_date_limite')
    def CtrlDate(self):
        for val in self:
            if val.x_date_debut > val.x_date_limite:
                raise ValidationError(
                    _("Enregistrement impossible. La date de début doit être inférieure à la date de limite."))

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select no_code from hr_cpte_avis where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'AVIS' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_avis(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # Plan gpec
            self.name = 'AVIS' + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE hr_cpte_avis SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'C'})

    def action_appr(self):
        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # Classe pour gerer le compteur pour les avis de recrutement


class Compteur_avis(models.Model):
    _name = "hr_cpte_avis"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe pour gerer les candidats
class HrCandidat(models.Model):
    _name = 'hr_candidat'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char('Code', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année en cours', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_candidat_line', 'name', string='Ajout Des Candidats')
    x_line_c_ids = fields.One2many('hr_correcteur_line', 'name', string='Ajout Des Correcteurs')
    x_line_n_ids = fields.One2many('hr_note_line', 'name', string='Ajout Des Notes')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Approuver'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select no_code from hr_cpte_listecandidat where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'LIST' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_listecandidat(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # Plan gpec
            self.name = 'LIST' + '/' + ok
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_cpte_listecandidat SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'C'})

    def action_appr(self):
        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # classe pour ajouter les candidats automatiquement


class HrCandidatLine(models.Model):
    _name = 'hr_candidat_line'

    # fonction de concatenation du nom et prenom
    @api.onchange('x_nom', 'x_prenom')
    def _concat(self):
        for tests in self:
            tests.concat_fields = (tests.x_nom or '') + ' ' + (tests.x_prenom or '')

    name = fields.Many2one('hr_candidat')
    _rec_name = 'concat_fields'
    concat_fields = fields.Char()

    x_emploi_id = fields.Many2one('hr_emploi', string='Poste', required=True)
    x_civilite = fields.Selection([
        ('monsieur', "Monsieur"),
        ('madame', "Madame"),
        ('mademoiselle', "Mademoiselle"),
    ], required=True, string="Civilité")
    x_nom = fields.Char(string='Nom', required=True)
    x_prenom = fields.Char(string='Prenom(s)', required=True)
    x_nom_jeune_fille = fields.Char(string='Nom jeune fille')
    x_date_naiss = fields.Date(string='Date de naissance', required=True)
    x_lieu_naiss = fields.Many2one('ref_localite', string='Lieu de naissance', required=True)
    type = fields.Selection([
        ('cnib', 'CNIB'),
        ('passport', 'PASSPORT'),
        ('autre', 'Autre')
    ], string='Type Pièce', default="cnib", required=True)
    date_delivrance = fields.Date(string="Date Delivrance", required=True)
    lieu_delivrance = fields.Many2one('ref_localite', string="Lieu Délivrance", required=True)

    x_cnib = fields.Char(string='N° Pièce', required=True)
    x_nationalite_id = fields.Many2one('ref_nationalite', string='Nationalité', required=True)
    x_tel = fields.Char(string='Télephone', required=True)
    x_email = fields.Char(string='Email')
    x_rue = fields.Char(string='Rue')
    x_secteur = fields.Many2one('hr_secteur', string='Secteur')
    x_ville = fields.Many2one('hr_ville', string='Ville')
    x_boite_p = fields.Char(string='Boite Postale')
    x_diplome_id = fields.Many2one('hr_diplome', string='Diplôme', required=True)
    x_num_dossier = fields.Char(string='N° Dossier')
    x_experience = fields.Char(string='Expérience')
    x_langue = fields.Many2one('hr_langue', string='Langue')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# classe pour ajouter les correcteurs des candidats
class HrCorrecteurLine(models.Model):
    _name = 'hr_correcteur_line'

    # fonction de concatenation du nom et prenom
    @api.onchange('x_nom', 'x_prenom')
    def _concat(self):
        for tests in self:
            tests.concat_fields = (tests.x_nom or '') + ' ' + (tests.x_prenom or '')

    name = fields.Many2one('hr_candidat')
    _rec_name = 'concat_fields'
    concat_fields = fields.Char()

    x_emploi_id = fields.Many2one('hr_emploi', string='Poste', required=True)
    x_civilite = fields.Selection([
        ('monsieur', "Monsieur"),
        ('madame', "Madame"),
        ('mademoiselle', "Mademoiselle"),
    ], required=True, string="Civilité")
    x_nom = fields.Char(string='Nom', required=True)
    x_prenom = fields.Char(string='Prenom(s)', required=True)
    x_nom_jeune_fille = fields.Char(string='Nom jeune fille')
    x_date_naiss = fields.Date(string='Date de naissance', required=True)
    x_lieu_naiss = fields.Many2one('ref_localite', string='Lieu de naissance', required=True)
    x_nationalite_id = fields.Many2one('ref_nationalite', string='Nationalité', required=True)
    x_tel = fields.Char(string='Télephone', required=True)
    x_email = fields.Char(string='Email')
    x_rue = fields.Char(string='Rue')
    x_secteur = fields.Many2one('hr_secteur', string='Secteur')
    x_ville = fields.Many2one('hr_ville', string='Ville')
    x_boite_p = fields.Char(string='Boite Postale')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# classe pour ajouter les notes des candidats
class HrNoteLine(models.Model):
    _name = 'hr_note_line'

    name = fields.Many2one('hr_candidat')

    x_emploi_id = fields.Many2one('hr_emploi', string='Poste', required=True)
    x_correcteur_id = fields.Many2one('hr_correcteur_line', string='Correcteur', required=True)
    x_candidat_id = fields.Many2one('hr_candidat_line', string='Candidat', required=True)
    x_note = fields.Float(string='Note')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# Classe pour gerer le compteur pour les mise à jour des candidats
class Compteur_candidat(models.Model):
    _name = "hr_cpte_listecandidat"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe pour gerer les cv et lettre
class HrCvLettre(models.Model):
    _name = 'hr_cv_candidat'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    _rec_name = 'x_candidat_id'
    name = fields.Char('Code', readonly=True)
    x_candidat_id = fields.Many2one('hr_candidat_line', string='Candidat', required=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Poste', required=True)

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année en cours', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_cv_candidat_line', 'name', string='Ajout Des Candidats')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)

# classe pour ajouter les cv et lettres
class HrCvLettreine(models.Model):
    _name = 'hr_cv_candidat_line'
    name = fields.Many2one('hr_cv_candidat')
    obj = fields.Char(string='Objet', required=True)
    fichier_joint = fields.Binary(string='Pièce jointe', attachment=True, required=True)

    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# classe pour ajouter les resultats des candidats
class HrResultats(models.Model):
    _name = 'hr_resultats'

    name = fields.Char('Code')
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)

    x_emploi_id = fields.Many2one('hr_plan_recrutement_line', string='Poste', required=True,
                                  states={'S': [('readonly', True)]})
    x_nbre_poste = fields.Integer(string='Nbre Poste', readonly=True)
    # x_lieu = fields.Many2one('hr_lieu', string = 'Lieu', required = True)
    x_diplome = fields.Char(string='Dipôme', readonly=True)
    x_line_ids = fields.One2many('hr_resultats_line', 'name', string='Resultats', states={'S': [('readonly', True)]})

    x_duree_contrat = fields.Char(string='Durée du contrat')
    x_struct_benef = fields.Char(string='Structure Bénéficiaire', readonly=True)
    x_service = fields.Char(string='Service Bénéficiaire', readonly=True)
    x_direction = fields.Char(string='Direction Bénéficiaire', readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('Ap', 'Approuver'),
        ('An', 'Annuler'),
        ('S', 'Contrat Signé'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select no_code from hr_cpte_resultcandidat where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'RES' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_resultcandidat(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # RESULTA n°
            self.name = 'RES' + '/' + ok
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_cpte_resultcandidat SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_appr(self):
        self.write({'state': 'Ap'})

    def action_ann(self):
        self.write({'state': 'An'})

    def action_contrat(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        x_emploi_id = int(self.x_emploi_id.x_emploi_id.x_emploi_id.id)

        x_struc_benef = str(self.x_struct_benef)
        x_direction = str(self.x_direction)
        x_service = str(self.x_service)

        for record in self.x_line_ids:
            x_noms = record.x_nom
            x_tele = record.x_tel
            x_result_id = int(record.x_resultat)
            if record.x_resultat == 1:
                record.env.cr.execute(
                    """UPDATE hr_resultats_line SET x_contrat_signe = 'Oui' WHERE x_resultat = 1 and company_id = %d and x_exercice_id = %d""" % (
                    x_struct_id, annee))
                # record.env.cr.execute("""INSERT INTO hr_employee(name,tel,resource_id, emergency_phone,x_categorie_employe_id,x_type_employe_id,x_fonction_id,x_zone_id,x_date_naissance,personne_id,ref_identification,x_mode_paiement,x_emploi_id,x_type_piece_id,resource_calendar_id,active,company_id,charge_femme,charge_enfant,x_solde_indiciaire_ctrct) VALUES(%s,%s,3,'',1,6,1,1,'2005-01-31',1,'','',1,1,1,'t',%s,0,0,0)""",(x_noms,x_tele,x_struct_id))
            else:
                record.env.cr.execute(
                    """UPDATE hr_resultats_line SET x_contrat_signe = 'Non' WHERE x_resultat = 2 and company_id = %d and x_exercice_id = %d""" % (
                    x_struct_id, annee))
        self.write({'state': 'S'})

    @api.onchange('x_emploi_id')
    def remplir_nbre(self):
        if self.x_emploi_id:
            self.x_nbre_poste = self.x_emploi_id.x_nb_poste
            self.x_diplome = self.x_emploi_id.x_diplome
            self.x_struct_benef = self.x_emploi_id.company_id.name
            self.x_direction = self.x_emploi_id.direction_id.name
            self.x_service = self.x_emploi_id.x_service_id.name

    # fonction de remplissage du tableau
    def remplissage(self):
        if self.x_emploi_id:
            emploi_id = int(self.x_emploi_id.x_emploi_id.x_emploi_id.id)
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            for vals in self:
                vals.env.cr.execute(
                    """select (C.x_nom || ' ' || C.x_prenom) as nom, (C.x_date_naiss) as date,(C.type) as type,(C.x_cnib) as cnib,(C.date_delivrance) as date, (C.x_tel) as tel from hr_candidat_line C where C.x_emploi_id = %d and C.company_id = %d and C.x_exercice_id = %d""" % (
                    emploi_id, x_struct_id, annee))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'x_nom': line['nom'], 'x_date_naiss': line['date'], 'type': line['type'],
                                          'x_cnib': line['cnib'], 'date_delivrance': line['date'],
                                          'x_tel': line['tel']}))
                self.x_line_ids = result

# classe pour ajouter les resultats des candidats en ligne
class HrResultatsLine(models.Model):
    _name = 'hr_resultats_line'

    name = fields.Many2one('hr_resultats')
    x_nom = fields.Char(string='Nom/Prénom(s)', readonly=True)
    x_date_naiss = fields.Date(string='Date de Naissance', readonly=True)
    type = fields.Char(string='Type Pièce', readonly=True)
    date_delivrance = fields.Date(string="Date Delivrance", readonly=True)
    lieu_delivrance = fields.Char(string="Lieu Délivrance", readonly=True)
    x_cnib = fields.Char(string='N° Pièce', readonly=True)
    x_tel = fields.Char(string='Télephone', readonly=True)
    x_observations = fields.Text(string='Observations')
    x_resultat = fields.Selection([
        ('1', 'Admis(e)'),
        ('2', 'Ajourné(e)'),
    ], string="Resultat", default=1)
    rang = fields.Selection([
        ('1', "1er"),
        ('2', "2è"),
        ('3', "3è"),
        ('4', "4è"),
        ('5', "5è"),
        ('6', "6è"),
        ('7', "7è"),
        ('8', "8è"),
        ('9', "9è"),
        ('10', "10è"),
        ('11', "11è"),
        ('12', "12è"),
        ('13', "13è"),
        ('14', "14è"),
        ('15', "15è"),
        ('16', "16è"),
    ], required=False, string='Rang', default=1)
    x_contrat_signe = fields.Char(string='Contrat Signé', readonly=True)
    fichier_joint = fields.Binary(string="Joindre décision d'engagement", attachment=True, required=True)

    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# Classe pour gerer le compteur pour les resultats des candidats
class Compteur_resultat_candidat(models.Model):
    _name = "hr_cpte_resultcandidat"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe secteur
class Hrsecteur(models.Model):
    _name = 'hr_secteur'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    code = fields.Char(string='Code', size=2, required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe ville
class Hrville(models.Model):
    _name = 'hr_ville'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    code = fields.Char(string='Code', size=2, required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe langue
class HrLangue(models.Model):
    _name = 'hr_langue'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    code = fields.Char(string='Code', size=2, required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

#classe pour parametrer les visas
class HrParametreVisa(models.Model):
     _name = 'hr_param_visa'
     _rec_name = 'company_id'
     name = fields.Text('Contenu', required = True)
     x_exercice_id = fields.Many2one('ref_exercice',string = "Année",required = True, default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), readonly=True)
     company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id, readonly = True)
     current_user = fields.Many2one('res.users','Utilisateur', default=lambda self: self.env.user)
     date_enreg = fields.Date(string = "Date Opération", default=date.today(), readonly= True)
     active = fields.Boolean(string = "Etat", default=True)