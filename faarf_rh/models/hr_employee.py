from odoo import models, fields, api
from datetime import datetime, date


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # Nationalité & Autre Information
    x_nationalite_id = fields.Many2one('ref_nationalite', default=lambda self: self.env['ref_nationalite'].search(
        [('code_nationalite', '=', 'BF')]), string='Nationalité')
    matricule_genere = fields.Char(string="Matricule")
    matricule = fields.Char(string="Mle Fonctionnaire ")
    x_type_piece_id = fields.Many2one("hr_typepiece", string="Type pièce", required=True)
    ref_identification = fields.Char(string='Ref.Identification', required=True)
    # Information de  contact
    tel = fields.Char(string='Telephone', required=True)
    personne_id = fields.Char('Personne à prevenir en cas de besoin', required=True)
    x_email = fields.Char(string="Email")
    # Statut
    genre = fields.Selection([
        ('masculin', 'Masculin'), ('feminin', 'Feminin'),
        ('autre', 'Autre')],
        string='Genre', default="masculin")
    situation_marital = fields.Selection([
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('concubinage', 'Concubinage'),
        ('veuf(ve)', 'Veuf(ve)'),
        ('divorce', 'Divorcé(e)')],
        string='Etat civil', default="celibataire")
    charge_femme = fields.Integer(string="Charge femme", required=True)
    charge_enfant = fields.Integer(string="Charge enfant", required=True, compute="calcul_charge_enfant")
    charge = fields.Integer(store=True, string="Charge total", readonly=True, compute="calcul_charge")
    x_montant_charge = fields.Float(string="Montant charge", readonly=True, store=True, compute='mnt_charge_field')

    # Naissance
    x_date_naissance = fields.Date(string='Date de naissance', required=True)
    x_nb_annee_retraite = fields.Many2one("hr_nbreannee", string="Age de retraite", required=True)
    x_date_retraite = fields.Date(string='Date retraite', compute="_compute_date_retraite")
    lieu_naiss = fields.Many2one('ref_localite', string='Lieu de naissance')
    # Éducation
    x_diplome_id = fields.Many2one("hr_diplome", string="Dernier diplôme")
    x_diplome_recrut_id = fields.Many2one("hr_diplome", string="Diplôme de recrutement")
    branche = fields.Char(string="Branche d'étude")
    ecole = fields.Char(string="Ecole/Université")
    observations = fields.Html(string='Observations')

    # Informations professionnelles
    type_id = fields.Many2one(comodel_name='hr_contract_type', string='Type contrat')  # type contrat
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)
    struct_id = fields.Many2one("hr.payroll.structure", string="Type employé",
                                required=True)  # type employe/srtuture salariale
    struct_id_code = fields.Char(string='Struct_id_code', required=False, related="struct_id.code")
    x_emploi_id = fields.Many2one("hr_emploi", string="Emploi", required=True, )
    x_fonction_id = fields.Many2one("hr_fonctionss", string="Fonction", required=True)
    hr_service = fields.Many2one("hr_service", string="Service")
    x_unite_id = fields.Many2one("hr_unite", string="Unite", required=False)
    x_zone_id = fields.Many2one("hr_zone", string="Zone", required=True)
    x_mode_paiement = fields.Selection([
        ('billetage', 'Billetage'),
        ('virement', 'Virement'),
    ], string="Mode de Paiement", default='virement', required=True)
    num_banque = fields.Char('N° compte bancaire', required=True)
    x_banque_id = fields.Many2one('res.bank', 'Banque', required=True)
    intitule = fields.Char(string="Intitulé du compte")

    date_sercice = fields.Date(string="Date Service")

    # Situation administrative de l'agent dans l'Etat
    x_classees_id = fields.Many2one('hr_classe', string='Classe')
    x_categorie_id = fields.Many2one('hr_categorie', string='Catégorie')
    x_echelle_id = fields.Many2one('hr_echelle', string='Echelle')
    x_echellon_id = fields.Many2one('hr_echellon', string='Echelon')
    x_classification = fields.Char(store=True, string="Classification")
    date_modiff = fields.Date(string='Date effet', default=date.today())
    date_debut = fields.Date(string="Date d'engagement", default=date.today())
    date_fin = fields.Date(string="Date fin")
    x_solde_indiciaire = fields.Float(string="Solde Indiciaire", readonly=True,
                                      compute="cal_sal_base")  # salaire de base des fonctionnaires
    x_solde_indiciaire_net = fields.Float(string="Salaire de base", compute="cal_sal_base",
                                          readonly=True)  # salaire de base des fonctionnaires + montant residence
    x_indice = fields.Float(string='Indice', compute="cal_sal_base")

    # Situation administrative de l'agent dans l'EPE
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=False)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=False)
    x_echellon_c_id = fields.Many2one('hr_echellon', required=False, string='Echelon')
    x_solde_indiciaire_ctrct = fields.Float(string="Salaire de base", required=True)  # salaire de base des contractuels

    date_embauche = fields.Date(string="Date d'embauche", default=date.today())
    date_fin_embauche = fields.Date(string="Date fin")
    date_modiff = fields.Date(string='Date effet', default=date.today())

    # CALCUL DE L'EMOLUMENT
    x_emolument_ctrct = fields.Float(string="Emolument Brut")
    x_taux_retenu_emolmt = fields.Float(string="Taux retenue (%)")
    x_mnt_taux_retenu_emolmt = fields.Float(string="Montant Taux")
    x_emolument_ctrct_net = fields.Float(string="Emolument Net", readonly=True)

    # Declaration variables Indemnités
    x_indem_resp = fields.Float(string="Indemn.Resp", readonly=False)
    x_indem_astr = fields.Float(string="Indemn.Astreinte", compute="cal_indem_astr")
    x_indem_techn = fields.Float(string="Indemn.Technicité", readonly=False)
    x_indem_specif = fields.Float(string="Indemn.Spécifique GRH", readonly=False)
    x_indem_loge = fields.Float(string="Indemn.Logement", readonly=False)
    x_indem_transp = fields.Float(string="Indemn.Transport", readonly=False)
    x_indem_inform = fields.Float(string="Indemn.Informatique", readonly=False)
    x_indem_exploit = fields.Float(string="Indemn.Exploitation-Réseau", readonly=False)
    x_indem_finance = fields.Float(string="Indemn.Resp.Financière", readonly=False)
    x_indem_garde = fields.Float(string="Indemn.Garde", readonly=False)
    x_indem_risque = fields.Float(string="Indemn.Risque.Contagion", readonly=False)
    x_indem_suj = fields.Float(string="Indemn.Sujétion Géographique", readonly=False)
    x_indem_form = fields.Float(string="Indemn.Formation", readonly=False)
    x_indem_caisse = fields.Float(string="Indemn.Caisse", readonly=False)
    x_indem_veste = fields.Float(string="Indemn.Vestimentaire", readonly=False)
    x_indem_spec_inspect_trav = fields.Float(string="Indemn.Spécifique Inspecteur de Travail", readonly=False)
    x_indem_spec_inspect_ifc = fields.Float(string="Indemn.Spécifique Forfaitaire Compensatrice", readonly=False)
    x_indem_spec_inspect_irp = fields.Float(string="Indemn.Spécifique de Responsabilité Pécunière", readonly=False)
    x_indem_spec_inspect_ish = fields.Float(string="Indemn.Spécifique Harmonisée Personnel MENA et MESRSI",
                                            readonly=False)
    x_indem_prime_rendement = fields.Float(string="Prime rendement", readonly=False)
    x_indemnite_residence = fields.Float(string='Indemnité de residence', compute="cal_x_indemnite_residence")
    x_allocation_familial = fields.Float(store=True, string='Allocation Familiale', compute='mnt_alloc')

    # exoneration
    x_indem_resp_exo = fields.Float(store=True, string="Exo.Resp", readonly=True,
                                    compute='calcul_exoneration_responsabilite')
    x_indem_astr_exo = fields.Float(store=True, string="Exo.Astreinte", readonly=True,
                                    compute='calcul_exoneration_astreintes')
    x_indem_techn_exo = fields.Float(store=True, string="Exo.Technicité", readonly=True,
                                     compute='calcul_exoneration_technicites')
    x_indem_specif_exo = fields.Float(store=True, string="Exo.Spécifique GRH", readonly=True,
                                      compute='calcul_exoneration_specifiques')
    x_indem_specif_it_exo = fields.Float(store=True, string="Exo.Spécifique IT", readonly=True,
                                         compute='calcul_exoneration_specifiques_it')
    x_indem_specif_irp_exo = fields.Float(store=True, string="Exo.Spécifique IRP", readonly=True,
                                          compute='calcul_exoneration_specifiques_irp')
    x_indem_specif_ifc_exo = fields.Float(store=True, string="Exo.Spécifique IFC", readonly=True,
                                          compute='calcul_exoneration_specifiques_ifc')
    x_indem_specif_ish_exo = fields.Float(store=True, string="Exo.Spécifique ISH", readonly=True,
                                          compute='calcul_exoneration_specifiques_ish')
    x_total_exo = fields.Float(store=True, string="Exo.Total", readonly=True, compute='calcul_exoneration_total')
    x_indem_loge_exo = fields.Float(store=True, string="Exo.Logement", readonly=True,
                                    compute='calcul_exoneration_logement')
    x_indem_transp_exo = fields.Float(store=True, string="Exo.Transport", readonly=True,
                                      compute='calcul_exoneration_transport')
    x_indem_inform_exo = fields.Float(store=True, string="Exo.Informatique", readonly=True,
                                      compute='calcul_exoneration_informatique')
    x_indem_exploit_exo = fields.Float(store=True, string="Exo.Exploitation-Réseau", readonly=True,
                                       compute='calcul_exoneration_exploitation')
    x_indem_finance_exo = fields.Float(store=True, string="Exo.Resp.Financière", readonly=True,
                                       compute='calcul_exoneration_resp_finance')
    x_indem_garde_exo = fields.Float(store=True, string="Exo.Garde", readonly=True, compute='calcul_exoneration_garde')
    x_indem_risque_exo = fields.Float(store=True, string="Exo.Risque.Contagion", readonly=True,
                                      compute='calcul_exoneration_risque')
    x_indem_suj_exo = fields.Float(store=True, string="Exo.Sujétion Géographique", readonly=True,
                                   compute='calcul_exoneration_sujetion')
    x_indem_form_exo = fields.Float(store=True, string="Exo.Formation", readonly=True,
                                    compute='calcul_exoneration_formation')
    x_indem_caisse_exo = fields.Float(store=True, string="Exo.Caisse", readonly=True,
                                      compute='calcul_exoneration_caisse')
    x_indem_veste_exo = fields.Float(store=True, string="Exo.Vestimentaire", readonly=True,
                                     compute='calcul_exoneration_veste')
    x_indem_residence_exo = fields.Float(store=True, string="Exo.Résidence", readonly=True,
                                         compute='calcul_exoneration_residence')
    x_prime_exo = fields.Float(store=True, string="Exo.Prime Rendement", readonly=True,
                               compute='calcul_exoneration_prime')

    # Information Salariale
    x_salaire_base = fields.Float(string="Salaire de base", required=True, compute='cal_sal_base_c_f')
    x_total_indemnites = fields.Float(store=True, string="Totale indemnité", readonly=True, compute='cal_total_indem')
    x_remuneration_total = fields.Float("Rémunération totale", readonly=True, store=True,
                                        compute='calcul_remuneration_total')
    x_salaire_brut = fields.Float(store=True, string="Salaire Brut", readonly=True, compute='calcul_salaire_brut')
    mnt_total_retenues = fields.Float(string='Totale retenue', store=True, readonly=True, compute='cal_total_retenue')
    x_abattement_forfaitaire = fields.Float(store=True, string="Abattement forfaitaire", readonly=True,
                                            compute='calcul_abattement')  # Abattement
    x_salaire_net_imposable = fields.Float(store=True, string="Base imposable", readonly=True,
                                           compute='calcul_sni')  # SNI

    # cotisation sociale
    x_mnt_carfo = fields.Float(string="Montant CARFO", readonly=False)  # Montant CARFO = 8% du salaire de base
    x_mnt_patronal_carfo = fields.Float(string="Part Patronale CARFO",
                                        readonly=False)  # Montant CARFO Patronal = 15.5% du salaire de base
    x_mnt_cnss = fields.Float(string="Montant CNSS", readonly=False, store=True,
                              compute='mnt_cnss_field')  # Montant CNSS = 5.5% de la remuneration total
    x_mnt_patronal_cnss = fields.Float(string="Part Patronale CNSS", readonly=False,
                                       store=True)  # Montant CNSS Patronal = 16% de la remuneration total
    # Retenue IUTS
    x_retenue_iuts = fields.Float(string="IUTS 0 Charge", readonly=False, store=True, compute='retenue_iuts_field')
    x_iuts_net = fields.Float(string="IUTS avec Charge", readonly=True, compute='net_iuts_fields')
    x_net_payer = fields.Float(string="Net à payer", readonly=False, store=True,
                               compute='net_payer_field')  # Net à payer fonctionnaire

    # Affectation du solde indiciaire et calcul du salaire de base fonctionnaire
    @api.depends('x_echellon_id', 'x_classees_id', 'x_echelle_id', 'x_categorie_id')
    def cal_sal_base(self):
        for rec in self:
            val_class = int(rec.x_classees_id)
            val_echel = int(rec.x_echelle_id)
            val_echellon = int(rec.x_echellon_id)
            val_cat = int(rec.x_categorie_id)
            if val_class != False and val_echel != False and val_echellon != False and val_cat != False:
                res = self.env['hr_grillesalariale'].search(
                    [('x_echellon_id', '=', val_echellon), ('x_class_id', '=', val_class),
                     ('x_categorie_id', '=', val_cat),
                     ('x_echelle_id', '=', val_echel)])
                rec.x_solde_indiciaire = round(res.x_salbase)  # x_salbase=solde indiciaire
                x_indemnite_residence = round((res.x_salbase * 10 / 100) + 0.1)  # 0.1:permet de mieux arrondir
                rec.x_solde_indiciaire_net = rec.x_solde_indiciaire + x_indemnite_residence  # solde indiciaire_net= salaire de base
                rec.x_indice = round(res.x_indice)
            else:
                rec.x_solde_indiciaire = 0
                rec.x_indemnite_residence = 0
                rec.x_solde_indiciaire_net = 0
                rec.x_indice = 0

    # def write(self, vals):
    #     struct_id = self.struct_id
    #     vals['struct_id'] = None
    #     super(HrEmployee, self).write(vals)
    #     print(self.struct_id)
    #     vals['struct_id'] = struct_id
    #     return super(HrEmployee, self).write(vals)

    @api.depends('x_solde_indiciaire', 'struct_id')
    def cal_x_indemnite_residence(self):
        for rec in self:
            if rec.struct_id.code == 'FCT_MD':
                rec.x_indemnite_residence = round((rec.x_solde_indiciaire * 10 / 100) + 0.1)
            else:
                rec.x_indemnite_residence = 0

    # fonction de recherche permettant de retourner le salaire de base dans la grille des contractuels en fonction
    # des paramètres
    @api.onchange('x_echellon_c_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def cal_sal_basec(self):
        for rec in self:
            val_echel_c = int(rec.x_echelle_c_id)
            val_echellon_c = int(rec.x_echellon_c_id)
            val_struct = int(rec.company_id.id)
            val_cat_c = int(rec.x_categorie_c_id)
            if val_echel_c != False and val_echellon_c != False and val_cat_c != False and val_struct != False:
                res = self.env['hr_grillesalariale_contractuel'].search(
                    [('x_echellon_c_id', '=', val_echellon_c), ('x_categorie_c_id', '=', val_cat_c),
                     ('x_echelle_c_id', '=', val_echel_c), ('company_id', '=', val_struct)])
                rec.x_solde_indiciaire_ctrct = round(res.x_salbase_ctrt)
            else:
                rec.x_solde_indiciaire_ctrct = 0

    # Affectation
    @api.depends('x_solde_indiciaire', 'x_solde_indiciaire_ctrct', 'struct_id')
    def cal_sal_base_c_f(self):
        for rec in self:
            rec.x_salaire_base = 0
            if rec.struct_id.code == 'FCT_MD':
                rec.x_salaire_base = rec.x_solde_indiciaire_net
            if rec.struct_id.code in ('CTRCT', 'FCT_DETACH'):
                rec.x_salaire_base = rec.x_solde_indiciaire_ctrct

                # fonction qui permet d'additionner les indemnités

    @api.depends('x_indem_resp', 'x_indem_astr', 'x_indem_techn', 'x_indem_specif', 'x_indem_spec_inspect_trav',
                 'x_indem_spec_inspect_irp', 'x_indem_spec_inspect_ish', 'x_indem_spec_inspect_ifc', 'x_indem_loge',
                 'x_indem_transp', 'x_indem_inform', 'x_indem_exploit', 'x_indem_finance', 'x_indem_garde',
                 'x_indem_risque', 'x_indem_suj', 'x_indem_form', 'x_indem_caisse', 'x_solde_indiciaire',
                 'x_indem_prime_rendement')
    def cal_total_indem(self):
        for val in self:
            val.x_total_indemnites = round(
                val.x_indem_resp + val.x_indem_astr + val.x_indem_techn + val.x_indem_specif
                + val.x_indem_spec_inspect_trav + val.x_indem_spec_inspect_irp + val.x_indem_spec_inspect_ish
                + val.x_indem_spec_inspect_ifc + val.x_indem_loge + val.x_indem_transp + val.x_indem_inform
                + val.x_indem_exploit + val.x_indem_finance + val.x_indem_garde + val.x_indem_risque
                + val.x_indem_suj + val.x_indem_form + val.x_indem_caisse + val.x_indem_prime_rendement + val.x_indemnite_residence)

    @api.depends('x_salaire_base', 'x_total_indemnites')
    def calcul_remuneration_total(self):
        for rec in self:
            if rec.struct_id.code == 'FCT_MD':
                rec.x_remuneration_total = (rec.x_solde_indiciaire + rec.x_total_indemnites)
            if rec.struct_id.code in ('CTRCT', 'FCT_DETACH'):
                rec.x_remuneration_total = (rec.x_salaire_base + rec.x_total_indemnites)

    # fonction qui permet d'avoir le montant carfo à partir du salaire de base
    @api.onchange('struct_id', 'x_solde_indiciaire')
    def mnt_carfo_fields(self):
        for rec in self:
            if rec.struct_id.code in ('FCT_MD', 'FCT_DETACH'):
                rec.x_mnt_carfo = round((rec.x_solde_indiciaire * 8) / 100)
                rec.x_mnt_patronal_carfo = round((rec.x_solde_indiciaire * 15.5) / 100)

                rec.x_mnt_cnss = 0.0
                rec.x_mnt_patronal_cnss = 0.0

    # fonction qui permet d'avoir le montant cnss à partir du salaire de base
    @api.depends('struct_id', 'x_remuneration_total')
    def mnt_cnss_field(self):
        for val in self:
            if val.struct_id.code == 'CTRCT':
                resul = round((val.x_remuneration_total * 5.5) / 100)
                if resul > 33000:
                    val.x_mnt_cnss = 33000
                    val.x_mnt_patronal_cnss = 96000
                else:
                    val.x_mnt_cnss = round((val.x_remuneration_total * 5.5) / 100)
                    val.x_mnt_patronal_cnss = round((val.x_remuneration_total * 16) / 100)

                val.x_mnt_carfo = 0.0
                val.x_mnt_patronal_carfo = 0.0

    # fonction qui permet d'avoir le montant cnss à partir du salaire de base
    @api.depends('x_mnt_carfo', 'x_mnt_cnss', 'x_iuts_net')
    def cal_total_retenue(self):
        for rec in self:
            rec.mnt_total_retenues = rec.x_mnt_carfo + rec.x_mnt_cnss + rec.x_iuts_net

    # calcul du salaire brut pour le fonctionnaire puisque Rénumeration Totale déjà connue
    @api.depends('x_remuneration_total', 'x_mnt_carfo', 'x_salaire_base')
    def calcul_salaire_brut(self):
        for vals in self:
            cnss_deductible = 0
            if vals.struct_id.code == 'CTRCT':
                cnss_sb = vals.x_salaire_base * 0.08
                cnss_rt = vals.x_remuneration_total * (5.5 / 100)
                cnss_deductible = min([cnss_sb, cnss_rt, 33000])

            vals.x_salaire_brut = vals.x_remuneration_total - cnss_deductible - vals.x_mnt_carfo

    # calcul abattement forfaitaire
    @api.depends('x_salaire_base', 'x_solde_indiciaire')
    def calcul_abattement(self):
        for vals in self:
            x_cat = vals.x_categorie_c_id.name
            x_cat_f = vals.x_categorie_id.name
            if vals.struct_id.code in ('CTRCT', 'FCT_DETACH'):
                if x_cat == '1' or x_cat == '2' or x_cat == '6':
                    vals.x_abattement_forfaitaire = round((vals.x_salaire_base * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire = round((vals.x_salaire_base * 25) / 100)
            if vals.struct_id.code == 'FCT_MD':
                if x_cat_f == 'A' or x_cat_f == 'B' or x_cat_f == 'P':
                    vals.x_abattement_forfaitaire = round((vals.x_solde_indiciaire * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire = round((vals.x_solde_indiciaire * 25) / 100)

    # calcul DU SALAIRE NET IMPOSABLE (SNI)
    @api.depends('x_salaire_brut', 'x_total_exo', 'x_abattement_forfaitaire')
    def calcul_sni(self):
        for vals in self:
            val1 = vals.x_salaire_brut - vals.x_total_exo - vals.x_abattement_forfaitaire
            val2 = val1 - (val1 % 100)
            vals.x_salaire_net_imposable = val2

    # fonction qui permet d'avoir la de l'iuts
    @api.depends('x_salaire_net_imposable')
    def retenue_iuts_field(self):
        for val in self:
            if 0 <= val.x_salaire_net_imposable <= 30000.0:
                val.x_retenue_iuts = round(val.x_salaire_net_imposable * 0)
            elif 30001.0 <= val.x_salaire_net_imposable <= 50000.0:
                val.x_retenue_iuts = round((val.x_salaire_net_imposable - 30001.0) * 12.1 / 100)
            elif 50001.0 <= val.x_salaire_net_imposable <= 80000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 50001.0) * 13.9 / 100) + 2420)
            elif 80001.0 <= val.x_salaire_net_imposable <= 120000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 80001.0) * 15.7 / 100) + 6590)
            elif 120001.0 <= val.x_salaire_net_imposable <= 170000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 120001.0) * 18.4 / 100) + 12870)
            elif 170001.0 <= val.x_salaire_net_imposable <= 250000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 170001.0) * 21.7 / 100) + 22070)
            else:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 250001.0) * 25 / 100) + 39430)

    # fonction qui permet d'avoir le montant en fonction du nombre de charge pour les deux
    @api.depends('charge', 'x_retenue_iuts')
    def mnt_charge_field(self):
        for val in self:
            if val.charge == 0:
                val.x_montant_charge = round(val.x_retenue_iuts * 0)
            elif val.charge == 1:
                val.x_montant_charge = round((val.x_retenue_iuts * 8) / 100)
            elif val.charge == 2:
                val.x_montant_charge = round((val.x_retenue_iuts * 10) / 100)
            elif val.charge == 3:
                val.x_montant_charge = round((val.x_retenue_iuts * 12) / 100)
            else:
                val.x_montant_charge = round((val.x_retenue_iuts * 14) / 100)

    # fonction qui permet d'avoir le montant net de l'iuts pour le contractuel 031002
    @api.depends('x_retenue_iuts', 'x_montant_charge')
    def net_iuts_fields(self):
        for val in self:
            val.x_iuts_net = round(val.x_retenue_iuts - val.x_montant_charge)

    # fonction qui permet d'avoir le montant net à payer pour le fonctionnaires
    @api.depends('x_remuneration_total', 'x_allocation_familial', 'mnt_total_retenues', )
    def net_payer_field(self):
        for val in self:
            val.x_net_payer = round(
                val.x_remuneration_total + val.x_allocation_familial - val.mnt_total_retenues)

    # fonction de calcul du montant de l'allocation
    @api.depends('charge', 'struct_id')
    def mnt_alloc(self):
        for vals in self:
            if vals.struct_id.code in ('FCT_MD', 'FCT_DETACH'):
                vals.x_allocation_familial = vals.charge_enfant * 2000
            else:
                vals.x_allocation_familial = 0

    # Calcul exonérations
    @api.depends('x_indem_resp', 'x_salaire_brut')
    def calcul_exoneration_responsabilite(self):
        for vals in self:
            indem_resp = vals.x_indem_resp
            premiere_limite_res = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_resp_exo = min([premiere_limite_res, indem_resp, 50000])

    @api.depends('x_indem_astr', 'x_salaire_brut')
    def calcul_exoneration_astreintes(self):
        for vals in self:
            premiere_limite_astr = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_astr_exo = min([premiere_limite_astr, vals.x_indem_astr, 50000])

    # indemnités de technicités
    @api.depends('x_indem_techn', 'x_salaire_brut')
    def calcul_exoneration_technicites(self):
        for vals in self:
            premiere_limite_tech = round((vals.x_salaire_brut * 5) / 100)
            x_indem_techn = round(vals.x_indem_techn)
            vals.x_indem_techn_exo = min([premiere_limite_tech, x_indem_techn, 50000])

    # indemnités de spécifiques GRH
    @api.depends('x_indem_specif', 'x_salaire_brut')
    def calcul_exoneration_specifiques(self):
        for vals in self:
            vals.x_indem_specif_exo = 0
            premiere_limite_spec = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_exo = min([premiere_limite_spec, vals.x_indem_specif, 50000])

    # indemnités de spécifiques IT
    @api.depends('x_indem_spec_inspect_trav', 'x_salaire_brut')
    def calcul_exoneration_specifiques_it(self):
        for vals in self:
            premiere_limite_spec_it = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_it_exo = min([premiere_limite_spec_it, vals.x_indem_spec_inspect_trav, 50000])

    # indemnités de spécifiques IRP
    @api.depends('x_indem_spec_inspect_irp', 'x_salaire_brut')
    def calcul_exoneration_specifiques_irp(self):
        for vals in self:
            premiere_limite_spec_irp = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_irp_exo = min([premiere_limite_spec_irp, vals.x_indem_spec_inspect_irp, 50000])

    # indemnités de spécifiques ISH
    @api.depends('x_indem_spec_inspect_ish', 'x_salaire_brut')
    def calcul_exoneration_specifiques_ish(self):
        for vals in self:
            premiere_limite_spec_ish = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_ish_exo = min([premiere_limite_spec_ish, vals.x_indem_spec_inspect_ish, 30000])

    # indemnités de spécifiques IFC
    @api.depends('x_indem_spec_inspect_ifc', 'x_salaire_brut')
    def calcul_exoneration_specifiques_ifc(self):
        for vals in self:
            premiere_limite_ifc = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_ifc_exo = min([premiere_limite_ifc, vals.x_indem_spec_inspect_ifc, 50000])

    # indemnités d'informatiques
    @api.depends('x_indem_inform', 'x_salaire_brut')
    def calcul_exoneration_informatique(self):
        for vals in self:
            premiere_limite_info = round(vals.x_salaire_brut * 0.05)
            vals.x_indem_inform_exo = min([premiere_limite_info, vals.x_indem_inform, 50000])

    # indemnités de exploitations reseaux
    @api.depends('x_indem_exploit', 'x_salaire_brut')
    def calcul_exoneration_exploitation(self):
        for vals in self:
            premiere_limite_exploi = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_exploit_exo = min([premiere_limite_exploi, vals.x_indem_exploit, 50000])

    # indemnités de responsabilités financières
    @api.depends('x_indem_finance', 'x_salaire_brut')
    def calcul_exoneration_resp_finance(self):
        for vals in self:
            premiere_limite_finance = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_finance_exo = min([premiere_limite_finance, vals.x_indem_finance, 50000])

    # indemnités de garde
    @api.depends('x_indem_garde', 'x_salaire_brut')
    def calcul_exoneration_garde(self):
        for vals in self:
            premiere_limite_garde = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_garde_exo = min([premiere_limite_garde, vals.x_indem_garde, 50000])

    # indemnités de risque
    @api.depends('x_indem_risque', 'x_salaire_brut')
    def calcul_exoneration_risque(self):
        for vals in self:
            premiere_limite_risque = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_risque_exo = min([premiere_limite_risque, vals.x_indem_risque, 50000])

    # indemnités de sujetion
    @api.depends('x_indem_suj', 'x_salaire_brut')
    def calcul_exoneration_sujetion(self):
        for vals in self:
            premiere_limite_suj = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_suj_exo = min([premiere_limite_suj, vals.x_indem_suj, 50000])

    # indemnités de formation
    @api.depends('x_indem_form', 'x_salaire_brut')
    def calcul_exoneration_formation(self):
        for vals in self:
            premiere_limite_form = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_form_exo = min([premiere_limite_form, vals.x_indem_form, 50000])

    # indemnités de caisse
    @api.depends('x_indem_caisse', 'x_salaire_brut')
    def calcul_exoneration_caisse(self):
        for vals in self:
            premiere_limite_caisse = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_caisse_exo = min([premiere_limite_caisse, vals.x_indem_caisse, 50000])

    # indemnités de veste
    @api.depends('x_indem_veste', 'x_salaire_brut')
    def calcul_exoneration_veste(self):
        for vals in self:
            premiere_limite_veste = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_veste_exo = min([premiere_limite_veste, vals.x_indem_veste, 50000])

    # indemnités de residence
    @api.depends('x_solde_indiciaire', 'x_salaire_brut')
    def calcul_exoneration_residence(self):
        for vals in self:
            if vals.struct_id.code == 'FCT_MD':
                premiere_limite = round((vals.x_salaire_brut * 5) / 100)
                vals.x_indem_residence_exo = min([premiere_limite, vals.x_solde_indiciaire, 50000])
            else:
                vals.x_indem_residence_exo = 0

    # exoneration prime de rendement
    @api.depends('x_indem_prime_rendement', 'x_salaire_brut')
    def calcul_exoneration_prime(self):
        for vals in self:
            premiere_limite = round((vals.x_salaire_brut * 5) / 100)
            vals.x_prime_exo = min([premiere_limite, vals.x_indem_prime_rendement, 50000])

    @api.depends('x_indem_loge', 'x_salaire_brut')
    def calcul_exoneration_logement(self):
        for vals in self:
            premiere_limite_log = round((vals.x_salaire_brut * 20) / 100)
            vals.x_indem_loge_exo = min([premiere_limite_log, vals.x_indem_loge, 75000])

    @api.depends('x_indem_transp', 'x_salaire_brut')
    def calcul_exoneration_transport(self):
        for vals in self:
            premiere_limite_trans = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_transp_exo = min([premiere_limite_trans, vals.x_indem_transp, 30000])

    @api.depends('x_indem_resp_exo', 'x_indem_astr_exo', 'x_indem_techn_exo', 'x_indem_specif_exo',
                 'x_indem_specif_it_exo', 'x_indem_specif_ifc_exo', 'x_indem_specif_irp_exo',
                 'x_indem_specif_ish_exo', 'x_indem_loge_exo', 'x_indem_transp_exo', 'x_indem_inform_exo',
                 'x_indem_exploit_exo', 'x_indem_finance_exo', 'x_indem_garde_exo', 'x_indem_risque_exo',
                 'x_indem_suj_exo', 'x_indem_form_exo', 'x_indem_caisse_exo', 'x_indem_veste_exo', 'x_prime_exo',
                 'x_indem_residence_exo')
    def calcul_exoneration_total(self):
        for vals in self:
            vals.x_total_exo = vals.x_indem_resp_exo + vals.x_indem_astr_exo + vals.x_indem_techn_exo + vals.x_indem_specif_exo + vals.x_indem_loge_exo + vals.x_indem_transp_exo + vals.x_indem_inform_exo + vals.x_indem_exploit_exo + vals.x_indem_finance_exo + vals.x_indem_garde_exo + vals.x_indem_risque_exo + vals.x_indem_suj_exo + vals.x_indem_form_exo + vals.x_indem_caisse_exo + vals.x_indem_veste_exo + vals.x_indem_specif_it_exo + vals.x_indem_specif_ifc_exo + vals.x_indem_specif_irp_exo + vals.x_indem_specif_ish_exo + vals.x_prime_exo + vals.x_indem_residence_exo

    @api.depends('charge_femme', 'charge_enfant')
    def calcul_charge(self):
        self.charge = self.charge_femme + self.charge_enfant

    enfants_ids = fields.One2many('hr_employee_enfant', 'employee_id', string="Enfant", index=True)
    x_acte_ids = fields.One2many('hr_piece_detachement', 'x_employees_id', string='Joindre acte Detachement')
    x_acte_dec_ids = fields.One2many('hr_piece_disposition', 'x_employees_id', string='Joindre acte Decision')
    x_actes_ids = fields.One2many('hr_decret_nomination', 'x_employees_id', string='Joindre acte de nomination')
    x_dossier_ind_ids = fields.One2many('hr_dossier_individuel', 'x_employees_id', string='Joindre Fichiers')
    x_note_ids = fields.One2many(
        comodel_name='hr_employee_note',
        inverse_name='employee_id',
        string='Notes',
        required=False)

    # FONCTION DE calcul de la date de depart a la retraite d'un employe
    @api.depends("x_date_naissance", "x_nb_annee_retraite")
    def _compute_date_retraite(self):
        for rec in self:
            rec.x_date_retraite = None
            if rec.x_nb_annee_retraite or rec.x_date_naissance:
                anne = int(rec.x_nb_annee_retraite.name)
                date1 = rec.x_date_naissance.strftime("%Y-%m-%d")
                date2 = rec.x_date_naissance.year + anne
                rec.x_date_retraite = datetime(date2, rec.x_date_naissance.month, rec.x_date_naissance.day, 0, 0, 0,
                                               0).date()

    @api.depends('enfants_ids')
    def calcul_charge_enfant(self):
        for val in self:
            charge_enfant = 0
            for e in val.enfants_ids:
                if e.etat == "1" and e.age <= 15:
                    charge_enfant = charge_enfant + 1
                elif e.etat == "2" and e.age <= 17:
                    charge_enfant = charge_enfant + 1
                elif e.etat == "3" and e.age <= 20:
                    charge_enfant = charge_enfant + 1
                elif e.etat == "4":
                    charge_enfant = charge_enfant + 1

            val.charge_enfant = charge_enfant


class HrEmployeesEnfant(models.Model):
    _name = "hr_employee_enfant"

    name = fields.Char(string="Nom et Prénoms", required=True)
    date_naissance = fields.Date(string='Date naissance', required=True, default=date.today())
    age = fields.Integer(string="Age", compute="calcul_age")

    est_pris = fields.Boolean(string='Est_pris', required=False, compute="cal_est_pris")

    etat = fields.Selection([
        ('1', 'Ordinaire'),
        ('2', 'Apprentissage'),
        ('3', 'Etude'),
        ('4', 'Besoin Spécifique'),
    ], 'Status', default='1', required=True)

    sexe = fields.Selection([
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    ], 'Sexe', default='M', index=True, required=True)

    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)

    @api.depends('date_naissance')
    def calcul_age(self):
        for val in self:
            val.age = 0
            if val.date_naissance:
                start_date = date.today()
                end_date = val.date_naissance
                val.age = (start_date - end_date).days / 365

    @api.depends('etat', 'age')
    def cal_est_pris(self):
        for val in self:
            if val.etat == "1" and val.age <= 15:
                val.est_pris = True
            elif val.etat == "2" and val.age <= 17:
                val.est_pris = True
            elif val.etat == "3" and val.age <= 20:
                val.est_pris = True
            elif val.etat == "4":
                val.est_pris = True
            else:
                val.est_pris = False


# Creation de la classe hr_employee_ fichier_oint_line permettant d'ajouter un  acte de detachement
class HrEmployeePieceDetachement(models.Model):
    _name = "hr_piece_detachement"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_acte = fields.Date(string="Date acte")
    date_effet = fields.Date(string="Date effet")
    date_fin = fields.Date(string="Date fin")
    ref_acte = fields.Char(string="Ref acte")
    fichier_joint = fields.Binary(string='Joindre acte', attachment=True)


# Creation de la classe hr_employee_ decret_nomination permettant d'ajouter un  acte de nomination
class HrEmployeeDecretNomination(models.Model):
    _name = "hr_decret_nomination"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_nomination = fields.Date(string="Date nomination")
    date_effet = fields.Date(string="Date effet")
    date_fin = fields.Date(string="Date fin")
    ref_acte = fields.Char(string="Ref acte nomination")
    fichier_joint = fields.Binary(string='Joindre acte', attachment=True)
    etat_nomination = fields.Selection([
        ('1', "En cours"),
        ('2', "Terminé"),
    ], required=True, string="Etat Nomination", default=1)


# Creation de la classe hr_employee_ fichier_oint_line permettant d'ajouter un  acte de decision
class HrEmployeePieceDecision(models.Model):
    _name = "hr_piece_disposition"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_acte_dec = fields.Date(string="Date acte disposition")
    date_effet_dec = fields.Date(string="Date effet disposition")
    date_fin_dec = fields.Date(string="Date fin disposition")
    ref_acte_dec = fields.Char(string="Ref acte disposition")
    fichier_joint_dec = fields.Binary(string='Joindre acte disposition', attachment=True)


# Creation de la classe hr_employee_ fichier_joint_line permettant de suivre le dossier individuel du personnel
class HrEmployeeDossierIndividuel(models.Model):
    _name = "hr_dossier_individuel"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_op = fields.Date(string="Date", default=date.today())
    objet_ligne = fields.Char(string="Intitulé")
    fichier_joint = fields.Binary(string='Joindre Fichier', attachment=True)


class HrEmployeeNote(models.Model):
    _name = "hr_employee_note"

    note = fields.Integer(string='Note', required=False)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)

    @api.model
    def annee_selection(self):
        year = 2000  # replace 2000 with your a start year
        year_list = []
        while year != 2100:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    def _default_annee(self):
        print(fields.Date.context_today(self).year)
        return str(fields.Date.context_today(self).year)

    annee = fields.Selection(
        annee_selection,
        string="Année",
        default=_default_annee)
