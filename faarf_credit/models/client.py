from odoo import models, fields, api, _
from odoo.http import request
from datetime import datetime
from odoo.exceptions import ValidationError


class CreditClient(models.Model):
    """Definir un client infividuelle"""

    _name = "credit_clients"
    _description = "Faarf client"
    _order = "numero_client"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Nom", required=True)
    parent_id = fields.Many2one('credit_clients', string='Parent', index=True, ondelete="restrict")

    def _default_type_client(self):
        types_clients = self.env['credit_type_client'].search([('code', '=', 'IND')])
        if types_clients:
            for t in types_clients:
                return t

    type_client = fields.Many2one('credit_type_client', 'Type client', required=False, default=_default_type_client)
    type_client_code = fields.Char("code", related='type_client.code')
    numero_client = fields.Char("N° client", readonly=True)
    cycle_credit = fields.Integer(string='Cycle de crédit', required=False)
    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=True, )

    # identification
    # individuelle
    photo = fields.Binary('Photo', help="Joindre la photo de l'étudiant")
    signature = fields.Binary(string='Signature', required=False, compute_sudo= True)
    type_piece = fields.Many2one('ref_type_piece', string='Type pièce', required=False)
    copie_cnib = fields.Binary('Copie pièce', help="", track_visibility='always')
    num_piece = fields.Char("N° Pièce", track_visibility='always')
    nip = fields.Char("N.I.P")
    dte_piece = fields.Date("Date Ets")
    dte_piece_exp = fields.Date("Date Exp")
    # groupe
    copie_agrement = fields.Binary('Agrément/récépissé', help="")
    num_agrement = fields.Char("N° agré./récép.")
    dte_agrement = fields.Date("Date agré./récép.")
    membre_ids = fields.One2many('credit_client_membre', inverse_name='groupe_id', string='Membres',
                                 required=False)

    hide_type_client = fields.Boolean(string='Hide_type_client', required=False)

    # membres_ids = fields.One2many('credit_clients', inverse_name='parent_id', string='Membres',
    #                              required=False, ondelete="restrict")
    membres_ids = fields.Many2many(
        comodel_name='credit_clients',
        relation="client_clients",
        column1="parent_id",
        column2="child_id",
        string='Membres')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive departments.'))

    # secretaire_id = fields.Many2one('credit_client_membre', string='Secretaire', required=False)
    # secretaire_id = fields.Many2one('credit_client_membre', string='Secretaire', required=False)
    presidente_id = fields.Many2one('credit_client_membre', string='Présidente', required=False)
    secretaire_id = fields.Many2one('credit_client_membre', string='Secrétaire', required=False)
    tresoriere_id = fields.Many2one('credit_client_membre', string='Trésorière', required=False)

    x_presidente_id = fields.Many2one('credit_clients', string='Présidente', required=False)
    x_secretaire_id = fields.Many2one('credit_clients', string='Secrétaire', required=False)
    x_tresoriere_id = fields.Many2one('credit_clients', string='Trésorière', required=False)

    #localisation
    latitude = fields.Float(string='Geo Latitude')
    lat = fields.Float(string='Geo Latitude')
    longitude = fields.Float(string='Geo Longitude')
    date_localization = fields.Date(string='Date_localization', required=False)

    garantie_line_ids = fields.One2many(
        comodel_name='credit_client_garantie',
        inverse_name='cliente_id',
        string='Garantie',
        required=False)

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        print(ip_address)
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize("",
                                        "",
                                        "Ouagadougou",
                                        "",
                                        "Burkina")

            if result:
                partner.write({
                    'latitude': result[0],
                    'longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return True

    # adresse
    telephone = fields.Char("Téléphone", required=True)
    telephone_est_pro = fields.Boolean('Téléphone (propiétaire)?', required=False, default=1)
    proprietaire = fields.Char("Propiétaire", required=False)
    mail = fields.Char("E-mail")
    personne_a_contacte = fields.Char("Personne à contacter", required=False)
    telephone_pers_a_contacte = fields.Char("Téléphone", required=False)
    pays = fields.Many2one("res.country", "Pays")
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    region_id = fields.Many2one("ref_region", "Région", required=True)
    province_id = fields.Many2one("ref_province", "Province", required=True)
    departement_id = fields.Many2one("ref_departement", "Département", required=True)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=True)
    latitude = fields.Float("Latitude")
    longitude = fields.Float("Longitude")
    rue = fields.Char("Rue")
    # ville = fields.Many2one("faarf.ville", "Ville")
    # personnelle
    date_naiss = fields.Date("Date de naissance")
    lieu_naiss = fields.Char("Lieu de naissance")
    etat_civil = fields.Selection([
        ('C', 'Célibataire'), ('M', 'Mariée'),
        ('D', 'Divorcée'), ('V', 'Veuve')], string="Etat civil")
    langues_parles = fields.Char("Langues parlées")
    profession = fields.Char("Profession")
    domaine_activite_id = fields.Many2one('credit_activite', string="Domaine d'activité", required=False)
    nombre_enfants = fields.Integer(string="Nombre d'enfants", required=False)
    personnes_charge = fields.Integer(string='Personnes à charges', required=False)
    pvh = fields.Selection([('Y', 'Oui'), ('N', 'NON')], string="Handicap ?", required=False, default="N")

    autre_info = fields.Text("Autres informationss")

    date_ad = fields.Date("Date adhésion", default=fields.Date.context_today, required=True)
    date_appro = fields.Date("Date approbation", readonly=True)
    state = fields.Selection(string='Etat', readonly=True, default="N",
                             selection=
                             [('N', 'Nouvelle'), ('A', 'Approuvée')], )
    company_id = fields.Many2one('res.company', string='Structure', required=True,
                                 default=lambda self: self.env.company)

    # active = fields.Boolean("Actif", default=True)

    current_user_x_zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zone',
                                               default=lambda self: self.env.user.x_zone_ids)

    @api.model
    def create(self, vals):
        result = super(CreditClient, self).create(vals)
        if result:
            client_compteur = self.env['credit_compteur_client'].search(
                [('type_client.codification', '=', result.type_client.codification)])
            nombre = 1
            if client_compteur:
                nombre = client_compteur.nombre + 1
                client_compteur.nombre = nombre
                nombre = str(nombre).zfill(8)
            else:
                self.env['credit_compteur_client'].create({
                    'nombre': 1,
                    'type_client': result.type_client.id
                })
                nombre = str(nombre).zfill(8)
            result.numero_client = str(result.type_client.codification) + str(result.region_id.libcourt) + nombre
            result.state = 'A'
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', '|',
                      ('numero_client', operator, name), ('name', operator, name),
                      ('nip', operator, name), ('num_piece', operator, name),
                      ('num_agrement', operator, name)
            ]

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         result.append((rec.id, '%s - %s' % (rec.numero_client, rec.name)))
    #     return result

    def get_vehicles(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Crédits',
            'view_mode': 'tree',
            'res_model': 'credit_credit',
            'domain': [('cliente_id', '=', self.id)],
            'context': "{'create': False, 'edit': False, 'delete': False}",
            # 'views': [[self.env.ref('account.view_move_tree').id, 'list'],
            #           [self.env.ref('account.view_move_form').id, 'form']],
        }

    credits_count = fields.Integer(string=' crédits_count', required=False, compute="calcul_credits_count")

    def calcul_credits_count(self):
        self.credits_count = self.env['credit_credit'].search_count([('cliente_id', '=', self.id)])

    @api.onchange('village_id')
    def onchange_x_village_id(self):
        for val in self:
            gestionnaire_id = None
            if val.village_id:
                users = self.env['res.users'].search(
                    [('x_user_role_id.code', '=', 'ROLEGEST')])

                for u in users:
                    for v in u.x_village_ids:
                        if v.id == val.village_id.id:
                            gestionnaire_id = u
                            break

            val.gestionnaire_id = gestionnaire_id

class CreditGroupeMembre(models.Model):
    """ cette classe defini un membre d'un groupement / association / groupe solidaire"""
    _name = "credit_client_membre"
    _description = ""

    name = fields.Char("Nom", required=True)
    numero_membre = fields.Char("N° du membre", readonly=True)
    groupe_id = fields.Many2one('credit_clients', string='Credit', required=False)
    # credit_id = fields.Many2one('credit_credit', string='Crédit', required=False)

    # identification
    # individuelle
    photo = fields.Binary('Photo', help="Joindre la photo de l'étudiant", required=False)
    signature = fields.Binary(string='Signature', required=False, compute_sudo=True)
    copie_cnib = fields.Binary('Copie CNIB', help="", required=True)
    num_piece = fields.Char("N° Pièce", required=True)
    nip = fields.Char("NIP", required=True)
    dte_piece = fields.Date("Date pièce", required=True)
    # adresse
    telephone = fields.Char("Téléphone", required=False)
    mail = fields.Char("E-mail")
    personne_a_contacte = fields.Char("Personne à contacter", required=False)
    telephone_pers_a_contacte = fields.Char("Téléphone", required=False)
    pays = fields.Many2one("res.country", "Pays")
    zone_id = fields.Many2one("ref_zone", "Zone", required=False)
    region_id = fields.Many2one("ref_region", "Région", required=False)
    province_id = fields.Many2one("ref_province", "Province", required=False)
    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    village_id = fields.Many2one("ref_village", "Village/secteur", required=False)
    latitude = fields.Float("Latitude")
    longitude = fields.Float("Longitude")
    rue = fields.Char("Rue")

    # personnelle
    date_naiss = fields.Date("Date de naissance")
    lieu_naiss = fields.Char("Lieu de naissance")
    etat_civil = fields.Selection([
        ('C', 'Célibataire'), ('M', 'Mariée'),
        ('D', 'Divorcée'), ('V', 'Veuve')], string="Etat civil")
    langues_parles = fields.Char("Langues parlées")
    profession = fields.Char("Profession")
    nombre_enfants = fields.Integer(string="Nombre d'enfants", required=False)
    personnes_charge = fields.Integer(string='Personnes à charges', required=False)

    autre_info = fields.Text("Autres informationss")

    date_ad = fields.Date("Date adhésion", default=fields.Date.context_today, required=True)
    date_appro = fields.Date("Date approbation", readonly=True)
    state = fields.Selection(string='Etat', readonly=True, default="N",
                             selection=
                             [('N', 'Nouvelle'), ('A', 'Approuvée')], )

    current_user_x_zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zone',
                                               default=lambda self: self.env.user.x_zone_ids)

    # active = fields.Boolean("Actif", default=True)


class CreditTitreMembre(models.Model):
    """ cette classe defini un membre d'un groupement / association / groupe solidaire"""
    _name = "credit_client_titre_membre"
    _description = ""

    name = fields.Char(string='Titre', required=True)
    code = fields.Char(string='Code', required=False)


class CreditGroupe(models.Model):
    """Definir un client infividuelle"""

    _name = "credit_groupe"
    _description = "Faarf groupement/groupe solodaire"
    _order = "numero_groupe"


class CreditDemandeRendezVous(models.Model):
    """Demande de rendez vous"""
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = "credit_dmde_rendez_vous"
    _description = "Demande de rendez vous"
