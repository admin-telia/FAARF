from odoo import fields, api, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from num2words import num2words


# classe type conge
class HrTypeConge(models.Model):
    _name = 'hr_typeconges'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe type d'absence
class HrTypeAbsence(models.Model):
    _name = 'hr_typeabsence'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe titre poste
class HrTitrePoste(models.Model):
    _name = 'hr_titreposte'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Class pour gerer les demandes de congé
class HrDemandeConge(models.Model):
    _name = "hr_demandeconge"
    _order = 'sequence, id'
    _rec_name = 'current_user'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of demande de conge.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    name = fields.Char(string="Code", size=50, readonly=True)
    x_type_conge_id = fields.Many2one('hr_typeconges', string='Type de congé', required=True,
                                      states={'A': [('readonly', True)], 'C': [('readonly', True)],
                                              'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_nbre_jours1 = fields.Integer(compute='_nombre_jours', string='Nombre Jours')
    nb_sous = fields.Integer(string='Jours non ouvrables', required=True,
                             states={'A': [('readonly', True)], 'C': [('readonly', True)], 'Re': [('readonly', True)],
                                     'An': [('readonly', True)]})

    x_nbre_jours = fields.Integer(string='Durée')
    x_date_debut = fields.Date('Date debut', required=True, default=date.today(),
                               states={'A': [('readonly', True)], 'C': [('readonly', True)],
                                       'An': [('readonly', True)]})
    x_date_fin = fields.Date('Date fin', required=True, default=date.today(),
                             states={'A': [('readonly', True)], 'C': [('readonly', True)], 'Re': [('readonly', True)],
                                     'An': [('readonly', True)]})
    observation = fields.Text('Observations', required=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année',
                                     default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('hr.employee', 'Bénéficiaire', required=True)
    date_op = fields.Date(string="Date", default=date.today())
    report = fields.Selection([
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ], 'Reporté', default='Non')
    x_date_debut_report = fields.Date('Date debut', states={'A': [('readonly', True)], 'C': [('readonly', True)],
                                                            'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_date_fin_report = fields.Date('Date fin', states={'A': [('readonly', True)], 'C': [('readonly', True)],
                                                        'Re': [('readonly', True)], 'An': [('readonly', True)]})
    raison_report = fields.Text(string='Raison', states={'A': [('readonly', True)], 'C': [('readonly', True)],
                                                         'Re': [('readonly', True)], 'An': [('readonly', True)]})
    reste = fields.Integer(string='Reste', readonly=True)
    reste_c_ad = fields.Integer(string='Reste CA', readonly=True)

    # fonction pour contrôler les dates (date de debut ne doit pas etre superieur à la date de fin)
    @api.constrains('x_date_debut', 'x_date_fin')
    def CtrlDate(self):

        for val in self:
            if val.x_date_debut > val.x_date_fin:
                raise ValidationError(_(
                    "Enregistrement impossible. La date de début  doit être toujours inférieure à la date de fin"))

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'En cours de traitement'),
        ('C', 'Confirmer par le chef de service'),
        ('Re', 'Rejeter par le chef de service'),
        ('A', 'Approuver par le Responsable'),
        ('An', 'Annuler par le responsable'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    x_titre = fields.Char(string='Titre', default="AUTORISATION DE CONGE",
                          states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p2 = fields.Char(string='Phrase 2', default='atteste que M./Mme/Mlle',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p3 = fields.Char(string='Phrase 3', default='au  ', states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p4 = fields.Char(string='Phrase 4', default='est autorisé(e) a jouir librement de ses congés du ',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p5 = fields.Char(string='Phrase 5', default='Au', states={'Re': [('readonly', True)]})
    p6 = fields.Char(string='Phrase 6',
                     default='En foi de quoi, la présente autorisation lui est délivrée pour servir et valoir ce que de droit',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    responsale = fields.Many2one('res.users', string='Responsable', readonly=False,
                                 states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_emploi = fields.Char(string='Emploi', readonly=True,
                           states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_fonction = fields.Many2one('hr_fonctionss', string='Fonction',
                                 states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_direction = fields.Char(string='Direction', readonly=True,
                              states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_service = fields.Char(string='Service', readonly=True,
                            states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    date_attest = fields.Date(string="Date", default=date.today(),
                              states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    active = fields.Boolean(string="Etat", default=True)
    observation = fields.Text(string='Observations', states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_date_debut_att = fields.Date('Date debut', readonly=False,
                                   states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_date_fin_att = fields.Date('Date fin', readonly=False,
                                 states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    fichier_joint = fields.Binary(string='Joindre Autorisation(fichier pdf,word,etc.)', attachment=True)
    fichier_interim_joint = fields.Binary(string='Joindre Note Interim(fichier pdf,word,etc.)', attachment=True)

    x_localite_id = fields.Many2one('ref_localite', string='Localité',
                                    states={'V': [('readonly', True)], 'Re': [('readonly', True)],
                                            'A': [('readonly', True)], 'C': [('readonly', True)],
                                            'An': [('readonly', True)]})
    x_a = fields.Char(string='A', default='A',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    x_destinateur = fields.Char(string='Destinateur', default="Monsieur, le Directeur Général De TelIa INFORMATIQUE",
                                states={'V': [('readonly', True)], 'Re': [('readonly', True)],
                                        'A': [('readonly', True)], 'C': [('readonly', True)],
                                        'An': [('readonly', True)]})
    date_oper = fields.Date(string="Date/Heure", default=date.today(),
                            states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                                    'C': [('readonly', True)], 'An': [('readonly', True)]})
    x_objet = fields.Char(string='Objet', default="Demande de congé annuel",
                          states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                                  'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_0 = fields.Char(string='Phrase 1', default='Monsieur, ',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_1 = fields.Char(string='Phrase 2', default="J'ai l'honneur de solliciter de votre haute bienveillance ",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_2 = fields.Char(string='Phrase 3', default="l'obtention de mon congé annuel partiel 2020 de deux(02) semaines.",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_3 = fields.Char(string='Phrase 4', default='Ce congé débutera le 16 Février et prendra fin le 02 mars 2020.',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_4 = fields.Char(string='Phrase 5',
                      default="Dans l'attente d'une suite favorable, Je vous prie d'agréer, Monsieur",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_5 = fields.Char(string='Phrase 6', default='le Directeur Général, mes sentiments les plus distingués.',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_6 = fields.Char(string='Phrase 7', default="L'intéressé",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'Employé', required=False)

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_nbre_jours1', 'nb_sous')
    def _nombre_jours_dure(self):
        for vals in self:
            if vals.x_nbre_jours1:
                vals.x_nbre_jours = vals.x_nbre_jours1 - vals.nb_sous

    # fonction de recuperation de la durée totale de la demande
    @api.onchange('x_date_debut', 'x_date_fin')
    def _nombre_jours(self):
        for vals in self:
            if vals.x_date_debut and vals.x_date_fin:
                vals.x_nbre_jours1 = 1 + (vals.x_date_fin - vals.x_date_debut).days

    # fonction de recuperation de la fonction
    @api.onchange('x_type_conge_id')
    def _fction(self):
        for vals in self:
            user_id = int(vals.current_user)
            vals.env.cr.execute(
                "select (S.name) as service,(Em.name) as emploi from hr_employee E, ref_service S, res_users U, hr_emploi Em where E.x_emploi_id = Em.id and E.user_id = U.id and S.id = U.x_service_id and E.id = %d" % (
                    user_id))
            rows = vals.env.cr.dictfetchall()
            vals.x_emploi = rows and rows[0]['emploi']
            vals.x_service = rows and rows[0]['service']

    # fonction de recherche du nombre de jour de congé restant pour l'employé en cours
    @api.onchange('x_type_conge_id', 'current_user')
    def _nbr_restant_conge(self):
        no_ex = int(self.x_exercice_id)
        if self.x_type_conge_id.name == "Congé annuel":
            for vals in self:
                # x_type_id = int(vals.x_type_conge_id)
                x_user_id = int(vals.current_user)
                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste = res and res[0] or 0
        elif self.x_type_conge_id.name == "Congé de maternité":
            for vals in self:
                # x_type_id = int(vals.x_type_conge_id)
                x_user_id = int(vals.current_user)
                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr_maternite) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste = res and res[0] or 0

                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste_c_ad = res and res[0] or 0

        elif self.x_type_conge_id.name == "Congé pour examens ou concours":
            for vals in self:
                # x_type_id = int(vals.x_type_conge_id)
                x_user_id = int(vals.current_user)
                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr_examen) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste = res and res[0] or 0

                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste_c_ad = res and res[0] or 0

        elif self.x_type_conge_id.name == "Congé de paternité":
            for vals in self:
                # x_type_id = int(vals.x_type_conge_id)
                x_user_id = int(vals.current_user)
                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr_paternite) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste = res and res[0] or 0

                vals.env.cr.execute(
                    """select distinct(CL.x_nbre_jr) as nbre from hr_employee E, hr_compte_conge_line CL where E.id = CL.x_employe_id and E.id = %d and CL.x_exercice_id = %d""" % (
                    x_user_id, no_ex))
                res = vals.env.cr.fetchone()
                self.reste_c_ad = res and res[0] or 0

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        if self.x_nbre_jours1 == 0:
            raise ValidationError(
                _('Impossible de valider 0 jours demandés....Verifiez votre date de fin de demande svp!!!!'))
        elif self.x_nbre_jours1 > 30:
            raise ValidationError(_('Une demande de congés ne peut excéder 30 jours.'))
        elif self.reste == 0 and self.reste_c_ad == 0:
            raise ValidationError(_(
                'Votre compteur est à 0...imposible pour vous de demander quoi que ce soit, adressez vous à qui de droit svp!!!!'))
        else:
            x_struct_id = int(self.company_id)
            self.env.cr.execute("select no_code from hr_cpte_dde where company_id = %d" % (x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'DDE' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO hr_cpte_dde(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
            else:

                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                # demande
                self.name = 'DDE' + '/' + ok
                vals = c1
                self.env.cr.execute("UPDATE hr_cpte_dde SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

            self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_appr(self):
        x_user_id = int(self.current_user)
        x_nbre = int(self.x_nbre_jours)
        if self.x_type_conge_id.name == "Congé annuel":
            for record in self:
                record.env.cr.execute(
                    "UPDATE hr_employee SET x_compte_conge = x_compte_conge - %d WHERE id = %d" % (x_nbre, x_user_id))
                if record.report == 'Oui':
                    record.x_date_debut_att = record.x_date_debut_report
                    record.x_date_fin_att = record.x_date_fin_report
                else:
                    record.x_date_debut_att = record.x_date_debut
                    record.x_date_fin_att = record.x_date_fin
            self.write({'state': 'A'})
        elif self.x_type_conge_id.name == "Congé de maternité":
            if self.reste != 0:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_conge_maternite = x_compte_conge_maternite - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})

            else:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_conge = x_compte_conge - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})


        elif self.x_type_conge_id.name == "Congé de paternité":
            if self.reste != 0:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_conge_paternite = x_compte_conge_paternite - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})

            else:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_conge = x_compte_conge - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})

        elif self.x_type_conge_id.name == "Congé pour examens ou concours":
            if self.reste != 0:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_examens = x_compte_examens - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})
            else:
                for record in self:
                    record.env.cr.execute(
                        "UPDATE hr_employee SET x_compte_conge = x_compte_conge - %d WHERE id = %d" % (
                        x_nbre, x_user_id))
                    if record.report == 'Oui':
                        record.x_date_debut_att = record.x_date_debut_report
                        record.x_date_fin_att = record.x_date_fin_report
                    else:
                        record.x_date_debut_att = record.x_date_debut
                        record.x_date_fin_att = record.x_date_fin
                self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    def action_report(self):
        self.write({'state': 'Re'})

    # Classe pour gerer le compteur pour la demande de congé


class Compteur_demande_conge(models.Model):
    _name = "hr_cpte_dde"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# Class pour gerer les demandes d'autorisation d'absence
class HrDemandeAutoAbsence(models.Model):
    _name = "hr_demandeautoabsence"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of auto absence.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    name = fields.Char(string="Code", size=50, readonly=True)
    x_type_absence_id = fields.Many2one('hr_typeabsence', string="Type d'absence", required=True,
                                        states={'A': [('readonly', True)], 'Re': [('readonly', True)],
                                                'C': [('readonly', True)], 'An': [('readonly', True)]})
    x_nbre_jours1 = fields.Integer(compute='_nombre_jours', string='Nombre Jours')
    nb_sous = fields.Integer(string='Jours non ouvrables', required=True,
                             states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'C': [('readonly', True)],
                                     'An': [('readonly', True)]})
    x_nbre_jours = fields.Integer(string='Duréé', readonly=True)
    x_date_debut = fields.Date('Date debut', required=True, default=date.today(),
                               states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'C': [('readonly', True)],
                                       'An': [('readonly', True)]})
    x_date_fin = fields.Date('Date fin', required=True, default=date.today(),
                             states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'C': [('readonly', True)],
                                     'An': [('readonly', True)]})
    observation = fields.Text('Observations', required=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année',
                                     default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Bénéficiaire', default=lambda self: self.env.user)
    date_op = fields.Date(string="Date", default=date.today())
    reste = fields.Integer(string='Reste', readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'En cours de traitement'),
        ('C', 'Confirmée par le chef de service'),
        ('Re', 'Rejetée par le chef de service'),
        ('A', 'Approuvée par le Responsable'),
        ('An', 'Annulée par le responsable'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    ok_chef_service = fields.Boolean(string='Avis Chef Service',
                                     states={'A': [('readonly', True)], 'Re': [('readonly', True)],
                                             'An': [('readonly', True)]})
    observation_chef_service = fields.Text('Observations Chef Service')

    ok_drh = fields.Boolean(string='Avis DRH',
                            states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'An': [('readonly', True)]})
    observation_drh = fields.Text('Observations DRH')

    ok_dg = fields.Boolean(string='Décision DG',
                           states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'An': [('readonly', True)]})
    observation_dg = fields.Text('Observations DG')

    x_titre = fields.Char(string='Titre', default="AUTORISATION D'ABSENCE",
                          states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p2 = fields.Char(string='Phrase 2', default='atteste que M./Mme/Mlle',
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p3 = fields.Char(string='Phrase 3', default='au  ', states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p4 = fields.Char(string='Phrase 4', default="est autorisé(e) à s'absenter durant la période du ",
                     states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p5 = fields.Char(string='Phrase 5', default='Au ', states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    p6 = fields.Char(string='Phrase 6',
                     default='En foi de quoi, la présente autorisation lui est délivrée pour servir et valoir ce que de droit ',
                     states={'A': [('readonly', True)], 'Re': [('readonly', True)], 'An': [('readonly', True)]})
    responsale = fields.Many2one('res.users', string='Responsable', readonly=False,
                                 states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_emploi = fields.Char(string='Emploi', readonly=True)
    x_fonction = fields.Many2one('hr_fonctionss', string='Fonction',
                                 states={'Re': [('readonly', True)], 'An': [('readonly', True)]})
    x_direction = fields.Char(string='Direction', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    date_attest = fields.Date(string="Date", default=date.today())
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    observation = fields.Text(string='Observations')
    fichier_joint = fields.Binary(string='Joindre Autorisation(fichier pdf,word,etc.)', attachment=True)

    x_localite_id = fields.Many2one('ref_localite', string='Localité',
                                    states={'V': [('readonly', True)], 'Re': [('readonly', True)],
                                            'A': [('readonly', True)], 'C': [('readonly', True)],
                                            'An': [('readonly', True)]})
    x_a = fields.Char(string='A', default='A',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    x_destinateur = fields.Char(string='Destinateur', default="Monsieur, le Directeur Général De TelIa INFORMATIQUE",
                                states={'V': [('readonly', True)], 'Re': [('readonly', True)],
                                        'A': [('readonly', True)], 'C': [('readonly', True)],
                                        'An': [('readonly', True)]})
    date_oper = fields.Date(string="Date/Heure", default=date.today(),
                            states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                                    'C': [('readonly', True)], 'An': [('readonly', True)]})
    x_objet = fields.Char(string='Objet', default="Demande d'autorisation d'absence",
                          states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                                  'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_0 = fields.Char(string='Phrase 1', default='Monsieur, ',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_1 = fields.Char(string='Phrase 2', default="J'ai l'honneur de solliciter de votre haute bienveillance ",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_2 = fields.Char(string='Phrase 3', default="l'autorisation d'absence d'une durée de 3 jours.",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_3 = fields.Char(string='Phrase 4',
                      default='Cette absence débutera le 25 Février et prendra fin le 27 Février 2020.',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_4 = fields.Char(string='Phrase 5',
                      default="Dans l'attente d'une suite favorable, Je vous prie d'agréer, Monsieur",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_5 = fields.Char(string='Phrase 6', default='le Directeur Général, mes sentiments les plus distingués.',
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    p_6 = fields.Char(string='Phrase 7', default="L'intéressé",
                      states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                              'C': [('readonly', True)], 'An': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user,
                              states={'V': [('readonly', True)], 'Re': [('readonly', True)], 'A': [('readonly', True)],
                                      'C': [('readonly', True)], 'An': [('readonly', True)]})

    @api.constrains('x_date_debut', 'x_date_fin')
    def CtrlDate(self):

        for val in self:
            if val.x_date_debut > val.x_date_fin:
                raise ValidationError(_(
                    "Enregistrement impossible. La date de début doit être toujours inférieure à la date de fin"))

    # fonction de recuperation de la fonction
    @api.onchange('x_type_absence_id')
    def _fction(self):
        for vals in self:
            user_id = int(vals.current_user)
            vals.env.cr.execute(
                """select (S.name) as service,(Em.name) as emploi from hr_employee E, ref_service S, res_users U, hr_emploi Em where E.x_emploi_id = Em.id and E.user_id = U.id and S.id = U.x_service_id and E.user_id = %d""" % (
                    user_id))
            rows = vals.env.cr.dictfetchall()
            vals.x_emploi = rows and rows[0]['emploi']
            vals.x_service = rows and rows[0]['service']

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_nbre_jours1', 'nb_sous')
    def _nombre_jours_dure(self):
        for vals in self:
            if vals.x_nbre_jours1:
                text = ''
                vals.x_nbre_jours = vals.x_nbre_jours1 - vals.nb_sous
                text += num2words(1250000, lang='fr')
                print('traduit', text)

    # fonction de recuperation de la durée totale de la demande
    @api.onchange('x_date_debut', 'x_date_fin')
    def _nombre_jours(self):
        for vals in self:
            if vals.x_date_debut and vals.x_date_fin:
                vals.x_nbre_jours1 = 1 + (vals.x_date_fin - vals.x_date_debut).days

    # fonction de recherche du nombre de jour de congé restant pour l'employé en cours
    @api.onchange('x_type_absence_id')
    def _nbr_restant_supl(self):
        if self.x_type_absence_id:
            for vals in self:
                x_user_id = int(vals.current_user)
                print('user', x_user_id)
                vals.env.cr.execute(
                    """select (E.x_compte_auto_abs) as nbre from hr_employee E where E.user_id = %d""" % (x_user_id))
                res = vals.env.cr.fetchone()
                self.reste = res and res[0] or 0
                print('nbre jour', self.reste)

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):

        if self.reste < self.x_nbre_jours:
            raise ValidationError(
                _('Le nombre de congé demandé est supérieur au nombre total restant pour vous...Adressez vous à votre supérieur svp'))
        else:
            x_struct_id = int(self.company_id)
            self.env.cr.execute("select no_code from hr_cpte_auto where company_id = %d" % (x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'AUTO' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO hr_cpte_auto(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
            else:
                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                # demande
                self.name = 'AUTO' + '/' + ok
                vals = c1
                self.env.cr.execute("UPDATE hr_cpte_auto SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))
        self.write({'state': 'V'})


    def action_confirmer(self):
        x_nbre = int(self.x_nbre_jours)
        for record in self:
            if record.x_nbre_jours >= 2 and record.ok_chef_service == False:
                raise ValidationError(_('Veuillez cocher la case chef service pour valider avant de confirmer svp!'))
            else:
                self.write({'state': 'C'})

    def action_rejeter(self):
        self.write({'state': 'Re'})

    def action_appr(self):
        x_user_id = int(self.current_user)
        x_nbre = int(self.x_nbre_jours)
        for record in self:
            if record.x_nbre_jours <= 2:
                record.env.cr.execute(
                    "UPDATE hr_employee SET x_compte_conge_sup = x_compte_conge_sup - %d  WHERE user_id = %d" % (
                    x_nbre, x_user_id))
            else:
                if self.ok_chef_service == False or self.ok_drh == False or self.ok_dg == False:
                    raise ValidationError(
                        _('Verifiez que les validations des différents supérieurs ont été effectuées svp!'))

        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # Classe pour gerer le compteur pour la demande de congé


class Compteur_demande_auto_conge(models.Model):
    _name = "hr_cpte_auto"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe pour gerer les comptes de congé
class HrCompteConge(models.Model):
    _name = 'hr_compte_conge'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of compte conge.", default=10)

    name = fields.Char('Code', readonly=True)
    x_service_id = fields.Many2one('hr_service', string='Service', required=False)
    x_type_conge_id = fields.Many2one('hr_typeconges', string='Type de congé', required=False)
    x_nbre_jr_alloue = fields.Integer(string='Congé Annuel (jrs)', required=True, default=30)
    x_nbre_jr_auto_abs = fields.Integer(string='Congé Absence (jrs)', required=True, default=10)
    x_nbre_jr_maternite = fields.Integer(string='Congé Maternité (jrs)', required=True, default=90)
    x_nbre_jr_paternite = fields.Integer(string='Congé Paternité (jrs)', required=True, default=3)
    x_nbre_jr_examen = fields.Integer(string='Congé Examen (jrs)', required=True, default=5)
    # x_nbre_jr_cpl = fields.Integer(string = 'Nb. Jour Additionnel', required = True,default=10)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année en cours', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_compte_conge_line', 'name', string='Ajout Des Candidats')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Approuver'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # fonction de remplissage du tableau
    def action_valider(self):
        if self.x_exercice_id:
            x_service_id = int(self.x_service_id)
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)
            """x_nbre_administratif = int(self.x_nbre_jr_alloue)
            x_nbre_jr_auto_abs = int(self.x_nbre_jr_auto_abs)
            x_nbre_jr_maternite = int(self.x_nbre_jr_maternite)
            x_nbre_jr_paternite = int(self.x_nbre_jr_paternite)
            x_nbre_jr_examen = int(self.x_nbre_jr_examen)"""
            # x_nbre_j = int(self.x_nbre_jr_cpl)
            for vals in self:
                vals.env.cr.execute(
                    """select (E.id) as id, (E.name) as employe, (E.genre) as genre,(D.name) as direction from hr_employee E, hr_department D where E.x_direction_id = D.id and E.company_id = %d""" % (
                        x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0,
                                   {'x_employe_id': line['id'], 'genre': line['genre'], 'x_employe': line['employe'],
                                    'x_direction': line['direction']}))
                self.x_line_ids = result

            self.MajCpte()

    def MajCpte(self):

        v_id = int(self.id)
        x_nbre_administratif = int(self.x_nbre_jr_alloue)
        x_nbre_jr_auto_abs = int(self.x_nbre_jr_auto_abs)
        x_nbre_jr_maternite = int(self.x_nbre_jr_maternite)
        x_nbre_jr_paternite = int(self.x_nbre_jr_paternite)
        x_nbre_jr_examen = int(self.x_nbre_jr_examen)

        self.env.cr.execute("""select * from hr_compte_conge_line where name = %d """ % (v_id))

        for val in self.env.cr.dictfetchall():
            self.env.cr.execute("""update hr_compte_conge_line set x_nbre_jr = %s, x_nbre_jr_auto_abs = %s, x_nbre_jr_maternite = %s, x_nbre_jr_examen = %s
            where genre = 'feminin' and name = %s """,
                                (x_nbre_administratif, x_nbre_jr_auto_abs, x_nbre_jr_maternite, x_nbre_jr_examen, v_id))

            self.env.cr.execute("""update hr_compte_conge_line set x_nbre_jr = %s, x_nbre_jr_auto_abs = %s, x_nbre_jr_paternite = %s, x_nbre_jr_examen = %s
            where genre = 'masculin' and name = %s """,
                                (x_nbre_administratif, x_nbre_jr_auto_abs, x_nbre_jr_paternite, x_nbre_jr_examen, v_id))

        self.write({'state': 'V'})

    def action_confirmer(self):
        x_struct_id = int(self.company_id)
        self.env.cr.execute("select no_code from hr_cpte_conge where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'CCG' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cpte_conge(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            # Compte Congé
            self.name = 'CCG' + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE hr_cpte_conge SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'C'})

    def action_appr(self):
        x_struct_id = int(self.company_id)
        for record in self.x_line_ids:
            val_id = int(record.x_employe_id)
            val_nbre = int(record.x_nbre_jr)
            val_nbre_auto = int(record.x_nbre_jr_auto_abs)
            val_nbre_maternite = int(record.x_nbre_jr_maternite)
            val_nbre_paternite = int(record.x_nbre_jr_paternite)
            val_nbre_examen = int(record.x_nbre_jr_examen)
            self.env.cr.execute(
                "UPDATE hr_employee SET x_compte_conge =  %d,x_compte_conge_maternite = %d,x_compte_auto_abs = %d,x_compte_examens = %d WHERE id = %d and genre = 'feminin' " % (
                val_nbre, val_nbre_maternite, val_nbre_auto, val_nbre_examen, val_id))

            self.env.cr.execute(
                "UPDATE hr_employee SET x_compte_conge =  %d,x_compte_conge_paternite = %d,x_compte_auto_abs = %d,x_compte_examens = %d WHERE id = %d and genre = 'masculin' " % (
                val_nbre, val_nbre_paternite, val_nbre_auto, val_nbre_examen, val_id))

        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # classe pour ajouter les employés dans le ajouter ligne


class HrCompteConge(models.Model):
    _name = 'hr_compte_conge_line'
    name = fields.Many2one('hr_compte_conge', ondelete='cascade')
    x_employe_id = fields.Integer(string='Id Employé', readonly=True)
    genre = fields.Selection([('masculin', 'Masculin'), ('feminin', 'Féminin')], string='Genre', readonly=True)
    x_employe = fields.Char(string='Employé', readonly=True)
    x_direction = fields.Char(string='Direction', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    x_nbre_jr = fields.Integer(string='Congé annuel(jrs)', readonly=True)
    x_nbre_jr_auto_abs = fields.Integer(string='Jour Absence(jrs)', readonly=True)
    x_nbre_jr_maternite = fields.Integer(string='Congé Maternité(jrs)', readonly=True)
    x_nbre_jr_paternite = fields.Integer(string='Congé paternité(jrs)', readonly=True)
    x_nbre_jr_examen = fields.Integer(string='Congé Examen(jrs)', readonly=True)

    # x_nbre_jr_sup = fields.Integer(string = 'Jour additionnel', readonly = True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# Classe pour gerer le compteur pour les compteurs de congé
class Compteur_Compte_conge(models.Model):
    _name = "hr_cpte_conge"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe pour gerer les decisions de congés
class HrDecisionConge(models.Model):
    _name = 'hr_decision_conge'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    name = fields.Char('Code', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)
    # x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_line_ids = fields.One2many('hr_decision_conge_line', 'x_deci_id', string='Liste des employés')
    x_decision = fields.Char('Code',
                             default='/MDENP/SG/ANPTIC/SG/DRH/ accordant un congé Administratifs aux agents contracteuls')
    x_titre = fields.Char(string='Titre',
                          default="LE DIRECTEUR GENERAL DE L'AGENCE NATIONALE DE PROMOTION DES TECHNOLOGIES DE L'INFORMATION ET DE LA COMMUNICATION")
    observation = fields.Text(string='Observations')
    fichier_joint = fields.Binary(string='Joindre Pièce (pdf,word,xls)', attachment=True)
    x_titre_id = fields.Many2one('hr_titreposte', string='Titre Du Poste')
    x_employee_id = fields.Many2one('hr.employee', string='Employé')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # def action_recherch(self):
    #     if self.x_type_employe_id:
    #         x_struct_id = int(self.company_id)
    #         x_type_id = int(self.x_type_employe_id)
    #         x_ty = str(self.x_type_employe_id.name)
    #         for vals in self:
    #             if x_ty == 'Fonctionnaire Detaché' or x_ty == 'Fonctionnaire Mis à Disposition':
    #                 vals.env.cr.execute(
    #                     """SELECT (E.id) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(EM.id) as emploi,(S.id) as service, (ST.name) as structure, (E.date_debut) as debut,(E.date_fin) as fin FROM hr_employee E,hr_emploi EM, hr_service S, hr_payroll_structure ST WHERE E.x_emploi_id = EM.id AND E.hr_service = S.id AND E.x_type_employe_id = ST.id AND E.x_type_employe_id = %d and E.company_id = %d""" % (
    #                     x_type_id, x_struct_id))
    #                 rows = vals.env.cr.dictfetchall()
    #                 result = []
    #
    #                 # delete old payslip lines
    #                 vals.x_line_ids.unlink()
    #                 for line in rows:
    #                     result.append((0, 0, {'x_employee_id': line['employe'], 'mat_ctrct': line['matricule_ctrct'],
    #                                           'mat_fct': line['matricule'], 'x_emploi_id': line['emploi'],
    #                                           'x_service_id': line['service'], 'x_date_debut': line['debut'],
    #                                           'x_date_fin': line['fin']}))
    #                 self.x_line_ids = result
    #             elif x_ty == 'Contractuel':
    #                 vals.env.cr.execute(
    #                     """SELECT (E.id) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(EM.id) as emploi,(S.id) as service, (ST.name) as structure, (E.date_embauche) as debut,(E.date_fin_embauche) as fin FROM hr_employee E,hr_emploi EM, hr_service S, hr_payroll_structure ST WHERE E.x_emploi_id = EM.id AND E.hr_service = S.id AND E.x_type_employe_id = ST.id AND E.x_type_employe_id = %d and E.company_id = %d""" % (
    #                     x_type_id, x_struct_id))
    #                 rows = vals.env.cr.dictfetchall()
    #                 result = []
    #
    #                 # delete old payslip lines
    #                 vals.x_line_ids.unlink()
    #                 for line in rows:
    #                     result.append((0, 0, {'x_employee_id': line['employe'], 'mat_ctrct': line['matricule_ctrct'],
    #                                           'mat_fct': line['matricule'], 'x_emploi_id': line['emploi'],
    #                                           'x_service_id': line['service'], 'x_date_debut': line['debut'],
    #                                           'x_date_fin': line['fin']}))
    #                 self.x_line_ids = result
    #             else:
    #                 vals.env.cr.execute(
    #                     """SELECT (E.id) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(EM.id) as emploi,(S.id) as service, (ST.name) as structure, (E.date_debut) as debut,(E.date_fin) as fin FROM hr_employee E,hr_emploi EM, hr_service S, hr_payroll_structure ST WHERE E.x_emploi_id = EM.id AND E.hr_service = S.id AND E.x_type_employe_id = ST.id AND E.x_type_employe_id = %d and E.company_id = %d""" % (
    #                     x_type_id, x_struct_id))
    #                 rows = vals.env.cr.dictfetchall()
    #                 result = []
    #
    #                 # delete old payslip lines
    #                 vals.x_line_ids.unlink()
    #                 for line in rows:
    #                     result.append((0, 0, {'x_employee_id': line['employe'], 'mat_ctrct': line['matricule_ctrct'],
    #                                           'mat_fct': line['matricule'], 'x_emploi_id': line['emploi'],
    #                                           'x_service_id': line['service'], 'x_date_debut': line['debut'],
    #                                           'x_date_fin': line['fin']}))
    #                 self.x_line_ids = result
    #             self.write({'state': 'R'})

    # FONCTION DE calcul de la date de depart a la retraite d'un employe
    def action_valider(self):
        anne = 1
        for record in self.x_line_ids:
            if record.x_date_effet_conge == False:
                date1 = record.x_date_debut.strftime("%Y-%m-%d")
                date2 = record.x_date_debut.year + anne
                record.x_date_effet_conge = datetime(date2, record.x_date_debut.month - 1,
                                                     (record.x_date_debut.day - 1), 0, 0, 0, 0).date()
            else:
                date1 = record.x_date_effet_conge.strftime("%Y-%m-%d")
                date2 = record.x_date_effet_conge.year + anne
                record.x_date_effet_conge = datetime(date2, record.x_date_effet_conge.month - 1,
                                                     (record.x_date_effet_conge.day - 1), 0, 0, 0, 0).date()

            self.write({'state': 'V'})

    # fonction qui permettre de genere la reference du bulletin d'un employé
    def action_confirmer(self):
        val_struct = int(self.company_id)
        nom_structure = self.company_id.code_struct
        self.env.cr.execute("select no_decision from hr_compteur_decision where company_id = %d" % (val_struct))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_compteur_decision(company_id,no_decision)  VALUES(%d , %d)""" % (val_struct, vals))
        else:
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_compteur_decision SET no_decision = %d  WHERE company_id = %d" % (vals, val_struct))

        self.write({'state': 'C'})


# classe pour gerer les lignes des decisions de congé
class HrDecisionCongeLine(models.Model):
    _name = 'hr_decision_conge_line'
    x_deci_id = fields.Many2one('hr_decision_conge')
    x_employee_id = fields.Many2one('hr.employee', string='Employé')
    mat_ctrct = fields.Char('Mlle Contractuel')
    mat_fct = fields.Char('Mlle Fonctionnaire')
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi')
    x_service_id = fields.Many2one('hr_service', string='Service')
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    x_date_effet_conge = fields.Date('Date effet')
    lieu_jouissance = fields.Char('Lieu')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# Classe pour gerer le compteur pour les decisions
class Compteur_decision(models.Model):
    _name = "hr_compteur_decision"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_decision = fields.Integer()
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))


# classe pour gerer les plannings de congés
class HrPlanningConge(models.Model):
    _name = 'hr_planning_conge'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    _rec_name = 'x_exercice_id'
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    date_enreg = fields.Date(string="Date Opération", default=date.today(), readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Choisir Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=False)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=False)
    x_line_ids = fields.One2many('hr_planning_conge_line', 'x_plann_id', string='Planning',
                                 states={'C': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # fonction de remplissage du tableau de planning des congés
    def action_recherch(self):
        x_struct_id = int(self.company_id)
        x_exo_id = int(self.x_exercice_id)
        for vals in self:
            vals.env.cr.execute(
                """SELECT * FROM hr_decision_conge_line WHERE x_exercice_id = %d and company_id = %d""" % (
                x_exo_id, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []

            # delete old payslip lines
            vals.x_line_ids.unlink()
            for line in rows:
                result.append((0, 0, {'x_employee_id': line['x_employee_id'], 'mat_ctrct': line['mat_ctrct'],
                                      'mat_fct': line['mat_fct'], 'x_emploi_id': line['x_emploi_id'],
                                      'x_service_id': line['x_service_id'],
                                      'x_date_effet_conge': line['x_date_effet_conge'], 'x_date_debut': '',
                                      'x_date_fin': '', 'lieu_jouissance': line['lieu_jouissance'],
                                      'x_exercice_id': line['x_exercice_id'], 'company_id': line['company_id']}))
            self.x_line_ids = result
        self.write({'state': 'R'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})


# classe pour gerer les lignes de planning de congés
class HrPlanningCongeLine(models.Model):
    _name = 'hr_planning_conge_line'
    x_plann_id = fields.Many2one('hr_planning_conge')
    x_employee_id = fields.Many2one('hr.employee', string='Employé')
    mat_ctrct = fields.Char('Mlle Contractuel')
    mat_fct = fields.Char('Mlle Fonctionnaire')
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi')
    x_service_id = fields.Many2one('hr_service', string='Service')
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    x_date_effet_conge = fields.Date('Date effet')
    lieu_jouissance = fields.Char('Lieu')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    nbre_jours = fields.Integer('Durée', readonly=True)

    # fonction de recuperation de la durée totale du conge
    @api.onchange('x_date_fin', 'x_date_debut')
    def _nombre_jours(self):
        for vals in self:
            if vals.x_date_debut and vals.x_date_fin:
                vals.nbre_jours = (vals.x_date_fin - vals.x_date_debut).days

    # fonction pour contrôler les dates (date de debut ne doit pas etre superieur à la date de fin)
    @api.constrains('x_date_debut', 'x_date_fin')
    def CtrlDate(self):

        for val in self:
            if val.x_date_debut > val.x_date_fin:
                raise ValidationError(_(
                    "Enregistrement impossible. La date de début  doit être toujours inférieure à la date de fin"))