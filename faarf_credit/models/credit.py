from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _name = "credit_credit"
    _description = "Definition de la table credit"
    _order = 'date_demande desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='N° prêt', required=False, readonly='1', default="-")
    secteur_activite = fields.Many2one("credit_activite", string="Domaine activité", required=False)
    periode_deblocage = fields.Date(string='Période deblocage', required=False)
    num_demande = fields.Char(string='N° Demande', required=False, readonly='1', default="-")
    type_client = fields.Many2one('credit_type_client', 'Type Cliente', required=False)
    type_client_code = fields.Char("code")
    fa = fields.Boolean(string='Fa payé', required=False, )
    fa_state = fields.Selection(string='Fa_state',
                                selection=[('1', 'FA'),
                                           ('2', 'Ordre'),
                                           ('3', 'Restitué'), ],
                                required=False, default="1")

    cycle_credit = fields.Integer(string='Cycle Crédit', required=False)
    nature_credit = fields.Selection(
        string='Type crédit', default="1",
        selection=[('1', 'Nouvelle demande'),
                   ('2', 'Renouvellement'), ],
        required=False, )
    credit_solde = fields.Integer(string='Credit soldé', required=False)

    nbr_benef = fields.Integer(string='Nombre bénéficiare', required=False, default=1)
    commentaires = fields.Html(string='Commentaires', required=False)
    cliente_id = fields.Many2one('credit_clients', string='Cliente', required=True)
    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', required=False)
    superviseur_id = fields.Many2one('res.users', string='Superviseur')
    charge_clientele_id = fields.Many2one('res.users', string='Chargée clientele', default=lambda self: self.env.user)
    current_user_x_zone_ids = fields.Many2many('ref_zone', string='Zone', default=lambda self: self.env.user.x_zone_ids)
    type_produit = fields.Selection(string='Type produit',
                                    selection=[('CREDIT', 'CREDIT'),
                                               ('PROJET', 'Projet/Programme'), ],
                                    required=True)

    date_demande = fields.Date(string='Date Demande', required=True, default=fields.Date.context_today)
    date_debut_paiement = fields.Date(string='Date', required=False, default=fields.Date.context_today)
    date_appro = fields.Date("Date approbation/Rejet", readonly=False)

    montant_demande = fields.Float(string='Montant sollicité ', required=False, digits=(16, 0))
    montant_accorde = fields.Float(string='Montant accordé ', required=False, digits=(16, 0))
    montant_accorde_c = fields.Float(string='Montant comité ', required=False, digits=(16, 0))
    taux_int_annuel = fields.Float(string="Taux d'intérêt annuel", required=False)
    duree_pret = fields.Integer(string='Durée prêt (mois)', required=False)
    periodicite = fields.Selection(string='Periodicité', required=False,
                                   selection=[('1', 'Mensuelle'), ('2', 'Bimensuelle'),
                                              ('3', 'Trimestrielle'), ('4', 'Chaque 4 mois'),
                                              ('5', 'Chaque 5 mois'), ('6', 'Semestrielle'),
                                              ('7', 'Chaque 7 mois'), ('8', 'Chaque 8 mois'),
                                              ('U', 'Unique'), ],
                                   default="1")
    nbr_tranche = fields.Integer(string="Nombre d'échéance", required=False)
    periodicites = fields.Many2one(comodel_name='credit_periodicite', string='Periodicité', required=False)
    meth_cal_interet = fields.Selection(string='Méthode de calcul', required=False,
                                        selection=[('1', 'Amortissement linéaire'),
                                                   ('2', 'Amortissement dégressif')], default="1")
    montant_mensualite = fields.Float(string="Mensualite", required=False, digits=(16, 0),
                                      compute="calcul_montant_interet", store=True)
    montant_interet = fields.Float(string="Montant d'intérêt", required=False, digits=(16, 0),
                                   compute="calcul_montant_interet", store=True)
    total_rembourser = fields.Float(string="Total à rembourser", required=False, digits=(16, 0),
                                    compute="calcul_total_rembourser", store=True)

    taux_int_garantie = fields.Float(string="Taux FA", required=False)
    montant_garantie = fields.Float(string="FA", required=False, digits=(16, 0),
                                    compute="calcul_montant_garantie", store=True)
    taux_frais_dossier = fields.Float(string="Taux frais dossier", required=False, default=1)
    montant_frais_dossier = fields.Float(string='Frais dossier', required=False, digits=(16, 0),
                                         compute="calcul_frais_dossier")
    is_assurance = fields.Boolean(string='Assurance ?', required=False)
    assureur_id = fields.Many2one('credit_assureur', string='Assureur', required=False)
    frais_assurance = fields.Float(string="Frais assurance", required=False, digits=(16, 0), )
    montant_ass_gest = fields.Float(string='Mnt gestionnaire', required=False, digits=(16, 0),
                                    compute="calcul_frais_assurances")
    montant_ass_bailleur = fields.Float(string='Mnt Bailleur', required=False, digits=(16, 0),
                                        compute="calcul_frais_assurances")
    montant_assureur = fields.Float(string='Assureur', required=False, digits=(16, 0),
                                    compute="calcul_frais_assurances")
    # nbr_tranche = fields.Integer(string='Durée de prêt', required=True)

    differe_paiement = fields.Integer(string='Différé de paiement', required=False)
    commission = fields.Float(string='Commission de crédit', required=False, digits=(16, 0))
    cap_der_chance = fields.Float(string='Capital de la dernière tranche', required=False, digits=(16, 0))
    bailleur_id = fields.Many2one('credit_bailleur', string='Bailleur', required=False)
    produit_credit = fields.Many2one('credit_param_produit', string='Produit crédit', required=False)
    but_credit = fields.Char(string='Objet crédit', required=True)

    document_ids = fields.One2many('credit_credit_document', inverse_name='credit_id', string='Documents',
                                   required=False)
    documents_ids = fields.One2many(
        comodel_name='credit_credit_documents',
        inverse_name='credit_id',
        string='documents',
        required=False)

    # avis
    avis_gestionnaire = fields.Text(string='Avis gestionnaire', required=False)
    # avis_superviseur = fields.Text(string='Avis superviseur', required=False)
    avis_superviseur = fields.Selection(
        string='Avis superviseur',
        selection=[('A', 'Accordée'),
                   ('Aj', 'Ajournée'),
                   ('R', 'Réfusée'), ],
        required=False, )
    montant_superviseur = fields.Float(string="Montant proposé", required=False, digits=(16, 0))
    avis_commite_antenne = fields.Text(string="Avis du comité", required=False)
    avis_commite_credit = fields.Text(string='Avis du comité', required=False)
    avis_directrice = fields.Text(string='Avis de la Directrice', required=False)
    avis_commite_ca = fields.Text(string="Avis du comité", required=False)

    # comite
    date_comite_r = fields.Date("Date approbation/Rejet", readonly=False, default=fields.Date.context_today)

    # localisation
    zone_id = fields.Many2one("ref_zone", "Zone", required=True)
    region_id = fields.Many2one("ref_region", "Région", required=True)
    province_id = fields.Many2one("ref_province", "Province", required=True)
    departement_id = fields.Many2one("ref_departement", "Commune", required=True)
    village_id = fields.Many2one("ref_village", "Secteur/Village", required=True)
    localisation = fields.Text(string='Autres informations', required=False)
    telephone = fields.Char("Téléphone", required=True, related="cliente_id.telephone")
    telephone_est_pro = fields.Boolean('Téléphone (est propiétaire)?', required=False,
                                       related="cliente_id.telephone_est_pro")
    proprietaire = fields.Char("Propiétaire", required=False, related="cliente_id.proprietaire")
    mail = fields.Char("E-mail", related="cliente_id.mail")
    personne_a_contacte = fields.Char("Personne à contacter", required=False, related="cliente_id.personne_a_contacte")
    telephone_pers_a_contacte = fields.Char("Téléphone", required=False, related="cliente_id.telephone_pers_a_contacte")

    # groupement/association
    membres_ids = fields.One2many('credit_credit_membre', inverse_name='credit_id', string='Membres', required=False)
    presidente_id = fields.Many2one('credit_client_membre', string='Présidente', required=False,
                                    related="cliente_id.presidente_id")
    secretaire_id = fields.Many2one('credit_client_membre', string='Secrétaire', required=False,
                                    related="cliente_id.secretaire_id")
    tresoriere_id = fields.Many2one('credit_client_membre', string='Trésorière', required=False,
                                    related="cliente_id.tresoriere_id")

    # compte d'exploitation
    compte_exploit_ids = fields.One2many('credit_compte_exploitation', inverse_name='credit_id',
                                         string="Compte d'exploitation", required=False)

    # ligne pour tableau d'amortissement
    credit_lignes_ids = fields.One2many(
        comodel_name="credit_credit_line", inverse_name='credit_id', string="Tableau d'amortissement", required=False)

    # Notation
    crit_fondamentaux_ids = fields.One2many(
        comodel_name='credit_credit_crit_fond', inverse_name='produit_id', string='Critères fondamentaux',
        required=False)

    crit_complementaires_ids = fields.One2many(
        comodel_name='credit_credit_crit_compl', inverse_name='produit_id', string='Critères Complementaires',
        required=False)
    note = fields.Integer(string='Note', required=False, compute="calcul_note", store=True)
    notes = fields.Integer(string='Note', required=False, compute="calcul_note", store=True)
    is_antenne = fields.Boolean(string='Montant max. antenne régionale', compute='cal_onchange_produit_mtn')
    is_com_credit = fields.Boolean(string='Montant max. comité crédit', compute='cal_onchange_produit_mtn')
    is_dg = fields.Boolean(string='Montant max. directrice', compute='cal_onchange_produit_mtn')
    ordre_remboursment = fields.Selection(string='Ordre de remboursement',
                                          selection=[('1', 'Garantie -> Capital -> Intérêt'),
                                                     ('2', 'Garantie -> Intérêt -> Capital'),
                                                     ('3', 'Capital -> Intérêt -> Garantie'),
                                                     ('4', 'Capital -> Garantie -> Intérêt'),
                                                     ('5', 'Intérêt -> Capital -> Garantie'),
                                                     ('6', 'Intérêt -> Garantie -> Capital'), ],
                                          required=False, default='1')

    is_affiche = fields.Boolean(string='is affiche', required=False, default=0)

    # eeeee
    delais_grace = fields.Integer(string='Nombre de bénéficiare', required=False, default=1)
    is_interet_decaiss = fields.Boolean(string='Intérêt payé au décaissement',
                                        required=False)
    is_interet_deb = fields.Boolean(string='Intérêt payé au début de tranche',
                                    required=False, )
    is_fa = fields.Boolean(string='FA', required=False)
    is_garantie_decaiss = fields.Boolean(string='FA payé au décaissement',
                                         required=False, )
    is_garantie_deb = fields.Boolean(string='FA payé au début de tranche',
                                     required=False, )
    is_unique = fields.Boolean(string='Echéance unique', required=False)
    is_unique_int = fields.Boolean(string='Echéance unique/intérêt', required=False)

    credit_pv_id = fields.Many2one('credit_credit_pv', string='Credit_pv', required=False)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    required=True)


    # @api.model
    # def create(self, vals):
    #     credits = self.env['credit_credit'].search([('cliente_id', '=', vals.get('cliente_id'))])
    #     if credits:
    #        raise  ValidationError("Cliente à déja un crédit en cours")
    #
    #     result = super(CreditCredit, self).create(vals)
    #     return result

    def unlink(self):
        for val in self:
            if val.num_demande:
                raise ValidationError("Vous ne pouvez pas supprimer cette demande")

            return super(CreditCredit, self).unlink()

    @api.depends('crit_fondamentaux_ids', 'crit_complementaires_ids')
    def calcul_note(self):
        for val in self:
            note = 0
            for c in val.crit_fondamentaux_ids:
                note = note + c.score
            for c in val.crit_complementaires_ids:
                note = note + c.score

            val.note = note

    def affiche_document(self):
        sc = self.type_client.codification == '01'
        ef = self.type_client.codification == '02'
        grp = self.type_client.codification == '03'
        ass = self.type_client.codification == '04'
        gs = self.type_client.codification == '05'
        ind = self.type_client.codification == '06'

        domain = [('produit_id', '=', self.produit_credit.id)]
        if sc:
            domain.append(('sc', '=', True))
        elif ef:
            domain.append(('ef', '=', True))
        elif grp:
            domain.append(('grp', '=', True))
        elif ass:
            domain.append(('ass', '=', True))
        elif gs:
            domain.append(('gs', '=', True))
        elif ind:
            domain.append(('ind', '=', True))
        else:
            return 0

        result = self.env['credit_prod_document'].search(domain)

        self.documents_ids.unlink()
        x_lines_ids = []
        for r in result:
            x_lines_ids.append((0, 0,
                                {'name': r.name, 'est_obligatoire': r.est_obligatoire,
                                 }))
        self.documents_ids = x_lines_ids

    @api.onchange('is_interet_deb')
    def onchange_is_interet_deb(self):
        for val in self:
            val.is_interet_decaiss = 1
            val.is_interet_decaiss = 0
            print(val.is_interet_decaiss)

    @api.onchange('is_interet_decaiss')
    def onchange_is_interet_decaiss(self):
        for val in self:
            val.is_interet_deb = False

    @api.onchange('is_garantie_deb')
    def onchange_is_garantie_deb(self):
        for val in self:
            val.is_garantie_decaiss = False

    @api.onchange('is_garantie_decaiss')
    def onchange_is_garantie_decaiss(self):
        for val in self:
            val.is_garantie_deb = False

    def name_get(self):
        result = []
        for rec in self:
            if rec.name != '-':
                result.append((rec.id, '%s - %s' % (rec.name, rec.cliente_id.name)))
            elif rec.num_demande != '-':
                result.append((rec.id, '%s - %s' % (rec.num_demande, rec.cliente_id.name)))
            else:
                result.append((rec.id, '00000 - %s' % (rec.cliente_id.name)))
        return result

    @api.onchange('cliente_id')
    def on_change_cliente_id(self):
        for val in self:
            val.zone_id = val.cliente_id.zone_id
            val.region_id = val.cliente_id.region_id
            val.province_id = val.cliente_id.province_id
            val.departement_id = val.cliente_id.departement_id
            val.village_id = val.cliente_id.village_id

            # val.gestionnaire_id = val.cliente_id.gestionnaire_id
            # val.superviseur_id = val.cliente_id.gestionnaire_id.x_superviseur_id
            val.type_client = val.cliente_id.type_client
            val.type_client_code = val.type_client.code

            # credit_client_solde = val.env['credit_credit'].search([
            #     ('cliente_id', '=', val.cliente_id.id),
            #     ('membre_ids.membre_id.id', '=', val.cliente_id.id),
            #     ('state', '=', 'RB')])
            # val.credit_solde = len(credit_client_solde) ('state', '=', 'RB')

            credits = self.env['credit_credit'].search([])
            credit_solde = 0
            for c in credits:
                print(c.cliente_id.nip)
                print(self.cliente_id.nip)
                print("***")
                if c.cliente_id.nip == self.cliente_id.nip:
                    credit_solde += 1

                # for m in c.membres_ids:
                #     if m.nip == self.cliente_id.nip:
                #         credit_solde += 1

            val.credit_solde = credit_solde

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
                val.superviseur_id = gestionnaire_id.x_superviseur_id

    @api.onchange('produit_credit')
    def onchange_produit_credit(self):
        for val in self:
            if val.type_client_code == "IND":
                val.taux_int_garantie = val.produit_credit.taux_garantie
                val.taux_frais_dossier = val.produit_credit.taux_frais_dossier
                if val.cliente_id.pvh == 'Y':
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel_psh
                else:
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel
            elif val.type_client_code == "GROUP":
                val.taux_int_garantie = val.produit_credit.taux_garantie_gs
                val.taux_frais_dossier = val.produit_credit.taux_frais_dossier_gs
                if val.cliente_id.pvh == 'Y':
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel_psh_gs
                else:
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel_gs
            else:
                val.taux_int_garantie = val.produit_credit.taux_garantie_ass
                val.taux_frais_dossier = val.produit_credit.taux_frais_dossier_ass
                if val.cliente_id.pvh == 'Y':
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel_psh_ass
                else:
                    val.taux_int_annuel = val.produit_credit.taux_int_annuel_ass

            val.ordre_remboursment = val.produit_credit.ordre_remboursment
            read_group_res = val.env['credit_credit'].read_group(domain=[('produit_credit', '=', val.produit_credit.id),
                                                                         ('cliente_id', '=', val.cliente_id.id)],
                                                                 fields=['cycle_credit:max'],
                                                                 groupby=['cliente_id'])
            val.cycle_credit = 1
            for c in read_group_res:
                if c.get('cycle_credit'):
                    val.cycle_credit = c.get('cycle_credit') + 1
                else:
                    val.cycle_credit = 1

            val.nature_credit = '1'
            if val.cycle_credit > 1:
                val.nature_credit = '2'

    @api.onchange('produit_credit', 'montant_accorde')
    def cal_onchange_produit_mtn(self):

        for val in self:
            val.is_antenne = 0
            val.is_com_credit = 0
            val.is_dg = 0
            val.is_antenne = val.montant_accorde <= val.produit_credit.montant_max_antenne
            val.is_com_credit = val.montant_accorde <= val.produit_credit.montant_max_com_credit
            val.is_dg = val.montant_accorde <= val.produit_credit.montant_max_dg

    @api.onchange('montant_demande')
    def calcul_montant_accorde(self):
        for val in self:
            val.montant_accorde = val.montant_demande
            val.montant_superviseur = val.montant_demande

    @api.onchange('montant_accorde_c')
    def calcul_montant_accorde_c(self):
        for val in self:
            if val.montant_accorde_c <= val.montant_demande:
                val.montant_accorde = val.montant_accorde_c

    @api.onchange('duree_pret', 'periodicite')
    def on_change_duree_pret(self):
        for val in self:
            val.nbr_tranche = 0
            if val.periodicite == 'U':
                periodicite = 1
                if val.duree_pret:
                    periodicite = val.duree_pret
            else:
                periodicite = int(val.periodicite)

            nbr_tranche = int(val.duree_pret / periodicite)
            nbr_tranche = nbr_tranche * periodicite

            if nbr_tranche == val.duree_pret:
                val.nbr_tranche = val.duree_pret / periodicite

    @api.depends('montant_accorde', 'nbr_tranche', 'taux_int_annuel', 'periodicite', 'meth_cal_interet')
    def calcul_montant_interet(self):
        for val in self:
            val.montant_mensualite = 0
            if val.meth_cal_interet == '1':
                periodicite = 1
                if val.periodicite == 'U':
                    if val.duree_pret:
                        periodicite = val.duree_pret
                else:
                    periodicite = int(val.periodicite)

                nbr_tranche = int(val.nbr_tranche)
                nbr_mois = periodicite * nbr_tranche

                taux_int_annuel_mensuel = (val.taux_int_annuel / 100) / 12
                interet_mensuel = val.montant_accorde * taux_int_annuel_mensuel
                # interet_annuel = self.montant_accorde * (self.taux_int_annuel / 100)
                interet = interet_mensuel * nbr_mois
                val.montant_interet = round(interet)
            else:
                periodicite = 1
                if val.periodicite == 'U':
                    if val.duree_pret:
                        periodicite = val.duree_pret
                else:
                    periodicite = int(val.periodicite)

                c = val.montant_accorde  # capital
                t_mensuel = (val.taux_int_annuel / 100) / 12  # taux mensuel
                nbr_tranche = int(val.nbr_tranche)
                n = periodicite * nbr_tranche  # nombre de mois
                mensualite = (c * t_mensuel) / (1 - pow((1 + t_mensuel), (-1 * n)))

                val.montant_mensualite = mensualite
                total_a_rembourse = mensualite * n
                val.montant_interet = round(total_a_rembourse - val.montant_accorde)

    @api.depends('montant_interet')
    def calcul_total_rembourser(self):
        for val in self:
            val.total_rembourser = val.montant_accorde + val.montant_interet + val.montant_garantie

    @api.depends('montant_accorde', 'taux_int_garantie')
    def calcul_montant_garantie(self):
        for val in self:
            val.montant_garantie = round((val.montant_accorde * val.taux_int_garantie) / 100)

    @api.depends('montant_accorde', 'taux_frais_dossier')
    def calcul_frais_dossier(self):
        for val in self:
            val.montant_frais_dossier = round((val.montant_accorde * val.taux_frais_dossier) / 100)

    @api.depends('assureur_id', 'bailleur_id', 'frais_assurance')
    def calcul_frais_assurances(self):
        for val in self:
            val.montant_ass_bailleur = 0
            val.montant_ass_gest = 0
            val.montant_assureur = 0
            if val.bailleur_id and val.assureur_id and val.frais_assurance:
                result = self.env['credit_param_assureur'].search([('assureur_id', '=', val.assureur_id.id),
                                                                   ('bailleur_id', '=', val.bailleur_id.id)])
                if result:
                    val.montant_ass_bailleur = round((val.frais_assurance * result[0].taux_bailleur) / 100)
                    val.montant_ass_gest = round((val.frais_assurance * result[0].taux_gestionnaire) / 100)
                    val.montant_assureur = round((val.frais_assurance * result[0].taux_assureur) / 100)

    def calcul_tableau_amortissement(self):
        """Cela crée automatiquement le versement que le client doit payer
        en fonction de la date de début de paiement et du nombre de versements."""
        for credit in self:
            credit.credit_lignes_ids.unlink()
            if credit.meth_cal_interet == '1':
                if credit.is_interet_deb and credit.is_garantie_deb:
                    pass
                elif credit.is_interet_deb and credit.is_garantie_decaiss:
                    pass
                if credit.is_interet_decaiss and credit.is_garantie_deb:
                    pass
                elif credit.is_interet_decaiss and credit.is_garantie_decaiss:
                    pass
                elif credit.is_interet_deb:
                    credit.ta_interet_debut(credit)
                elif credit.is_interet_decaiss:
                    credit.ta_interet_decaiss(credit)
                elif credit.is_garantie_deb:
                    credit.ta_fa_debut(credit)
                elif credit.is_garantie_decaiss:
                    credit.ta_fa_decaiss(credit)
                else:
                    credit.ta_normal(credit)
            else:
                credit.ta_normal_degressif(credit)

        return True

    @api.onchange('membres_ids')
    def onchange_membres_ids(self):
        for val in self:
            if val.type_client_code in ('ASS', 'GROUP'):
                val.nbr_benef = len(val.membres_ids)
            else:
                val.nbr_benef = 1

    def genere_num_credit(self):
        credit_compteur = self.env['credit_compteur_credit'].search(
            [('code_gestionnaire', '=', self.gestionnaire_id.code_gestionnaire)])
        nombre = 1
        if credit_compteur:
            nombre = credit_compteur.nombre + 1
            credit_compteur.nombre = nombre
            nombre = str(nombre).zfill(6)
        else:
            self.env['credit_compteur_credit'].create({
                'nombre': 1,
                'code_gestionnaire': self.gestionnaire_id.code_gestionnaire
            })
            nombre = str(nombre).zfill(6)
        self.name = str(self.province_id.code_province) + str(self.gestionnaire_id.code_gestionnaire) + nombre


class CreditCreditLine(models.Model):
    _name = "credit_credit_line"
    _description = "Line du tableau d'amortissement"

    numero = fields.Integer(string='N°', required=False)
    date = fields.Date(string="Date", required=False, )
    montant = fields.Float(string="Principal dû", required=False, digits=(16, 0))
    interet = fields.Float(string="Intérêt dû", required=False, digits=(16, 0))
    garantie = fields.Float(string="FA dû", required=False, digits=(16, 0))
    total = fields.Float(string="Total", required=False, digits=(16, 0))

    credit_id = fields.Many2one('credit_credit', string='Crédit', required=False)


class CreditCreditMembre(models.Model):
    """ cette classe defini un membre d'un groupement / association / groupe solidaire"""
    _name = "credit_credit_membre"
    _description = ""

    name = fields.Many2one('credit_client_membre', string='Membre', required=False, )
    membre_id = fields.Many2one('credit_clients', string='Membre', required=True)
    nom = fields.Char(string='Nom et Prénoms', required=False, related='membre_id.name')
    nip = fields.Char(string='N.I.P', required=False, related='membre_id.nip')
    num_piece = fields.Char(string='CNIB', required=False, related='membre_id.num_piece')
    telephone = fields.Char(string='Téléphone', required=False, related='membre_id.telephone')
    rang = fields.Integer(string='Rang Crédit', required=False)
    montant = fields.Float(string='Montant sollicité', required=True)
    montant_propose = fields.Float(string='Montant proposé', required=True)
    montant_debloque = fields.Float(string='Montant débloqué', required=True)
    secteur_activite = fields.Many2one("credit_activite", string="Domaine activité", required=False)
    domaine_active = fields.Char(
        string='Activité individuelle',
        required=False)
    titre = fields.Selection(
        string='Titre',
        selection=[('P', 'Présidente'),
                   ('S', 'Secrétaire'),
                   ('T', 'Trésorière'), ],
        required=False, default="P")
    titres = fields.Many2one(
        comodel_name='credit_client_titre_membre',
        string='Titre',
        required=False)

    # membre_ids = []

    credit_id = fields.Many2one('credit_credit', string='Credit', required=False)
    client_id = fields.Many2one('credit_clients', string='Client', required=False,
                                compute="on_change_credit_id", )
    membres_ids = fields.Many2many(comodel_name='credit_clients', string='Membres_ids',
                                   compute="on_change_credit_id", store=False)

    # @api.model
    # def create(self, vals):
    #     if not vals['client_id']:
    #         raise ValidationError("Veuillez d'abord selectionner la cliente avant d'en choisir les membres")
    #
    #     rec = self._cr.execute("SELECT * FROM client_clients WHERE parent_id=%s and child_id=%s",
    #                            [vals['client_id'], vals['membre_id']])
    #
    #     if not rec:
    #         self._cr.execute("INSERT INTO client_clients (parent_id, child_id) values (%s, %s)",
    #                          [vals['client_id'], vals['membre_id']])
    #
    #     result = super(CreditCreditMembre, self).create(vals)
    #     return result
    #
    # def write(self, vals):
    #     """Override default Odoo write function and extend."""
    #     result = super(CreditCreditMembre, self).write(vals)
    #
    #     print("Maxx1")
    #     if not self.client_id:
    #         raise ValidationError("Veuillez d'abord selectionner la cliente avant de choisir les membres")
    #
    #     self._cr.execute("SELECT * FROM client_clients WHERE parent_id=%s and child_id=%s",
    #                      [self.client_id.id, self.membre_id.id])
    #     rec = self._cr.fetchall()
    #     print("Maxx2")
    #     print(rec)
    #     if not rec:
    #         self._cr.execute("INSERT INTO client_clients (parent_id, child_id) values (%s, %s)",
    #                          [self.client_id.id, self.membre_id.id])
    #
    #     return result

    @api.depends('credit_id')
    def on_change_credit_id(self):
        self.membres_ids = self.credit_id.cliente_id.membres_ids.ids
        self.client_id = self.credit_id.cliente_id
        # return {'domain':
        #             {'membre_id': [('id', 'in', self.credit_id.cliente_id.membres_ids.ids)]},
        #         }


class CreditCreditDocument(models.Model):
    _name = "credit_credit_document"
    _description = "Autres documents"

    name = fields.Char(string='Titre', required=False)
    document = fields.Binary(string="Document")
    est_obligatoire = fields.Boolean(string='Obligatoire ?', required=False)

    credit_id = fields.Many2one('credit_credit', string='Credit', required=False)


# Critere de notation credit
class CreditCreditCritereFond(models.Model):
    """Definir un type de client."""

    _name = "credit_credit_crit_fond"
    _description = ""

    name = fields.Char(string="Eléments d'analyse", required=True)
    borne_sup = fields.Integer(string='Borne supérieure', required=True)
    borne_inf = fields.Integer(string='Borne inférieure', required=True)
    bareme = fields.Integer(string='Barème', required=False)
    score = fields.Integer(string='Score', required=False)

    sequence = fields.Integer(string='Séquence', required=True)

    produit_id = fields.Many2one(
        comodel_name='credit_credit',
        string='Produit_id',
        required=False)


class CreditCreditCritereComp(models.Model):
    """Definir un type de client."""

    _name = "credit_credit_crit_compl"
    _description = ""

    name = fields.Char(string="Eléments d'analyse", required=True)
    borne_sup = fields.Integer(string='Borne supérieure', required=True)
    borne_inf = fields.Integer(string='Borne inférieure', required=True)
    bareme = fields.Integer(string='Barème', required=False)
    score = fields.Integer(string='Score', required=False)

    sequence = fields.Integer(string='Séquence', required=True)

    produit_id = fields.Many2one(
        comodel_name='credit_credit',
        string='Produit_id',
        required=False)


class CreditCreditDocument(models.Model):
    """Definir un type de client."""

    _name = "credit_credit_documents"
    _description = ""

    name = fields.Char(string="Titre", required=True)
    est_obligatoire = fields.Boolean(string='Obligatoire ?', required=False)
    fichier = fields.Binary(string="", )

    credit_id = fields.Many2one(
        comodel_name='credit_credit',
        string='Produit_id',
        required=False)
