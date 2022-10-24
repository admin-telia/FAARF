from odoo import fields, api, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from num2words import num2words
import time


class ActeAmpliation(models.Model):
    _name = 'hr_actes_ampliations'

    name = fields.Char(string='Titre', required=False)


# classe type conge
class ActeAutoAbsence(models.Model):
    _name = 'hr_acte_auto_absence'

    name = fields.Many2one('hr.employee', string='Employé', required=True)
    duree = fields.Integer(string='Durée (en jours)', required=False)
    date_deb = fields.Date(string='Date début', required=False)

    ampliation_ids = fields.Many2many(comodel_name='hr_actes_ampliations', string='Ampliations')
    motif = fields.Char(string='Motif', required=False)

    texte = fields.Html(string="Texte", required=False, )

    @api.onchange('name', 'duree', 'date_deb', 'ampliation_ids', 'motif')
    def onchange_name(self):
        self.texte = f"""
            <h2 style="text-align:center"> AUTORISATION D'ABSENCE</h2>
            <br/>
            <p> Une autorisation d'absence  de {num2words(self.duree, lang='fr')} ({self.duree})
            jours calendaires pour compter du {self.date_deb.strftime('%A')} {self.date_deb.strftime('%d/%m/%y')} 
            est accordée à Madame {self.name.name}, 
            Mle {self.name.matricule}, {self.name.x_fonction_id.name}  {self.motif} 
            </p>
            """


class ActeCertifCessServive(models.Model):
    _name = 'hr_acte_certif_cess_service'

    name = fields.Char(string='N°', required=False)
    employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    signataire_id = fields.Many2one('res.users', string='Signataire', required=True)
    ampliation_ids = fields.Many2many(comodel_name='hr_actes_ampliations', string='Ampliations')

    nom = fields.Char(string='Nom et Prénom', required=False, related="employe_id.name")
    matricule = fields.Char(string='Matricule', required=False, related="employe_id.matricule")
    fonction = fields.Char(string='Fonction', required=False, related="employe_id.x_fonction_id.name")
    emploi = fields.Char(string='Emploi', required=False, related="employe_id.x_emploi_id.name")

    texte = fields.Html(string='Texte', required=False,
                        default="""
                            <p style="font-size: 14px;">
                                Je soussigné, Directeur des Ressources Humaines du Fonds d'Appui aux activités Rémunératrices des Femmes (FAARF), 
                                certifie que Madame BA/SANGO DAMATA, matricule 21821<b> </b>, 
                                bénéficiaire d'un congé de maternité suivant décision n°2022-000006/ MGSNFAH/SG/FAARF/DRH du 04 février 2022 
                                a effectivement cessé service le 04 février 2022.
                            </p>
                            <p><br></p><p>
                            <font style="font-size: 14px;">
                                En Foi de quoi le présent certificat est établi pour servir et valoir ce que de droit.</font>
                            <br></p>
                        """)


# actes administratifs
class HrActesAdType(models.Model):
    _name = "hr_actes_ad_type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type acte administratif"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char(string='Code', required=False)
    sequence = fields.Char(readonly=True)

    @api.onchange('name')
    def change_lib_acte(self):
        for vals in self:
            if vals.name:
                vals.name = (vals.name).upper()


class HrActesAdModele(models.Model):
    _name = "hr_actes_ad_modele"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Nouveau modèle par defaut"

    name = fields.Many2one('hr_actes_ad_type', string="Acte", required=True)
    contenu = fields.Html(string="Contenu par defaut")
    entete = fields.Html(string="Entête")
    sequence = fields.Char(readonly=True)


class HrActesAdministratif(models.Model):
    _name = "hr_acte_administratif"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'employe_id'

    employe_id = fields.Many2one('hr.employee', required=True, string="Employé")
    matricule = fields.Char(string="N° matricule", related="employe_id.matricule", readonly=True)
    fonction = fields.Char(string="Fonction", related="employe_id.x_fonction_id.name", readonly=True)
    emploi = fields.Char(string="Fonction", related="employe_id.x_emploi_id.name", readonly=True)

    acte_id = fields.Many2one("hr_actes_ad_type", string="Type Acte", required=True)
    date_ets = fields.Date(string='Date', required=False, default=fields.Date.context_today)
    contenu_acte = fields.Html(string="Texte")
    entete_acte = fields.Html(string="Entête")
    state = fields.Selection(
        [("brouillon", "Brouillon"), ("drh", "Envoyé à DRH"), ("dcmef", "Envoyé à DCMEF"), ("visa", "Visé")],
        string="Etat du dossier", default="brouillon")
    ampliation_ids = fields.One2many(
        comodel_name='hr_acte_ad_ampliation',
        inverse_name='acte_id',
        string='Ampliations',
        required=False)
    sequence = fields.Char(readonly=True)

    signataire_id = fields.Many2one(comodel_name='res.users', string='Signataire', required=False)
    lieu = fields.Char(string='Lieu', required=False, default="Fait à Ouagadougou le,")

    def action_brouillon(self):
        self.state = "brouillon"

    def action_drh(self):
        self.state = "drh"

    def action_dcmef(self):
        self.state = "dcmef"

    def action_visa(self):
        self.state = "visa"

    @api.onchange('employe_id')
    def change_employee(self):
        for rec in self:
            tmp = rec.contenu_acte
            if rec.employe_id.name:
                tmp = tmp.replace('[NOM]', rec.employe_id.name)
            if rec.employe_id.matricule:
                tmp = tmp.replace('[MATRICULE]', rec.employe_id.matricule)
            if rec.employe_id.department_id:
                tmp = tmp.replace('[DIRECTION]', rec.employe_id.x_emploi_id.name)
            if rec.employe_id.x_emploi_id:
                tmp = tmp.replace('[EMPLOI]', rec.employe_id.x_emploi_id.name)
            if rec.employe_id.x_fonction_id:
                tmp = tmp.replace('[FONCTION]', rec.employe_id.x_fonction_id.name)
            if rec.employe_id.x_categorie_id:
                tmp = tmp.replace('[CATEGORIE]', rec.employe_id.x_categorie_id.name)
            if rec.employe_id.x_echelle_id:
                tmp = tmp.replace('[ECHELLE]', rec.employe_id.x_echelle_id.name)
            if rec.employe_id.x_echellon_id:
                tmp = tmp.replace('[ECHELON]', rec.employe_id.x_echellon_id.name)
            rec.contenu_acte = tmp

    @api.onchange('acte_id')
    def check_c_acte(self):
        for rec in self:
            if rec.acte_id:
                record = self.env['hr_actes_ad_modele'].search([('name.id', '=', rec.acte_id.id)])
                rec.contenu_acte = record.contenu
                rec.entete_acte = record.entete


class HrActesAdministratifAmpli(models.Model):
    _name = "hr_acte_ad_ampliation"
    _description = "Gestion des ampliations"

    name = fields.Many2one('hr_acte_ad_ampliation_lib', string="Ampliation")
    nombre_ampliation = fields.Integer(string="Nombre")
    acte_id = fields.Many2one('hr_acte_administratif', string="Acte")
    decision_id = fields.Many2one('hr_decision_administratif', string="Acte")


class HrActesAdministratifAmpliLib(models.Model):
    _name = "hr_acte_ad_ampliation_lib"
    _description = "Gestion des intitulés des ampliations"

    name = fields.Char(string="Libellé", required=True)


# decision administratif
class HrDecisionAdType(models.Model):
    _name = "hr_decision_ad_type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Decision administratif"

    name = fields.Char(string="Libellé", required=True)
    code = fields.Char(string='Code', required=False)
    sequence = fields.Char(readonly=True)

    @api.onchange('name')
    def change_lib_acte(self):
        for vals in self:
            if vals.name:
                vals.name = vals.name.upper()


class HrDecisionAdModele(models.Model):
    _name = "hr_decision_ad_modele"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Many2one('hr_decision_ad_type', string="Type décision", required=True)
    contenu = fields.Html(string="Contenu")
    decret = fields.Html(string="decret")
    entete = fields.Html(string="Entête")
    article1 = fields.Text(string='Article 1', required=False)
    article2 = fields.Text(string='Article 2', required=False)
    article3 = fields.Text(string='Article 3', required=False)
    article4 = fields.Text(string='Article 4', required=False)
    article5 = fields.Text(string='Article 5', required=False)
    article6 = fields.Text(string='Article 6', required=False)
    article7 = fields.Text(string='Article 7', required=False)
    article8 = fields.Text(string='Article 8', required=False)
    sequence = fields.Char(readonly=True)


class HrDecisionAdministratif(models.Model):
    _name = "hr_decision_administratif"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'decision_modele_id'

    employe_ids = fields.Many2many(comodel_name='hr.employee', string='Employés', required=False)

    decision_modele_id = fields.Many2one("hr_decision_ad_modele", string="Type Acte", required=True)
    date_ets = fields.Date(string='Date', required=False, default=fields.Date.context_today)
    contenu_decision = fields.Html(string="Texte")
    entete_decicion = fields.Html(string="Entête")
    decret_decicion = fields.Html(string="Décret")
    article1 = fields.Text(string='Article 1', required=False)
    article2 = fields.Text(string='Article 2', required=False)
    article3 = fields.Text(string='Article 3', required=False)
    article4 = fields.Text(string='Article 4', required=False)
    article5 = fields.Text(string='Article 5', required=False)
    article6 = fields.Text(string='Article 6', required=False)
    article7 = fields.Text(string='Article 7', required=False)
    article8 = fields.Text(string='Article 8', required=False)
    state = fields.Selection(
        [("brouillon", "Brouillon"), ("drh", "Envoyé à DRH"), ("dcmef", "Envoyé à DCMEF"), ("visa", "Visé")],
        string="Etat du dossier", default="brouillon")
    ampliation_ids = fields.One2many(
        comodel_name='hr_acte_ad_ampliation',
        inverse_name='decision_id',
        string='Ampliations',
        required=False)
    sequence = fields.Char(readonly=True)

    signataire_id = fields.Many2one(comodel_name='res.users', string='Signataire', required=False)
    lieu = fields.Char(string='Lieu', required=False, default="Fait à Ouagadougou le,")

    def action_brouillon(self):
        self.state = "brouillon"

    def action_drh(self):
        self.state = "drh"

    def action_dcmef(self):
        self.state = "dcmef"

    def action_visa(self):
        self.state = "visa"

    @api.onchange('decision_modele_id')
    def check_decision_modele(self):
        for rec in self:
            if rec.decision_modele_id:
                record = self.env['hr_decision_ad_modele'].search([('name.id', '=', rec.decision_modele_id.id)])

                rec.entete_decicion = record.entete
                rec.decret_decicion = record.decret
                rec.article1 = record.article1
                rec.article2 = record.article2
                rec.article3 = record.article3
                rec.article4 = record.article4
                rec.article5 = record.article5
                rec.article6 = record.article6
                rec.article7 = record.article7
                rec.article8 = record.article8