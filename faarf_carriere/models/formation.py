from odoo import fields, models, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


# expression des besoins annuels de formation des employés par service ou direction
class BesoinsFormationAnnules(models.Model):
    _name = 'hr_besoinformation'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of type previsions.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string="Code", size=50)
    date_besoin = fields.Datetime(string='Date/Heure', default=datetime.today())
    beneficiaire = fields.Many2one('hr_service', string="Adressé à", required=True)
    service_demandeur = fields.Many2one('hr_service', string='Service demandeur', required=True)
    objet_besoin = fields.Text(string='Objet')
    x_line_ids = fields.One2many('hr_besoinformation_line', 'x_besoin_id', string='Ajout Des Compétences ')
    active = fields.Boolean(string="Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('R', 'Receptionner'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # fonction de recuperation du service de l'utilisateur connecté et changement d'etat
    def action_valider(self):
        self.write({'state': 'V'})
        for record in self.x_line_ids:
            """if record.qte_demandee <= 0:
                raise ValidationError(_('Veuillez saisir une quantitée supérieure ou égale à 1'))"""

        x_struct_id = int(self.company_id)
        x_user_id = int(self.current_user)
        self.env.cr.execute(
            """select (R.id) AS id,(R.name) AS service, (R.code) AS code From ref_service R, res_users U where R.id = U.x_service_id and U.id = %s and U.company_id = %s""",
            (x_user_id, x_struct_id))
        rows = self.env.cr.dictfetchall()

        cd_serv = rows and rows[0]['code']
        self.env.cr.execute("select no_code from hr_compteur_fbesoin where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_compteur_fbesoin(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:

            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.name = '/' + ok
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_compteur_fbesoin SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

    def action_eng_recep(self):
        self.write({'state': 'R'})

    # fonction de recuperation de l'année en cours


class FormationLine(models.Model):
    _name = 'hr_besoinformation_line'
    x_besoin_id = fields.Many2one('hr_besoinformation', string='Type formation')
    # _rec_name = 'x_theme'
    name = fields.Many2one('hr_domaine', string='Domaine', required=True)
    x_theme = fields.Many2one('hr_theme', string='Thème', required=True)
    formateur = fields.Selection([
        ('Intérieur', 'Intérieur'),
        ('Extérieur', 'Extérieur')
    ], string='Formateur', index=True, readonly=False, copy=False, default='Intérieur', required=True)
    x_nbre_paticipant = fields.Integer(string='Nbre de participants', required=True)
    x_nbre_session = fields.Integer(string='Nbre de sessions', required=True)
    x_nbre_jours = fields.Integer(string='Nbre de jours', required=True)
    x_strucuture_concerne_ids = fields.Many2many('res.company', string='Structures concernées')
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    x_mnt = fields.Float(string='Montant', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# Class pour gerer la centralisation des besoins annuels de chaque service de chaque EPE
class HrCentralisationBesoinsAnnuels(models.Model):
    _name = "hr_central_besoinformation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string="Code", size=50, readonly=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année',
                                     default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_central_besoinformation_line', 'x_besoin_central_id',
                                 string='Liste Des Domaines de formations', readonly=True)
    x_line_p_ids = fields.One2many('hr_central_besoinservice_line', 'x_service_central_id',
                                   string='Liste Des Services Demandeurs', readonly=True)
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

            self.env.cr.execute(
                "select count(*) from hr_cpte_central_besoin where x_exercice_id = %d and company_id = %d" % (
                    annee, x_struct_id))
            val = self.env.cr.fetchone()
            val1 = val and val[0] or 0
            if val1 == 0:
                for vals in self:
                    vals.env.cr.execute(
                        """select count(H.id) AS nb_service, (D.id) as domaine,(T.id) as theme, SUM(L.x_nbre_paticipant) as nbre from hr_besoinformation_line L, hr_besoinformation B, hr_domaine D,hr_theme T,hr_service H where L.x_besoin_id = B.id and D.id = L.name and H.id = B.service_demandeur and T.id = L.x_theme and B.x_exercice_id = %s and B.company_id = %s and B.state = 'R' GROUP by domaine,theme""",
                        (annee, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0, {'domaine': line['domaine'], 'x_theme': line['theme'],
                                              'x_nbre_paticipant': line['nbre'],
                                              'service_demandeur': line['nb_service']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """select (H.name) AS service, (D.id) as domaine,(T.id) as theme from hr_besoinformation_line L, hr_besoinformation B, hr_domaine D,hr_theme T, hr_service H where L.x_besoin_id = B.id and D.id = L.name and T.id = L.x_theme and H.id = B.service_demandeur and B.x_exercice_id = %s and B.company_id = %s and B.state = 'R' GROUP BY service,domaine,theme""",
                        (annee, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_p_ids.unlink()
                    for lines in rows:
                        result.append((0, 0, {'domaine': lines['domaine'], 'x_theme': lines['theme'],
                                              'service_demandeur': lines['service']}))
                    self.x_line_p_ids = result

                    x_user_id = int(self.current_user)
                    self.env.cr.execute(
                        """select (R.id) AS id, (R.name) AS service, (R.code) AS code From ref_service R, res_users U where R.id = U.x_service_id and U.id = %s and U.company_id = %s""",
                        (x_user_id, x_struct_id))
                    rows = self.env.cr.dictfetchall()
                    self.service_traiteur = rows and rows[0]['service']

                    self.env.cr.execute(
                        "select no_code from hr_cpte_central_besoin where company_id = %d" % (x_struct_id))
                    lo = self.env.cr.fetchone()
                    no_lo = lo and lo[0] or 0
                    c1 = int(no_lo) + 1
                    c = str(no_lo)
                    if c == "0":
                        ok = str(c1).zfill(4)
                        self.name = 'CBA' + '/' + ok
                        vals = c1
                        self.env.cr.execute(
                            """INSERT INTO hr_cpte_central_besoin(company_id,no_code,x_exercice_id)  VALUES(%d , %d, %d)""" % (
                                x_struct_id, vals, annee))
                    else:

                        c1 = int(no_lo) + 1
                        c = str(no_lo)
                        ok = str(c1).zfill(4)
                        self.name = 'CBA' + '/' + ok
                        vals = c1
                        self.env.cr.execute(
                            "UPDATE hr_cpte_central_besoin SET no_code = %d,x_exercice_id =%d  WHERE company_id = %d" % (
                                vals, annee, x_struct_id))

                self.write({'state': 'F'})
            else:
                raise ValidationError(_('Impossible de faire une double centralisation dans la même année'))


# class pour gerer les lignes de centralisation des besoins annuels en formation
class HrCentralisationBesoinsAnnuelsLine(models.Model):
    _name = "hr_central_besoinformation_line"
    x_besoin_central_id = fields.Many2one('hr_central_besoinformation')
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    formateur = fields.Text(string='Formateur')
    x_nbre_paticipant = fields.Integer(string='Nbre de participants')
    x_nbre_session = fields.Integer(string='Nbre de sessions')
    x_nbre_jours = fields.Integer(string='Nbre de jours')
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    mnt = fields.Float(string='Montant')
    service_demandeur = fields.Char(string='Nombre Service demandeur')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# class pour gerer les lignes de centralisation des besoins annuels en formation pour les services
class HrCentralisationBesoinsAnnuelsLineService(models.Model):
    _name = "hr_central_besoinservice_line"
    x_service_central_id = fields.Many2one('hr_central_besoinformation')
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    service_demandeur = fields.Char(string='Service demandeur')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année')


# Formation
# classe  PLAN formation trienal
class HrPlanFormationTrienal(models.Model):
    _name = 'hr_plan_formation_trienal'
    _order = 'sequence, id'
    _rec_name = 'x_exercice_id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of ministere.", default=10)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_plan = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_plan_formation_trienal_line', 'x_plan_id',
                                 string='Liste Des Domaines de formations', states={'A': [('readonly', True)]})
    x_line_p_ids = fields.One2many('hr_plan_besoinservice_trienal_line', 'x_service_besoin_id',
                                   string='Liste Des Services demandeurs', readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Approuver'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    etat = fields.Selection([('N', "Non affiché"), ('A', "Affiché")], string="Etat", default="N")

    @api.onchange('x_plan')
    def verif_plan(self):
        for vals in self:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            vals.env.cr.execute(
                """select count(P.id) AS nb from hr_plan_formation P where P.x_plan = 'initial' and P.x_exercice_id = %s and P.company_id = %s""" % (
                    annee, x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0

            if no_lo == 1 and vals.x_plan == 'initial':
                raise ValidationError(
                    _('Impossible de faire 2 plans de type initial pour la même année, veuillez selectionner plan modifié svp'))

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_appr(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """UPDATE hr_plan_formation SET state = 'An' WHERE x_exercice_id = %d and company_id = %d""" % (
                    annee, x_struct_id))
        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # fonction de remplissage du tableau des services demandeurs
    def action_voirservice(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self.x_line_ids:
            x_theme_id = int(vals.x_theme)
            vals.env.cr.execute(
                """select (H.id) AS service, (D.id) as domaine,(T.id) as theme from hr_besoinformation_line L, hr_besoinformation B, hr_domaine D,hr_theme T, hr_service H where L.x_besoin_id = B.id and D.id = L.name and T.id = L.x_theme and H.id = B.service_demandeur and L.x_theme = %s and B.x_exercice_id = %s and B.company_id = %s and B.state = 'R' GROUP BY service,domaine,theme""",
                (x_theme_id, annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []

            if rows:
                # delete old payslip lines
                # vals.x_line_p_ids.unlink()
                for lines in rows:
                    result.append((0, 0, {'domaine': lines['domaine'], 'x_theme': lines['theme'],
                                          'service_demandeur': lines['service']}))
                self.x_line_p_ids = result
            else:
                raise ValidationError(_("Pas de données à afficher"))

            self.write({'etat': 'A'})

            # fonction de recherche du plan de centralisation pour mettre en place le plan trienal

    def recherche(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """SELECT L.* FROM hr_central_besoinformation C, hr_central_besoinformation_line L WHERE C.id = L.x_besoin_central_id AND C.company_id = %d AND C.x_exercice_id = %d and C.state = 'F'""" % (
                    x_struct_id, annee))
            rows = vals.env.cr.dictfetchall()
            result = []
            print('données', rows)

            # delete old payslip lines
            vals.x_line_ids.unlink()
            for lines in rows:
                result.append((0, 0, {'x_type_formation_id': '', 'x_type_session_id': '', 'domaine': lines['domaine'],
                                      'x_theme': lines['x_theme'], 'x_nbre_paticipant': lines['x_nbre_paticipant'],
                                      'formateur': '', 'x_nbre_session': '', 'x_date_debut': '', 'x_date_fin': '',
                                      'x_nbre_jours': '', 'mnt': '', 'service_demandeurs': lines['service_demandeur'],
                                      'lieu_f': ''}))
            vals.x_line_ids = result


# classe  PLAN line formation trienal
class HrPlanFormationTrienalLine(models.Model):
    _name = 'hr_plan_formation_trienal_line'
    _rec_name = 'x_theme'
    x_plan_id = fields.Many2one('hr_plan_formation_trienal', ondelete='cascade')

    x_type_formation_id = fields.Many2one('hr_type_formation', string="Type Formation", required=False)
    x_type_session_id = fields.Many2one('hr_type_session', string='Type Session', size=2, required=False)
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    formateur = fields.Selection([
        ('Intérieur', 'Intérieur'),
        ('Extérieur', 'Extérieur')
    ], string='Formateur', index=True, readonly=False, copy=False, default='Intérieur')
    x_nbre_paticipant = fields.Integer(string='Nbre de participants')
    x_nbre_session = fields.Integer(string='Nbre de sessions')
    x_nbre_jours = fields.Integer(string='Nbre de jours', readonly=True)
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    mnt = fields.Integer(string='Montant')
    mnt_a_soustrair = fields.Integer(string='Montant', store=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    service_demandeur = fields.Integer(readonly=True)
    service_demandeurs = fields.Integer(string='Nombre Service demandeur', readonly=True)
    lieu_f = fields.Many2one('hr_lieu', string='Lieu', required=False)
    etat = fields.Char(string="Exécuté", default='non', readonly=True)
    etat_exe = fields.Integer(string="Etat", default=0)

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_date_debut', 'x_date_fin')
    def nbre_j(self):
        for vals in self:
            if vals.x_date_fin and vals.x_date_debut:
                vals.x_nbre_jours = (vals.x_date_fin - vals.x_date_debut).days
                if vals.x_nbre_jours < 0:
                    raise ValidationError(_("La date de début ne peut pas être supérieure à la date de fin."))

    @api.onchange('x_theme')
    def remplir_liste(self):
        for vals in self:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            x_theme_id = int(self.x_theme)
            vals.env.cr.execute(
                """select count(H.id) AS nb_service, SUM(L.x_nbre_paticipant) as nbre from hr_besoinformation_line L, hr_besoinformation B,hr_service H where L.x_besoin_id = B.id and H.id = B.service_demandeur and L.x_theme = %d and B.x_exercice_id = %d and B.company_id = %d""" % (
                    x_theme_id, annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()

            self.x_nbre_paticipant = rows and rows[0]['nbre']
            self.service_demandeurs = rows and rows[0]['nb_service']

    @api.onchange('mnt')
    def remplir_mnt(self):
        for vals in self:
            vals.mnt_a_soustrair = vals.mnt


# class pour gerer les lignes de plan des besoins annuels en formation trienal pour les services
class HrPlanBesoinsAnnuelsTrienalLineService(models.Model):
    _name = "hr_plan_besoinservice_trienal_line"
    x_service_besoin_id = fields.Many2one('hr_plan_formation_trienal', ondelete='cascade')
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    service_demandeur = fields.Many2one('hr_service', string='Service demandeur')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année')


# classe  PLAN formation
class HrPlanFormation(models.Model):
    _name = 'hr_plan_formation'
    _order = 'sequence, id'
    _rec_name = 'x_exercice_id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of ministere.", default=10)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_plan = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_plan_formation_line', 'x_plan_id', string='Liste Des Domaines de formations',
                                 states={'A': [('readonly', True)]})
    x_line_p_ids = fields.One2many('hr_plan_besoinservice_line', 'x_service_besoin_id',
                                   string='Liste Des Services demandeurs', readonly=False)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('A', 'Approuver'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    x_plan = fields.Selection([
        ('initial', 'Initial'),
        ('modifie', 'Modifié'),
        ('hors', 'Hors-Plan'),
    ], string="Type Plan", default='', required=True)

    @api.onchange('x_plan')
    def verif_plan(self):
        for vals in self:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            vals.env.cr.execute(
                """select count(P.id) AS nb from hr_plan_formation P where P.x_plan = 'initial' and P.x_exercice_id = %s and P.company_id = %s""" % (
                    annee, x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0

            if no_lo == 1 and vals.x_plan == 'initial':
                raise ValidationError(
                    _('Impossible de faire 2 plans de type initial pour la même année, veuillez selectionner plan modifié svp'))

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_appr(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """UPDATE hr_plan_formation SET state = 'An' WHERE x_exercice_id = %d and company_id = %d""" % (
                    annee, x_struct_id))
        self.write({'state': 'A'})

    def action_ann(self):
        self.write({'state': 'An'})

    # fonction de remplissage du tableau des services demandeurs
    def action_voir(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self.x_line_ids:
            x_theme_id = int(vals.x_theme)
            vals.env.cr.execute(
                """select (H.id) AS service, (D.id) as domaine,(T.id) as theme from hr_besoinformation_line L, hr_besoinformation B, hr_domaine D,hr_theme T, hr_service H where L.x_besoin_id = B.id and D.id = L.name and T.id = L.x_theme and H.id = B.service_demandeur and L.x_theme = %s and B.x_exercice_id = %s and B.company_id = %s and B.state = 'R' GROUP BY service,domaine,theme""",
                (x_theme_id, annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []
            # vals.x_line_p_ids.unlink()
            if rows:

                # delete old payslip lines
                for lines in rows:
                    result.append((0, 0, {'domaine': lines['domaine'], 'x_theme': lines['theme'],
                                          'service_demandeur': lines['service']}))
                self.x_line_p_ids = result
            else:
                raise ValidationError(_("Pas de données à afficher"))

    # fonction de remplissage du tableau avec les formations retrouvées
    def action_retrouver(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """select L.* ,(LI.id) as lieu from hr_plan_formation_line L, hr_plan_formation P,hr_lieu LI where P.id = L.x_plan_id AND LI.id = L.lieu_f and P.state = 'A' and L.etat = 'non' and L.x_exercice_id = %d and L.company_id = %d """ % (
                    annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []
            if rows:

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for lines in rows:
                    result.append((0, 0, {'name': lines['name'], 'x_type_session_id': lines['x_type_session_id'],
                                          'domaine': lines['domaine'], 'x_theme': lines['x_theme'],
                                          'x_nbre_paticipant': lines['x_nbre_paticipant'],
                                          'formateur': lines['formateur'], 'x_nbre_session': lines['x_nbre_session'],
                                          'x_date_debut': lines['x_date_debut'], 'x_date_fin': lines['x_date_fin'],
                                          'x_nbre_jours': lines['x_nbre_jours'], 'mnt': lines['mnt'],
                                          'service_demandeurs': lines['service_demandeurs'], 'lieu_f': lines['lieu']}))
                vals.x_line_ids = result
            else:
                raise ValidationError(_("Pas de données à afficher"))

    # fonction de recherche du plan de centralisation pour mettre en place le plan trienal
    def recherche(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """SELECT L.* FROM hr_plan_formation_trienal T, hr_plan_formation_trienal_line L WHERE T.id = L.x_plan_id AND T.company_id = %d AND T.x_exercice_id = %d and T.state = 'A' and L.etat = 'non' """ % (
                    x_struct_id, annee))
            rows = vals.env.cr.dictfetchall()
            if rows:
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for lines in rows:
                    result.append((0, 0, {'id_plan_trienal': lines['id'], 'name': lines['x_type_formation_id'],
                                          'x_type_session_id': lines['x_type_session_id'], 'domaine': lines['domaine'],
                                          'x_theme': lines['x_theme'], 'x_nbre_paticipant': lines['x_nbre_paticipant'],
                                          'formateur': lines['formateur'], 'x_nbre_session': lines['x_nbre_session'],
                                          'x_date_debut': lines['x_date_debut'], 'x_date_fin': lines['x_date_fin'],
                                          'x_nbre_jours': lines['x_nbre_jours'], 'mnt': lines['mnt'],
                                          'service_demandeurs': lines['service_demandeurs'],
                                          'lieu_f': lines['lieu_f']}))
                vals.x_line_ids = result
            else:
                raise ValidationError(_("Pas de données à afficher"))

            # classe  PLAN line formation


class HrPlanFormationLine(models.Model):
    _name = 'hr_plan_formation_line'
    _rec_name = 'x_theme'
    x_plan_id = fields.Many2one('hr_plan_formation', ondelete='cascade')

    id_plan_trienal = fields.Integer('Id')
    name = fields.Many2one('hr_type_formation', string="Type Formation", required=False)
    x_type_session_id = fields.Many2one('hr_type_session', string='Type Session', size=2, required=False)
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    formateur = fields.Selection([
        ('Intérieur', 'Intérieur'),
        ('Extérieur', 'Extérieur')
    ], string='Formateur', index=True, readonly=False, copy=False, default='Intérieur')
    x_nbre_paticipant = fields.Integer(string='Nbre de participants')
    x_nbre_session = fields.Integer(string='Nbre de sessions')
    x_nbre_jours = fields.Integer(string='Nbre de jours', readonly=True)
    x_date_debut = fields.Date('Date debut')
    x_date_fin = fields.Date('Date fin')
    mnt = fields.Integer(string='Montant')
    mnt_a_soustrair = fields.Integer(string='Montant', store=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    service_demandeur = fields.Integer(readonly=True)
    service_demandeurs = fields.Integer(string='Nombre Service demandeur', readonly=True)
    lieu_f = fields.Many2one('hr_lieu', string='Lieu', required=False)
    etat = fields.Char(string="Exécuté", default='non', readonly=True)
    etat_exe = fields.Integer(string="Etat", default=0)

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_date_debut', 'x_date_fin')
    def nbre_j(self):
        for vals in self:
            if vals.x_date_debut and vals.x_date_fin:
                vals.x_nbre_jours = (vals.x_date_fin - vals.x_date_debut).days
                if vals.x_nbre_jours < 0:
                    raise ValidationError(_("La date de début ne peut pas supérieure à la date de fin."))

    @api.onchange('x_theme')
    def remplir_liste(self):
        for vals in self:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            x_theme_id = int(self.x_theme)
            vals.env.cr.execute(
                """select count(H.id) AS nb_service, SUM(L.x_nbre_paticipant) as nbre from hr_besoinformation_line L, hr_besoinformation B,hr_service H where L.x_besoin_id = B.id and H.id = B.service_demandeur and L.x_theme = %d and B.x_exercice_id = %d and B.company_id = %d""" % (
                    x_theme_id, annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()

            self.x_nbre_paticipant = rows and rows[0]['nbre']
            self.service_demandeurs = rows and rows[0]['nb_service']

    @api.onchange('mnt')
    def remplir_mnt(self):
        for vals in self:
            vals.mnt_a_soustrair = vals.mnt

    @api.onchange('mnt')
    def CtrlMnt(self):
        for val in self:
            if val.mnt < 0:
                raise ValidationError(_("Le montant ne peut pas être inférieure à 0."))


# class pour gerer les lignes de plan des besoins annuels en formation pour les services
class HrPlanBesoinsAnnuelsLineService(models.Model):
    _name = "hr_plan_besoinservice_line"
    x_service_besoin_id = fields.Many2one('hr_plan_formation')
    domaine = fields.Many2one('hr_domaine', string='Domaine')
    x_theme = fields.Many2one('hr_theme', string='Thème')
    service_demandeur = fields.Many2one('hr_service', string='Service demandeur')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année')


# classe de suivi des plans de formation adoptés
class HrSuiviPlan(models.Model):
    _name = "hr_suivi_plan"
    _rec_name = 'x_exercice_id'
    x_exercice_id = fields.Many2one('ref_exercice', string="Année",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_line_ids = fields.One2many('hr_suivi_plan_line', 'x_suivi_id', string="Liste",
                                 states={'A': [('readonly', True)], 'T': [('readonly', True)]})
    x_line_p_ids = fields.One2many('hr_suivi_participant_line', 'x_suivi_id', string="Liste Des Participants",
                                   states={'A': [('readonly', True)], 'T': [('readonly', True)]})
    x_mnts = fields.Float(string='Montant Total')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_consultation = fields.Date(string="Date Consultation", default=date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Rechercher'),
        ('V', 'Valider'),
        ('E', "Exécution en cours"),
        ('T', "Terminer"),
        ('A', "Annuler"),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_terminer(self):
        for record in self.x_line_ids:
            if record.etats == 2:
                raise ValidationError(
                    _("Impossible de terminer ce suivi de formation, Vérifiez qu'il n'existe pas de formation non exécutée"))
            else:
                self.write({'state': 'T'})

    def action_en_cours_exe(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self.x_line_ids:
            id = int(vals.id_line)
            id_trienal = int(vals.id_trienal)
            if vals.etats == 1:
                self.env.cr.execute(
                    """UPDATE hr_plan_formation_line SET etat_exe = 1, etat = 'oui' WHERE id = %d AND x_exercice_id = %d and company_id = %d""" % (
                        id, annee, x_struct_id))
                self.env.cr.execute(
                    """UPDATE hr_plan_formation_trienal_line SET etat_exe = 1, etat = 'oui' WHERE id = %d AND x_exercice_id = %d and company_id = %d""" % (
                        id_trienal, annee, x_struct_id))
            else:
                self.env.cr.execute(
                    """UPDATE hr_plan_formation_line SET etat_exe = 2, etat = 'non' WHERE id = %d AND x_exercice_id = %d and company_id = %d""" % (
                        id, annee, x_struct_id))
                self.env.cr.execute(
                    """UPDATE hr_plan_formation_trienal_line SET etat_exe = 2, etat = 'non' WHERE id = %d AND x_exercice_id = %d and company_id = %d""" % (
                        id_trienal, annee, x_struct_id))

    # fonction de remplissage du tableau avec les formations retrouvées afin d'assurer le suivi
    def remplir(self):
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """select L.* from hr_plan_formation_line L, hr_plan_formation P where P.id = L.x_plan_id and P.state = 'A'and L.etat = 'non' and L.x_exercice_id = %d and L.company_id = %d """ % (
                    annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []
            if rows:
                # delete old payslip lines
                vals.x_line_ids.unlink()
                for lines in rows:
                    result.append((0, 0, {'id_line': lines['id'], 'id_trienal': lines['id_plan_trienal'],
                                          'name': lines['name'], 'x_type_session_id': lines['x_type_session_id'],
                                          'domaine': lines['domaine'], 'x_theme': lines['x_theme'],
                                          'x_nbre_paticipant': lines['x_nbre_paticipant'],
                                          'formateur': lines['formateur'], 'x_nbre_session': lines['x_nbre_session'],
                                          'x_date_debut': lines['x_date_debut'], 'x_date_fin': lines['x_date_fin'],
                                          'x_nbre_jours': lines['x_nbre_jours'], 'mnt': lines['mnt'],
                                          'service_demandeurs': lines['service_demandeurs']}))
                vals.x_line_ids = result

                # remplissage de la table de liste des participants
                vals.env.cr.execute(
                    """SELECT PL.* FROM hr_participant_retenus_line PL, hr_plan_formation_line L, hr_plan_formation P WHERE  P.id = L.x_plan_id and PL.x_type_formation_id = L.name and PL.domaine_id = L.domaine and PL.x_theme_id = L.x_theme and P.state = 'A' and L.etat = 'non' and PL.x_exercice_id = %d and PL.company_id = %d""" % (
                        annee, x_struct_id))
                rows1 = vals.env.cr.dictfetchall()
                print('les données', rows1)
                results = []
                # delete old payslip lines
                vals.x_line_p_ids.unlink()
                for lines in rows1:
                    results.append((0, 0, {'x_employee': lines['x_employee_id'], 'x_domaine': lines['domaine_id'],
                                           'x_theme': lines['x_theme_id'], 'x_service': lines['x_service_id'],
                                           'company_id': lines['company_id'], 'x_exercice_id': lines['x_exercice_id']}))
                self.x_line_p_ids = results

                self.write({'state': 'R'})
            else:
                raise ValidationError(_("Pas de données à afficher"))

    def action_annuler(self):
        self.write({'state': 'A'})


# class permettant de recueillir les lignes de la requête
class HrSuiviPlanLine(models.Model):
    _name = "hr_suivi_plan_line"
    x_suivi_id = fields.Many2one('hr_suivi_plan')

    id_line = fields.Integer(string='Id')
    id_trienal = fields.Integer(string='Id trien')
    name = fields.Many2one('hr_type_formation', string="Type Formation", readonly=False)
    x_type_session_id = fields.Many2one('hr_type_session', string='Type Session', readonly=False)
    domaine = fields.Many2one('hr_domaine', string='Domaine', readonly=False)
    x_theme = fields.Many2one('hr_theme', string='Thème', readonly=False)
    formateur = fields.Selection([
        ('Intérieur', 'Intérieur'),
        ('Extérieur', 'Extérieur')
    ], string='Formateur', index=True, readonly=False, copy=False, default='Intérieur')
    x_nbre_paticipant = fields.Integer(string='Nbre de participants')
    x_nbre_session = fields.Integer(string='Nbre de sessions')
    x_nbre_jours = fields.Integer(string='Jours', readonly=True)
    x_date_debut = fields.Date('Date debut', readonly=False)
    x_date_fin = fields.Date('Date fin', readonly=False)
    mnt = fields.Integer(string='Montant', readonly=False)

    etats = fields.Selection([
        ('1', 'Oui'),
        ('2', 'Non'),
    ], string="Exécuté", default=2)
    etat_exe = fields.Selection([
        ('0', 0),
        ('1', 1),
    ], string="Etat", default=0)
    report = fields.Selection([
        ('1', 'Oui'),
        ('2', 'Non'),
    ], string="Report", default=2)
    x_date_debuts = fields.Date('Report debut')
    x_date_fins = fields.Date('Report fin')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)


# classe pour ajouter les particiapants automatiquement
class HrSuiviParticipantsLine(models.Model):
    _name = 'hr_suivi_participant_line'
    x_suivi_id = fields.Many2one('hr_suivi_plan')

    x_employee = fields.Many2one('hr.employee', string='Employé', readonly=False)
    x_domaine = fields.Many2one('hr_domaine', string='Domaine', readonly=False)
    x_theme = fields.Many2one('hr_theme', string='Thème', readonly=False)
    x_service = fields.Many2one('hr_service', string='Service', readonly=False)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    # classe de suivi financier des formations adoptées
    class HrSuiviFinancier(models.Model):
        _name = "hr_suivi_financier"
        name = fields.Many2one('hr_type_formation', string='Type Formation', required=True)
        x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                        default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                        readonly=True)
        company_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
        # x_line_ids = fields.One2many('hr_suivi_financier_line','x_suivi_f_id', string = "Liste")
        x_service_id = fields.Many2one('hr_service', string='Service', required=False)
        current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
        date_debut_op = fields.Date(string="Date debut opération", default=date.today(), readonly=True)
        active = fields.Boolean(string="Etat", default=True)
        x_line_p_ids = fields.One2many('hr_etat_financier_line', 'x_etat_f_id', string="Etat")

        domaine_id = fields.Many2one('hr_domaine', string='Domaine', required=True)
        domaine = fields.Char(string='Domaine')
        x_theme_id = fields.Many2one('hr_theme', string='Thème', required=True)
        x_theme = fields.Char(string='Thème')
        mnt_actuel = fields.Integer(string='Montant Actuel', readonly=True)
        mnt_a_payer = fields.Integer(string='Montant à payer', required=True)
        mnt_restant = fields.Integer(string='Montant restant', readonly=True)
        date_paiement = fields.Date(string="Date paiement", default=date.today(), readonly=True)
        mode_paiement = fields.Many2one('hr_modepaiement', string="Mode paiement", required=True)
        ref_paiement = fields.Char(string="Réf. paiement")
        fichier_joint = fields.Binary(string='Joindre Pièce', attachment=True)

        @api.onchange('x_theme_id')
        def remplir_mt(self):
            for vals in self:
                annee = int(self.x_exercice_id)
                x_struct_id = int(self.company_id)
                x_theme_id = int(self.x_theme_id)
                vals.env.cr.execute(
                    """select (L.mnt_a_soustrair) as mnt from hr_plan_formation_line L, hr_plan_formation P where L.x_plan_id = P.id and L.x_theme = %d and L.x_exercice_id = %d and L.company_id = %d and P.state = 'A' """ % (
                        x_theme_id, annee, x_struct_id))
                rows = vals.env.cr.dictfetchall()

                self.mnt_actuel = rows and rows[0]['mnt']
                self.x_theme = self.x_theme_id.lib_long

        @api.onchange('domaine_id')
        def remplir_domaine(self):
            if self.domaine_id:
                self.domaine = self.domaine_id.lib_long

        @api.onchange('mnt_a_payer')
        def remplir_mt_rest(self):
            if self.mnt_a_payer:
                self.mnt_restant = self.mnt_actuel - self.mnt_a_payer

        # fonction de validation du paiement
        def action_valider(self):
            for record in self:
                val_id_financ = int(record.id)
                val_id_domaine = int(record.domaine_id)
                val_id = int(record.x_theme_id)
                x_struct_id = int(self.company_id)
                x_exo_id = int(self.x_exercice_id)
                val_mnt_act = int(record.mnt_actuel)
                val_mnt_a_p = int(record.mnt_a_payer)
                val_mnt_rest = int(record.mnt_restant)
                date = str(self.date_paiement.strftime("%Y-%m-%d"))
                domaine = str(record.domaine_id.lib_long)
                theme = str(record.x_theme_id.lib_long)

                if val_mnt_a_p > val_mnt_act:
                    raise ValidationError(
                        _('Vous avez saisi un montant supérieur au montant restant, veuillez ré-saisir un montant inférieur ou égal au montant restant à payer svp!'))
                elif val_mnt_a_p == 0:
                    raise ValidationError(_('Saisissez un montant valide svp!'))
                else:
                    # on fait le update ici
                    record.env.cr.execute(
                        """UPDATE hr_plan_formation_line set mnt_a_soustrair = mnt_a_soustrair - %d WHERE x_theme = %d AND company_id = %d AND x_exercice_id = %d""" % (
                            val_mnt_a_p, val_id, x_struct_id, x_exo_id))
                    # on fait l'insertion ici
                    record.env.cr.execute(
                        """INSERT INTO hr_etat_financier_line(x_etat_f_id,domaine_id,domaine,x_theme_id,x_theme,mnt_actuel,mnt_a_payer,mnt_restant,date_paiement,company_id,x_exercice_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (val_id_financ, val_id_domaine, domaine, val_id, theme, val_mnt_act, val_mnt_a_p, val_mnt_rest,
                         date, x_struct_id, x_exo_id))

            self.mnt_a_payer = 0

    # class permettant d'avoir l'etat de paiement des formations
    class HrEtatSuiviFinancierLine(models.Model):
        _name = "hr_etat_financier_line"
        x_etat_f_id = fields.Many2one('hr_suivi_financier')
        domaine_id = fields.Integer(string='Id Domaine')
        domaine = fields.Char(string='Domaine', readonly=True)
        x_theme_id = fields.Integer(string='Id Thème')
        x_theme = fields.Char(string='Thème', readonly=True)
        mnt_actuel = fields.Integer(string='Montant Actuel', readonly=True)
        mnt_a_payer = fields.Integer(string='Montant à payer', readonly=True)
        mnt_restant = fields.Integer(string='Montant restant', readonly=True)
        date_paiement = fields.Date(string="Date paiement", readonly=True)
        x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                        default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
        company_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)

    # classe de saisie consultation plan de formation
    class HrConsultationPlanFormation(models.Model):
        _name = "hr_consult_plan"
        _order = 'sequence, id'
        sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
        name = fields.Char(string='Code stage', readonly=True)
        _rec_name = 'x_exercice_id'

        x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                        default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
        company_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
        x_mnts = fields.Float(string='Montant Total')
        current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
        date_consultation = fields.Date(string="Date Consultation", default=date.today(), readonly=True)
        x_line_ids = fields.One2many('hr_consult_plan_line', 'x_cons_id', string="Liste", readonly=True)
        x_line_p_ids = fields.One2many('hr_consu_suivi_participant_line', 'x_cons_id', string="Liste Particiapnts",
                                       readonly=True)

        # fonction de remplissage du tableau
        def remplissage(self):
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            for vals in self:
                vals.env.cr.execute(
                    """select * from hr_plan_formation_line L, hr_plan_formation P where P.id = L.x_plan_id and P.state = 'A' and L.x_exercice_id = %d and L.company_id = %d """ % (
                        annee, x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []
                print('données', rows)

                # delete old payslip lines
                vals.x_line_ids.unlink()
                self.x_mnts = 0.0
                for lines in rows:
                    result.append((0, 0, {'name': lines['name'], 'x_type_session_id': lines['x_type_session_id'],
                                          'domaine': lines['domaine'], 'x_theme': lines['x_theme'],
                                          'formateur': lines['formateur'],
                                          'x_nbre_paticipant': lines['x_nbre_paticipant'],
                                          'x_nbre_session': lines['x_nbre_session'],
                                          'x_nbre_jours': lines['x_nbre_jours'], 'x_date_debut': lines['x_date_debut'],
                                          'x_date_fin': lines['x_date_fin'], 'x_lieu_id': lines['lieu_f'],
                                          'mnt': lines['mnt'], 'service_demandeur': lines['service_demandeurs']}))
                    self.x_mnts += lines['mnt']
                vals.x_line_ids = result

                # remplissage de la table de liste des participants
                vals.env.cr.execute(
                    """SELECT * FROM hr_participant_retenus_line  WHERE  x_exercice_id = %d and company_id = %d""" % (
                        annee, x_struct_id))
                rows1 = vals.env.cr.dictfetchall()
                print('les données', rows1)
                results = []
                # delete old payslip lines
                vals.x_line_p_ids.unlink()
                for lines in rows1:
                    results.append((0, 0, {'x_employee': lines['x_employee_id'], 'x_domaine': lines['domaine_id'],
                                           'x_theme': lines['x_theme_id'], 'x_service': lines['x_service_id'],
                                           'company_id': lines['company_id'], 'x_exercice_id': lines['x_exercice_id']}))
                self.x_line_p_ids = results

    # class permettant de recueillir les lignes de la requête
    class HrConsultationPlanFormationLine(models.Model):
        _name = "hr_consult_plan_line"

        x_cons_id = fields.Many2one('hr_consult_plan')
        name = fields.Many2one('hr_type_formation', string='Type Formation')

        x_type_session_id = fields.Many2one('hr_type_session', string='Type Session')

        domaine = fields.Many2one('hr_domaine', string='Domaine')
        x_theme = fields.Many2one('hr_theme', string='Thème')
        formateur = fields.Char(string='Formateur')
        x_nbre_paticipant = fields.Integer(string='Nbre de participants')
        x_nbre_session = fields.Integer(string='Nbre de sessions')
        x_nbre_jours = fields.Integer(string='Nbre de jours')
        x_date_debut = fields.Date(string='Date debut')
        x_date_fin = fields.Date(string='Date fin')
        x_lieu_id = fields.Many2one('hr_lieu', string='Lieu')
        mnt = fields.Float(string='Montant')
        service_demandeur = fields.Integer(string='Nbre Service')

    # classe pour ajouter les particiapants automatiquement
    class HrConsultationSuiviParticipantsLine(models.Model):
        _name = 'hr_consu_suivi_participant_line'
        x_cons_id = fields.Many2one('hr_consult_plan')

        x_employee = fields.Many2one('hr.employee', string='Employé', readonly=False)
        x_domaine = fields.Many2one('hr_domaine', string='Domaine', readonly=False)
        x_theme = fields.Many2one('hr_theme', string='Thème', readonly=False)
        x_service = fields.Many2one('hr_service', string='Service', readonly=False)
        x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                        default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                        readonly=True)
        company_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id, readonly=True)


# classe permettant à chaque service de faire l'inscription des participants par rapport aux thèmes de son service retenu
class HrParticipants(models.Model):
    _name = 'hr_participant'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of participants.", default=10)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    x_type_formation_id = fields.Many2one('hr_type_formation', string='Type Formation', required=True)
    x_type_formation = fields.Char(string='Type Formation')
    name = fields.Many2one('hr_domaine', string='Domaine', required=True)
    domaine = fields.Char(string='Domaine')
    x_theme_id = fields.Many2one('hr_theme', string='Thème', required=True)
    x_theme = fields.Char(string='Thème')
    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_employee = fields.Char(string='Employé')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_service_id = fields.Many2one('hr_service', string='Service', required=True)
    x_service = fields.Char(string='Service')
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_participant_line', 'name', readonly=True)

    @api.onchange('x_type_formation_id')
    def remplir_type_f(self):
        if self.x_type_formation_id:
            self.x_type_formation = self.x_type_formation_id.lib_long

    @api.onchange('x_theme_id')
    def remplir_theme(self):
        if self.x_theme_id:
            self.x_theme = self.x_theme_id.lib_long

    @api.onchange('name')
    def remplir_domaine(self):
        if self.name:
            self.domaine = self.name.name

    @api.onchange('employee_id')
    def remplir_employe(self):
        if self.employee_id:
            self.x_employee = self.employee_id.name

    @api.onchange('x_service_id')
    def remplir_service(self):
        if self.x_service_id:
            self.x_service = self.x_service_id.name

    # fonction de validation du participant
    def action_valider(self):
        for record in self:
            val_id = int(self.id)
            val_id_domaine = int(record.name)
            val_id_type = int(record.x_type_formation_id)
            val_id_theme = int(record.x_theme_id)
            val_id_emp = int(record.employee_id)
            val_id_service = int(record.x_service_id)
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)
            domaine = str(record.name.lib_long)
            type = str(record.x_type_formation_id.lib_long)
            theme = str(record.x_theme_id.lib_long)
            employe = str(record.employee_id.name)
            service = str(record.x_service_id.name)
            record.env.cr.execute(
                """INSERT INTO hr_participant_line(name,x_type_formation_id,x_type_formation,domaine_id,domaine,x_theme_id,x_theme,x_employee_id,x_employee,x_service_id,x_service,x_exercice_id,company_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (val_id, val_id_type, type, val_id_domaine, domaine, val_id_theme, theme, val_id_emp, employe,
                 val_id_service, service, x_exo_id, x_struct_id))


# classe pour ajouter les particiapants automatiquement
class HrParticipantsLine(models.Model):
    _name = 'hr_participant_line'
    name = fields.Many2one('hr_participant')
    x_type_formation_id = fields.Integer(string='Id type formation')
    x_type_formation = fields.Char(string='Type formation', readonly=True)
    domaine_id = fields.Integer(string='Id Domaine')
    domaine = fields.Char(string='Domaine', readonly=True)
    x_theme_id = fields.Integer(string='Id Thème')
    x_theme = fields.Char(string='Thème', readonly=True)
    x_employee_id = fields.Integer(string='Employé', readonly=True)
    x_employee = fields.Char(string='Employé', readonly=True)
    x_service_id = fields.Integer(string='id_Service', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)


# classe permettant de mettre en place la liste des participant définitifs aux différentes formations
class HrParticipantsRetenus(models.Model):
    _name = 'hr_participant_retenus'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of participants.", default=10)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    x_type_formation_id = fields.Many2one('hr_type_formation', string='Type Formation', required=True)
    x_type_formation = fields.Char(string='Type Formation')
    name = fields.Many2one('hr_domaine', string='Domaine', required=True)
    domaine = fields.Char(string='Domaine')
    x_theme_id = fields.Many2one('hr_theme', string='Thème', required=True)
    x_theme = fields.Char(string='Thème')
    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_employee = fields.Char(string='Employé')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_service_id = fields.Many2one('hr_service', string='Service', required=True)
    x_service = fields.Char(string='Service')
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_participant_retenus_line', 'name', readonly=True)

    @api.onchange('x_type_formation_id')
    def remplir_type_f(self):
        if self.x_type_formation_id:
            self.x_type_formation = self.x_type_formation_id.lib_long

    @api.onchange('x_theme_id')
    def remplir_theme(self):
        if self.x_theme_id:
            self.x_theme = self.x_theme_id.lib_long

    @api.onchange('name')
    def remplir_domaine(self):
        if self.name:
            self.domaine = self.name.name

    @api.onchange('employee_id')
    def remplir_employe(self):
        if self.employee_id:
            self.x_employee = self.employee_id.name

    @api.onchange('x_service_id')
    def remplir_service(self):
        if self.x_service_id:
            self.x_service = self.x_service_id.name

    # fonction de validation du participant
    def action_valider(self):
        for record in self:
            val_id = int(self.id)
            val_id_domaine = int(record.name)
            val_id_type = int(record.x_type_formation_id)
            val_id_theme = int(record.x_theme_id)
            val_id_emp = int(record.employee_id)
            val_id_service = int(record.x_service_id)
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)
            domaine = str(record.name.lib_long)
            type = str(record.x_type_formation_id.lib_long)
            theme = str(record.x_theme_id.lib_long)
            employe = str(record.employee_id.name)
            service = str(record.x_service_id.name)
            record.env.cr.execute(
                """INSERT INTO hr_participant_retenus_line(name,x_type_formation_id,x_type_formation,domaine_id,domaine,x_theme_id,x_theme,x_employee_id,x_employee,x_service_id,x_service,x_exercice_id,company_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (val_id, val_id_type, type, val_id_domaine, domaine, val_id_theme, theme, val_id_emp, employe,
                 val_id_service, service, x_exo_id, x_struct_id))


# classe permettant de mettre en place la liste des participant définitifs aux différentes formations line
class HrParticipantsRetenusLine(models.Model):
    _name = 'hr_participant_retenus_line'
    name = fields.Many2one('hr_participant_retenus')
    x_type_formation_id = fields.Integer(string='Id type formation')
    x_type_formation = fields.Char(string='Type formation', readonly=True)
    domaine_id = fields.Integer(string='Id Domaine')
    domaine = fields.Char(string='Domaine', readonly=True)
    x_theme_id = fields.Integer(string='Id Thème')
    x_theme = fields.Char(string='Thème', readonly=True)
    x_employee_id = fields.Integer(string='Employé', readonly=True)
    x_employee = fields.Char(string='Employé', readonly=True)
    x_service_id = fields.Integer(string='id_Service', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    @api.onchange('employee_id')
    def remplir_service(self):
        if self.employee_id:
            self.x_service = self.employee_id.hr_service.name
            self.x_fonction = self.employee_id.x_fonction_id.name


# Class pour gerer la centralisation des participants de chaque service de chaque EPE
class HrCentralisationParticipants(models.Model):
    _name = "hr_central_participant"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string="Code", size=50, readonly=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année',
                                     default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_central_participant_line', 'x_besoin_central_id',
                                 string='Liste Des Domaines de formations', readonly=True)
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
                    """SELECT domaine_id,domaine,x_theme_id,x_theme,x_employee_id,x_employee,x_service_id,x_service FROM hr_participant_line WHERE x_exercice_id = %s AND company_id = %s GROUP BY domaine_id,domaine,x_theme_id,x_theme,x_employee_id,x_employee,x_service_id,x_service""",
                    (annee, x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'domaine_id': line['domaine_id'], 'domaine': line['domaine'],
                                          'x_theme_id': line['x_theme_id'], 'x_theme': line['x_theme'],
                                          'x_employee_id': line['x_employee_id'], 'x_employee': line['x_employee'],
                                          'x_service_id': line['x_service_id'], 'x_service': line['x_service']}))
                self.x_line_ids = result

            x_user_id = int(self.current_user)
            self.env.cr.execute(
                """select (R.id) AS id, (R.name) AS service, (R.code) AS code From ref_service R, res_users U where R.id = U.x_service_id and U.id = %s and U.company_id = %s""",
                (x_user_id, x_struct_id))
            rows = self.env.cr.dictfetchall()
            self.service_traiteur = rows and rows[0]['service']

            self.env.cr.execute("select no_code from hr_cpte_central_participant where company_id = %d" % (x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'CP' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO hr_cpte_central_participant(company_id,no_code)  VALUES(%d , %d)""" % (
                        x_struct_id, vals))
            else:

                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                self.name = 'CP' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE hr_cpte_central_participant SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'F'})


# class pour gerer les lignes de centralisation des participants annuels en formation
class HrCentralisationParticipantsLine(models.Model):
    _name = "hr_central_participant_line"
    x_besoin_central_id = fields.Many2one('hr_central_participant')
    domaine_id = fields.Integer(string='Id Domaine')
    domaine = fields.Char(string='Domaine', readonly=True)
    x_theme_id = fields.Integer(string='Id Thème')
    x_theme = fields.Char(string='Thème', readonly=True)
    x_employee_id = fields.Integer(string='Employé', readonly=True)
    x_employee = fields.Char(string='Employé', readonly=True)
    x_service_id = fields.Integer(string='id_Service')
    x_service = fields.Char(string='Service')


# classe de saisie consultation formation suivie par les employés
class HrConsultationPlanFormationEmploye(models.Model):
    _name = "hr_consult_plan_employe"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    name = fields.Char(string='Code stage', readonly=True)
    _rec_name = 'x_employee_id'
    x_employee_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_mnts = fields.Float(string='Montant Total')
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_consultation = fields.Date(string="Date Consultation", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_consult_plan_emp_line', 'x_cons_id', string="Liste", readonly=True)

    # fonction de remplissage du tableau
    def remplissage(self):
        x_emp = int(self.x_employee_id)
        annee = int(self.x_exercice_id)
        x_struct_id = int(self.company_id)
        for vals in self:
            vals.env.cr.execute(
                """SELECT PL.* , (E.matricule) as mat, (E.matricule_genere) as mat_c FROM hr_suivi_participant_line PL, hr_employee E  WHERE E.id = PL.x_employee AND PL.x_employee = %d AND PL.x_exercice_id = %d and PL.company_id = %d """ % (
                    x_emp, annee, x_struct_id))
            rows = vals.env.cr.dictfetchall()
            result = []
            print('données', rows)

            # delete old payslip lines
            vals.x_line_ids.unlink()
            for lines in rows:
                result.append((0, 0, {'mat': lines['mat'], 'mat_c': lines['mat_c'], 'domaine': lines['x_domaine'],
                                      'x_theme': lines['x_theme'], 'x_service_id': lines['x_service']}))
            vals.x_line_ids = result


# class permettant de recueillir les lignes de la requête
class HrConsultationPlanFormationEmployeLine(models.Model):
    _name = "hr_consult_plan_emp_line"

    x_cons_id = fields.Many2one('hr_consult_plan_employe')
    mat = fields.Char(string='Mlle Fonctionnaire', readonly=True)
    mat_c = fields.Char(string='Mlle Contractuel', readonly=True)
    domaine = fields.Many2one('hr_domaine', string='Domaine', readonly=True)
    x_theme = fields.Many2one('hr_theme', string='Thème', readonly=True)
    x_service_id = fields.Many2one('hr_service', string='Service', readonly=True)


# classe de saisie appreciation individuel des employés
class HrAppreciationIndividuelle(models.Model):
    _name = "hr_appreciation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    name = fields.Char(string='Code stage', readonly=True)
    _rec_name = 'x_exercice_id'

    x_theme_id = fields.Many2one('hr_theme', string='Thème', required=True, states={'R': [('readonly', True)]})
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    appreciation = fields.Text(string='Votre appréciation', required=True, states={'R': [('readonly', True)]})
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_appreciation = fields.Date(string="Date Consultation", default=date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('C', 'Confirmer'),
        ('R', 'Receptionner'),
        ('An', 'Annuler'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # fonction de changement d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    def action_valider(self):
        self.write({'state': 'V'})

    def action_confirmer(self):
        self.write({'state': 'C'})

    def action_recep(self):
        self.write({'state': 'R'})

    def action_ann(self):
        self.write({'state': 'An'})

    # classe de centralisation appreciation individuel des employés


class HrAppreciationCentralisation(models.Model):
    _name = "hr_appreciation_centralisation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    name = fields.Char(string='Code stage', readonly=True)
    _rec_name = 'x_exercice_id'

    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_central = fields.Date(string="Date Centralisation", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_appreciation_centralisation_line', 'x_central_id', string="Liste Centralisation")

    # fonction de remplissage du tableau
    def centraliser(self):
        if self.x_exercice_id:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            for vals in self:
                vals.env.cr.execute(
                    """SELECT (A.appreciation) as app ,(T.name) as theme, (P.name) as nom FROM hr_appreciation A, res_users U, res_partner P,hr_theme T WHERE A.current_user = U.id and T.id = A.x_theme_id AND U.partner_id = P.id AND A.x_exercice_id = %d AND A.company_id = %d AND A.state = 'R' GROUP BY theme,nom,app""" % (
                        annee, x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'user_id': line['nom'], 'them': line['theme'], 'app': line['app']}))
                self.x_line_ids = result


# classe de centralisation appreciation  des employés
class HrAppreciationCentralisationLine(models.Model):
    _name = "hr_appreciation_centralisation_line"
    x_central_id = fields.Many2one('hr_appreciation_centralisation')
    user_id = fields.Char('Employé')
    them = fields.Char('Thème')
    app = fields.Text('Appréciation')
    x_exercice_id = fields.Many2one('ref_exercice', string="Année", required=True,
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
