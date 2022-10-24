from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from num2words import num2words
from datetime import date

class BudgPieceEngP(models.Model):
    _name = "budg_piece_engagement_p"

    lb_long = fields.Many2one("ref_piece_justificatives", "Libellé", required=True)
    oblige = fields.Boolean("Obligatoire")
    nombre = fields.Integer("Nombre")
    ref = fields.Char("Référence", required=True)
    montant = fields.Integer("Montant")
    dte = fields.Date("Date")
    eng_id = fields.Many2one("budg_engagement_p", ondelete='cascade')
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")


class BudgEngagementP(models.Model):
    _name = "budg_engagement_p"
    _rec_name = "no_eng"
    _order = " id desc"

    no_eng = fields.Char(string="N° engagement", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", required=True,
                                 states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                         'V': [('readonly', True)], 'L': [('readonly', True)],
                                         'O': [('readonly', True)]})
    prog_id = fields.Many2one("budg_programme_p", string="Programme", required=True,
                              states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                      'V': [('readonly', True)], 'L': [('readonly', True)],
                                      'O': [('readonly', True)]})
    action_id = fields.Many2one("budg_param_action_p", string="Action", required=True,
                                states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                        'V': [('readonly', True)], 'L': [('readonly', True)],
                                        'O': [('readonly', True)]})
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", required=True,
                                  states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                          'V': [('readonly', True)], 'L': [('readonly', True)],
                                          'O': [('readonly', True)]})
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", required=True,
                                  states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                          'V': [('readonly', True)], 'L': [('readonly', True)],
                                          'O': [('readonly', True)]})
    article_id = fields.Many2one("budg_param_article_p", string="Article", required=True,
                                 states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                         'V': [('readonly', True)], 'L': [('readonly', True)],
                                         'O': [('readonly', True)]})
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", required=True,
                               states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                       'V': [('readonly', True)], 'L': [('readonly', True)],
                                       'O': [('readonly', True)]})
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", required=True,
                                  states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                          'V': [('readonly', True)], 'L': [('readonly', True)],
                                          'O': [('readonly', True)]})
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", required=True,
                                     states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                             'V': [('readonly', True)], 'L': [('readonly', True)],
                                             'O': [('readonly', True)]})
    type_budget_id = fields.Many2one("budg_typebudget", string="Type de budget",
                                     states={'R': [('readonly', True)], 'W': [('readonly', True)],
                                             'V': [('readonly', True)], 'L': [('readonly', True)],
                                             'O': [('readonly', True)]})
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", required=True, string="Catégorie Benef./Four.",
                                           states={'W': [('readonly', True)], 'V': [('readonly', True)],
                                                   'L': [('readonly', True)], 'O': [('readonly', True)]})
    no_beneficiaire = fields.Many2one("ref_beneficiaire", required=True, string="Identité Benef./Four.",
                                      states={'V': [('readonly', True)], 'L': [('readonly', True)],
                                              'O': [('readonly', True)]})
    typedossier = fields.Many2one("budg_typedossierbudg",
                                  default=lambda self: self.env['budg_typedossierbudg'].search([('code', '=', 'ENG')]),
                                  string="Type de dossier", readonly=True)
    lb_obj = fields.Text(string="Objet", size=300, required=True,
                         states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)],
                                 'L': [('readonly', True)], 'O': [('readonly', True)]})
    mnt_init_eng = fields.Float(string="Montant initiale engagé", digits=(20, 0), compute="mnt_init_eng")
    credit_eng = fields.Float(string="Montant initiale engagé sur l'engagement", digits=(20, 0))
    mnt_eng = fields.Float(string="Montant engagement", digits=(20, 0), required=True,
                           states={'R': [('readonly', True)],
                                   'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],
                                   'O': [('readonly', True)]})
    mnt_liq = fields.Float(string="Montant liquidé", digits=(20, 0))
    credit_dispo = fields.Float(string="Crédit disponible", digits=(20, 0), readonly=True,
                                states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)],
                                        'L': [('readonly', True)], 'O': [('readonly', True)]})
    piecejust_ids = fields.One2many("budg_piece_engagement_p", 'eng_id')
    dt_visa_cf = fields.Date(string="Date Visa")
    cpte_benef = fields.Char('compte')
    imput_benef = fields.Many2one("ref_souscompte", "imput beneficiaire")
    cpte_rub = fields.Char('compte rub')
    modereg = fields.Many2one('ref_modereglement', 'Mode de règlement')
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date", required=True)
    mnt_lbudg_ap = fields.Float(string="Nouveau disponible", compute='mnt_nvo_dispo')
    mnt_annule = fields.Float(string="Montant annulé", digits=(20, 0))
    mnt_tot_eng = fields.Float(string="Montant total engagé", digits=(20, 0))
    cumul = fields.Float(string='Cumul des engagement antérieurs')
    ref_mp = fields.Many2one("faarf.ppm.contrat", string="Réf. Marché")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
    acc_number = fields.Char(string="N° Compte", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    user_id = fields.Many2one('res.users', string='user', track_visibilty='onchange', readonly=True,
                              default=lambda self: self.env.user)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    state = fields.Selection([('draft', 'Brouillon'), ('N', 'Confirmé'), ('V', 'Approuvé'), ('A', 'Annulé'),
                              ('W', 'Visé'), ('R', 'Rejeté'), ('LC', 'Liquidation partielle'), ('L', 'Liquidé'), ],
                             'Etat', default='draft', index=True, required=True, readonly=True, copy=False,
                             track_visibility='always')
    credit_disponible = fields.Float("Crédit disponible avant", compute='credits_disponible')
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], default='N')
    reste = fields.Integer()
    signataire_1 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '1')]))
    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def user(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id', 'mnt_eng')
    def _controleexercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % no_ex)
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

            if record.mnt_eng <= 0:
                raise ValidationError(_("Le montant de l'engagement doit être supérieur à 0."))
            elif record.mnt_eng > record.credit_dispo:
                raise ValidationError(_("Le montant de l'engagement doit être inférieur ou égal au crédit disponible."))

    @api.depends('mnt_eng')
    def amount_to_words(self):
        self.text_amount = num2words(self.mnt_eng, lang='fr')

    @api.onchange('no_beneficiaire')
    def cpte(self):
        self.cpte_benef = self.no_beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
        self.imput_benef = self.no_beneficiaire.cpte_fournisseur.souscpte.id
        self.bank_id = self.no_beneficiaire.bank_id
        self.acc_number = self.no_beneficiaire.acc_number

    @api.onchange('rubrique_id')
    def cpterub(self):
        self.cpte_rub = self.rubrique_id.cpte_id.souscpte.concate_souscpte

    def action_eng_confirmer(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_sec = int(self.section_id)
        val_prog = int(self.prog_id)
        val_act = int(self.action_id)
        val_chap = int(self.chapitre_id)
        val_activ = int(self.activite_id)
        val_art = int(self.article_id)
        val_par = int(self.parag_id)
        val_rub = int(self.rubrique_id)

        self.write({'state': 'N'})
        self.env.cr.execute(
            "select noeng from budg_compteur_eng_p where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        eng = self.env.cr.fetchone()
        no_eng = eng and eng[0] or 0
        c1 = int(no_eng) + 1
        c = str(no_eng)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_eng = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_eng_p(x_exercice_id,company_id,noeng)  VALUES(%d ,%d, %d)"""
                % (val_ex, val_struct, vals))
        else:
            c1 = int(no_eng) + 1
            ok = str(c1).zfill(4)
            self.no_eng = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_eng_p SET noeng = %d WHERE x_exercice_id = %d and company_id = %d"
                % (vals, val_ex, val_struct))

        self.env.cr.execute(
            """select distinct l.mnt_disponible from budg_ligne_exe_dep_p l where l.section_id = %d 
            and l.prog_id = %d and 
            and l.action_id = %d l.chapitre_id = %d and l.activite_id = %d and l.article_id = %d and l.parag_id = %d 
            and l.rub_id = %d and x_exercice_id = %d and company_id = %d"""
            % (val_sec, val_prog, val_act, val_chap, val_activ, val_art, val_par, val_rub, val_ex, val_struct))
        res = self.env.cr.fetchone()[0] or 0

        if self.mnt_eng > res:
            raise ValidationError(_("Le montant de l'engagement est supérieur au montant budgétisé"))

        else:
            self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET mnt_engage = (select sum(mnt_eng)
            FROM  budg_engagement_p WHERE section_id = %d and prog_id = %d and action_id = %d and chapitre_id = %d 
            and activite_id = %d and article_id = %d and parag_id = %d and rub_id = %d and x_exercice_id = %d and 
            company_id = %d and state not in ('draft','A','R')), mnt_disponible = (mnt_corrige - mnt_engage)
            WHERE section_id = %d and prog_id = %d and 
            action_id = %d and chapitre_id = %d and activite_id = %d and article_id = %d and parag_id = %d 
            and rub_id = %d and x_exercice_id = %d and company_id = %d"""
                                % (val_sec, val_prog, val_chap, val_act, val_activ, val_art, val_par, val_rub,
                                   val_ex, val_struct,
                                   val_sec, val_prog, val_chap, val_act, val_activ, val_art, val_par, val_rub,
                                   val_ex, val_struct))

            self.reste = self.mnt_eng

            self.credit_ouvert()
            self.cumul_anterieur()
            self.mnt_nvo_dispo()
            self.mnt_sum_eng()

    # Crédit ouvert sur la ligne
    def credit_ouvert(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_sec = int(self.section_id)
        val_prog = int(self.prog_id)
        val_act = int(self.action_id)
        val_chap = int(self.chapitre_id)
        val_activ = int(self.activite_id)
        val_art = int(self.article_id)
        val_par = int(self.parag_id)
        val_rub = int(self.rubrique_id)

        self.env.cr.execute("""select mnt_corrige from budg_ligne_exe_dep where section_id = %d and prog_id = %d and 
            action_id = %d and chapitre_id = %d and activite_id = %d and article_id = %d and parag_id = %d 
            and rub_id = %d and x_exercice_id = %d and company_id = %d"""
                            % (val_sec, val_prog, val_chap, val_act, val_activ, val_art, val_par, val_rub,
                               val_ex, val_struct))

        res = self.env.cr.fetchone()
        self.credit_eng = res and res[0] or 0

    # cumul des engagements antérieurs
    def cumul_anterieur(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_sec = int(self.section_id)
        val_prog = int(self.prog_id)
        val_act = int(self.action_id)
        val_chap = int(self.chapitre_id)
        val_activ = int(self.activite_id)
        val_art = int(self.article_id)
        val_par = int(self.parag_id)
        val_rub = int(self.rubrique_id)
        v_eng = str(self.no_eng)

        self.env.cr.execute("""select coalesce(sum(e.mnt_eng),0) FROM budg_engagement_p e
        where section_id = %s and prog_id = %s and action_id = %s and chapitre_id = %s and activite_id = %s 
        and article_id = %s and parag_id = %s and rub_id = %s and x_exercice_id = %s and company_id = %s 
        and no_eng <> %s and state not in ('draft','A','R') """, (val_sec, val_prog, val_chap, val_act, val_activ,
                                                                  val_art,
                                                                  val_par, val_rub, val_ex, val_struct, v_eng))

        res1 = self.env.cr.fetchone()
        r2 = res1 and res1[0] or 0

        self.cumul = r2

    # Récupération du nouveau disponible
    @api.depends('credit_disponible', 'mnt_eng')
    def mnt_nvo_dispo(self):

        self.mnt_lbudg_ap = self.credit_disponible - self.mnt_eng

    def mnt_sum_eng(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_sec = int(self.section_id)
        val_prog = int(self.prog_id)
        val_act = int(self.action_id)
        val_chap = int(self.chapitre_id)
        val_activ = int(self.activite_id)
        val_art = int(self.article_id)
        val_par = int(self.parag_id)
        val_rub = int(self.rubrique_id)

        self.env.cr.execute("""select sum(e.mnt_eng) FROM budg_engagement_p
        WHERE section_id = %d and prog_id = %d and action_id = %d and chapitre_id = %d and activite_id = %d 
        and article_id = %d and parag_id = %d and rub_id = %d and x_exercice_id = %d and 
        company_id = %d and state not in ('draft','A','R')"""
                            % (val_sec, val_prog, val_chap, val_act, val_activ, val_art,
                               val_par, val_rub, val_ex, val_struct))
        res = self.env.cr.fetchone()
        self.mnt_tot_eng = res and res[0] or 0

    @api.depends('credit_eng', 'cumul')
    def credits_disponible(self):
        self.credit_disponible = self.credit_eng - self.cumul

    def action_eng_approuver(self):
        if self.type_procedure.type_procedure == '001':
            self.write({'state': 'V'})
        else:
            self.write({'state': 'W'})

    def action_eng_viser(self):
        self.write({'state': 'W'})

    def action_eng_rejeter(self):
        self.write({'state': 'R'})

    @api.onchange('rubrique_id')
    def cred_dipso(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_sec = int(self.section_id)
        val_prog = int(self.prog_id)
        val_act = int(self.action_id)
        val_chap = int(self.chapitre_id)
        val_activ = int(self.activite_id)
        val_art = int(self.article_id)
        val_par = int(self.parag_id)
        val_rub = int(self.rubrique_id)

        result = self.env['budg_ligne_exe_dep_p'].search(
            [('prog_id.id', '=', val_prog), ('section_id.id', '=', val_sec),
             ('chapitre_id.id', '=', val_chap), ('action_id.id', '=', val_act),
             ('activite_id.id', '=', val_activ), ('article_id.id', '=', val_art),
             ('parag_id.id', '=', val_par), ('rub_id.id', '=', val_rub),
             ('company_id.id', '=', val_struct), ('x_exercice_id.id', '=', val_ex)])
        print("resut", result)
        self.credit_dispo = result.mnt_disponible


class BudgCompteurengaP(models.Model):
    _name = "budg_compteur_eng_p"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    noeng = fields.Integer(default=0)


class BudgApprobationGroupEngP(models.Model):
    _name = 'budg_appro_group_eng_p'
    _rec_name = 'dte'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,
                                 string='Structure')
    dte = fields.Date("Date", default=fields.Date.context_today, readonly=True)
    appro_ids = fields.One2many("budg_appro_group_eng_line_p", "appro_id")
    state = fields.Selection([('A', 'A approuver'), ('V', 'Approuvés')], default='A', string="Etat")

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    @api.constrains('x_exercice_id')
    def _controleexercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        val_struct = int(self.company_id)
        val_ex = int(self.x_exercice_id)

        for vals in self:
            vals.env.cr.execute(""" SELECT * from budg_engagement_p e where e.state = 'N' and e.company_id = %d and 
            e.x_exercice_id = %d order by no_eng desc""" % (val_struct, val_ex))
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.appro_ids.unlink()
            for line in rows:
                result.append((0, 0, {'eng_id': line['id'], 'prog_id': line['prog_id'],
                                      'section_id': line['section_id'], 'action_id': line['action_id'],
                                      'chapitre_id': line['chapitre_id'], 'activite_id': line['activite_id'],
                                      'article_id': line['article_id'], 'para_id': line['parag_id'],
                                      'rubrique_id': line['rubrique_id'], 'x_exercice_id': line['x_exercice_id'],
                                      'company_id': line['company_id'], 'mnt': line['mnt_eng'],
                                      'objet': line['lb_obj'], 'typeprocedure': line['type_procedure']}))
            self.appro_ids = result

    def approuver(self):

        no_ex = int(self.x_exercice_id)
        struct = int(self.company_id)
        v_id = int(self.id)

        self.env.cr.execute("""SELECT l.* FROM budg_appro_group_eng_line_p l, budg_appro_group_eng_p e WHERE l.appro_id = e.id and e.id = %d
        and e.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

        for val in self.env.cr.dictfetchall():
            eng = val['eng_id']
            prog = val['prog_id']
            sec = val['section_id']
            act = val['action_id']
            activ = val['activite_id']
            chap = val['chapitre_id']
            art = val['article_id']
            par = val['para_id']
            rub = val['rub_id']
            procedure = val['typeprocedure']
            approuver = val['approuver']

            if approuver == True:

                if procedure == 1:
                    self.env.cr.execute("""UPDATE budg_engagement_p SET state = 'V' WHERE id = %d and prog_id = %d and section_id = %d and 
                    chapitre_id = %d and action_id = %d and activite_id = %d and article_id = %d
                    and parag_id = %d and rubrique_id = %d and company_id = %d and x_exercice_id = %d"""
                                        % (eng, prog, sec, chap, act, activ, art, par, rub, struct, no_ex))
                    self.write({'state': 'V'})
                else:
                    self.env.cr.execute("""UPDATE budg_engagement_p SET state = 'W' WHERE id = %d and prog_id = %d and section_id = %d and 
                                        chapitre_id = %d and action_id = %d and activite_id = %d and article_id = %d
                                        and parag_id = %d and rubrique_id = %d and company_id = %d and x_exercice_id = %d"""
                                        % (eng, prog, sec, chap, act, activ, art, par, rub, struct, no_ex))

                    self.write({'state': 'V'})


class BudgApprobationGroupLineP(models.Model):
    _name = 'budg_appro_group_eng_line_p'

    appro_id = fields.Many2one("budg_appro_group_eng_p", ondelete='cascade')
    eng_id = fields.Many2one("budg_engagement_p", "N° Eng", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    mnt = fields.Float("Montant", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    typeprocedure = fields.Many2one("budg_typeprocedure", "Type de procédure")
    beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", readonly=True, string="Exercice")
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.user.company_id.id)
    approuver = fields.Boolean("Approuver ?")

    class BudgAnnulationEngagement(models.Model):
        _name = "budg_annulation_engagement_p"
        _rec_name = "eng_id"

        eng_id = fields.Many2one("budg_engagement_p", "N° Engagement", required=True,
                                 domain=['|', '|', ('state', '=', 'R'), ('state', '=', 'V'), ('state', '=', 'N')])
        section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
        prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
        action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
        chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
        activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
        article_id = fields.Many2one("budg_param_article_p", string="Article")
        parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
        rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
        mnt = fields.Float("Montant", readonly=True)
        objet = fields.Text("Objet", readonly=True)
        beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
        company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
        state = fields.Selection([('V', 'Approuvé'), ('A', 'Annulé')], default='V', string="Etat", required=True)

        current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
        x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

        # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
        @api.onchange('current_users')
        def User(self):
            if self.current_users:
                self.x_exercice_id = self.current_users.x_exercice_id

        @api.constrains('x_exercice_id')
        def _controle_exercice(self):
            no_ex = int(self.x_exercice_id)
            v_ex = int(self.x_exercice_id.no_ex)
            for record in self:
                record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
                res = self.env.cr.fetchone()
                val = res and res[0] or 0
                if val == 0:
                    raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

        @api.onchange("eng_id")
        def valeur(self):
            for vals in self:
                if vals.eng_id:
                    self.prog_id = self.eng_id.prog_id
                    self.section_id = self.eng_id.section_id
                    self.action_id = self.eng_id.action_id
                    self.chapitre_id = self.eng_id.chapitre_id
                    self.activite_id = self.eng_id.activite_id
                    self.article_id = self.eng_id.article_id
                    self.para_id = self.eng_id.parag_id
                    self.rub_id = self.eng_id.rubrique_id
                    self.mnt = self.eng_id.mnt_eng
                    self.beneficiaire = self.eng_id.no_beneficiaire
                    self.objet = self.eng_id.lb_obj

        def annuler_engagement(self):

            for val in self:
                eng = int(val.eng_id)
                prog = int(val.prog_id)
                sec = int(val.section_id)
                act = int(val.action_id)
                chap = int(val.chapitre_id)
                activ = int(val.activite_id)
                art = int(val.article_id)
                par = int(val.para_id)
                rub = int(val.rub_id)
                no_ex = int(val.x_exercice_id)
                struct = int(val.company_id)
                mnt = int(val.mnt)

                self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_disponible = mnt_disponible + %d
                WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d and 
                activite_id = %d and article_id = %d and paragraphe_id = %d and rub_id = %d and company_id = %d and x_exercice_id = %d"""
                                    % (mnt, prog, sec, act, chap, activ, art, par, rub, struct, no_ex))

                self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_engage = mnt_engage - %d
                WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d and 
                activite_id = %d and article_id = %d and paragraphe_id = %d and rub_id = %d and company_id = %d and x_exercice_id = %d"""
                                    % (mnt, prog, sec, act, chap, activ, art, par, rub, struct, no_ex))

                self.env.cr.execute(
                    """UPDATE budg_engagement_p SET state = 'A' WHERE id = %d and x_exercice_id = %d and company_id = %d"""
                    % (eng, no_ex, struct))

                self.write({'state': 'A'})


class BudgCorrectionEngagementApprobationP(models.Model):
    _name = "budg_correction_engagement_approbation_p"
    _rec_name = "eng_id"

    eng_id = fields.Many2one("budg_engagement_p", "N° Engagement", required=True, domain=[('state', '=', 'V')])
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    mnt = fields.Float("Montant", readonly=True)
    objet = fields.Text("Objet", readonly=False)
    beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
    imput_benef = fields.Many2one("ref_souscompte", string="Imput benef")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('V', 'Approuvé'), ('C', 'Corrigé')], default='V', string="Etat", required=True)

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def user(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _controle_exercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    # Récuperer les elements de l'engagement choisi
    @api.onchange("eng_id")
    def valeur(self):
        for vals in self:
            if vals.eng_id:
                self.prog_id = self.eng_id.prog_id
                self.section_id = self.eng_id.section_id
                self.action_id = self.eng_id.action_id
                self.chapitre_id = self.eng_id.chapitre_id
                self.activite_id = self.eng_id.activite_id
                self.article_id = self.eng_id.article_id
                self.para_id = self.eng_id.parag_id
                self.rub_id = self.eng_id.rubrique_id
                self.mnt = self.eng_id.mnt_eng
                self.beneficiaire = self.eng_id.no_beneficiaire
                self.objet = self.eng_id.lb_obj

    # Correction de l'engagement
    def corriger(self):
        for val in self:
            benef = int(val.beneficiaire)
            obj = str(val.objet)
            eng = int(val.eng_id)
            no_ex = int(val.x_exercice_id)
            struct = int(val.company_id)

            if self.beneficiaire:
                self.imput_benef = int(self.beneficiaire.cpte_fournisseur.souscpte.id)
                cpte_benef = int(self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte)
                self.env.cr.execute(
                    """UPDATE budg_engagement SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (benef, self.imput_benef, cpte_benef, eng, no_ex, struct))
                self.env.cr.execute(
                     """UPDATE budg_liqord_p SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                     (benef, self.imput_benef, cpte_benef, eng, no_ex, struct))
                self.env.cr.execute(
                     """UPDATE budg_mandat_p SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                     (benef, self.imput_benef, cpte_benef, eng, no_ex, struct))

                self.write({'state': 'C'})

            elif self.objet:
                self.env.cr.execute(
                    """UPDATE budg_engagement_p SET lb_obj = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (obj, eng, no_ex, struct))
                self.env.cr.execute(
                     """UPDATE budg_liqord_p SET lb_obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                     (obj, eng, no_ex, struct))
                self.env.cr.execute(
                     """UPDATE budg_mandat_p SET obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                     (obj, eng, no_ex, struct))

                self.write({'state': 'C'})
            else:
                raise ValidationError(_("Pas de données à corriger."))


class BudgBordEngP(models.Model):
    _name = "budg_bordereau_engagement_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_eng = fields.Char(string='N° Bord. Eng',
                              default=lambda self: self.env['ir.sequence'].next_by_code('no_bord_eng'))
    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Transmission d'engagement pour CG",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
    date_emis = fields.Date("Date d'émision", default=fields.Date.context_today, readonly=True)
    date_recus = fields.Date("Date de réception")
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    cd_acteur_accuse = fields.Char(string="Acteur")
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    engagement_ids = fields.Many2many("budg_engagement_p", "eng_id_p", string="Liste des engagements", ondelete="restrict")
    state = fields.Selection([('N', 'Nouveau'),('T', 'Envoyé à CG'),('R', 'Réceptionné par CG'),
    ], 'Etat', default='N', required=True, readonly=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    signataire_3 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '3')]))

    @api.onchange('current_users')
    def user(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _controle_exercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    @api.depends('totaux')
    def amount_to_words(self):
        self.text_amount = num2words(self.totaux, lang='fr')

    def action_generer_bord_eng(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_id = int(self.id)

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_eng_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_eng_p(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_eng_p SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.env.cr.execute(""" SELECT sum(mnt_eng) FROM budg_engagement_p e , budg_bordereau_engagement_p b, eng_id_p be
		WHERE e.state = 'V' and b.x_exercice_id = %d AND b.company_id = %d AND be.budg_bordereau_engagement_id = %d 
		AND e.id = be.budg_engagement_p_id AND be.budg_bordereau_engagement_p_id = b.id""" % (val_ex, val_struct, val_id))
        res = self.env.cr.fetchone()
        resu = res and res[0] or 0
        if resu <= 0:
            raise ValidationError(_("Le bordereau doit contenir uniquement que des engagements approuvés."))
        else:
            self.totaux = resu

            self.env.cr.execute(""" SELECT sum(totaux) FROM budg_bordereau_engagement_p b
            WHERE b.x_exercice_id = %d AND b.company_id = %d and b.id != %d """ % (val_ex, val_struct, val_id))
            res1 = self.env.cr.fetchone()
            self.total_prec = res1 and res1[0] or 0

            self.write({'state': 'T'})


class BudgCompteurBordEngP(models.Model):
    _name = "budg_compteur_bord_eng_p"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordeng = fields.Integer(default=0)


class BudgBordEngCtrlP(models.Model):
    _name = "budg_bordereau_engagement_controle_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Reception d'Engagement de DFC",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default="CG", readonly=True)
    date_emis = fields.Date("Date d'émision", readonly=True)
    date_recus = fields.Date("Date de réception", readonly=True)
    date_recep = fields.Date("Date de réception par DFC", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    bord_recu = fields.Many2one("budg_bordereau_engagement_p", "N° Bord. reçu", required=True,
                                domain=[('state', '=', 'T')])
    cd_acteur_accuse = fields.Char(string="Acteur")
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    engagement_ids = fields.One2many("budg_liste_engagment_p", "bord_id")
    state = fields.Selection([
        ('N', 'Nouveau'),
        ('R', 'Réceptionner bordereau'),
    ], 'Etat', default='N', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select b.dt_etat as dte, b.id as eng, b.prog_id as prog, b.section_id as sec, b.action as act, b.chapitre_id as chap,
            and b.activite_id as activ, b.cd_article_id as art, b.parag_id as par, b.rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
            b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement_p b, budg_bordereau_engagement_p bb, eng_id_p i 
            where bb.id = %d and i.budg_engagement_p_id = b.id and i.budg_bordereau_engagement_p_id = bb.id and b.company_id = %d and b.x_exercice_id = %d and b.state = 'V' """
                                % (id_bord, val_struct, val_ex))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.engagement_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_eng': line['eng'], 'prog_id': line['prog'],
                                      'section_id': line['sec'], 'action_id': line['act'],
                                      'chapitre_id': line['chap'], 'activite_id': line['activ'],
                                      'article_id': line['art'], 'parag_id': line['par'],
                                      'rubrique_id': line['rub'], 'type_procedure': line['proc'],
                                      'type_beneficiaire_id': line['typeb'], 'no_beneficiaire': line['benef'],
                                       'lb_obj': line['obj'], 'mnt_eng': line['mnt']}))
            self.engagement_ids = result

    def receptionner(self):

        bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_eng_ctrl_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_eng_ctrl_p(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_eng_ctrl_p SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.date_recus = date.today()

        self.env.cr.execute(
            """UPDATE budg_bordereau_engagement_p SET state ='R', date_recus = %s WHERE id = '%s' and x_exercice_id = %s and company_id = %s""",
            (self.date_recus, bord, val_ex, val_struct))

        self.afficher()

        self.write({'state': 'R'})

    def envoyer(self):

        self.write({'state': 'E'})

        self.date_emis = date.today()


class BudgListeEngagementP(models.Model):
    _name = 'budg_liste_engagment_p'

    bord_id = fields.Many2one('budg_bordereau_engagement_controle_p', ondelete='cascade')
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
    no_eng = fields.Many2one("budg_engagement_p", string="N° engagement", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", readonly=True)
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string="Identité")
    lb_obj = fields.Text(string="Objet", size=300, readonly=True)
    mnt_eng = fields.Float(string="Montant engagement", readonly=True)
    piecejust_ids = fields.One2many("budg_liste_piece_eng_p", 'eng_id', readonly=True)
    dt_visa_cf = fields.Date(string="Date Visa")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet")
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([
        ('V', 'Approuvé'),
        ('W', 'Visé'),
        ('R', 'Rejeté'),
    ], default='V', string='Etat', index=True, readonly=True, track_visibility='always')
    credit_disponible = fields.Integer()
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='N')
    observation = fields.Text("Observation")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)

    def viser(self):

        for vals in self:
            eng = int(vals.no_eng)
            val_strcut = int(vals.company_id)

            self.env.cr.execute(
                """UPDATE budg_engagement_p SET state ='W', envoyer_daf = 'Y' WHERE id = %d and company_id = %d"""
                % (eng, val_strcut))

            self.write({'state': 'W'})

    def rejeter(self):

        eng = int(self.no_eng)
        val_strcut = int(self.company_id)

        val_rejet = self.motif_rejet

        self.env.cr.execute(
            """UPDATE budg_engagement_p SET state ='R', motif_rejet = %s WHERE id = %s and company_id = %s""",
            (val_rejet, eng, val_strcut))

        self.write({'state': 'R'})

    def afficher_piece(self):

        eng = int(self.no_eng)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute(
                "select lb_long as lib, oblige as obl, ref as re, montant as mnt, dte as dte, nombre as nbr from budg_piece_engagement_p where eng_id = %d and company_id = %d" % (
                eng, val_struct))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.piecejust_ids.unlink()
            for line in rows:
                result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'dte': line['dte'], 'ref': line['re'],
                                      'mnt': line['mnt'], 'nbr': line['nbr']}))
            self.piecejust_ids = result


class BudgListePieceEngP(models.Model):
    _name = "budg_liste_piece_eng_p"

    eng_id = fields.Many2one("budg_liste_engagment_p", ondelete='cascade')
    lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
    oblige = fields.Boolean("Obligatoire", readonly=True)
    ref = fields.Char("Référence", readonly=True)
    dte = fields.Date("Date", readonly=True)
    nbr = fields.Integer("Nombre", readonly=True)
    mnt = fields.Integer("Montant", readonly=True)

"""c'est ici que je dois voir"""
class BudgBordEngRenvoiDafP(models.Model):
    _name = "budg_bordereau_engagement_renvoi_daf_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Transmission d'Engament pour DFC",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='CG', readonly=True)
    bord_recu = fields.Many2one("budg_bordereau_engagement_controle_p", "N° Bord.", required=False,
                                domain=[('state', '=', 'R')])
    date_emis = fields.Date("Date d'émision", readonly=True)
    date_recus = fields.Date("Date de réception")
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    cd_acteur_accuse = fields.Char(string="Acteur")
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    engagement_ids = fields.One2many("budg_liste_engagment_renvoi_p", "bord_id", string="Liste des engagements")
    state = fields.Selection([
        ('N', 'Nouveau'),
        ('E', 'Envoyé bordereau à DFC'),
        ('R', 'Bordereau receptionné par DFC'),
    ], 'Etat', default='N', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    signataire_3 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '3')]))

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select b.dt_etat as dte, b.no_eng as eng, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
			b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_liste_engagment b 
			where b.company_id = %d and b.state = 'W' and b.x_exercice_id = %d and envoyer_daf = 'N' """ % (
            val_struct, val_ex))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.engagement_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_eng': line['eng'], 'cd_titre_id': line['titre'],
                                      'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
                                      'cd_article_id': line['art'],
                                      'cd_paragraphe_id': line['par'], 'cd_rubrique_id': line['rub'],
                                      'type_procedure': line['proc'], 'type_beneficiaire_id': line['typeb'],
                                      'no_beneficiaire': line['benef'], 'lb_obj': line['obj'], 'mnt_eng': line['mnt']}))
            self.engagement_ids = result

    def envoyer(self):

        bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute("""select * from budg_liste_engagment_renvoi_p r, budg_bordereau_engagement_renvoi_daf_p d 
		where r.bord_id = d.id and r.bord_id = %d and r.company_id = %d and r.envoyer = 'Y'""" % (bord, val_struct))
        for val in self.env.cr.dictfetchall():
            envo = val['envoyer']

            self.env.cr.execute("""UPDATE budg_liste_engagment_p SET envoyer_daf ='Y' WHERE id = %d and x_exercice_id = %d and
			company_id = %d""" % (envo, val_ex, val_struct))

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_eng_renvoi_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_eng_renvoi_p(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_eng_renvoi_p SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.date_emis = date.today()

        self.write({'state': 'E'})


class BudgListeEngagementRenvoiP(models.Model):
    _name = 'budg_liste_engagment_renvoi_p'

    bord_id = fields.Many2one('budg_bordereau_engagement_renvoi_daf_p', ondelete='cascade')
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
    no_eng = fields.Many2one("budg_engagement", string="N° engagement", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", v=True)
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string="Identité")
    lb_obj = fields.Text(string="Objet", size=300, readonly=True)
    mnt_eng = fields.Float(string="Montant engagement", readonly=True)
    dt_visa_cf = fields.Date(string="Date Visa")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet")
    x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([
        ('V', 'Approuvé'),
        ('W', 'Visé'),
        ('R', 'Rejeté'),
    ], default='W', string='Etat', index=True, readonly=True, track_visibility='always')
    envoyer = fields.Selection([('Y', 'Oui'), ('N', 'Non')], default="Y", string="Envoyé ?")
    credit_disponible = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


class Budg_CompteurBordEngRenvoiP(models.Model):
    _name = "budg_compteur_bord_eng_renvoi_p"

    x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordeng = fields.Integer(default=0)


class BudgBordEngRecepCtrlP(models.Model):
    _name = "budg_bordereau_engagement_recep_controle_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Réception d'Engagement de CG",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='DFC', readonly=True)
    bord_recu = fields.Many2one("budg_bordereau_engagement_renvoi_daf_p", "N° Bord. réçu", required=True,
                                domain=[('state', '=', 'E')])
    date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
    date_recus = fields.Date("Date de réception", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    cd_acteur_accuse = fields.Char(string="Acteur")
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    engagement_ids = fields.Many2many("budg_liste_engagment_recu_p", "bord_p_id", string="Liste des engagements",
                                      ondelete="restrict")
    state = fields.Selection([
        ('E', 'Bordereau envoyé par CG'),
        ('R', 'Bordereau réceptionné'),
    ], 'Etat', default='E', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        if self.bord_recu:
            for vals in self:
                vals.env.cr.execute("""select b.dt_etat as dte, b.no_eng as eng, b.prog_id as prog, b.section_id as sec, b.action_id as act,
                b.chapitre_id as chap, b.activite_id as activ, b.article_id as art, b.parag_id as par, b.rubrique_id as rub, 
                b.type_procedure as proc, b.type_beneficiaire_id as typeb, b.no_beneficiaire as benef, b.lb_obj as obj, 
                b.mnt_eng as mnt from budg_liste_engagment_renvoi b where b.bord_id = %d and b.company_id = %d and b.state = 'W' and b.envoyer = 'Y' """
                                    % (id_bord, val_struct))

                rows = vals.env.cr.dictfetchall()
                result = []

                vals.engagement_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'dt_etat': line['dte'], 'no_eng': line['eng'],
                                          'prog_id': line['prog'], 'section_id': line['sec'],
                                           'action_id': line['act'], 'chapitre_id': line['chap'],
                                          'activite_id': line['art'], 'article_id': line['art'],
                                          'parag_id': line['par'], 'rubrique_id': line['rub'],
                                          'type_procedure': line['proc'], 'type_beneficiaire_id': line['typeb'],
                                          'no_beneficiaire': line['benef'], 'lb_obj': line['obj'],
                                          'mnt_eng': line['mnt']}))
                self.engagement_ids = result

    def receptionner(self):

        bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.date_recus = date.today()

        self.env.cr.execute(
            """UPDATE budg_bordereau_engagement_controle_p SET state ='R', date_recep = '%s' WHERE id = %s and x_exercice_id = %s and company_id = %s""" % (
            self.date_recus, bord, val_ex, val_struct))

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_eng_recep_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_eng_recep_p(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_eng_recep_p SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.afficher()

        self.write({'state': 'R'})


class BudgListeEngagementRecuP(models.Model):
    _name = 'budg_liste_engagment_recu_p'

    bord_id = fields.Many2one('budg_bordereau_engagement_recep_controle_p', ondelete='cascade')
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
    no_eng = fields.Many2one("budg_engagement", string="N° engagement", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", v=True)
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string="Identité")
    lb_obj = fields.Text(string="Objet", size=300, readonly=True)
    mnt_eng = fields.Float(string="Montant engagement", readonly=True)
    dt_visa_cf = fields.Date(string="Date Visa")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([
        ('V', 'Approuvé'),
        ('W', 'Visé'),
        ('R', 'Rejeté'),
    ], default='V', string='Etat', index=True, readonly=True, track_visibility='always')
    credit_disponible = fields.Integer()
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


class Budg_CompteurBordEngRecepP(models.Model):
    _name = "budg_compteur_bord_eng_recep_p"

    x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordeng = fields.Integer(default=0)


class BudgBordEngRejeteCtrlP(models.Model):
    _name = "budg_bordereau_engagement_rejet_controle_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Rejet d'Engagement de CG",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='CG', readonly=True)
    date_emis = fields.Date("Date émision", readonly=True)
    date_recus = fields.Date("Date de réception", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    cd_acteur_accuse = fields.Char(string="Acteur")
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    engagement_ids = fields.One2many("budg_liste_engagment_rejet_p", "bord_id", string="Liste des engagements")
    state = fields.Selection([
        ('N', 'Nouveau'),
        ('E', 'Bordereau envoyé à DFC'),
        ('R', 'Réceptionné bordereau par DFC'),
    ], 'Etat', default='N', required=True)
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    @api.constrains('x_exercice_id')
    def _controle_exercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select b.dt_etat as dte, b.id as eng, b.prog_id as prog, b.section_id as sec,b.action_id as act, b.chapitre_id as chap,
            b.activite_id as activ, b.article_id as art, b.parag_id as par, b.rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
            b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement_p b
            where b.company_id = %d and x_exercice_id = %d and b.state = 'R' """ % (val_struct, val_ex))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.engagement_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_eng': line['eng'], 'prog_id': line['prog'],
                                      'section_id': line['sec'], 'chapitre_id': line['chap'], 'action_id': line['act'],
                                      'activite_id': line['activ'], 'article_id': line['art'],
                                      'parag_id': line['par'], 'rubrique_id': line['rub'],
                                      'type_procedure': line['proc'], 'type_beneficiaire_id': line['typeb'],
                                      'no_beneficiaire': line['benef'], 'lb_obj': line['obj'],'mnt_eng': line['mnt']}))
                self.engagement_ids = result

    def envoyer(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.date_emis = date.today()

        self.env.cr.execute("select bordeng from budg_compteur_bord_eng_rejet_p where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng_rejet_p(x_exercice_id,company_id,bordeng) VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute("UPDATE budg_compteur_bord_eng_rejet_p SET bordeng = %d WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))
        self.write({'state': 'E'})

class BudgListeEngagementRejetP(models.Model):
    _name = 'budg_liste_engagment_rejet_p'

    bord_id = fields.Many2one('budg_bordereau_engagement_rejet_controle_p', ondelete='cascade')
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
    no_eng = fields.Many2one("budg_engagement_p", string="N° engagement", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", v=True)
    type_beneficiaire_id = fields.Many2one("ref_typebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string="Bénéficiaire")
    lb_obj = fields.Text(string="Objet", readonly=True)
    mnt_eng = fields.Float(string="Montant", readonly=True)
    dt_visa_cf = fields.Date(string="Date Visa")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([('R', 'Rejeté')], default='R', string='Etat', readonly=True)
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')
    observation = fields.Text("Observations")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


class BudgBordEngRecepRejetCtrlP(models.Model):
    _name = "budg_bordereau_engagement_recep_rejet_controle_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    no_bord_en = fields.Char(string='Bord. N°', readonly=True)
    type_bord_trsm = fields.Char("Type de bordereau", default="Réception bordereau de rejet d'engagement", readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
    bord_recu = fields.Many2one("budg_bordereau_engagement_rejet_controle_p", "Bord. reçu", required=True,
                                domain=[('state', '=', 'E')])
    date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
    date_recus = fields.Date("Date de réception", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    cd_acteur_accuse = fields.Char(string="Acteur")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    rejet_ids = fields.One2many("budg_engagement_rejeter_p", "rejet_id", string="Liste des engagements",
                                ondelete="restrict")
    state = fields.Selection([('E', 'Envoyé par CG'), ('R', 'Réceptionné')],
                             'Etat', default='E', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select * from budg_liste_engagment_rejet_p b
            where b.bord_id = %d and b.company_id = %d and b.x_exercice_id = %d and b.state = 'R' """ % (
            id_bord, val_struct, val_ex))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.rejet_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dt_etat'], 'eng_id': line['no_eng'],
                                      'beneficiciare': line['no_beneficiaire'], 'objet': line['lb_obj'],
                                      'montant': line['mnt_eng'], 'motif_rejet': line['motif_rejet']}))
            self.rejet_ids = result

    def receptionner(self):

        bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.date_recus = date.today()

        self.env.cr.execute("""UPDATE budg_bordereau_engagement_rejet_controle_p SET state ='R', date_recus = %s WHERE id = %s and x_exercice_id = %s and
        company_id = %s""", (self.date_recus, bord, val_ex, val_struct))

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_eng_recep_rejet_ctrl_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_eng_recep_rejet_ctrl_p(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)"""
                % (val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_eng_recep_rejet_ctrl_p SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d"
                % (vals, val_ex, val_struct))

        self.afficher()
        self.write({'state': 'R'})


class BudgEngRejeterP(models.Model):
    _name = "budg_engagement_rejeter_p"

    rejet_id = fields.Many2one("budg_bordereau_engagement_recep_rejet_controle_p", ondelte='cascade')
    dt_etat = fields.Date("Date", readonly=True)
    eng_id = fields.Many2one("budg_engagement_p", "N° Engagement", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    beneficiciare = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    montant = fields.Float("Montant", readonly=True)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('R', 'Rejeté')], string="Etat", default="R", readonly=True)


class Budg_Compteur_bordRecepEngCfP(models.Model):
    _name = "budg_compteur_bord_eng_recep_rejet_ctrl_p"

    x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordeng = fields.Integer(default=0)


class BudgCorrectionEngagementRejetP(models.Model):
    _name = "budg_correction_engagement_rejet_p"
    _rec_name = "eng_id"

    eng_id = fields.Many2one("budg_engagement_p", "N° Engagement", required=True, domain=[('state', '=', 'R')])
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    mnt = fields.Float("Montant", readonly=True)
    anc_objet = fields.Text("Objet", readonly=True)
    objet = fields.Text("Objet", readonly=False)
    anc_beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
    cpte_benef = fields.Char('compte')
    imput_benef = fields.Char('imput')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('R', 'Rejeté'), ('C', 'Corrigé')], default='R', string="Etat", required=True)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'), ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'),
                                    ('4', 'Erreur Bénéficiaire'), ('5', 'Erreur Objet')],
                                   string="Motif du rejet", readonly=True)
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    piece_ids = fields.One2many("budg_piecejustificativecorrectmandat", "mdt_id")

    @api.onchange('current_users')
    def user(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    @api.onchange("eng_id")
    def valeur(self):
        for vals in self:
            if vals.eng_id:
                self.prog_id = self.eng_id.prog_id
                self.section_id = self.eng_id.section_id
                self.action_id = self.eng_id.action_id
                self.chapitre_id = self.eng_id.chapitre_id
                self.activite_id = self.eng_id.activite_id
                self.article_id = self.eng_id.article_id
                self.para_id = self.eng_id.parag_id
                self.rubrique_id = self.eng_id.rubrique_id
                self.mnt = self.eng_id.mnt_eng
                self.anc_beneficiaire = self.eng_id.no_beneficiaire
                self.anc_objet = self.eng_id.lb_obj
                self.motif_rejet = self.eng_id.motif_rejet

    @api.onchange('beneficiaire')
    def cpte(self):
        self.cpte_benef = self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
        self.imput_benef = self.beneficiaire.cpte_fournisseur.souscpte.id

    def corriger(self):
        eng = int(self.eng_id)
        no_ex = int(self.x_exercice_id)
        struct = int(self.company_id)
        for val in self:
            if val.motif_rejet == '1':
                raise ValidationError(_("Correction impossible pour ce motif. Veuillez annuler cet engagement et reprendre un nouveau."))
            elif val.motif_rejet == '2':
                raise ValidationError(_("Correction impossible pour ce motif. Veuillez annuler cet engagement et reprendre un nouveau."))
            elif val.motif_rejet == '3':
                benef = int(val.beneficiaire)
                cpte = val.cpte_benef
                imput = val.imput_benef
                val.env.cr.execute("""UPDATE budg_engagement SET state='V' WHERE id = %s and x_exercice_id = %s and company_id = %s""",( eng, no_ex, struct))
                val.write({'state': 'C'})
                val.env.cr.execute("""select * from budg_piecejustificativecorrecteng where mdt_id = %s""")
                for vals in val.env.cr.dictfetchall():
                    pj = vals['piecejust_id']
                    ref = vals['reference']
                    dte = vals['datepj']
                    obl = vals['active']
                    mnt = vals['montant']
                    nbre = vals['nombre']

                    self.env.cr.execute("""INSERT INTO budg_piece_eng(lb_long, ref, dte, oblige, montant, nombre, eng_id) VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre, eng))
            elif val.motif_rejet == '4':
                benef = int(val.beneficiaire)
                cpte = self.cpte_benef
                imput = self.imput_benef
                val.env.cr.execute("""UPDATE budg_engagement SET state='V', no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""" ,(benef, cpte, imput, eng, no_ex, struct))
                val.write({'state': 'C'})
            elif val.motif_rejet == '5':
                obj = str(val.objet)
                val.env.cr.execute("""UPDATE budg_engagement SET lb_obj = %s, state='V' WHERE id = %s and x_exercice_id = %s and company_id = %s""",(obj, eng, no_ex, struct))
                val.write({'state': 'C'})
            else:
                raise ValidationError(_("Pas de données à corriger."))


class Budg_PieceJustiCorrecEngP(models.Model):
    _name = "budg_piecejustificativecorrecteng_p"

    piecejust_id = fields.Many2one('ref_piece_justificatives', string="Intitulé")
    reference = fields.Char("Références", size=35)
    datepj = fields.Date('Date')
    active = fields.Boolean("Obligé ?", default=True)
    montant = fields.Integer('Montant', size=15)
    nombre = fields.Integer("Nbre copies(s)")
    eng_id = fields.Many2one("budg_correction_engagement_rejet_p",ondelete='cascade')


class BudgPieceLiqP(models.Model):
    _name = "budg_piece_liq_p"

    lb_long = fields.Many2one("ref_piece_justificatives", "Libellé")
    oblige = fields.Boolean("Obligé")
    nombre = fields.Integer("Nombre")
    ref = fields.Char("Référence")
    montant = fields.Integer("Montant")
    dte = fields.Date("Date")
    liq_id = fields.Many2one("budg_liqord_p", ondelete='cascade')
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")


class BudgLiqOrdP(models.Model):
    _name = "budg_liqord_p"
    _rec_name = "no_lo"
    _order = " id desc"

    type_procedure = fields.Many2one('budg_typeprocedure', string="Type de procédure", readonly=True)
    no_eng = fields.Many2one("budg_engagement_p", "Engagement", required=True,
                             domain=['|', ('state', '=', 'W'), ('state', '=', 'LC')],
                             states={'N': [('readonly', True)], 'L': [('readonly', True)], 'A': [('readonly', True)]})
    no_lo = fields.Char(string="N°liquidation",
                        states={'N': [('readonly', True)], 'L': [('readonly', True)], 'V': [('readonly', True)],
                                'A': [('readonly', True)]}, readonly=True)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    res_liq = fields.Integer(string="Reste à liquider", compute="_mnt_restant", store=True)
    mnt_ord = fields.Integer(string="Montant ordonnancé")
    mnt_paye = fields.Integer(string="Montant à liquider",
                              states={'N': [('readonly', True)], 'L': [('readonly', True)], 'V': [('readonly', True)],
                                      'A': [('readonly', True)]})
    mnt_eng = fields.Integer(string="Reste Montant Eng.", readonly=True)

    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)

    nb_pjust = fields.Integer()
    typedossier = fields.Many2one("budg_typedossierbudg",
                                  default=lambda self: self.env['budg_typedossierbudg'].search([('code', '=', 'LIQ')]),
                                  string="Type de dossier", readonly=True, )
    modereg = fields.Many2one('ref_modereglement', 'Mode de règlement', readonly=True)
    piecejust_line_ids = fields.One2many("budg_piece_liq_p", 'liq_id')
    agence_bank_id = fields.Char(string="N° Agence")
    dt_visa_cf = fields.Integer(string="Date Visa Cf")
    dt_visa_ord = fields.Integer(string="Date Visa Ord")
    dt_visa_ac = fields.Integer(string="Date Visa Ac")
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date liquidation", required=True,
                          states={'L': [('readonly', True)], 'A': [('readonly', True)]})
    dispo_engs = fields.Float()
    total_liq_engs = fields.Float()
    cpte_benef = fields.Char('compte')
    cpte_rub = fields.Char('cpte rub')
    imput_benef = fields.Many2one('ref_souscompte', 'imput')
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    categorie_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", string="Caté de bénéf/four", readonly=True)
    cd_type_accompte = fields.Many2one("budg_typeaccompte", string="Type d'accompte", required=True,
                                       states={'N': [('readonly', True)], 'L': [('readonly', True)],
                                               'A': [('readonly', True)]})
    no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", readonly=True)
    ref_mp = fields.Char('Réf. Marché', readonly=True)
    lb_obj = fields.Text(string="Objet", readonly=True)
    rf_mp = fields.Many2one("budg_marche")
    typ_budg_id = fields.Many2one("budg_typebudget")
    certif_id = fields.Many2one("budg_certification", "Motif de certification",
                                states={'L': [('readonly', True)], 'A': [('readonly', True)]})
    dt_demande = fields.Date()
    motif_rejet = fields.Char(string="Motif rejet")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([('draft', 'Brouillon'), ('N', 'Nouveau'), ('L', 'Liquidée'), ('A', 'Annulée'),
                              ], string='Etat', default='draft', index=True, readonly=True, copy=False,
                             track_visibility='always')
    active = fields.Boolean(default=True)
    etat = fields.Char(default="En cours")
    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
    acc_number = fields.Char(string="N° Compte", readonly=True)

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id', 'mnt_paye')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

            if record.mnt_paye <= 0:
                raise ValidationError(_("Le montant de la liquidation doit être supérieur à 0."))

    @api.depends('mnt_paye')
    def amount_to_words(self):
        self.text_amount = num2words(self.mnt_paye, lang='fr')

    def action_liquidation_confirmer(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select noliq from budg_compteur_liq_p where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_lo = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_liq_p(x_exercice_id,company_id,noliq)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.no_lo = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_liq_p SET noliq = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.write({'state': 'N'})

    def afficher_piece(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        eng = int(self.no_eng)

        for vals in self:
            vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, b.nombre as nbr, dte as dt, ref as ref, 
            montant as montant from budg_piece_engagement_p b where b.x_exercice_id = %d and b.company_id = %d
            and b.eng_id = %d order by b.id""" % (val_ex, val_struct, eng))
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.piecejust_line_ids.unlink()
            for line in rows:
                result.append((0, 0, {'lb_long': line['lib'], 'oblige': line['obl'], 'nombre': line['nbr'],
                                      'ref': line['ref'], 'dte': line['dt'], 'montant': line['montant']}))
            self.piecejust_line_ids = result

    def action_liquidation_liquider(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_eng = self.no_eng.no_eng
        mnt_paye = int(self.mnt_paye)

        if self.cd_type_accompte.cd_type_accompte == "AU":
            self.env.cr.execute(
                "UPDATE budg_engagement_p SET state = 'L', reste = reste - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s",
                (mnt_paye, val_eng, val_ex, val_struct))

            self.write({'state': 'L'})
            self.dispo_eng()
            self.total_liq_eng()
        else:
            self.env.cr.execute(
                "UPDATE budg_engagement_p SET state = 'LC', reste = reste - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s",
                (mnt_paye, val_eng, val_ex, val_struct))

            self.write({'state': 'L'})
            self.dispo_eng()
            self.total_liq_eng()

    def dispo_eng(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        v_eng = self.no_eng

        self.env.cr.execute("""select (sum(l.mnt_eng) - l.mnt_paye) FROM budg_liqord_p l, budg_engagement_p e
        WHERE e.id = %d and e.id = l.no_eng and l.company_id = %d and l.x_exercice_id = %d group by l.mnt_eng, l.mnt_paye"""
                            % (v_eng, val_struct, val_ex))
        res = self.env.cr.fetchone()
        self.dispo_engs = res and res[0] or 0

    def total_liq_eng(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        v_eng = int(self.no_eng)

        self.env.cr.execute("""select sum(l.mnt_paye) FROM budg_liqord_p l, budg_engagement_p e
        WHERE e.id = l.no_eng and l.no_eng = %d and l.company_id = %d and l.x_exercice_id = %d 
        and l.state not in ('A') group by l.mnt_paye""" % (v_eng, val_struct, val_ex))
        res = self.env.cr.fetchone()
        self.total_liq_engs = res and res[0] or 0

    def action_liquidation_certifier(self):
        self.write({'state': 'V'})

    def action_liquidation_annuler(self):
        self.write({'state': 'A'})

    @api.onchange('cd_type_accompte')
    def compute_mnt_paye(self):
        if self.cd_type_accompte.cd_type_accompte != "AU":
            self.mnt_paye = 0
        else:
            self.mnt_paye = self.mnt_eng

    @api.depends('mnt_eng', 'mnt_paye')
    def _mnt_restant(self):
        for x in self:
            x.res_liq = x.mnt_eng - x.mnt_paye

    @api.onchange('no_eng')
    def no_eng_on_change(self):

        if self.no_eng:
            self.prog_id = self.eng_id.prog_id
            self.section_id = self.eng_id.section_id
            self.action_id = self.eng_id.action_id
            self.chapitre_id = self.eng_id.chapitre_id
            self.activite_id = self.eng_id.activite_id
            self.article_id = self.eng_id.article_id
            self.para_id = self.eng_id.parag_id
            self.rubrique_id = self.eng_id.rubrique_id
            self.mnt_eng = self.no_eng.reste
            self.type_procedure = self.no_eng.type_procedure
            self.categorie_beneficiaire_id = self.no_eng.type_beneficiaire_id
            self.type_beneficiaire_id = self.no_eng.type_beneficiaire_id
            self.no_beneficiaire = self.no_eng.no_beneficiaire
            self.lb_obj = self.no_eng.lb_obj
            self.cpte_benef = self.no_eng.cpte_benef
            self.cpte_rub = self.no_eng.cpte_rub
            self.imput_benef = self.no_eng.imput_benef
            self.ref_mp = self.no_eng.ref_mp
            self.modereg = self.no_eng.modereg.id
            self.bank_id = self.no_eng.bank_id
            self.acc_number = self.no_eng.acc_number


class Budg_Compteur_liqP(models.Model):
    _name = "budg_compteur_liq_p"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    noliq = fields.Integer()


class BudgMandatP(models.Model):
    _name = "budg_mandat_p"
    _rec_name = "no_mandat"
    _order = " id desc"

    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", readonly=True)
    no_eng = fields.Many2one("budg_engagement_p", string="N° engagement", readonly=True)
    no_mandat = fields.Char(string="N° Ordonnance", readonly=True)
    no_lo = fields.Many2one("budg_liqord_p", string="Liquidation",
                            domain=[('state', '=', 'L'), ('etat', '=', 'En cours')],
                            states={'N': [('readonly', True)], 'A': [('readonly', True)], 'O': [('readonly', True)],
                                    'V': [('readonly', True)], 'R': [('readonly', True)], 'I': [('readonly', True)],
                                    'J': [('readonly', True)], 'E': [('readonly', True)], 'F': [('readonly', True)]},
                            required=True)
    mnt_eng = fields.Integer(string="Montant", readonly=True)
    typedossier = fields.Many2one("budg_typedossierbudg",
                                  default=lambda self: self.env['budg_typedossierbudg'].search([('code', '=', 'LIQ')]),
                                  string="Type de dossier", readonly=True)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    cpte_benef = fields.Char('compte')
    cpte_rub = fields.Char('compte rub')
    imput_benef = fields.Many2one('ref_souscompte', 'imput')
    mnt_annule = fields.Integer(default=0)
    mnt_ord = fields.Integer(string="Montant", readonly=True)
    mnt_paye = fields.Integer(string="Montant payé")
    ac_cf = fields.Selection([('AC', 'AC'), ('CF', 'CF')], string='Banque')
    agence_id = fields.Many2one("ref_banque_agence", string="Banque")
    num_compte = fields.Char(string="N° Compte")
    piecejust_ids = fields.One2many("budg_piece_ord_p", 'mandat_id')
    bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
    agence_bank_id = fields.Char(string="N° Agence")
    acc_number = fields.Char(string="N° compte", readonly=True)
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date mandat", required=True,
                          states={'A': [('readonly', True)], 'O': [('readonly', True)], 'V': [('readonly', True)],
                                  'R': [('readonly', True)], 'I': [('readonly', True)], 'J': [('readonly', True)],
                                  'E': [('readonly', True)], 'F': [('readonly', True)]})
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie Four.")
    categorie_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", string="Caté de bénéf/four", readonly=True)
    no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", readonly=True)
    no_beneficiaires = fields.Many2one("ref_beneficiaire", string="Id Benef", readonly=True)
    obj = fields.Text(string="Objet mandat", readonly=True)
    modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
    type_accompte_id = fields.Many2one("budg_typeaccompte", string="Type d'accompte", readonly=True)
    typ_budg_id = fields.Many2one("budg_typebudget")
    commentaire = fields.Text()
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('draft', 'Brouillon'), ('N', 'Confirmé'),
        ('A', 'Annulé'), ('O', 'Ordonnancé'),
        ('I', 'Visé par AC/DFC'), ('J', 'Rejété par DFC'),
        ('E', 'Pris en charge'), ('F', 'Payé'),
    ], 'Etat', default='draft', index=True, readonly=True, copy=False, track_visibility='always')
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    active = fields.Boolean(default="False")
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], default='N')
    signataire_1 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '1')]))
    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '4')]))
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    @api.depends('mnt_ord')
    def amount_to_words(self):
        self.text_amount = num2words(self.mnt_ord, lang='fr')

    def action_mandat_brouillon(self):
        self.write({'state': 'draft'})

    def action_mandat_confirme(self):

        val_ex = int(self.x_exercice_id)
        v_id = int(self.no_lo.no_eng.id)
        val_struct = int(self.company_id)
        val_lo = int(self.no_lo)

        self.env.cr.execute(
            "select nomand from budg_compteur_mand_p where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        mandat = self.env.cr.fetchone()
        no_mandat = mandat and mandat[0] or 0
        c1 = int(no_mandat) + 1
        c = str(no_mandat)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_mandat = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_mand_p(x_exercice_id,company_id,nomand)  VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_mandat) + 1
            c = str(no_mandat)
            ok = str(c1).zfill(4)
            self.no_mandat = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_mand_p SET nomand = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.write({'state': 'N'})

        self.env.cr.execute(
            "UPDATE budg_liqord_p set etat = 'Terminé' where id = %d and x_exercice_id = %d and company_id = %d" % (
            val_lo, val_ex, val_struct))

    def action_mandat_ordonnance(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        prog = int(self.no_eng.prog_id)
        sec = int(self.no_eng.section_id)
        act = int(self.no_eng.action_id)
        chap = int(self.no_eng.chapitre_id)
        activ = int(self.no_eng.activite_id)
        art = int(self.no_eng.article_id)
        par = int(self.no_eng.paragraphe_id)
        rub = int(self.no_eng.rubrique_id)

        self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET mnt_mandate = (select sum(BM.mnt_ord) 
        FROM budg_ligne_exe_dep_p BE, budg_engagement_p E, budg_mandat_p BM WHERE E.no_eng = BM.no_eng AND BE.prog_id = E.prog_id 
        and BE.section_id = E.section_id and BE.action_id = E.action_id and BE.chapitre_id = E.chapitre_id 
        and BE.activite_id = E.activite_id and BE.article_id = E.article_id and
        BE.parag_id = E.parag_id and BE.rubrique_id = E.rubrique_id and
        BE.prog_id = %d and BE.section_id = %d and BE.action_id = %d BE.cd_chapitre_id = %d and BE.activite_id = %d and
        BE.article_id = %d and BE.parag_id = %d and BE.cd_rubrique_id = %d and BE.x_exercice_id = %d and BE.company_id = %d 
        and state not in ('draft','A','J')) WHERE prog_id = %d and 
        section_id = %d and action_id = %d and chapitre_id = %d and activite_id = %d and article_id = %d and parag_id = %d and 
        rubrique_id = %d and x_exercice_id = %d and company_id = %d"""
                            % (prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct,
                               prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct))

        self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET reste_mandat = (mnt_engage - mnt_mandate) 
        WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d and activite_id = %d and
        article_id = %d and cd_paragraphe_id = %d and rubrique_id = %d and x_exercice_id = %d and company_id = %d"""
                            % (prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct))
        self.write({'state': 'O'})

    def afficher_piece(self):
        val_liq = int(self.no_lo)

        for vals in self:
            vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, 
            montant as mnt, b.dte as dte, b.nombre as nbr, b.ref as ref 
            from budg_piece_liq_p b where liq_id = %d""" % (val_liq))
            rows = vals.env.cr.dictfetchall()
            result = []
            vals.piecejust_ids.unlink()
            for line in rows:
                result.append((0, 0, {'lb_long': line['lib'], 'oblige': line['obl'], 'dte': line['dte'],
                                      'nombre': line['nbr'], 'montant': line['mnt'], 'ref': line['ref']}))
            self.piecejust_ids = result

    # Annulation de l'engagement
    def action_mandat_annule(self):

        self.write({'state': 'A'})
        self.mnt_annule = self.mnt_ord

    def action_mandat_visa_ac(self):
        self.write({'state': 'I'})

    def action_mandat_rejeter_ac(self):
        self.write({'state': 'J'})

    # Chargement de la liquidation choisie
    @api.onchange('no_lo')
    def no_lo_on_change(self):

        if self.no_lo:
            self.type_accompte_id = self.no_lo.cd_type_accompte
            self.mnt_eng = self.no_lo.mnt_eng
            self.mnt_ord = self.no_lo.mnt_paye
            self.no_eng = self.no_lo.no_eng
            self.obj = self.no_lo.lb_obj
            self.type_procedure = self.no_lo.type_procedure
            self.prog_id = self.no_lo.prog_id
            self.section_id = self.no_lo.section_id
            self.action_id = self.no_lo.action_id
            self.chapitre_id = self.no_lo.chapitre_id
            self.activite_id = self.no_lo.activite_id
            self.article_id = self.no_lo.article_id
            self.para_id = self.no_lo.parag_id
            self.rubrique_id = self.no_lo.rubrique_id
            self.categorie_beneficiaire_id = self.no_lo.categorie_beneficiaire_id
            self.type_beneficiaire_id = self.no_lo.type_beneficiaire_id
            self.no_beneficiaire = self.no_lo.no_beneficiaire
            self.cpte_benef = self.no_lo.cpte_benef
            self.cpte_rub = self.no_lo.cpte_rub
            self.imput_benef = self.no_lo.imput_benef
            # self.ref_mp = self.no_lo.ref_mp
            self.modereg = self.no_lo.modereg
            self.bank_id = self.no_lo.bank_id
            self.acc_number = self.no_lo.acc_number


class Budg_Compteur_mand(models.Model):
    _name = "budg_compteur_mand"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    nomand = fields.Integer(default=0)


class BudgPieceOrdP(models.Model):
    _name = "budg_piece_ord_p"

    lb_long = fields.Many2one("ref_piece_justificatives", "Libellé")
    oblige = fields.Boolean("Obligé")
    nombre = fields.Integer("Nombre")
    ref = fields.Char("Référence")
    dte = fields.Date("Date")
    montant = fields.Integer("Montant")
    mandat_id = fields.Many2one("budg_mandat_p", ondelete='cascade')
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")


class BudgApprobationGroupMdtP(models.Model):
    _name = 'budg_appro_group_mdt_p'
    _rec_name = 'dte'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,
                                 string='Structure')
    dte = fields.Date("Date", default=fields.Date.context_today, readonly=True)
    appro_ids = fields.One2many("budg_appro_group_mdt_line_p", "appro_id")
    state = fields.Selection([('A', 'A approuver'), ('V', 'Approuvés')], default='A', string="Etat")

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        val_struct = int(self.company_id)
        val_ex = int(self.x_exercice_id)

        for vals in self:
            vals.env.cr.execute(""" SELECT * from budg_mandat_p m
            where state = 'N' and m.company_id = %d and 
            m.x_exercice_id = %d""" % (val_struct, val_ex))
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.appro_ids.unlink()
            for line in rows:
                result.append((0, 0, {'mdt_id': line['id'], 'prog_id': line['prog_id'],
                                    'section_id': line['section_id'], 'action_id': line['action_id'],
                                    'chapitre_id': line['chapitre_id'], 'activite_id': line['activite_id'],
                                    'article_id': line['article_id'], 'parag_id': line['parag_id'],
                                    'rubrique_id': line['rubrique_id'], 'x_exercice_id': line['x_exercice_id'],
                                    'company_id': line['company_id'], 'mnt': line['mnt_ord'], 'objet': line['obj']}))
            self.appro_ids = result

    def approuver(self):
        no_ex = int(self.x_exercice_id)
        struct = int(self.company_id)
        v_id = int(self.id)

        self.env.cr.execute("""SELECT l.* FROM budg_appro_group_mdt_line_p l, budg_appro_group_mdt_p m 
        where l.appro_id = m.id and m.id = %d and l.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

        for val in self.env.cr.dictfetchall():
            mdt = val['mdt_id']
            prog = val['prog_id']
            sec = val['section_id']
            act = val['action_id']
            chap = val['chapitre_id']
            activ = val['activite_id']
            art = val['article_id']
            par = val['parag_id']
            rub = val['rubrique_id']
            approuver = val['approuver']

            if approuver == True:
                self.env.cr.execute("""UPDATE budg_mandat_p SET state = 'O' WHERE id = %s and prog_id = %s and 
                section_id = %s and action_id = %s and chapitre_id = %s and activite_id = %s and article_id = %s 
                and parag_id = %s and rubrique_id = %s and company_id = %s"""
                                    % (mdt, prog, sec, act, chap, activ, art, par, rub, struct))

                self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET mnt_mandate = (select sum(BM.mnt_ord) 
                FROM budg_ligne_exe_dep_p BE, budg_engagement_p E, budg_mandat_p BM WHERE E.id = BM.no_eng AND BE.prog_id = E.prog_id 
                and BE.section_id = E.section_id and BE.chapitre_id = E.chapitre_id and BE.article_id = E.article_id and
                BE.parag_id = E.parag_id and BE.rubrique_id = E.rubrique_id and
                BE.prog_id = %s and BE.section_id = %s and BE.action_id = %s and BE.chapitre_id = %s and BE.activite_id = %s 
                and BE.article_id = %s and BE.parag_id = %s and 
                BE.rubrique_id = %s and BE.x_exercice_id = %s and BE.company_id = %s) WHERE prog_id = %s and 
                section_id = %s and action_id = %s and chapitre_id = %s and activite_id = %s and article_id = %s
                and parag_id = %s and rubrique_id = %s and x_exercice_id = %s and company_id = %s""",
                                    (prog, sec, act, chap, activ, art, par, rub, no_ex, struct, prog, sec,
                                     act, chap, activ, art, par, rub, no_ex, struct))

                self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET reste_mandat = (mnt_corrige - mnt_mandate) 
                WHERE id = %s and prog_id = %s and section_id = %s and action_id = %s and chapitre_id = %s and 
                activite_id = %s and article_id = %s and parag_id = %s and rubrique_id = %s and x_exercice_id = %s 
                and company_id = %s """, (prog, sec, act, chap, activ, art, par, rub, no_ex, struct))

                self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET taux = ((mnt_mandate * 100) / mnt_corrige)
                WHERE prog_id = %s and section_id = %s and action_id = %s and chapitre_id = %s and 
                activite_id = %s and article_id = %s and parag_id = %s and rubrique_id = %s and x_exercice_id = %s 
                and company_id = %s""", (prog, sec, act, chap, activ, art, par, rub, no_ex, struct))

        self.write({'state': 'V'})


class BudgApprobationGroupMdtLine(models.Model):
    _name = 'budg_appro_group_mdt_line_p'

    appro_id = fields.Many2one("budg_appro_group_mdt_p", ondelete='cascade')
    mdt_id = fields.Many2one("budg_mandat_p", "N° Ordonnance", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    mnt = fields.Float("Montant", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", readonly=True, string="Exercice")
    company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.user.company_id.id)
    approuver = fields.Boolean("Approuver ?")


class BudgAnnulMandatP(models.Model):
    _name = 'budg_mandat_annule_p'
    _rec_name = 'mandat_id'

    mandat_id = fields.Many2one('budg_mandat_p', "Ordonnance à annuler", domain=[('state', 'in', ['N', 'O', 'J'])],
                                required=True)
    montant = fields.Float('Montant', readonly=True)
    dte_mandat = fields.Date("Date Ordonnance", readonly=True)
    dte_annulation = fields.Date("Date d'annulation", required=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    typebenef = fields.Many2one("ref_categoriebeneficiaire", "Catégorie", readonly=True)
    nom = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    motif = fields.Text("Motif d'annulation", required=True)
    no_lo = fields.Many2one("budg_liqord_p", "Liquidation", readonly=True)
    no_engs = fields.Many2one("budg_engagement_p", "Eng", readonly=True)
    state = fields.Selection([
        ('N', 'Nouveau'), ('A', 'Annulé'), ], string='Etat', default='N')
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    @api.onchange('mandat_id')
    def OnChangeMdt(self):
        if self.mandat_id:
            self.montant = self.mandat_id.mnt_ord
            self.dte_mandat = self.mandat_id.dt_etat
            self.objet = self.mandat_id.obj
            self.typebenef = self.mandat_id.type_beneficiaire_id
            self.nom = self.mandat_id.no_beneficiaire
            self.prog_id = self.mandat_id.prog_id
            self.section_id = self.mandat_id.section_id
            self.action_id = self.mandat_id.action_id
            self.chapitre_id = self.mandat_id.chapitre_id
            self.activite_id = self.mandat_id.activite_id
            self.article_id = self.mandat_id.article_id
            self.parag_id = self.mandat_id.parag_id
            self.rubrique_id = self.mandat_id.rubrique_id
            self.no_lo = self.mandat_id.no_lo
            self.no_engs = self.mandat_id.no_eng

    def annuler(self):

        v_ex = int(self.x_exercice_id)
        v_struct = int(self.company_id)
        v_mdt = int(self.mandat_id)
        v_nolo = int(self.no_lo)
        v_eng = int(self.no_engs)
        v_mnt = int(self.montant)

        for val in self:
            self.env.cr.execute(
                """UPDATE budg_mandat_p SET state = 'A', mnt_annule = %s WHERE x_exercice_id = %s AND company_id = %s AND id = %s""",
                (v_mnt, v_ex, v_struct, v_mdt))
            self.env.cr.execute(
                """UPDATE budg_liqord_p SET state = 'A' WHERE x_exercice_id = %d AND company_id = %s AND id = %d""" % (
                v_ex, v_struct, v_nolo))
            self.env.cr.execute(
                """UPDATE budg_engagement_p SET state = 'V' WHERE x_exercice_id = %d AND company_id = %s AND id = %d""" % (
                v_ex, v_struct, v_eng))
            self.action_mandat_annuler()

    def action_mandat_annuler(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        v_mdt = int(self.mandat_id)

        prog = int(self.prog_id)
        sec = int(self.section_id)
        act = int(self.action_id)
        chap = int(self.chapitre_id)
        activ = int(self.activite_id)
        art = int(self.article_id)
        par = int(self.paragraphe_id)
        rub = int(self.rubrique_id)

        self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET mnt_mandate = (select DISTINCT sum(BM.mnt_ord) - BM.mnt_ord
        FROM budg_ligne_exe_dep_p BE, budg_mandat_p BM WHERE BM.id = %d AND 
        BE.prog_id = %d and BE.section_id = %d and BE.action_id = %d and BE.chapitre_id = %d and 
        BE.activite_id = %d and BE.article_id = %d and BE.parag_id = %d and 
        BE.rubrique_id = %d and BE.x_exercice_id = %d and BE.company_id = %d group by  BM.mnt_ord) 
        WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d
        and activite_id = %d and article_id = %d and parag_id = %d and rubrique_id = %d 
        and x_exercice_id = %d and company_id = %d"""
                            % (v_mdt, prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct,
                               prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct))

        self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET reste_mandat = (mnt_corrige - mnt_mandate) + mnt_mandate
        WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d and 
        activite_id = %d and article_id = %d and parag_id = %d and rubrique_id = %d and 
        x_exercice_id = %d and company_id = %d"""
                            % (prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct))

        self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET taux = ((mnt_mandate * 100) / mnt_corrige)
        WHERE prog_id = %d and section_id = %d and action_id = %d and chapitre_id = %d and 
        activite_id = %d and article_id = %d and parag_id = %d and rubrique_id = %d and 
        x_exercice_id = %d and company_id = %d"""
                            % (prog, sec, act, chap, activ, art, par, rub, val_ex, val_struct))

        self.write({'state': 'A'})


class BudgBordMdtRecepDcmefP(models.Model):
    _name = "budg_bordereau_mandatement_recep_dcmef_p"
    _rec_name = "no_bord_mandat"
    _order = " id desc"

    name = fields.Char()
    no_bord_mandat = fields.Char("Bord. N°", readonly=True)
    type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de Transmission de prise en charge",
                                 readonly=True)
    cd_acteur = fields.Char(string="Acteur", default="DFC", readonly=True)
    date_emis = fields.Date(string="Date d'émission", readonly=True)
    date_recus = fields.Date("Date de reception", readonly=True)
    date_envoi = fields.Date("Date d'émission PeC", readonly=True)
    date_recep = fields.Date("Date réception pour PeC", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    cd_acteur_accuse = fields.Char(string="Acteur", default="DFC", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    mandat_ids = fields.One2many("budg_liste_mandatement_recep_p", "liste_id")
    et_doss = fields.Selection([
        ('N', 'Nouveau'),
        ('PC', 'Envoyé pour PeC'),
        ('RP', 'Réceptionné pour PeC')
    ], 'Etat', default='N', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    signataire_2 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    total_gle = fields.Integer(string="Total gle", readonly=True)

    def MntPre(self):

        for val in self:
            val_id = int(val.id)
            val_ex = int(val.x_exercice_id)
            val_struct = int(val.company_id)

            val.env.cr.execute("""SELECT sum(mnt_ord) FROM budg_liste_mandatement_recep_p e,budg_bordereau_mandatement_recep_dcmef_p m
            WHERE e.envoyer = True AND m.company_id = %d AND e.liste_id = %d AND e.liste_id = m.id"""
                               % (val_struct, val_id))
            res = val.env.cr.fetchone()
            resu = res and res[0] or 0
            val.totaux = resu

            val.env.cr.execute("""SELECT sum(totaux) FROM budg_bordereau_mandatement_recep_dcmef b
            WHERE b.x_exercice_id = %d AND b.company_id = %d and b.id != %d and et_doss in ('PC','RP') """
                               % (val_ex, val_struct, val_id))
            res1 = val.env.cr.fetchone()
            val.total_prec = res1 and res1[0] or 0

            val.total_gle = val.totaux + val.total_prec

    @api.depends('totaux')
    def amount_to_words(self):
        self.text_amount = num2words(self.totaux, lang='fr')

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select m.dt_etat as dte, m.no_mandat as mdt, m.prog_id as prog, m.no_lo as liq, m.section_id as sec, 
            m.action_id as act, m.chapitre_id as chap, m.activite_id as activ,
            m.article_id as art, m.parag_id as par, m.rubrique_id as rub, m.type_beneficiaire_id as typeb,m.type_procedure as proc,
            m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m
            where m.company_id = %d and m.x_exercice_id = %d and m.state = 'O' and m.envoyer_daf = 'N' """
                                % (val_struct, val_ex))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.mandat_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_mandat': line['mdt'], 'no_lo': line['liq'],
                                      'type_procedure': line['proc'], 'prog_id': line['prog'],
                                      'section_id': line['sec'], 'action_id': line['act'], 'activite_id': line['activ'],
                                      'chapitre_id': line['chap'], 'article_id': line['art'],
                                      'parag_id': line['par'], 'rubrique_id': line['rub'],
                                      'type_beneficiaire_id': line['typeb'],'no_beneficiaire': line['benef'],
                                      'obj': line['obj'], 'mnt_ord': line['mnt']}))
            self.mandat_ids = result

    def approuver(self):
        no_ex = int(self.x_exercice_id)
        struct = int(self.company_id)
        v_id = int(self.id)

        self.env.cr.execute("""SELECT l.* FROM budg_liste_mandatement_recep_p l, budg_bordereau_mandatement_recep_dcmef_p m 
        where l.liste_id = m.id and m.id = %d and 
        l.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

        for val in self.env.cr.dictfetchall():
            mdt = val['no_mandat']
            prog = val['prog_id']
            sec = val['section_id']
            act = val['action_id']
            chap = val['chapitre_id']
            activ = val['activite_id']
            art = val['article_id']
            par = val['parag_id']
            rub = val['rubrique_id']
            approuver = val['envoyer']

            if approuver == True:
                self.env.cr.execute("""UPDATE budg_mandat_p SET envoyer_daf = 'Y' WHERE id = %s and prog_id = %s
                and section_id = %s and action_id = %s and chapitre_id = %s and activite_id = %s and article_id = %s
                and parag_id = %s and rubrique_id = %s and company_id = %s"""
                                    % (mdt, prog, sec, act, chap, activ, art, par, rub, struct))

    def envoyer(self):

        for vals in self:
            bord = int(vals.bord_recu)
            val_ex = int(vals.x_exercice_id.id)
            val_struct = int(vals.company_id.id)

            self.date_envoi = date.today()

            self.env.cr.execute(
                "select bordmand from budg_compteur_bord_mand_cf_p where x_exercice_id = %d and company_id = %d" % (
                val_ex, val_struct))
            bordmand = self.env.cr.fetchone()
            no_bord_mandat = bordmand and bordmand[0] or 0
            c1 = int(no_bord_mandat) + 1
            c = str(no_bord_mandat)
            print("la val eng", type(bordmand))
            if c == "0":
                ok = str(c1).zfill(4)
                self.no_bord_mandat = ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO budg_compteur_bord_mand_cf_p(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            else:
                c1 = int(no_bord_mandat) + 1
                c = str(no_bord_mandat)
                ok = str(c1).zfill(4)
                self.no_bord_mandat = ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE budg_compteur_bord_mand_cf_p SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))

            self.MntPre()
            self.approuver()
            self.write({'et_doss': 'PC'})


class BudgListeMdtRecepP(models.Model):
    _name = "budg_liste_mandatement_recep_p"

    liste_id = fields.Many2one("budg_bordereau_mandatement_recep_dcmef_p", ondelete='cascade', readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one('budg_typeprocedure', string="Type de procédure", readonly=True)
    no_eng = fields.Char(string="N° engagement", readonly=True)
    no_mandat = fields.Many2one("budg_mandat_p", string="N° Ordonnance", readonly=True)
    no_lo = fields.Many2one("budg_liqord_p", string="Liquidation", readonly=True)
    mnt_ord = fields.Integer(string="Montant", readonly=True)
    dt_etat = fields.Date(string="Date Ordonnance", readonly=True)
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Char(string="Bénéficiaire", readonly=True)
    obj = fields.Text(string="Objet", readonly=True)
    envoyer = fields.Boolean("Envoyer ?", readonly=False)
    modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
    motif_rejet = fields.Selection([('1', 'Erreur Montant'), ('2', 'Erreur')], string="Motif rejet", readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Visé par DCMEF'), ('R', 'Rejété par DCMEF'), ],
                             string='Etat', default='N', index=True, readonly=True, copy=False,
                             track_visibility='always')
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


class Budg_Compteur_bordMandCfP(models.Model):
    _name = "budg_compteur_bord_mand_cf_p"

    x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordmand = fields.Integer(default=0)


class BudgBordMdtControleviserP(models.Model):
    _name = "budg_bordereau_mandatement_controle_viser_p"
    _rec_name = "no_bord_mandat"
    _order = " id desc"

    name = fields.Char()
    no_bord_mandat = fields.Char("Bord. N°", readonly=True)
    type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de Reception Prise en Charge", readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='DAF', readonly=True)
    bord_recu = fields.Many2one("budg_bordereau_mandatement_recep_dcmef_p", required=True,
                                domain=[('et_doss', '=', 'PC')])
    date_emis = fields.Date(string="Date d'émission", default=fields.Date.context_today, readonly=True)
    date_recus = fields.Date("Date de reception", default=fields.Date.context_today, readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    mandat_ids = fields.One2many("budg_liste_mandatement_pc_p", "liste_id", string="Liste des mandats")

    et_doss = fields.Selection([
        ('N', 'Nouveau'),
        ('T', 'Envoyé pour prise en charge'),
        ('PC', 'Réceptionné pour prise en charge'),
    ], 'Etat', default='T', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def receptionner(self):
        for vals in self:
            bord = int(self.bord_recu)
            val_ex = int(vals.x_exercice_id.id)
            val_struct = int(vals.company_id.id)

            self.date_recus = date.today()

            self.env.cr.execute("""UPDATE budg_bordereau_mandatement_recep_dcmef_p SET et_doss ='RP', date_recep = %s  
            WHERE id = %s and x_exercice_id = %s and company_id = %s""", (self.date_recus, bord, val_ex, val_struct))

            vals.env.cr.execute(
                "select bordmand from budg_compteur_bord_mand_viser_p where x_exercice_id = %d and company_id = %d" % (
                val_ex, val_struct))
            bordmand = self.env.cr.fetchone()
            no_bord_mandat = bordmand and bordmand[0] or 0
            c1 = int(no_bord_mandat) + 1
            c = str(no_bord_mandat)
            print("la val eng", type(bordmand))
            if c == "0":
                ok = str(c1).zfill(4)
                self.no_bord_mandat = ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO budg_compteur_bord_mand_viser_p(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            else:
                c1 = int(no_bord_mandat) + 1
                c = str(no_bord_mandat)
                ok = str(c1).zfill(4)
                self.no_bord_mandat = ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE budg_compteur_bord_mand_viser_p SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))

        self.write({'et_doss': 'PC'})

        self.afficher()

    def afficher(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        id_bord = int(self.bord_recu)

        for vals in self:
            vals.env.cr.execute("""select distinct m.no_mandat as mdt, m.dt_etat as dte,m.no_lo as liq,
             m.prog_id as prog, m.section_id as sec,m.action_id as act, m.chapitre_id as chap,
             m.activite_id as activ, m.article_id as art, m.parag_id as par, m.rubrique_id as rub, 
             m.type_procedure as proc, m.type_beneficiaire_id as typeb,
             m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_liste_mandatement_recep m
             where m.liste_id = %d and m.company_id = %d and m.envoyer = True """ % (id_bord, val_struct))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.mandat_ids.unlink()

            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_lo': line['liq'], 'no_mandat': line['mdt'],
                                      'prog_id': line['prog'], 'section_id': line['sec'], 'action_id': line['act'],
                                      'chapitre_id': line['chap'],'activite_id': line['activ'], 'article_id': line['art'],
                                      'parag_id': line['par'], 'rubrique_id': line['rub'],
                                      'type_procedure': line['proc'], 'type_beneficiaire_id': line['typeb'],
                                      'no_beneficiaire': line['benef'], 'obj': line['obj'], 'mnt_ord': line['mnt']}))
            self.mandat_ids = result


class BudgListeMdtPcP(models.Model):
    _name = "budg_liste_mandatement_pc_p"

    liste_id = fields.Many2one("budg_bordereau_mandatement_controle_viser_p", ondelete='cascade')
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    type_procedure = fields.Many2one('budg_typeprocedure', string="Type de procédure", readonly=True)
    no_eng = fields.Char(string="N° engagement", readonly=True)
    no_mandat = fields.Many2one("budg_mandat", string="N° Ordonnance", readonly=True)
    no_lo = fields.Many2one("budg_liqord", string="Liquidation", readonly=True)
    mnt_ord = fields.Integer(string="Montant", readonly=True)
    dt_etat = fields.Date(default=fields.Date.context_today, string="Date Ordonnance", readonly=True)
    type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
    no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Identité", readonly=True)
    obj = fields.Text(string="Objet", readonly=True)
    etat = fields.Selection([('MR', 'Mise pour rejet'), ('R', 'Réjeté')])
    modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
    commentaire = fields.Text("Commentaire")
    piece_ids = fields.One2many("budg_liste_piece_mdt_pc_p", "mdt_id")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('N', 'Nouveau'), ('I', 'Pris en charge'), ('J', 'Rejéter')],
                             'Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    def PrendreEnCharge(self):

        mdt = int(self.no_mandat)
        val_struct = int(self.company_id)

        self.env.cr.execute("""UPDATE budg_mandat_p SET state ='I' WHERE id = %s and company_id = %s""",
                            (mdt, val_struct))

        self.write({'state': 'I'})

    def rejeter(self):

        mdt = int(self.no_mandat)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        com = self.commentaire
        mo = self.motif_rejet
        if self.motif_rejet == False:
            raise ValidationError(_("Veuillez préciser le motif de rejet d'abord !"))
        else:
            self.env.cr.execute(
                """UPDATE budg_mandat_p SET state ='J', motif_rejet = %s, commentaire = %s WHERE id = %s and company_id = %s""",
                (mo, com, mdt, val_struct))

            self.write({'state': 'J'})
            self.write({'etat': 'MR'})

    def afficher_piece(self):

        mdt = int(self.no_mandat)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute(
                "select lb_long as lib, oblige as obl, ref as re, montant as mnt, nombre as nbr from budg_piece_ord_p where mandat_id = %d" % (
                    mdt))
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.piece_ids.unlink()
            for line in rows:
                result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'ref': line['re'], 'mnt': line['mnt'],
                                      'nbr': line['nbr']}))
            self.piece_ids = result


class BudgListePieceMdtPcP(models.Model):
    _name = "budg_liste_piece_mdt_pc_p"

    mdt_id = fields.Many2one("budg_liste_mandatement_pc_p", ondelete='cascade')
    lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
    oblige = fields.Boolean("Obligatoire ?", readonly=True)
    ref = fields.Char("Référence", readonly=True)
    nbr = fields.Integer("Nombre", readonly=True)
    mnt = fields.Integer("Montant", readonly=True)


class Budg_Compteur_bord_mandPcP(models.Model):
    _name = "budg_compteur_bord_mand_pc_p"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    bordmand = fields.Integer(default=0)


class BudgCorrectionMandatP(models.Model):
    _name = "budg_correction_mandat_p"
    _rec_name = "mandat_id"

    mandat_id = fields.Many2one("budg_mandat_p", domain=['|', ('state', '=', 'R'), ('state', '=', 'J')], required=True,
                                string="N° Ordonnance")
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    mnt = fields.Float("Montant", readonly=True)
    anc_objet = fields.Text("Objet", readonly=True)
    objet = fields.Text("Objet", readonly=False)
    anc_beneficiaires = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    anc_beneficiaire = fields.Char("Id Bénéficiaire", readonly=True)
    beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
    cpte_benef = fields.Char('compte')
    imput_benef = fields.Char('imput')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('R', 'A corriger'), ('C', 'Corrigé')], default='R', string="Etat", required=True)
    etat = fields.Selection([('1', 'A mettre en bord. pour AC'), ('2', 'A mettre en bord. pour CG')], default='1',
                            string="Destinataire", required=False)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    commentaire = fields.Text("Commentaire", readonly=True)
    commentaire_daf = fields.Text("Commentaire", readonly=False)

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    piece_ids = fields.One2many("budg_piecejustificativecorrectmandat_p", "mdt_id")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    # Récuperer les elements du mandat rejeté choisi
    @api.onchange("mandat_id")
    def Valeur(self):
        for vals in self:
            if vals.mandat_id:
                self.prog_id = self.mandat_id.prog_id
                self.section_id = self.mandat_id.section_id
                self.action_id = self.mandat_id.action_id
                self.chapitre_id = self.mandat_id.chapitre_id
                self.activite_id = self.mandat_id.activite_id
                self.article_id = self.mandat_id.article_id
                self.parag_id = self.mandat_id.parag_id
                self.rubrique_id = self.mandat_id.rubrique_id
                self.mnt = self.mandat_id.mnt_ord
                self.anc_beneficiaire = self.mandat_id.no_beneficiaire
                self.anc_beneficiaires = self.mandat_id.no_beneficiaires
                self.anc_objet = self.mandat_id.obj
                self.motif_rejet = self.mandat_id.motif_rejet
                self.commentaire = self.mandat_id.commentaire

    @api.onchange('beneficiaire')
    def cpte(self):
        self.cpte_benef = self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
        self.imput_benef = self.beneficiaire.cpte_fournisseur.souscpte.id

    # Correction du mandat
    def corriger(self):
        mdt = int(self.mandat_id)
        no_ex = int(self.x_exercice_id)
        struct = int(self.company_id)
        for val in self:

            if val.motif_rejet == '1':
                raise ValidationError(
                    _("Correction impossible pour ce motif. Veuillez annuler ce mandat et son engagement lié et reprendre à nouveau le dossier."))

            elif val.motif_rejet == '2':
                raise ValidationError(
                    _("Correction impossible pour ce motif. Veuillez annuler ce mandat et son engagement lié et reprendre à nouveau le dossier."))

            elif val.motif_rejet == '3':
                mdt_id = int(self.mandat_id)
                m_id = int(self.id)
                liq = int(self.mandat_id.no_lo)
                no_eng = int(self.mandat_id.no_lo.no_eng)

                val.env.cr.execute("""select * from budg_piecejustificativecorrectmandat_p where mdt_id = %d""" % (m_id))
                for vals in val.env.cr.dictfetchall():
                    pj = vals['piecejust_id']
                    ref = vals['reference']
                    dte = vals['datepj']
                    obl = vals['active']
                    mnt = vals['montant']
                    nbre = vals['nombre']

                    self.env.cr.execute("""INSERT INTO budg_piece_ord_p(lb_long, ref, dte, oblige, montant, nombre, mandat_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre, mdt_id))

                    self.env.cr.execute("""INSERT INTO budg_piece_liq_p(lb_long, ref, dte, oblige, montant, nombre,liq_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre, liq))

                    self.env.cr.execute("""INSERT INTO budg_piece_engagement_p(lb_long, ref, dte, oblige, montant, nombre,eng_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre, no_eng))

                val.env.cr.execute(
                    """UPDATE budg_mandat_p SET state='O' WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (mdt, no_ex, struct))

                val.write({'state': 'C'})

            elif val.motif_rejet == '4':
                eng = val.mandat_id.no_eng
                liq = int(val.mandat_id.no_lo)
                benef = int(val.beneficiaire)
                benefs = val.beneficiaire.nm
                cpte = self.cpte_benef
                imput = self.imput_benef

                val.env.cr.execute(
                    """UPDATE budg_engagement_p SET no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                    (benef, cpte, imput, eng, no_ex, struct))

                val.env.cr.execute(
                    """UPDATE budg_liqord_p SET no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (benef, cpte, imput, liq, no_ex, struct))

                val.env.cr.execute(
                    """UPDATE budg_mandat_p SET state='O', no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (benef, cpte, imput, mdt, no_ex, struct))

                val.write({'state': 'C'})

            elif val.motif_rejet == '5':
                eng = val.mandat_id.no_eng
                liq = int(val.mandat_id.no_lo)
                obj = str(val.objet)

                val.env.cr.execute(
                    """UPDATE budg_engagement_p SET lb_obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
                    (obj, eng, no_ex, struct))

                val.env.cr.execute(
                    """UPDATE budg_liqord_p SET lb_obj = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (obj, liq, no_ex, struct))

                val.env.cr.execute(
                    """UPDATE budg_mandat_p SET obj = %s, state='O' WHERE id = %s and x_exercice_id = %s and company_id = %s""",
                    (obj, mdt, no_ex, struct))

                val.write({'state': 'C'})
            else:
                raise ValidationError(_("Pas de données à corriger."))


class Budg_PieceJustiCorrecP(models.Model):
    _name = "budg_piecejustificativecorrectmandat_p"

    piecejust_id = fields.Many2one('ref_piece_justificatives', string="Intitulé")
    reference = fields.Char("Références", size=35)
    datepj = fields.Date('Date')
    active = fields.Boolean("Obligé ?", default=True)
    montant = fields.Integer('Montant', size=15)
    nombre = fields.Integer("Nbre copies(s)")
    mdt_id = fields.Many2one("budg_correction_mandat_p", ondelete='cascade')


class BudgBordMdtControleRejetAcP(models.Model):
    _name = "budg_bordereau_mandatement_rejet_ac_p"
    _rec_name = "no_bord_en"
    _order = " id desc"

    name = fields.Char()
    no_bord_en = fields.Char("Bord. N°", readonly=True)
    type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de rejet d'ordonnances", readonly=True)
    cd_acteur = fields.Char(string="Acteur", readonly=True)
    date_emis = fields.Date(string="Date d'émission", readonly=True)
    date_recus = fields.Date("Date de reception", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    mandat_ids = fields.One2many("budg_detail_bord_mandat_rejet_ac_p", "bord_id", string="Liste des mandats")
    state = fields.Selection([
        ('N', 'Nouveau'), ('E', 'Envoyé à DFC '), ('R', 'Réceptionné par DFC '),
    ], 'Etat', default='N', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    signataire_4 = fields.Many2one("budg_signataire",
                                   default=lambda self: self.env['budg_signataire'].search([('code', '=', '4')]))

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def MntPre(self):

        for val in self:
            val_id = int(val.id)
            val_ex = int(val.x_exercice_id)
            val_struct = int(val.company_id)

            val.env.cr.execute("""SELECT sum(mnt_ord) FROM budg_detail_bord_mandat_rejet_ac_p e,budg_bordereau_mandatement_rejet_ac_p m
            WHERE e.envoyer_daf = 'Y' AND m.company_id = %d AND e.bord_id = %d AND e.bord_id = m.id"""
                               % (val_struct, val_id))
            res = val.env.cr.fetchone()
            resu = res and res[0] or 0
            val.totaux = resu

    @api.depends('totaux')
    def amount_to_words(self):
        self.text_amount = num2words(self.totaux, lang='fr')

    def afficher(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select b.dt_etat as dte, b.id as mdt, b.prog_id as prog, b.section_id as sec,
            b.action_id as act, b.chapitre_id as chap, b.activite_id as activ, b.article_id as art, b.parag_id as par,
            b.rubrique_id as rub, b.motif_rejet as motif_rejet, b.commentaire as commentaire,
            b.no_beneficiaire as benef, b.obj as obj, b.mnt_ord as mnt from budg_liste_mandatement_pc b 
            where b.company_id = %d and b.state = 'J' and etat = 'MR' """ % (val_struct))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.mandat_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dte'], 'no_mdt': line['mdt'], 'prog_id': line['prog'],
                                      'section_id': line['sec'], 'action_id': line['act'],
                                      'activitie_id': line['activ'],'chapitre_id': line['chap'],
                                      'article_id': line['art'], 'parag_id': line['par'],
                                      'rubrique_id': line['rub'], 'no_beneficiaire': line['benef'],
                                      'lb_obj': line['obj'], 'mnt_ord': line['mnt'], 'motif_rejet': line['motif_rejet'],
                                      'commentaire': line['commentaire']}))
            self.mandat_ids = result

    def envoyer(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.date_emis = date.today()

        self.env.cr.execute(
            "select bordeng from budg_compteur_bord_mandat_rejet_ac_p where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        bordeng = self.env.cr.fetchone()
        no_bord_en = bordeng and bordeng[0] or 0
        c1 = int(no_bord_en) + 1
        c = str(no_bord_en)
        if c == "0":
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO budg_compteur_bord_mandat_rejet_ac_p(x_exercice_id,company_id,bordeng) VALUES(%d, %d, %d)""" % (
                val_ex, val_struct, vals))
        else:
            c1 = int(no_bord_en) + 1
            c = str(no_bord_en)
            ok = str(c1).zfill(4)
            self.no_bord_en = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE budg_compteur_bord_mandat_rejet_ac_p SET bordeng = %d WHERE x_exercice_id = %d and company_id = %d" % (
                vals, val_ex, val_struct))

        self.majOrdonnance()

        self.write({'state': 'E'})

    # changer l'etat des ordonnances pour qu'elles s'affichent plus quand on veut mettre dans un bord de rejet
    def majOrdonnance(self):

        v_struct = int(self.company_id)
        print('struct', v_struct)

        self.env.cr.execute(
            """select * from budg_liste_mandatement_pc_p where etat = 'MR' and company_id = %d""" % (v_struct))
        for val in self.env.cr.dictfetchall():
            etat = val['etat']
            print('ecr', etat)
            no_mdt = val['no_mandat']
            print('lecr', no_mdt)
            self.env.cr.execute(
                """update budg_liste_mandatement_pc_p set etat ='R' where no_mandat = %d and company_id = %d""" % (
                no_mdt, v_struct))


class BudgListeMandatRejetAcP(models.Model):
    _name = 'budg_detail_bord_mandat_rejet_ac_p'

    bord_id = fields.Many2one('budg_bordereau_mandatement_rejet_ac_p', ondelete='cascade')
    dt_etat = fields.Date(string="Date", readonly=True)
    no_mdt = fields.Many2one("budg_mandat", string="N° Mandat", readonly=True)
    section_id = fields.Many2one("budg_section_p", string="Section", readonly=True)
    prog_id = fields.Many2one("budg_programme_p", string="Programme", readonly=True)
    action_id = fields.Many2one("budg_param_action_p", string="Action", readonly=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", string="Chapitre", readonly=True)
    activite_id = fields.Many2one("budg_param_activite_p", string="Activité", readonly=True)
    article_id = fields.Many2one("budg_param_article_p", string="Article")
    parag_id = fields.Many2one("budg_param_parag_p", string="Paragraphe", readonly=True)
    rubrique_id = fields.Many2one("budg_param_rub_p", string="Rubrique", readonly=True)
    no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", readonly=True)
    lb_obj = fields.Text(string="Objet", readonly=True)
    mnt_ord = fields.Float(string="Montant", readonly=True)
    dt_visa_cf = fields.Date(string="Date Visa")
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
                                    ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
                                    ('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
    commentaire = fields.Text("Commentaire")
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
    state = fields.Selection([('R', 'Rejeté')], default='R', string='Etat', readonly=True)
    envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


# Reception bordereau de rejet DCMEF /CG
class BudgBordEngRecepRejetAcP(models.Model):
    _name = "budg_bordereau_mandat_recep_rejet_ac_p"
    _rec_name = "type_bord_trsm"
    _order = " id desc"

    type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de rejet d'ordonnance", readonly=True)
    cd_acteur = fields.Char(string="Acteur", default='DFC', readonly=True)
    bord_recu = fields.Many2one("budg_bordereau_mandatement_rejet_ac_p", "Bord. reçu", required=True,
                                domain=[('state', '=', 'E')])
    date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
    date_recus = fields.Date("Date de réception", readonly=True)
    num_accuse = fields.Char()
    totaux = fields.Integer()
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    cd_acteur_accuse = fields.Char(string="Acteur", default='DFC')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    rejet_ids = fields.One2many("budg_mandat_rejeter_ac_p", "rejet_id", string="Liste des engagements",
                                ondelete="restrict")
    state = fields.Selection([('E', 'Envoyé'), ('R', 'Réceptionné'),
    ], 'Etat', default='E', required=True)
    total_prec = fields.Integer()

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    def afficher(self):

        id_bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        for vals in self:
            vals.env.cr.execute("""select * from budg_detail_bord_mandat_rejet_ac_p b
            where b.company_id = %s and b.bord_id = %s and b.state = 'R' """, (val_struct, id_bord))

            rows = vals.env.cr.dictfetchall()
            result = []

            vals.rejet_ids.unlink()
            for line in rows:
                result.append((0, 0, {'dt_etat': line['dt_etat'], 'mdt_id': line['no_mdt'],
                                      'beneficiciare': line['no_beneficiaire'], 'objet': line['lb_obj'],
                                      'commentaire': line['commentaire'], 'montant': line['mnt_ord'],
                                      'motif_rejet': line['motif_rejet']}))
            self.rejet_ids = result

    def receptionner(self):

        bord = int(self.bord_recu)
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.afficher()
        self.date_recus = date.today()

        self.env.cr.execute("""UPDATE budg_bordereau_mandatement_rejet_ac_p SET state ='R', date_recus = %s 
        WHERE id = %s and x_exercice_id = %s and company_id = %s""", (self.date_recus, bord, val_ex, val_struct))

        self.write({'state': 'R'})


class BudgMdtRejeteP(models.Model):
    _name = "budg_mandat_rejeter_ac_p"

    rejet_id = fields.Many2one("budg_bordereau_mandat_recep_rejet_ac_p", ondelte='cascade')
    dt_etat = fields.Date("Date", readonly=True)
    mdt_id = fields.Many2one("budg_mandat_p", "N° Ordonnance", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    beneficiciare = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
    montant = fields.Float("Montant", readonly=True)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'), ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'),
                                    ('4', 'Erreur Bénéficiaire'), ('5', 'Erreur Objet')], string="Motif du rejet",
                                   readonly=True)
    commentaire = fields.Text("Commentaire", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('R', 'Rejeté')], string="Etat", default="R", readonly=True)


class Budg_Compteur_bordMdtCAcP(models.Model):
	_name = "budg_compteur_bord_mandat_rejet_ac_p"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class Ordre_PaiementP(models.Model):
    _name = "budg_op_p"
    _rec_name = "no_op"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_op = fields.Char(string="OP N°", readonly=True)
    no_mandat = fields.Many2one("budg_mandat_p", string="N° Mandat")
    type_operation = fields.Many2one("budg_typeordrepaiement", string="Type de paiement", required=True)
    imput_benef = fields.Many2one("compta_plan_lines", string="Compte de tiers", required=True)
    imput_benefs = fields.Integer()
    date_emis = fields.Date(string="Date", default=fields.Date.context_today, readonly=True)
    date_etat = fields.Date()
    mnt_op = fields.Float("Montant", required=True)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                          readonly=True)
    md_reglement = fields.Many2one("ref_modereglement", string="Mode de paiement")
    lb_obj = fields.Text("Objet", size=350, required=True)
    mnt_paye = fields.Integer()
    cd_certif = fields.Many2one("budg_certification", string="Motif certification")
    type_beneficiaire = fields.Many2one("ref_categoriebeneficiaire", string="Catégorie", required=True)
    no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", required=True)
    motif_rejet = fields.Text("Motif de rejet", size=240)
    piece_ids = fields.Many2one("ref_piece_justificatives", "Pièce Justificative")
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
    et_doss = fields.Selection([
        ('draft', 'Brouillon'), ('N', 'Confirmer'), ('C', 'Certifier'), ('F', 'Payé'),
    ], 'Etat', default='draft', required=True, readonly=True, copy=False, track_visibility='always')
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

    # Controler l'exercice pour voir si ce n'est pas un exercice clos
    @api.constrains('x_exercice_id')
    def _ControleExercice(self):
        no_ex = int(self.x_exercice_id)
        v_ex = int(self.x_exercice_id.no_ex)
        for record in self:
            record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
            res = self.env.cr.fetchone()
            val = res and res[0] or 0
            if val == 0:
                raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

    @api.depends('mnt_op')
    def amount_to_words(self):
        self.text_amount = num2words(self.mnt_op, lang='fr')

    @api.onchange('imput_benef')
    def Imput(self):
        for val in self:
            val.imput_benefs = val.imput_benef.souscpte.id

    def action_op_confirmer(self):
        for vals in self:
            val_ex = int(vals.x_exercice_id.id)
            val_struct = int(vals.company_id.id)

            vals.env.cr.execute(
                "select op from budg_compteur_ordre_paiement_p where x_exercice_id = %d and company_id = %d" % (
                val_ex, val_struct))
            ope = self.env.cr.fetchone()
            no_op = ope and ope[0] or 0
            c1 = int(no_op) + 1
            c = str(no_op)
            # print("la val eng",type(ope))
            if c == "0":
                ok = str(c1).zfill(4)
                self.no_op = ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO budg_compteur_ordre_paiement_p(x_exercice_id,company_id,op)  VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            else:
                c1 = int(no_op) + 1
                c = str(no_op)
                ok = str(c1).zfill(4)
                self.no_op = ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE budg_compteur_ordre_paiement_p SET op = %d  WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))

            self.write({'et_doss': 'N'})

    def action_op_certifier(self):
        self.write({'et_doss': 'C'})


class Budg_compteur_ordre_paiementP(models.Model):
    _name = "budg_compteur_ordre_paiement_p"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    op = fields.Integer(default=0)
