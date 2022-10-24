import babel
from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from num2words import num2words
from odoo.exceptions import UserError, ValidationError

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
    x_line_ids = fields.One2many('hr_etat_carfo_line', 'x_element_id', string="Liste des élements")

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
    x_element_id = fields.Many2one('hr_etat_carfo')
    x_mnt = fields.Float(string='Montant')

# Etat cotisation CARFO Part Patronale
class HrEtatCarfoPat(models.TransientModel):
    _name = 'hr_etat_carfo_pat'
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
    x_line_ids = fields.One2many('hr_etat_carfo_pat_line', 'x_element_id', string="Liste des élements")

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

class HrEtatCarfoLinePat(models.TransientModel):
    _name = "hr_etat_carfo_pat_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_element_id = fields.Many2one('hr_etat_carfo_pat')
    x_mnt = fields.Float(string='Montant')


# Etat cotisation CNSS Part employe
class HrEtatCNSS(models.TransientModel):
    _name = 'hr_etat_cnss'
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
    x_line_ids = fields.One2many('hr_etat_cnss_line', 'x_element_id', string="Liste des élements")

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

class HrEtatCNSSLine(models.TransientModel):
    _name = "hr_etat_cnss_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_element_id = fields.Many2one('hr_etat_cnss')
    x_mnt = fields.Float(string='Montant')

# Etat cotisation CARFO Part Patronale
class HrEtatCNSSPat(models.TransientModel):
    _name = 'hr_etat_cnss_pat'
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
    x_line_ids = fields.One2many('hr_etat_cnss_pat_line', 'x_element_id', string="Liste des élements")

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

class HrEtatCNSSLinePAT(models.TransientModel):
    _name = "hr_etat_cnss_pat_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_element_id = fields.Many2one('hr_etat_cnss_pat')
    x_mnt = fields.Float(string='Montant')