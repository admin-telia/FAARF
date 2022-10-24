from odoo import fields, models, api
from num2words import num2words

class CreditEditionCovention(models.Model):
    """Definition de la table credit"""

    _name = "credit_edition_convention"
    _description = "Convention de credit"

    name = fields.Char(string='N°', required=False)
    credit_id = fields.Many2one('credit_credit', string='N° prêt', required=True)
    cliente_id = fields.Many2one('credit_clients', string='Cliente', related='credit_id.cliente_id')
    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', related='credit_id.gestionnaire_id')
    date = fields.Date(string='Date', required=False)
    date_annulle = fields.Date(string='Date', required=False)

    zone_id = fields.Many2one("ref_zone", "Zone", related="credit_id.zone_id")
    region_id = fields.Many2one("ref_region", "Région", related="credit_id.region_id")
    province_id = fields.Many2one("ref_province", "Province", related="credit_id.province_id")
    departement_id = fields.Many2one("ref_departement", "Commune", related="credit_id.departement_id")
    village_id = fields.Many2one("ref_village", "Secteur/Village", related="credit_id.village_id")

    capital = fields.Float(string="Capital prêté", required=False, digits=(16, 0), related="credit_id.montant_accorde")
    taux_int = fields.Float(string="Taux d'intérêt", required=False, digits=(16, 0), related="credit_id.taux_int_annuel")
    duree = fields.Integer(string="Durée du prêt", required=False, related="credit_id.duree_pret")
    type_echeance = fields.Selection(string='Periodicité', required=False,
                                   selection=[('1', 'Mensuelle'), ('2', 'Bimensuelle'),
                                              ('3', 'Trimestrielle'), ('4', 'Chaque 4 mois'),
                                              ('5', 'Chaque 5 mois'), ('6', 'Semestrielle'),
                                              ('7', 'Chaque 7 mois'), ('8', 'Chaque 8 mois'),
                                              ('U', 'Unique'), ],
                                   related="credit_id.periodicite")
    total_rb = fields.Float(string="Total à Rembourser", required=False, digits=(16, 0), related="credit_id.total_rembourser")
    fa_taux = fields.Float(string="Garantie/fonds de groupe", required=False, digits=(16, 0), related="credit_id.taux_int_garantie")
    fa_mtn = fields.Float(string="Montant Echéance Garantie", required=False, digits=(16, 0), related="credit_id.montant_garantie")

    state = fields.Selection([('N', 'N'), ('A', 'Approuvée'), ('AN', 'Annulée')],
                             string='Etat', readonly=True, default="N", )  # track_visibility='always')

    def approuver(self):
        convention = self.env['credit_edition_convention'].search([
            ('state', '=', 'A'),
            ('credit_id.id', '=', self.credit_id.id)])
        if convention:
            raise models.ValidationError("Il existe déjà une convention à l'etat Approuvé")

        credit_compteur = self.env['credit_compteur_convention'].search([])
        nombre = 1
        if credit_compteur:
            credit_compteur = credit_compteur[0]
            nombre = credit_compteur.nombre + 1
            credit_compteur.nombre = nombre
            nombre = str(nombre).zfill(9)
        else:
            self.env['credit_compteur_convention'].create({
                'nombre': 1,
            })
            nombre = str(nombre).zfill(9)

        self.name = nombre
        self.state = 'A'
        self.date = fields.Date.context_today(self)

    def set_annuler(self):
        self.state = 'AN'
        self.date_annulle = fields.Date.context_today(self)

class CreditCompteurConvention(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compteur_convention'

    code = fields.Char(string='Code', required=False)
    nombre = fields.Integer(string='Nombre', required=False)

class CreditEditionFicheDeblocage(models.Model):
    """Definition de la table credit"""

    _name = "credit_edition_fiche_deblocage"
    _description = "Fiche de deblocage"

    name = fields.Char(string='N°', required=False)
    credit_id = fields.Many2one('credit_credit', string='', required=False)
    cliente_id = fields.Many2one('credit_clients', string='Client', related='credit_id.cliente_id')
    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire de crédit', related='credit_id.gestionnaire_id')


    zone_id = fields.Many2one("ref_zone", "Zone", related="credit_id.zone_id")
    region_id = fields.Many2one("ref_region", "Région", related="credit_id.region_id")
    province_id = fields.Many2one("ref_province", "Province", related="credit_id.province_id")
    departement_id = fields.Many2one("ref_departement", "Commune", related="credit_id.departement_id")
    village_id = fields.Many2one("ref_village", "Secteur/Village", related="credit_id.village_id")
    state = fields.Selection([('N', 'N'), ('A', 'A')],
                             string='Etat', readonly=True, default="N", )  # track_visibility='always')

    x_mnt_en_lettre = fields.Char(string='Montant en lettres', compute="calcul_mt_lettre")

    @api.depends('credit_id')
    def calcul_mt_lettre(self):
        for rec in self:
            self.x_mnt_en_lettre = num2words(rec.credit_id.montant_accorde, lang='fr')