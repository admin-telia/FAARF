from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


# heritage de la classe employee
class HrEmployees(models.Model):
    _inherit = "hr.employee"

    x_rappel_ids = fields.One2many('payroll_rappel', 'x_employe_id', string="Rappels")
    x_trop_precu_ids = fields.One2many('payroll_trop_percu', 'x_employe_id', string="Trop percu")

    #rappel
    mnt_rappel_salaire = fields.Float(string="Rappel Salaire de base", required=True)
    mnt_rappel_loge = fields.Float(string="Salaire de base", required=True)
    # Trop percu
    mnt_percu_salaire = fields.Float(string="Trop percu Salaire de base", required=True)
    # precompte
    mnt_foner = fields.Float(string="Foner", required=True)

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def vide_rappel_percu_precompte(self):
        for val in self:
            emp_id = val.employee_id

            # rappel
            emp_id.mnt_rappel_salaire = 0
            emp_id.mnt_rappel_loge = 0

            # trop percu
            emp_id.mnt_percu_salaire = 0

            # precompte
            emp_id.mnt_foner = 0

    def calcul_rappel(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    if r.x_rappel_id.code == 'mnt_rappel_salaire':
                        emp_id.mnt_rappel_salaire = r.mnt_rappel
                    if r.x_rappel_id.code == 'mnt_rappel_loge':
                        emp_id.mnt_rappel_loge = r.mnt_rappel

    def set_valide_rappel(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    r.state = 'P'
                    r.fiche_paie_id = val.id

    def calcul_trop_percu(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            print(result)
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    if r.x_rappel_id.code == 'mnt_percu_salaire':
                        emp_id.mnt_percu_salaire = r.mnt_rappel

    def set_valide_trop_percu(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', emp_id.id),
                ('state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    r.state = 'P'
                    r.fiche_paie_id = val.id

    def calcul_precompte(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['hr_paie_precompte_line'].search((
                ('precompte_id.x_employe_id', '=', emp_id.id),
                ('precompte_id.state', '=', 'V'),
            ))

            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    if r.precompte_id.x_precompte_id.code == 'mnt_foner':
                        emp_id.mnt_foner = r.montant

    def set_valide_precompte(self):
        for val in self:
            emp_id = val.employee_id

            result = val.env['hr_paie_precompte_line'].search((
                ('precompte_id.x_employe_id', '=', emp_id.id),
                ('precompte_id.state', '=', 'V'),
            ))
            for r in result:
                mois_courant = val.date_from.month
                annee_courant = val.date_from.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    r.payslip_id = val.id
                    r.state = 'P'

    def compute_sheet(self):
        for val in self:
            val.vide_rappel_percu_precompte()
            val.calcul_rappel()
            val.calcul_trop_percu()
            val.calcul_precompte()
        return super(HrPayslip, self).compute_sheet()

    def action_payslip_done(self):
        for val in self:
            emp_id = val.employee_id
            result = self.env['hr.payslip'].search([
                ('employee_id', '=', emp_id.id),
                ('state', '=', "done"), ])

            mois_courant = val.date_from.month
            annee_courant = val.date_from.year
            for r in result:
                mois = r.date_from.month
                annee = r.date_from.year
                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(
                        _("Le bulletin de ce mois a été déjà génére et validé"))

            val.compute_sheet()

            val.set_valide_rappel()
            val.set_valide_trop_percu()
            val.set_valide_precompte()

            val.vide_rappel_percu_precompte()
        return super(HrPayslip, self).action_payslip_done()

# rappel
class PayrollRappel(models.Model):
    _name = "payroll_rappel"
    _rec_name = 'x_employe_id'
    _order = 'date'

    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_rappel_id = fields.Many2one('hr_rappel_element', string='Elément', required=True)
    date = fields.Date(string='Période', required=True)
    date_to = fields.Date(string='Date', required=True)
    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False)
    motif_ann_paie = fields.Char('Motif annulation', required=False)
    mnt_avant = fields.Float(string='Mont. perçu', required=True, default=0)
    mnt_apres = fields.Float(string='Mont. aurait dû', required=True, default=0)
    occurence = fields.Integer(string='Occurence', required=False, default=1)
    mnt_rappel = fields.Float(string='Montant rappel', required=True, default=0, compute="on_calcul_mtn")
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Payé'),
    ], 'Etat', default='draft', index=True, required=True)

    @api.onchange("date", "date_to")
    def pres(self):
        for val in self:
            if val.date and val.date_to:
                if val.date >= val.date_to:
                    raise ValidationError(_("La date de fin doit être superieur à la date de début"))

    def set_valider(self):
        for val in self:
            result = val.env['payroll_rappel'].search((
                ('x_employe_id', '=', val.x_employe_id.id),
                ('state', 'in', ('V', 'P')),
                ('x_rappel_id', '=', val.x_rappel_id.id),
            ))
            for r in result:
                mois_courant = val.date.month
                annee_courant = val.date.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(_("Vous avez déja enregistré un rappel pour cet élément dans cette période"))

            val.state = 'V'
            val.date_validation = date.today()

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation"))

            val.state = 'A'

    @api.depends("mnt_apres", "mnt_avant", "occurence")
    def on_calcul_mtn(self):
        for rec in self:
            rec.mnt_rappel = (rec.mnt_apres - rec.mnt_avant) * rec.occurence


class HrRappelElement(models.Model):
    _name = "hr_rappel_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)

# trop percu
class PayrollTropPercu(models.Model):
    _name = "payroll_trop_percu"
    _rec_name = 'x_employe_id'
    _order = 'date'

    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_rappel_id = fields.Many2one('hr_rappel_trop_percu_element', string='Elément', required=True)
    date = fields.Date(string='Date', required=True)
    date_to = fields.Date(string='Date', required=True)
    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False)
    motif_ann_paie = fields.Char('Motif annulation', required=False)
    mnt_avant = fields.Float(string='Mont. perçu', required=True, default=0)
    mnt_apres = fields.Float(string='Mont. aurait dû', required=True, default=0)
    occurence = fields.Integer(string='Occurence', required=False, default=1)
    mnt_rappel = fields.Float(string='Montant trop perçu', required=True, default=0, compute="on_calcul_mtn")
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Payé'),
    ], 'Etat', default='draft', index=True, required=True)

    @api.onchange("date", "date_to")
    def pres(self):
        for val in self:
            if val.date and val.date_to:
                if val.date >= val.date_to:
                    raise ValidationError(_("La date de fin doit être superieur à la date de début"))

    def set_valider(self):
        for val in self:
            result = val.env['payroll_trop_percu'].search((
                ('x_employe_id', '=', val.x_employe_id.id),
                ('state', 'in', ('V', 'P')),
                ('x_rappel_id', '=', val.x_rappel_id.id),
            ))
            for r in result:
                mois_courant = val.date.month
                annee_courant = val.date.year

                mois = r.date.month
                annee = r.date.year

                if mois_courant == mois and annee_courant == annee:
                    raise ValidationError(
                        _("Vous avez déja enregistré un trop perçu pour cet élément dans cette période"))

            val.state = 'V'
            val.date_validation = date.today()

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation"))

            val.state = 'A'

    @api.depends("mnt_apres", "mnt_avant", "occurence")
    def on_calcul_mtn(self):
        for rec in self:
            rec.mnt_rappel = (rec.mnt_avant - rec.mnt_apres) * rec.occurence


class HrTropPercuElement(models.Model):
    _name = "hr_rappel_trop_percu_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)


# Precompte#
class HrPaiePrecompte(models.Model):
    _name = "hr_paie_precompte"

    name = fields.Char(string="N°", default="/", readonly=True)
    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    x_precompte_id = fields.Many2one('hr_paie_precompte_element', string='Précompte', required=True)

    montant = fields.Float(string="Montant total", required=True, help="Montant du prêt")
    montant_echeance = fields.Float(string="Montant Echéance", required=True, help="Montant du prêt")
    nbr_echeance = fields.Integer(string="Nombre d'échéance", default=1, compute="calcul_echeance")
    date_deb = fields.Date(string="Date début paiement", required=True, default=fields.Date.today(), )

    lines_ids = fields.One2many('hr_paie_precompte_line', 'precompte_id', string="Lignes", index=True)

    date_validation = fields.Date(string='Date validation', required=False)
    raison = fields.Char('Motif', required=False)
    motif_ann_paie = fields.Char('Motif annulation/paiement', required=False)
    fiche_paie_id = fields.Many2one('hr.payslip', string='Fiche de paie', required=False)
    is_paye = fields.Boolean(string="Payé ?", default=False)

    montant_paye = fields.Float(string="Payé", required=True, compute="calcul_montant_paye")
    montant_reste = fields.Float(string="Reste", required=True, compute="calcul_montant_reste")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Payé'),
    ], 'Etat', default='draft', index=True, required=True)

    def set_valider(self):
        for val in self:
            result = val.env['hr_paie_precompte'].search((
                ('x_employe_id', '=', val.x_employe_id.id),
                ('state', 'in', ('V', 'P')),
                ('x_precompte_id', '=', val.x_precompte_id.id),
            ))

            if result:
                raise ValidationError(
                    _("Vous avez déja enregistré un précompte pour cet élément dans cette période"))

            if not len(val.lines_ids):
                raise ValidationError(
                    _("Le tableau d'amortissement ne peut être vide"))

            val.state = 'V'
            val.date_validation = date.today()
            for l in val.lines_ids:
                l.state = 'V'

    def set_annuler(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation/paiement"))

            val.state = 'A'
            for l in val.lines_ids:
                l.state = 'A'

    def set_payer(self):
        for val in self:
            if not val.motif_ann_paie:
                raise ValidationError(
                    _("Veuillez remplir le champ motif annulation/paiement"))

            val.state = 'P'
            for l in val.lines_ids:
                l.state = 'P'

    @api.depends('lines_ids')
    def calcul_montant_paye(self):
        for val in self:
            montant_paye = 0
            for l in val.lines_ids:
                if l.state == 'P':
                    montant_paye = montant_paye + l.montant

            val.montant_paye = montant_paye
            # if val.montant_paye == val.montant:
            #     val.state = 'P'

    @api.depends('montant', 'montant_paye')
    def calcul_montant_reste(self):
        for val in self:
            val.montant_reste = val.montant - val.montant_paye

    @api.depends('montant', 'montant_echeance')
    def calcul_echeance(self):
        for val in self:
            val.nbr_echeance = 0
            if val.montant_echeance:
                val.nbr_echeance = int(val.montant / val.montant_echeance)

    def calcul_ta(self):
        for val in self:
            val.lines_ids.unlink()
            date_start = datetime.strptime(str(val.date_deb), '%Y-%m-%d')
            for i in range(1, val.nbr_echeance):
                self.env['hr_paie_precompte_line'].create({
                    'date': date_start,
                    'montant': val.montant_echeance,
                    'precompte_id': val.id})
                date_start = date_start + relativedelta(months=1)

            montant_echeance = val.montant - (val.montant_echeance * (val.nbr_echeance - 1))
            self.env['hr_paie_precompte_line'].create({
                'date': date_start,
                'montant': montant_echeance,
                'precompte_id': val.id})

        return True


class HrPaiePrecompteElement(models.Model):
    _name = "hr_paie_precompte_element"
    _rec_name = 'libelle'

    code = fields.Char('Code', required=True)
    libelle = fields.Char('Libellé', required=True)


class HrPretLine(models.Model):
    _name = "hr_paie_precompte_line"
    _description = "Installment Line"

    date = fields.Date(string="Date", required=True, )
    montant = fields.Float(string="Montant", required=True)
    is_paye = fields.Boolean(string="Payé", help="Paid")
    precompte_id = fields.Many2one('hr_paie_precompte', string="Précompte")
    payslip_id = fields.Many2one('hr.payslip', string="Fiche de paie", help="Payslip")

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('A', 'Annulé'),
        ('P', 'Payé'),
    ], 'Etat', default='draft', index=True, required=True)
