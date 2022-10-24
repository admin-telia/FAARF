from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


# Fiche de credit
class CreditSyntheseFiche(models.TransientModel):
    """Definition de la table credit"""

    _name = 'credit_synthese_fiche'

    credit_id = fields.Many2one(comodel_name='credit_credit', string='Credit N°', required=False)

    line_ids = fields.One2many(
        comodel_name='credit_synthese_fiche_line',
        inverse_name='fiche_id',
        string='Line_ids',
        required=False)

    def set_afficher(self):
        tas = self.env['credit_credit_line'].search([('credit_id.id', '=', self.credit_id.id)])
        transactions = self.env['credit_credit_remboursement_line'].search([('credit_id.id', '=', self.credit_id.id)])

        self.line_ids.unlink()
        for c in tas:
            self.env['credit_synthese_fiche_line'].create({
                'date': c.date,
                'transaction': "Echance due",
                'piece_comptable': "",
                'principal': c.montant,
                'interet': c.interet,
                'fa': c.garantie,
                'penalite': 0,
                'solde_courant': 0,
                'solde_principal': 0,
                'solde_fa': 0,
                'solde_total': 0,
                'state': 'tranche',
                'fiche_id': self.id,
            })

        for c in transactions:
            self.env['credit_synthese_fiche_line'].create({
                'date': c.date,
                'transaction': "Remboursement",
                'piece_comptable': c.transaction,
                'principal': c.montant_p,
                'interet': c.interet_p,
                'fa': c.garantie_p,
                'penalite': c.penalite_p,
                'solde_courant': 0,
                'solde_principal': 0,
                'solde_fa': 0,
                'solde_total': 0,
                'state': 'remboursement',
                'fiche_id': self.id,
            })


class CreditSyntheseFicheLine(models.TransientModel):
    _name = 'credit_synthese_fiche_line'
    _order = 'date'

    date = fields.Date(string='Date', required=False)
    transaction = fields.Char(string='Transaction', required=False)
    piece_comptable = fields.Char(string='Piece Comptable', required=False)

    principal = fields.Float(string='Principal', required=False, digits=(16, 0))
    interet = fields.Float(string='Intérêt', required=False, digits=(16, 0))
    fa = fields.Float(string='FA', required=False, digits=(16, 0))
    penalite = fields.Float(string='Pénalité', required=False, digits=(16, 0))

    solde_courant = fields.Float(string='Solde Courant', required=False, digits=(16, 0))
    solde_principal = fields.Float(string='Solde Principal', required=False, digits=(16, 0))
    solde_interet = fields.Float(string='Solde Intérêt', required=False, digits=(16, 0))
    solde_fa = fields.Float(string='Solde FA', required=False, digits=(16, 0))
    solde_total = fields.Float(string='Solde Total', required=False, digits=(16, 0))

    fiche_id = fields.Many2one('credit_synthese_fiche', string='Fiche_id', required=False)

    state = fields.Selection([('remboursement', 'remboursement'),
                              ('tranche', 'tranche'),
                              ], string='Etat', readonly=True)


# demande recues
class CreditSyntheseDemande(models.TransientModel):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande'

    bailleur_id = fields.Many2one(comodel_name='credit_bailleur', string='Bailleur', required=False)
    date_deb = fields.Date(string='Période', required=False)
    date_fin = fields.Date(string='Date_deb', required=False)

    state = fields.Selection([('N', 'Non transmise'), ('G', 'Montée'),
                              ('DA', 'Accordée'), ('DR', 'Refusée')],
                             string='Etat', default="", )

    zone_id = fields.Many2one(comodel_name='ref_zone', string=' Zone', required=False)
    region_id = fields.Many2one(comodel_name='ref_region', string=' Région', required=False)
    province_id = fields.Many2one(comodel_name='ref_province', string='Province', required=False)
    departement_id = fields.Many2one(comodel_name='ref_departement', string=' Département', required=False)
    village_id = fields.Many2one(comodel_name='ref_village', string='Village/secteur', required=False)

    # zone_ids = fields.Many2many(comodel_name="ref_zone", string="Zone", required=True)
    # region_ids = fields.Many2many(comodel_name="ref_region", string="Région", required=True)
    # province_ids = fields.Many2many(comodel_name="ref_province", string="Province", required=True)
    # departement_ids = fields.Many2many(comodel_name="ref_departement", string="Département", required=True)
    # village_ids = fields.Many2many(comodel_name='ref_village', string='Village/secteur')

    line_ids = fields.One2many('credit_synthese_demande_line', inverse_name='synthese_id', string='Line_ids')

    def set_afficher(self):
        domain = []

        if self.bailleur_id:
            domain.append(('bailleur_id', '=', self.bailleur_id.id))
        if self.zone_id:
            domain.append(('zone_id', '=', self.zone_id.id))
        if self.region_id:
            domain.append(('region_id', '=', self.region_id.id))
        if self.province_id:
            domain.append(('province_id', '=', self.province_id.id))
        if self.departement_id:
            domain.append(('departement_id', '=', self.departement_id.id))
        if self.village_id:
            domain.append(('village_id', '=', self.village_id.id))
        if self.date_deb:
            domain.append(('date_demande', '>=', self.date_deb))
        if self.date_fin:
            domain.append(('date_demande', '<=', self.date_fin))
        if self.state:
            print(self.state)
            domain.append(('state', '=', self.state))

        credits = self.env['credit_credit'].search(domain)
        self.line_ids.unlink()
        for c in credits:
            self.env['credit_synthese_demande_line'].create({
                'name': c.name,
                'num_demande': c.num_demande,
                'cliente_id': c.cliente_id.name,
                'type_client': c.type_client.name,
                'gestionnaire_id': c.gestionnaire_id.name,
                'date_demande': c.date_demande,
                'montant_demande': c.montant_demande,
                'montant_accorde': c.montant_accorde,
                'bailleur_id': c.bailleur_id.name,
                'synthese_id': self.id,
            })


class CreditSyntheseDemandeLine(models.TransientModel):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande_line'

    name = fields.Char(string='Numéro du prêt', )
    num_demande = fields.Char(string='Numéro de la demande')
    cliente_id = fields.Char(string='Cliente')
    type_client = fields.Char('Type de client')
    gestionnaire_id = fields.Char(string='Gestionnaire', )

    date_demande = fields.Date(string='Date de la demande', )

    date_appro = fields.Date("Date approbation/Rejet")
    montant_demande = fields.Float(string='Montant demandé ', digits=(16, 0))
    montant_accorde = fields.Float(string='Montant accordé ', digits=(16, 0))

    taux_int_annuel = fields.Float(string="Taux d'intérêt annuel")
    nbr_tranche = fields.Integer(string='Durée de prêt')
    montant_interet = fields.Float(string="Montant d'intérêt", digits=(16, 0))
    total_rembourser = fields.Float(string="Total à rembourser", digits=(16, 0))

    taux_int_garantie = fields.Float(string="Taux fonds d'autonomisation")
    montant_garantie = fields.Float(string="Fonds d'autonomisation", digits=(16, 0))

    taux_frais_dossier = fields.Float(string="Taux frais de dossier")
    montant_frais_dossier = fields.Float(string='Frais de dossier', digits=(16, 0))

    bailleur_id = fields.Char(string='Bailleur', required=False)

    # localisation
    zone_id = fields.Char("Zone", )
    region_id = fields.Char("Région", )
    province_id = fields.Char("Province", )
    departement_id = fields.Char("Département", )
    village_id = fields.Char("Village/secteur", )

    synthese_id = fields.Many2one('credit_synthese_demande', cstring='Synthese_id', required=False)


# demandes par gestionnaire
class CreditSyntheseGestDemande(models.TransientModel):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande_gest'

    date_deb = fields.Date(string='Période', required=False)
    date_fin = fields.Date(string='Date_deb', required=False)
    zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zones')
    gestionnaire_id = fields.Many2one(comodel_name='res.users', string='Gestionnaire', required=False)
    # gestionnaire_ids = fields.Many2many(comodel_name='', string='')

    # zone_ids = fields.Many2many("ref_zone", "Zone", required=True)
    # region_id = fields.Many2many("ref_region", "Région", required=True)
    # province_id = fields.Many2many("ref_province", "Province", required=True)
    # departement_id = fields.Many2many("ref_departement", "Département", required=True)
    # village_id = fields.Many2many("ref_village", "Village/secteur", required=True)

    line_ids = fields.One2many('credit_synthese_demande_gest_line', inverse_name='synthese_id', string='Line_ids')

    state = fields.Selection([('G', 'Traité'),
                              ('G', 'Non Traité')],
                             string='Etat', default="G", )

    def set_afficher(self):

        domain = [('gestionnaire_id', '=', self.gestionnaire_id.id)]
        if self.date_deb:
            domain.append(('date_demande', '>=', self.date_deb))
        if self.date_fin:
            domain.append(('date_demande', '<=', self.date_fin))
        if self.state:
            domain.append(('state', '=', self.state))

        credits = self.env['credit_credit'].search(domain)
        self.line_ids.unlink()
        for c in credits:
            self.env['credit_synthese_demande_gest_line'].create({
                'name': c.name,
                'num_demande': c.num_demande,
                'cliente_id': c.cliente_id.name,
                'type_client': c.type_client.name,
                'gestionnaire_id': c.gestionnaire_id.name,
                'date_demande': c.date_demande,
                'montant_demande': c.montant_demande,
                'montant_accorde': c.montant_accorde,
                'bailleur_id': c.bailleur_id.name,
                'synthese_id': self.id,
            })


class CreditSyntheseDemandeGestLine(models.TransientModel):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande_gest_line'

    name = fields.Char(string='Numéro du prêt', )
    num_demande = fields.Char(string='Numéro de la demande')
    cliente_id = fields.Char(string='Cliente')
    type_client = fields.Char('Type de client')
    gestionnaire_id = fields.Char(string='Gestionnaire', )

    date_demande = fields.Date(string='Date de la demande', )

    date_appro = fields.Date("Date approbation/Rejet")
    montant_demande = fields.Float(string='Montant demandé ', digits=(16, 0))
    montant_accorde = fields.Float(string='Montant accordé ', digits=(16, 0))

    taux_int_annuel = fields.Float(string="Taux d'intérêt annuel")
    nbr_tranche = fields.Integer(string='Durée de prêt')
    montant_interet = fields.Float(string="Montant d'intérêt", digits=(16, 0))
    total_rembourser = fields.Float(string="Total à rembourser", digits=(16, 0))

    taux_int_garantie = fields.Float(string="Taux fonds d'autonomisation")
    montant_garantie = fields.Float(string="Fonds d'autonomisation", digits=(16, 0))

    taux_frais_dossier = fields.Float(string="Taux frais de dossier")
    montant_frais_dossier = fields.Float(string='Frais de dossier', digits=(16, 0))

    bailleur_id = fields.Char(string='Bailleur', required=False)

    # localisation
    zone_id = fields.Char("Zone", )
    region_id = fields.Char("Région", )
    province_id = fields.Char("Province", )
    departement_id = fields.Char("Département", )
    village_id = fields.Char("Village/secteur", )

    synthese_id = fields.Many2one('credit_synthese_demande_gest', string='Synthese_id', required=False)


# demandes par region
class CreditSyntheseRegion(models.Model):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande_region'

    date_deb = fields.Date(string='Période', required=False)
    date_fin = fields.Date(string='Date_deb', required=False)
    region_ids = fields.Many2many(comodel_name='ref_region', string='Regions')
    province_ids = fields.Many2many(comodel_name='ref_province', string='Provinces')
    departement_ids = fields.Many2many(comodel_name='ref_departement', string='Commune')
    village_ids = fields.Many2many(comodel_name='ref_village', string='Village/secteur')

    line_ids = fields.One2many('credit_synthese_demande_region_line', inverse_name='synthese_id', string='Line_ids')

    state = fields.Selection([('N', 'Non transmise'), ('G', 'Montée'),
                              ('DA', 'Accordée'), ('DR', 'Refusée')],
                             string='Etat', default="", )

    localisation = fields.Selection([('R', 'Région'), ('P', 'Province'),
                                     ('C', 'Commune'), ('V', 'Village/secteur')],
                                    string='Localisation', default="", )

    def set_afficher(self):
        domain = []
        if self.date_deb:
            domain.append(('date_demande', '>=', self.date_deb))
        if self.date_fin:
            domain.append(('date_demande', '<=', self.date_fin))
        if self.state:
            domain.append(('state', '=', self.state))
        if self.region_ids:
            domain.append(('region_id', 'in', self.region_ids.ids))
        if self.province_ids:
            domain.append(('province_id', 'in', self.province_ids.ids))
        if self.departement_ids:
            domain.append(('departement_id', 'in', self.departement_ids.ids))
        if self.village_ids:
            domain.append(('village_id', 'in', self.village_ids.ids))

        group_by = []
        if self.localisation == 'R':
            group_by.append('region_id')
        elif self.localisation == 'P':
            group_by.append('province_id')
        elif self.localisation == 'C':
            group_by.append('departement_id')
        else:
            group_by.append('village_id')

        read_group_res = self.env['credit_credit'].read_group(domain=domain,
                                                              fields=['montant_demande:sum', 'montant_accorde:sum'],
                                                              groupby=group_by)
        self.line_ids.unlink()
        for c in read_group_res:
            if self.localisation == 'R':
                nombre = c.get('region_id_count')
                name = c.get('region_id')[1]
            elif self.localisation == 'P':
                nombre = c.get('province_id_count')
                name = c.get('province_id')[1]
            elif self.localisation == 'C':
                nombre = c.get('departement_id_count')
                name = c.get('departement_id')[1]
            else:
                nombre = c.get('village_id_count')
                name = c.get('village_id')[1]

            self.env['credit_synthese_demande_region_line'].create({
                'localisation': name,
                'nombre': nombre,
                'montant_demande': c.get('montant_demande'),
                'synthese_id': self.id,
            })

        # for c in credits:
        #     print("Maxx")
        #     print(self)


class CreditSyntheseDemandeRegionLine(models.Model):
    """Definition de la table credit"""

    _name = 'credit_synthese_demande_region_line'

    nombre = fields.Float(string='Nombre', digits=(16, 0))
    montant_demande = fields.Float(string='Montant demandé ', digits=(16, 0))
    montant_accorde = fields.Float(string='Montant accordé ', digits=(16, 0))
    localisation = fields.Char(string='Localisation', required=False)

    synthese_id = fields.Many2one('credit_synthese_demande_region', string='Synthese_id', required=False)


# synthese portefeuille a risque
class CreditSynthesePorteRisque(models.Model):
    """Definition de la table credit"""

    _name = 'credit_synthese_porte_risque'

    date = fields.Date(string='Date', required=False)

    bailleur_ids = fields.Many2many(comodel_name='credit_bailleur', string='Bailleurs')
    zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zones')
    gestionnaire_ids = fields.Many2many(comodel_name='res.users', string='Gestionnaires')

    line_ids = fields.One2many('credit_synthese_porte_risque_line', inverse_name='synthese_id', string='Line_ids')

    def set_afficher(self):
        domain = []
        if self.bailleur_ids:
            domain.append(('bailleur_id', 'in', self.bailleur_ids.ids))
        if self.zone_ids:
            domain.append(('zone_id', 'in', self.zone_ids.ids))
        if self.gestionnaire_ids:
            domain.append(('gestionnaire_id', 'in', self.gestionnaire_ids.ids))

        credits = self.env['credit_credit'].search(domain)

        self.line_ids.unlink()
        for credit in credits:
            ta = self.env['credit_credit_line'].search([('credit_id.id', '=', credit.id)])
            principal_total = 0
            interet_total = 0
            for l in ta:
                principal_total += l['montant']
                interet_total += l['interet']

            rembours = self.env['credit_credit_remboursement_line'].search([('credit_id.id', '=', credit.id)])
            montant_prin_paye = 0
            interet_paye = 0
            for l in rembours:
                montant_prin_paye += l['montant_p']
                interet_paye += l['interet_p']

            # ta = self.env['credit_credit_line'].search([
            #     ('credit_id.id', '=', credit.id),
            #     ('date', '<', self.date)])
            # principal_total_d = 0
            # interet_total_d = 0
            # for l in ta:
            #     principal_total_d += l['montant']
            #     interet_total_d += l['interet']
            #
            # result_p = montant_prin_paye - principal_total_d
            #
            # montant_p_arriere = 0
            # if result_p < 0:
            #     montant_p_arriere = result_p * -1

            ta = self.env['credit_credit_line'].search([
                ('credit_id.id', '=', credit.id),
                ('date', '<', self.date)])
            result_p = montant_prin_paye
            montant_p_arriere = 0
            is_date = 1
            date = self.date
            for l in ta:
                result_p = result_p - l['montant']
                if result_p < 0:
                    if is_date:
                        date = l['date']
                        is_date = 0
                    montant_p_arriere = result_p * -1

            if montant_prin_paye:
                montant_prin_encours = principal_total - montant_prin_paye
                montant_risque_1 = montant_prin_encours
                montant_risque_30 = 0
                montant_risque_60 = 0
                montant_risque_90 = 0
                montant_risque_120 = 0
                montant_risque_150 = 0
                montant_risque_180 = 0

                print((self.date - date).days)
                if (self.date - date).days > 30:
                    montant_risque_30 = montant_prin_encours
                if (self.date - date).days > 60:
                    montant_risque_60 = montant_prin_encours
                if (self.date - date).days > 90:
                    montant_risque_90 = montant_prin_encours
                if (self.date - date).days > 120:
                    montant_risque_120 = montant_prin_encours
                if (self.date - date).days > 150:
                    montant_risque_150 = montant_prin_encours
                if (self.date - date).days > 180:
                    montant_risque_180 = montant_prin_encours

                self.env['credit_synthese_porte_risque_line'].create({
                    'name': credit.name,
                    'cliente_id': credit.cliente_id.name,
                    'type_client': credit.type_client.name,
                    'gestionnaire_id': credit.gestionnaire_id.name,
                    'montant_prin_encours': principal_total - montant_prin_paye,
                    'montant_p_arriere': montant_p_arriere,
                    'montant_prin_non_du': (principal_total - montant_prin_paye) - montant_p_arriere,
                    'montant_risque_1': montant_risque_1,
                    'montant_risque_30': montant_risque_30,
                    'montant_risque_60': montant_risque_60,
                    'montant_risque_90': montant_risque_90,
                    'montant_risque_120': montant_risque_120,
                    'montant_risque_150': montant_risque_150,
                    'montant_risque_180': montant_risque_180,
                    'synthese_id': self.id,
                })


class CreditSynthesePorteRisqueLine(models.Model):
    """Definition de la table credit"""

    _name = 'credit_synthese_porte_risque_line'

    name = fields.Char(string='Numéro du prêt', )
    cliente_id = fields.Char(string='Cliente')
    type_client = fields.Char('Type de client')
    gestionnaire_id = fields.Char(string='Gestionnaire', )
    montant_prin_encours = fields.Float(string='Total du principal en cours ', digits=(16, 0))
    montant_p_arriere = fields.Float(string='Montant principal en arriérés', digits=(16, 0))
    montant_prin_non_du = fields.Float(string='Total principal non encore dû', digits=(16, 0))
    montant_risque_1 = fields.Float(string='1 jours ou plus', digits=(16, 0))
    montant_risque_30 = fields.Float(string='30 jours ou plus', digits=(16, 0))
    montant_risque_60 = fields.Float(string='60 jours ou plus', digits=(16, 0))
    montant_risque_90 = fields.Float(string='90 jours ou plus', digits=(16, 0))
    montant_risque_120 = fields.Float(string='120 jours ou plus', digits=(16, 0))
    montant_risque_150 = fields.Float(string='150 jours ou plus', digits=(16, 0))
    montant_risque_180 = fields.Float(string='180 jours ou plus', digits=(16, 0))

    synthese_id = fields.Many2one('credit_synthese_demande_region', string='Synthese_id', required=False)
