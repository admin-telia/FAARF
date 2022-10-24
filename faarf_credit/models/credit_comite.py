from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCreditCommiteRegional(models.TransientModel):
    """ """
    _name = "credit_credit_comite_regional"
    _description = ""

    def _default_name(self):
        return "Comité regional"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=False)
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    note = fields.Integer(
        string='Note',
        required=False)
    note_inf = fields.Selection(
        string='Note Inf.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="1")
    note_sup = fields.Selection(
        string='Note Sup.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="20")

    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)

    commite_id = fields.Many2one(
        comodel_name='credit_credit_pv',
        string='Commité',
        required=True)

    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_dossier = fields.Integer(string='Nombre de dossiers', required=False, compute="calcul_nbr_dossier")

    @api.depends('credit_ids')
    def calcul_nbr_dossier(self):
        for val in self:
            val.nbr_dossier = len(val.credit_ids)

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        domain = [
            ('state', '=', 'CR'),
            ('bailleur_id', '=', self.bailleur_id.id),
            # ('produit_credit', '=', self.produit_credit.id),
            ('zone_id', '=', self.zone_id.id),
        ]
        if self.superviseur_id:
            domain.append(('superviseur_id', '=', self.superviseur_id.id))

        if self.note_inf:
            domain.append(('note', '>=', int(self.note_inf)))

        if self.note_sup:
            domain.append(('note', '<=', int(self.note_sup)))

        credit_ids = self.env['credit_credit'].search(domain)
        for c in credit_ids:
            c.credit_pv_id = self.commite_id

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})

    def set_accorde_r(self):
        for c in self.credit_ids:
            if c.is_antenne:
                c.set_accorde_r()

    def set_ajourne_r(self):
        for c in self.credit_ids:
            if c.is_antenne:
                c.set_ajourne_r()

    def set_refuse_r(self):
        for c in self.credit_ids:
            if c.is_antenne:
                c.set_refuse_r()

    # @api.onchange('credit_ids')
    # def on_change_cliente_id(self):
    #     print("maaa")
    #     self.afficher()


class CreditCreditCommiteCentral(models.TransientModel):
    """ """
    _name = "credit_credit_comite_central"
    _description = ""

    def _default_name(self):
        return "Comité Central"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    note_inf = fields.Selection(
        string='Note Inf.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="1")
    note_sup = fields.Selection(
        string='Note Sup.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="20")

    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)

    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_dossier = fields.Integer(string='Nombre de dossiers', required=False, compute="calcul_nbr_dossier")

    commite_id = fields.Many2one(
        comodel_name='credit_credit_pv',
        string='Commité',
        required=True)

    @api.depends('credit_ids')
    def calcul_nbr_dossier(self):
        for val in self:
            val.nbr_dossier = len(val.credit_ids)

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        domain = [
            ('state', '=', 'CC'),
            ('bailleur_id', '=', self.bailleur_id.id),
            # ('produit_credit', '=', self.produit_credit.id),
            ('zone_id', '=', self.zone_id.id),
        ]
        if self.superviseur_id:
            domain.append(('superviseur_id', '=', self.superviseur_id.id))

        if self.note_inf:
            domain.append(('note', '>=', int(self.note_inf)))

        if self.note_sup:
            domain.append(('note', '<=', int(self.note_sup)))

        credit_ids = self.env['credit_credit'].search(domain)
        for c in credit_ids:
            c.credit_pv_id = self.commite_id

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})

    def set_accorde_r(self):
        for c in self.credit_ids:
            if c.is_com_credit:
                c.set_accorde_cc()

    def set_ajourne_r(self):
        for c in self.credit_ids:
            if c.is_com_credit:
                c.set_ajourne_cc()

    def set_refuse_r(self):
        for c in self.credit_ids:
            if c.is_com_credit:
                c.set_refuse_cc()


class CreditCreditCommiteDG(models.TransientModel):
    """ """
    _name = "credit_credit_comite_dg"
    _description = ""

    def _default_name(self):
        return "DG"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    note_inf = fields.Selection(
        string='Note Inf.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="1")
    note_sup = fields.Selection(
        string='Note Sup.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="20")

    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)

    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_dossier = fields.Integer(string='Nombre de dossiers', required=False, compute="calcul_nbr_dossier")

    @api.depends('credit_ids')
    def calcul_nbr_dossier(self):
        for val in self:
            val.nbr_dossier = len(val.credit_ids)

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        domain = [
            ('state', '=', 'DG'),
            ('bailleur_id', '=', self.bailleur_id.id),
            # ('produit_credit', '=', self.produit_credit.id),
            ('zone_id', '=', self.zone_id.id),
        ]
        if self.superviseur_id:
            domain.append(('superviseur_id', '=', self.superviseur_id.id))

        if self.note_inf:
            domain.append(('note', '>=', int(self.note_inf)))

        if self.note_sup:
            domain.append(('note', '<=', int(self.note_sup)))

        credit_ids = self.env['credit_credit'].search(domain)
        for c in credit_ids:
            c.credit_pv_id = self.commite_id

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})

    def set_accorde_r(self):
        for c in self.credit_ids:
            if c.is_dg:
                c.set_accorde_dg()

    def set_ajourne_r(self):
        for c in self.credit_ids:
            if c.is_dg:
                c.set_ajourne_dg()

    def set_refuse_r(self):
        for c in self.credit_ids:
            if c.is_dg:
                c.set_refuse_dg()


class CreditCreditCommiteCA(models.TransientModel):
    """ """
    _name = "credit_credit_comite_ca"
    _description = ""

    def _default_name(self):
        return "Comité regional"

    name = fields.Char(string='Name', required=False, default=_default_name)

    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=True)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=True)
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    note_inf = fields.Selection(
        string='Note Inf.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="1")
    note_sup = fields.Selection(
        string='Note Sup.',
        selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
                   ('10', '10'),
                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                   ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ],
        required=False, default="20")
    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)

    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')

    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)

    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    nbr_dossier = fields.Integer(string='Nombre de dossiers', required=False, compute="calcul_nbr_dossier")

    @api.depends('credit_ids')
    def calcul_nbr_dossier(self):
        for val in self:
            val.nbr_dossier = len(val.credit_ids)

    def unlink(self):
        self.credit_ids = [(5, 0, 0)]

    def afficher(self):
        domain = [
            ('state', '=', 'CCA'),
            ('bailleur_id', '=', self.bailleur_id.id),
            # ('produit_credit', '=', self.produit_credit.id),
            ('zone_id', '=', self.zone_id.id),
        ]
        if self.superviseur_id:
            domain.append(('superviseur_id', '=', self.superviseur_id.id))

        if self.note_inf:
            domain.append(('note', '>=', int(self.note_inf)))

        if self.note_sup:
            domain.append(('note', '<=', int(self.note_sup)))

        credit_ids = self.env['credit_credit'].search(domain)
        for c in credit_ids:
            c.credit_pv_id = self.commite_id

        self.credit_ids = [(5, 0, 0)]
        self.sudo().write({'credit_ids': credit_ids})

    def set_accorde_r(self):
        pass

    def set_ajourne_r(self):
        pass

    def set_refuse_r(self):
        pass
