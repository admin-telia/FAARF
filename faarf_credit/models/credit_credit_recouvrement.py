from math import floor

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCreditPortRisque(models.Model):
    """Definition de la table credit"""

    _name = 'credit_credit_port_risque'
    _rec_name = 'date'

    bailleur_ids = fields.Many2many(comodel_name='credit_bailleur', string='Bailleurs', required=True)
    zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zones')
    x_region_ids = fields.Many2many(comodel_name='ref_region', string='Region', required=False)
    x_province_ids = fields.Many2many(comodel_name='ref_province', string='Province', required=False)
    x_departement_ids = fields.Many2many(comodel_name='ref_departement', string='Commune', required=False)
    x_village_ids = fields.Many2many(comodel_name='ref_village', string='Secteur/Village', required=False)
    gestionnaire_ids = fields.Many2many(comodel_name='res.users', string='Gestionnaires')
    date = fields.Date(string='Date', required=False)

    line_ids = fields.One2many('credit_credit_port_risque_line', inverse_name='synthese_id', string='Line_ids')
    duree = fields.Selection(
        string='Durée',
        selection=[('90', '90 jours ou plus'),
                   ('120', '120 jours ou plus'),
                   ('270', '270 jours ou plus')],
        default="90", required=True,)

    def set_afficher(self):
        # domain = [('state', '=', 'DC')]
        domain = [('state', '!=', 'DC')]
        if self.bailleur_ids:
            domain.append(('bailleur_id', 'in', self.bailleur_ids.ids))
        if self.zone_ids:
            domain.append(('zone_id', 'in', self.zone_ids.ids))
        if self.x_region_ids:
            domain.append(('region_id', 'in', self.x_region_ids.ids))
        if self.x_province_ids:
            domain.append(('province_id', 'in', self.x_province_ids.ids))
        if self.x_departement_ids:
            domain.append(('departement_id', 'in', self.x_departement_ids.ids))
        if self.x_village_ids:
            domain.append(('village_id', 'in', self.x_village_ids.ids))
        if self.gestionnaire_ids:
            domain.append(('gestionnaire_id', 'in', self.gestionnaire_ids.ids))

        credits = self.env['credit_credit'].search(domain)
        print(credits)
        print(domain)

        self.line_ids.unlink()
        ordre = 1
        for credit in credits:

            ta = self.env['credit_credit_line'].search([('credit_id.id', '=', credit.id)])
            principal_total = 0
            interet_total = 0
            garantie_total = 0
            for l in ta:
                principal_total += l['montant']
                interet_total += l['interet']
                garantie_total += l['garantie']

            rembours = self.env['credit_credit_remboursement_line'].search([('credit_id.id', '=', credit.id)])
            montant_prin_paye = 0
            interet_paye = 0
            garantie_paye = 0
            for l in rembours:
                montant_prin_paye += l['montant_p']
                interet_paye += l['interet_p']
                garantie_paye += l['garantie_p']

            result_p = montant_prin_paye + interet_paye + garantie_paye

            ta = self.env['credit_credit_line'].search([
                ('credit_id.id', '=', credit.id),
                ('date', '<', self.date)])

            montant_p_arriere = 0
            is_date = 1
            # date = self.date
            for l in ta:
                result_p = result_p - l['montant'] - l['interet'] - l['garantie']
                if result_p < 0:
                    if is_date:
                        date = l['date']
                        is_date = 0
                    montant_p_arriere = result_p * -1

            if is_date == 0 and (self.date - date).days >= int(self.duree):
                montant_total = principal_total + interet_total + garantie_total
                montant_total_paye = montant_prin_paye + interet_paye + garantie_paye
                montant_prin_encours = principal_total - montant_prin_paye
                montant_int_encours = interet_total - interet_paye
                montant_fa_encours = garantie_total - garantie_paye
                montant_du = montant_total - montant_total_paye

                montant_risque_1 = montant_du
                montant_risque_30 = 0
                montant_risque_60 = 0
                montant_risque_90 = 0
                montant_risque_120 = 0
                montant_risque_150 = 0
                montant_risque_180 = 0
                montant_risque_270 = 0

                print((self.date - date).days)
                if (self.date - date).days >= 30:
                    montant_risque_30 = montant_risque_1
                if (self.date - date).days >= 60:
                    montant_risque_60 = montant_risque_1
                if (self.date - date).days >= 90:
                    montant_risque_90 = montant_risque_1
                if (self.date - date).days >= 120:
                    montant_risque_120 = montant_risque_1
                if (self.date - date).days >= 150:
                    montant_risque_150 = montant_risque_1
                if (self.date - date).days >= 180:
                    montant_risque_180 = montant_risque_1
                if (self.date - date).days >= 270:
                    montant_risque_270 = montant_risque_1

                self.env['credit_credit_port_risque_line'].create({
                    'ordre': ordre,
                    'name': credit.name,
                    'cliente_id': credit.cliente_id.name,
                    'telephone': credit.cliente_id.telephone,
                    'type_client': credit.type_client.name,
                    'gestionnaire_id': credit.gestionnaire_id.name,
                    'jours_retard': (self.date - date).days,
                    'montant_total': montant_total,
                    'montant_rembourse': montant_total_paye,
                    'montant_du': montant_du,
                    'montant_prin_encours': montant_prin_encours,
                    'montant_int_encours': montant_int_encours,
                    'montant_fa_encours': montant_fa_encours,
                    'montant_risque_90': montant_risque_90,
                    'montant_risque_180': montant_risque_180,
                    'montant_risque_270': montant_risque_270,
                    'synthese_id': self.id,
                })
                ordre = ordre + 1


class CreditCreditPortRisqueLine(models.Model):
    """Definition de la table credit"""

    _name = 'credit_credit_port_risque_line'

    ordre = fields.Integer(string='Ordre', required=False)
    name = fields.Char(string='N°', )
    cliente_id = fields.Char(string='Cliente')
    telephone = fields.Char(string='Cliente')
    type_client = fields.Char('Type de client')
    gestionnaire_id = fields.Char(string='Gestionnaire', )
    montant_total = fields.Float(string='Total', digits=(16, 0))
    montant_rembourse = fields.Float(string='Remboursé', digits=(16, 0))
    montant_du = fields.Float(string='Dû', digits=(16, 0))
    montant_prin_encours = fields.Float(string='Princ. dû ', digits=(16, 0))
    montant_int_encours = fields.Float(string='Int. dû', digits=(16, 0))
    montant_fa_encours = fields.Float(string='Fa. dû', digits=(16, 0))
    montant_p_arriere = fields.Float(string='Montant principal en arriérés', digits=(16, 0))
    montant_prin_non_du = fields.Float(string='Total principal non encore dû', digits=(16, 0))
    jours_retard = fields.Integer(string='Jrs retard', required=False)
    montant_risque_1 = fields.Float(string='1 jours ou plus', digits=(16, 0))
    montant_risque_30 = fields.Float(string='30 jours ou plus', digits=(16, 0))
    montant_risque_60 = fields.Float(string='60 jours ou plus', digits=(16, 0))
    montant_risque_90 = fields.Float(string='90 jrs ou +', digits=(16, 0))
    montant_risque_120 = fields.Float(string='120 jours ou plus', digits=(16, 0))
    montant_risque_150 = fields.Float(string='150 jours ou plus', digits=(16, 0))
    montant_risque_180 = fields.Float(string='180 jrs ou +', digits=(16, 0))
    montant_risque_270 = fields.Float(string='270 jrs ou +', digits=(16, 0))

    synthese_id = fields.Many2one('credit_synthese_demande_region', string='Synthese_id', required=False)
