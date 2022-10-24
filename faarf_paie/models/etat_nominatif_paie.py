from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from num2words import num2words
from odoo.exceptions import UserError, ValidationError


# heritage de la classe des elements de salaires
class HrElementSalaire(models.Model):
    _inherit = "hr.salary.rule"
    code_etat_nominatif = fields.Char(string='Code Etat Nominatif', required=False)


# classe de parametrage des elements d'imputation
class HrImputationElement(models.Model):
    _name = 'hr_elementimputation'
    elt_salaire_id = fields.Many2one('hr.salary.rule', string='Element Salaire')
    type_id = fields.Many2one('hr.payroll.structure', string='Type personnel')
    titre_id = fields.Many2one('budg_titre', string='Titre')
    section_id = fields.Many2one('budg_section', string='Section')
    chapitre_id = fields.Many2one('budg_chapitre', string='Chapitre')
    article_id = fields.Many2one('budg_param_article', string='Article')
    paragraphe_id = fields.Many2one('budg_paragraphe', string='Paragraphe')
    rubrique_id = fields.Many2one('budg_rubrique', string='Rubrique')

    @api.model
    def create(self, vals):
        r = self.env['hr_elementimputation'].search([
            ('elt_salaire_id.id', '=', vals.get("elt_salaire_id")),
            ('type_id.id', '=', vals.get("type_id")),
        ])
        if r:
            raise ValidationError("Cet élement a été déjà paramétré")

        result = super(HrImputationElement, self).create(vals)
        return result


class HrBorderauPaie(models.Model):
    _name = 'hr_bordereau_paie'
    name = fields.Char(string='Intitulé Etat', required=True, compute="calcul_name")
    num = fields.Char(string='N°', required=False)
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=True)
    # x_elt_ra_sal_id = fields.Many2one('hr.salary.rule', string='Rappel Element', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_bordereau_paie_line', 'x_borderau_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    titre_id = fields.Many2one('budg_titre', string='Titre', compute="cal_imputation")
    section_id = fields.Many2one('budg_section', string='Section', compute="cal_imputation")
    chapitre_id = fields.Many2one('budg_chapitre', string='Chapitre', compute="cal_imputation")
    article_id = fields.Many2one('budg_article', string='Article', compute="cal_imputation")
    paragraphe_id = fields.Many2one('budg_paragraphe', string='Paragraphe', compute="cal_imputation")
    rubrique_id = fields.Many2one('budg_rubrique', string='Rubrique', compute="cal_imputation")

    state = fields.Selection(
        string='State',
        selection=[('B', 'Brouillon'),
                   ('V', 'Validé'),
                   ('A', 'Annulé'),
                   ('E', 'Engagé'), ],
        required=False, default="B")

    def unlink(self):
        for val in self:
            if val.state not in ('B', 'A'):
                raise UserError(_('Vous ne pouvez pas supprimer ce bordereau'))

    def valider(self):
        result = self.env['hr_bordereau_paie'].search((
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

        rb_compteur = self.env['hr_paie_compt_bord_paie'].search([])
        nombre = 1
        if rb_compteur:
            nombre = rb_compteur.nombre + 1
            rb_compteur.nombre = nombre
            nombre = str(nombre).zfill(8)
        else:
            self.env['hr_paie_compt_bord_paie'].create({
                'nombre': 1,
            })
            nombre = str(nombre).zfill(8)
        self.state = "V"
        self.num = nombre

    @api.depends('x_elt_sal_id', 'periode')
    def cal_imputation(self):
        for val in self:
            imp = self.env['hr_elementimputation'].search([
                ('x_type_employe_id.id', '=', val.x_type_employe_id.id),
                ('x_elt_sal_id.id', '=', val.x_elt_sal_id.id)])

            if imp:
                for rec in imp:
                    val.titre_id = rec.titre_id
                    val.section_id = rec.section_id
                    val.chapitre_id = rec.chapitre_id
                    val.article_id = rec.article_id
                    val.paragraphe_id = rec.paragraphe_id
                    val.rubrique_id = rec.rubrique_id
            else:
                val.titre_id = None
                val.section_id = None
                val.chapitre_id = None
                val.article_id = None
                val.paragraphe_id = None
                val.rubrique_id = None


    @api.depends('x_elt_sal_id', 'periode')
    def calcul_name(self):
        for val in self:
            if val.x_elt_sal_id and val.periode:
                val.name = "Etat nominatif de paie " + val.x_elt_sal_id.name + " " + val.periode
            else:
                val.name = "-"

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
        elt_salaire_ids = self.env['hr.salary.rule'].search([
            '|',
            ('id', '=', self.x_elt_sal_id.id),
            ('code_etat_nominatif', '=', self.x_elt_sal_id.code_etat_nominatif)])

        if self.x_type_employe_id and self.x_elt_sal_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip.line'].search([('slip_id.struct_id', '=', self.x_type_employe_id.id),
                                                           ('slip_id.date_from', '>=', self.x_date_debut),
                                                           ('slip_id.date_to', '<=', self.x_date_fin),
                                                           ('salary_rule_id', 'in', elt_salaire_ids.ids),
                                                           ('slip_id.state', '=', 'done')])
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1
                if e.employee_id.x_type_employe_id.code == 'CTRCT':
                    x_matricule = e.employee_id.matricule_genere
                else:
                    x_matricule = e.employee_id.matricule
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': x_matricule,
                                        'x_mnt': e.amount, 'numero': numero, 'x_element': e.name }))
                self.x_mnts = self.x_mnts + e.amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')


class HHrBorderauPaieLine(models.TransientModel):
    _name = "hr_bordereau_paie_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle')
    x_element = fields.Char(string='Element')
    x_borderau_id = fields.Many2one('hr_bordereau_paie')
    x_mnt = fields.Float(string='Montant')

class HrPaieBordereauPaieCompteur(models.Model):
    """Definition de la table credit"""

    _name = 'hr_paie_compt_bord_paie'

    nombre = fields.Integer(string='Nombre', required=False)