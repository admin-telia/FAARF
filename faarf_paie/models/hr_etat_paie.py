import babel
from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from num2words import num2words
from odoo.exceptions import UserError, ValidationError



# Etat livre paie
class HrLivrePaie(models.TransientModel):
    _name = "hr_livrepaie"
    type_emp = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_date_debut = fields.Date(string='Date début', required=True)
    x_date_fin = fields.Date(string='Date fin', required=True)
    x_line_ids = fields.One2many('hr_livrepaie_line', 'x_livre_id', string="Liste des élements de salaire",
                                 readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    date_op = fields.Datetime('Date/heure opération', default=datetime.today(), readonly=True)
    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    def action_rech(self):
        pass


class HrLivrePaieLine(models.TransientModel):
    _name = "hr_livrepaie_line"
    x_livre_id = fields.Many2one('hr_livrepaie')

    numero = fields.Integer(string='N°', readonly=True)
    mat = fields.Char(string='Mle Fct')
    mat_c = fields.Char(string='Mle Ctrct')
    nom = fields.Char(string='Nom/Prénom(s)')
    num_cnss = fields.Char('N°CNSS')
    categorie = fields.Char(string="Catégorie")
    echelle = fields.Char(string='Echelle')
    echelon = fields.Char(string='Echelon')
    emploi = fields.Char(string='Emploi')
    fonction = fields.Char(string='Fonction')

    salaire_base = fields.Float(string='Base EPE')

    resp = fields.Float(string='Indemn. Responsabilité')
    astr = fields.Float(string='Indemn. Astreinte')
    loge = fields.Float(string='Indemn. Logement')
    tech = fields.Float(string='Indemn. Technicité')
    spec = fields.Float(string='Indemn. Spécifique RH')
    spec_it = fields.Float(string='Indemn. Spécifique IT')
    spec_ifc = fields.Float(string='Indemn. Spécifique ICF')
    transp = fields.Float(string='Indemn. Transport')
    inf = fields.Float(string='Indemn. Informatique')
    reseau = fields.Float(string='Indemn. Exploitation-reseau')
    financ = fields.Float(string='Indemn. resp.financière')

    x_indem_garde = fields.Float(string="Indemn.Garde")
    x_indem_risque = fields.Float(string="Indemn.Risque.Contagion")
    x_indem_suj = fields.Float(string="Indemn.Sujétion Géographique")
    x_indem_form = fields.Float(string="Indemn.Formation")
    x_indem_caisse = fields.Float(string="Indemn.Caisse")
    x_indem_veste = fields.Float(string="Indemn.Vestimentaire")

    alloc_f = fields.Float(string='Allocation familliale')
    renum_t = fields.Float(string='Rénumeration totale')
    sal_brut = fields.Float(string='Salaire brut')
    nbre_charge = fields.Integer(string='Nbre Charge')
    mnt_agent_carfo = fields.Float(string='Cotisation agent CARFO')
    mnt_patronal_carfo = fields.Float(string='Cotisation patronal CARFO')

    mnt_agent_cnss = fields.Float(string='Cotisation agent CNSS')
    mnt_patronal_cnss = fields.Float(string='Cotisation patronal CNSS')

    base_imp = fields.Float(string='Base imposable')
    iuts = fields.Float(string='IUTS')
    foner = fields.Float(string='Retenue Foner')
    retenue_totale = fields.Float(string='Retenue Total')
    avance_sal = fields.Float(string='Base FP')
    autre_mnt = fields.Float(string='Indemn. Spécifique IRP')
    net = fields.Float(string='Salaire net')
    x_indem_prime_rendement = fields.Float(string='Prime de rendement')


# Etat element salaire
class HrEtatEltSalaire(models.TransientModel):
    _name = "hr_etat_elt_salaire"
    name = fields.Char(string='Intitulé Etat', required=True)
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=True)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_elt_salaire_line', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    state = fields.Selection(
        string='State',
        selection=[('B', 'Brouillon'),
                   ('V', 'Validé'),
                   ('E', 'Engagé'), ],
        required=False, default="B")

    def valider(self):
        result = self.env['hr_etat_elt_salaire'].search((
            ('x_elt_sal_id.id', '=', self.x_elt_sal_id.id),
            ('x_type_employe_id.id', '=', self.x_type_employe_id.id),
            ('state', '!=', 'B'),
        ))
        for r in result:
            mois_courant = self.x_date_debut.month
            annee_courant = self.x_date_debut.year

            mois = r.x_date_debut.month
            annee = r.x_date_debut.year

            if mois_courant == mois and annee_courant == annee:
                raise ValidationError("Le borderau de cette période a été déjà produit")
        self.state = "V"


    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_elt_sal_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip.line'].search([('slip_id.struct_id', '=', self.x_type_employe_id.id),
                                                           ('slip_id.date_from', '>=', self.x_date_debut),
                                                           ('slip_id.date_to', '<=', self.x_date_fin),
                                                           ('salary_rule_id', '=', self.x_elt_sal_id.id)])
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': e.employee_id.matricule,
                                        'x_matricule_c': e.employee_id.matricule,
                                        'x_mnt': e.amount, 'numero': numero
                                        }))
                self.x_mnts = self.x_mnts + e.amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        pass


class HrEtatEltSalaireLine(models.TransientModel):
    _name = "hr_etat_elt_salaire_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_element_id = fields.Many2one('hr_etat_elt_salaire')
    x_mnt = fields.Float(string='Montant')


# Etat cotisation CARFO Part employe
class HrEtatCarfo(models.TransientModel):
    _name = 'hr_etat_carfo'
    name = fields.Char(string='Intitulé Etat', required=True)
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=True)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_carfo', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_elt_sal_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip.line'].search([('slip_id.struct_id', '=', self.x_type_employe_id.id),
                                                           ('slip_id.date_from', '>=', self.x_date_debut),
                                                           ('slip_id.date_to', '<=', self.x_date_fin),
                                                           ('salary_rule_id', '=', self.x_elt_sal_id.id)])
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            for e in elements:
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': e.employee_id.id,
                                        'x_matricule_c': e.employee_id.id,
                                        'x_mnt': e.amount
                                        }))
                self.x_mnts = self.x_mnts + e.amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        pass

class HrEtatCarfoLine(models.TransientModel):
    _name = "hr_etat_carfo_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_element_id = fields.Many2one('hr_etat_elt_salaire')
    x_mnt = fields.Float(string='Montant')


# Etat mode paiement
class HrReportMode(models.TransientModel):
    _name = "hr_reportmode"
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)
    description = fields.Text(string='Description')
    _rec_name = 'x_mode_paiements'
    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_mode_paiements = fields.Selection([
        ('billetage', 'Billetage'),
        ('virement', 'Virement'),
    ], string="Mode de Paiement", default='billetage', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)), required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_reportmode_line', 'x_report_id', string="Liste des concernés")
    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Datetime(string='Date impression', default=datetime.today(), readonly=True)

    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau
    def remplissage(self):
        if self.x_mode_paiements and self.x_type_employe_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip'].search([('x_mode_paiement', '=', self.x_mode_paiements),
                                                      ('struct_id', '=', self.x_type_employe_id.id),
                                                      ('date_from', '>=', self.x_date_debut),
                                                      ('date_to', '<=', self.x_date_fin)])
            print(elements)
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            print("Max")
            self.x_line_ids.unlink()
            self.x_mnts = 0
            for e in elements:

                amount = 0
                for l in e.line_ids:
                    if l.code == 'x_net_payer':
                        amount = l.amount
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': e.employee_id.matricule,
                                        'x_sal_net': amount, 'numb': e.num_banque,
                                        'x_emploi': e.employee_id.x_emploi_id.name,
                                        'x_fonction': e.employee_id.x_fonction_id.name,
                                        }))
                self.x_mnts = self.x_mnts + amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self.x_mnts, lang='fr')


class HrReportModeLine(models.TransientModel):
    _name = "hr_reportmode_line"
    x_report_id = fields.Many2one('hr_reportmode')
    x_matricule = fields.Char(string='Matricule')
    name = fields.Char(string='Employé')
    numb = fields.Char(string='N° Compte')
    x_emploi = fields.Char(string='Emploi')
    x_fonction = fields.Char(string='Fonction')
    x_sal_net = fields.Float(string='Salaire net')
    x_mnt = fields.Float(string='Montant')
    x_type_struct = fields.Char(string='Type employé')


# Etat par banque
class HrReportBanque(models.TransientModel):
    _name = "hr_reportbanque"
    _rec_name = 'x_banq_id'
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)
    description = fields.Text(string='Description')
    x_banq_id = fields.Many2one('res.bank', string='Nom banque', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)), required=True)

    periode = fields.Char(store=True, readonly=True, string='Période')
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_reportbanque_line', 'x_report_id', string="Liste des concernés")
    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')
    date_op = fields.Datetime(string='Date impression', default=datetime.today(), readonly=True)

    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    def remplissages(self):
        if self.x_banq_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip'].search([('x_banque_id.id', '=', self.x_banq_id.id),
                                                      ('date_from', '>=', self.x_date_debut),
                                                      ('date_to', '<=', self.x_date_fin)])
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            for e in elements:
                amount = 0
                for l in e.line_ids:
                    if l.code == 'x_net_payer':
                        amount = l.amount
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': e.employee_id.id,
                                        'x_sal_net': amount, 'numb': e.num_banque,
                                        'x_emploi': e.contract_id.x_emploi_id.name,
                                        'x_fonction': e.contract_id.x_fonction_id.name,
                                        }))
                self.x_mnts = self.x_mnts + amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self.x_mnts, lang='fr')


class HrReportBanqueLine(models.TransientModel):
    _name = "hr_reportbanque_line"
    x_report_id = fields.Many2one('hr_reportbanque', ondelete="cascade")

    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Matricule')
    name = fields.Char(string='Employé')
    numb = fields.Char(string='N° Compte')
    x_emploi = fields.Char(string='Emploi')
    x_fonction = fields.Char(string='Fonction')
    x_sal_net = fields.Float(string='Salaire net')
    x_mnt = fields.Float(string='Montant')
