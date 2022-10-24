from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import date


class BudgSectionP(models.Model):

    _name = "budg_section_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgProgrammeP(models.Model):
    _name = "budg_programme_p"

    code = fields.Char(string="Code", size=3, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgActionP(models.Model):
    _name = "budg_action_p"

    code = fields.Char(string="Code", size=5, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgActiviteP(models.Model):
    _name = "budg_activite_p"

    code = fields.Char(string="Code", size=8, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgChapitreP(models.Model):
    _name = "budg_chapitre_p"

    code = fields.Char(string="Code", size=10, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgArticleP(models.Model):
    _name = "budg_article_p"

    code = fields.Char(string="Code", size=7, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgParagrapheP(models.Model):
    _name = "budg_paragraphe_p"

    code = fields.Char(string="Code", size=7, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgRubriqueP(models.Model):
    _name = "budg_rubrique_p"

    code = fields.Char(string="Code", size=7, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgParamActionP(models.Model):
    _name = "budg_param_action_p"
    _rec_name = "action_id"

    prog_id = fields.Many2one("budg_programme_p", "Programme", required=True)
    action_id = fields.Many2one("budg_action_p", "Action", required=True)


class BudgParamActiviteP(models.Model):
    _name = "budg_param_activite_p"
    _rec_name = "activite_id"

    prog_id = fields.Many2one("budg_programme_p", "Programme", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_activite_p", "Activité", required=True)


class BudgParamArticleP(models.Model):
    _name = "budg_param_article_p"
    _rec_name = "article_id"

    prog_id = fields.Many2one("budg_programme_p", "Programme", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_param_activite_p", "Activité", required=True)
    article_id = fields.Many2one("budg_article_p", "Article", required=True)


class BudgParamParagP(models.Model):
    _name = "budg_param_parag_p"
    _rec_name = "parag_id"

    prog_id = fields.Many2one("budg_programme_p", "Programme", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_param_activite_p", "Activité", required=True)
    article_id = fields.Many2one("budg_param_article_p", "Article", required=True)
    parag_id = fields.Many2one("budg_paragraphe_p", "Paragraphe", required=True)


class BudgParamRubP(models.Model):
    _name = "budg_param_rub_p"
    _rec_name = "rub_id"

    section_id = fields.Many2one("budg_section_p", "Programme", required=True)
    prog_id = fields.Many2one("budg_programme_p", "Programme", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_param_activite_p", "Activité", required=True)
    article_id = fields.Many2one("budg_param_article_p", "Article", required=True)
    parag_id = fields.Many2one("budg_param_parag_p", "Paragraphe", required=True)
    rub_id = fields.Many2one("budg_rubrique_p", "Rubrique", required=True)
    cpte_id = fields.Many2one("compta_plan_lines", "Compte", required=True)


"""pour les recettes"""


class BudgTitreRecP(models.Model):
    _name = "budg_titre_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgSectionRecP(models.Model):
    _name = "budg_section_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgChapitreRecP(models.Model):
    _name = "budg_chapitre_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgArticleRecP(models.Model):
    _name = "budg_article_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé long", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


class BudgParagrapheRecP(models.Model):
    _name = "budg_paragraphe_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)

class BudgRubriqueRecP(models.Model):
    _name = "budg_rubrique_rec_p"

    code = fields.Char(string="Code", size=2, required=True)
    name = fields.Char(string="Libellé long", size=100, required=True)
    lb_court = fields.Char(string="Libellé court", size=35, required=False)
    active = fields.Boolean('Actif', default=True)


"""Paramatrage nomenclature budget programme coté recette"""


class BudgParamSectionRecP(models.Model):
    _name = "budg_param_section_rec_p"
    _rec_name = "section_id"

    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_section_rec_p", "Section", required=True)


class BudgParamChapitreRecP(models.Model):
    _name = "budg_param_chapitre_rec_p"
    _rec_name = "chapitre_id"

    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_chapitre_rec_p", "Chapitre", required=True)


class BudgParamArticleRecP(models.Model):
    _name = "budg_param_article_rec_p"
    _rec_name = "article_id"

    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_param_chapitre_rec_p", "Chapitre", required=True)
    article_id = fields.Many2one("budg_article_rec_p", "Article", required=True)


class BudgParamParagrapheRecP(models.Model):
    _name = "budg_param_paragraphe_rec_p"
    _rec_name = "paragraphe_id"

    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_param_chapitre_rec_p", "Chapitre", required=True)
    article_id = fields.Many2one("budg_param_article_rec_p", "Article", required=True)
    paragraphe_id = fields.Many2one("budg_paragraphe_rec_p", "Paragraphe", required=True)


class BudgParamRubriqueRecP(models.Model):
    _name = "budg_param_rubrique_rec_p"
    _rec_name = "rub_id"

    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_param_chapitre_rec_p", "Chapitre", required=True)
    article_id = fields.Many2one("budg_param_article_rec_p", "Article", required=True)
    paragraphe_id = fields.Many2one("budg_paragraphe_rec_p", "Paragraphe", required=True)
    rub_id = fields.Many2one("budg_rubrique_rec_p", "Rubrique", required=True)
    cpte_id = fields.Many2one("compta_plan_lines", "Compte", required=True)


"""Budget programme dépense"""


class BudgBudgetDepP(models.Model):

    _name = "budg_budget_dep_p"
    _rec_name = "refp"

    typebudget_id = fields.Many2one("budg_typebudget", string="Type de Budget", required=True)
    cd_type_piece_budget = fields.Many2one("budg_typepiecebudget", string="Type de Pièce", required=True)
    refp = fields.Char(string="Ref.Piece", required=True)
    date_to = fields.Date(string="Date de mise en place", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    fichier_joint = fields.Binary(string="Joindre l'acte", attachment=True)
    rubrique_ids = fields.One2many("budg_ligne_budgetaire_dep_p", "budg_id", states={'E': [('readonly', True)]})
    state = fields.Selection([('AP', 'Avant projet'), ('N', 'Projet'), ('E', 'Exécutoire')],
                             'Etat', default='AP', required=True, readonly=True)
    date_execution = fields.Date("Date exécution")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    # @api.onchange('typebudget_id')
    # def controle_type_budget(self):
    #     val_ex = int(self.x_exercice_id)
    #     val_struct = int(self.company_id)
    #
    #     self.env.cr.execute(
    #         """select count(b.id) FROM budg_budget_dep_p b, budg_typebudget t, ref_exercice r
    #         WHERE b.x_exercice_id = %d AND
    #         b.company_id = %d and t.id = b.typebudget_id AND t.cd_type_budget = 'BI' """ % (val_ex, val_struct))
    #     res = self.env.cr.fetchone()
    #     val = res and res[0]
    #     if val > 0 and self.typebudget_id.cd_type_budget == 'BI':
    #         raise ValidationError(
    #             _('Le budget initial' + " " + str(self.x_exercice_id.no_ex) + " " + 'est déjà saisi.'))

    def valider_avt_projet(self):
        self.write({'state': 'N'})

    def budget_valider(self):
        self.date_execution = date.today()
        self.validation_budget()
        self.write({'state': 'E'})

    # fonction de validation et réaménagement budgetaire
    def validation_budget(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_budg = int(self.id)

        # recuperation des données des dépenses
        self.env.cr.execute("""SELECT  l.section_id, l.prog_id, l.chap_id, l.action_id, l.activite_id, 
        l.article_id, l.parag_id, l.rub_id, l.source_id,
        coalesce((l.montant),0) as mnts_budgetise FROM budg_ligne_budgetaire_dep_p l, budg_budget_dep_p b 
        WHERE b.x_exercice_id = %d AND b.company_id = %d 
        and l.budg_id = %d and b.id = l.budg_id""" % (val_ex, val_struct, val_budg))
        for line in self.env.cr.dictfetchall():

            v_sec = line['section_id']
            v_prog = line['prog_id']
            v_chap = line['chap_id']
            v_act = line['action_id']
            v_activ = line['activite_id']
            v_art = line['article_id']
            v_parag = line['parag_id']
            v_rub = line['rub_id']
            v_source = line['source_id']
            montant = line['montant']

            # curseur pour compter le nombre de ligne de depense dans la ligne executoire des dépenses
            self.env.cr.execute("""SELECT coalesce(count(*),0) FROM budg_ligne_exe_dep_p 
            WHERE section_id = %s AND prog_id = %s AND chap_id = %s AND action_id = %s AND activite_id = %s
            article_id = %s AND parag_id = %s AND rub_id = %s AND x_exercice_id = %s AND company_id = %s """,
                                (v_sec, v_prog, v_chap, v_act, v_activ, v_art, v_parag, v_rub, val_ex, val_struct))

            curs_verif_depense = self.env.cr.fetchone()[0] or 0
            # curs_verif_depense = curs_verif_dep and curs_verif_dep[0]
            print('nombre ligne de depense', curs_verif_depense)

            if curs_verif_depense == 0:
                self.env.cr.execute("""INSERT INTO budg_ligne_exe_dep_p 
                (section_id, prog_id, chap_id, action_id, activite_id,article_id,
                parag_id, rub_id, mnt_budgetise,mnt_corrige, mnt_disponible, 
                reste_mandat, company_id, x_exercice_id, budg_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                    (v_sec, v_prog, v_chap, v_act, v_activ, v_art, v_parag,
                                     v_rub, montant, montant, montant, montant, val_struct, val_ex, val_budg))
            else:
                self.env.cr.execute("""UPDATE budg_ligne_exe_dep_p SET mnt_corrige = coalesce((mnt_corrige),0) + %s, 
                mnt_disponible = coalesce((mnt_disponible),0) + %s, reste_mandat = coalesce((reste_mandat),0) + %s
                WHERE section_id = %s AND prog_id = %s AND chap_id = %s AND action_id = %s AND activite_id = %s
                AND article_id = %s AND parag_id = %s AND rub_id = %s AND source_id = %s 
                AND x_exercice_id = %s AND company_id = %s """, (montant, montant, montant, v_sec,
                                                                 v_prog, v_chap, v_act, v_activ, v_art,
                                                                 v_parag, v_rub, v_source, val_ex, val_struct))

    def afficher_rubrique(self):

        for vals in self:
            vals.env.cr.execute("""select prog_id as prog, action_id as act, activite_id as activ,
             article_id as art, parag_id as par, id as rub from budg_param_rub_p 
             order by pro, act, activ, par, art, id""")
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.rubrique_ids.unlink()
            for line in rows:
                result.append((0, 0,
                               {'section_id': line['sec'], 'prog_id': line['pro'], 'chap_id': line['chap'],
                                'action_id': line['act'], 'activite_id': line['activ'], 'article_id': line['art'],
                                'parag_id': line['par'], 'rub_id': line['rub']}))
            self.rubrique_ids = result


class BudgBudgetaireLineDepP(models.Model):
    _name = "budg_ligne_budgetaire_dep_p"

    budg_id = fields.Many2one("budg_budget_dep_p", ondelete='cascade')
    section_id = fields.Many2one("budg_section_p", "Section", required=True)
    prog_id = fields.Many2one("budg_param_action_p", "Programme", required=True)
    chap_id = fields.Many2one("budg_chapitre_p", "Chapitre", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_param_activite_p", "Activité", required=True)
    article_id = fields.Many2one("budg_param_article_p", "Article", required=True)
    parag_id = fields.Many2one("budg_param_parag_p", "Paragraphe", required=True)
    rub_id = fields.Many2one("budg_param_rub_p", "Rubrique", required=True)
    source_id = fields.Many2one("faarf.source.immo", "Source de financement", required=False)
    montant = fields.Float("Montant", required=True)


class BudgBudgetRecP(models.Model):
    _name = "budg_budget_rec_p"
    _rec_name = "refp"

    typebudget_id = fields.Many2one("budg_typebudget", string="Type de Budget", required=True)
    cd_type_piece_budget = fields.Many2one("budg_typepiecebudget", string="Type de Pièce", required=True)
    refp = fields.Char(string="Ref.Piece", required=True)
    date_to = fields.Date(string="Date de mise en place", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    fichier_joint = fields.Binary(string="Joindre l'acte", attachment=True)
    rubrique_ids = fields.One2many("budg_ligne_budgetaire_rec_p", "budg_id", states={'E': [('readonly', True)]})
    state = fields.Selection([('AP', 'Avant projet'), ('N', 'Projet'), ('E', 'Exécutoire')],
                             'Etat', default='AP', required=True, readonly=True)
    date_execution = fields.Date("Date exécution")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    def valider_avt_projet(self):
        self.write({'state': 'N'})

    def budget_valider(self):
        self.date_execution = date.today()
        self.validation_budget()
        self.write({'state': 'E'})

    # fonction de validation et réaménagement budgetaire
    def validation_budget(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_budg = int(self.id)

        # recuperation des données des dépenses
        self.env.cr.execute("""SELECT l.titre_id, l.section_id, l.chapitre_id, l.article_id, 
        l.parag_id
        coalesce((l.montant),0) as mnts_budgetise FROM budg_ligne_budgetaire_rec_p l, budg_budget_rec_p b 
        WHERE b.x_exercice_id = %d AND b.company_id = %d 
        and l.budg_id = %d and b.id = l.budg_id""" % (val_ex, val_struct, val_budg))
        for line in self.env.cr.dictfetchall():
            v_titre = line['titre_id']
            v_sec = line['section_id']
            v_chap = line['chap_id']
            v_art = line['article_id']
            v_parag = line['parag_id']
            v_rub = line['rub_id']
            montant = line['montant']

            # curseur pour compter le nombre de ligne de depense dans la ligne executoire des recettes
            self.env.cr.execute("""SELECT coalesce(count(*),0) FROM budg_ligne_exe_rec_p 
            WHERE titre_id = %s AND section_id = %s AND chapitre_id = %s AND 
            article_id = %s AND parag_id = %s AND rub_id = %s AND x_exercice_id = %s AND company_id = %s """,
                                (v_titre, v_sec, v_chap, v_art, v_parag, val_ex, val_struct))

            curs_verif_depense = self.env.cr.fetchone()[0] or 0
            # curs_verif_depense = curs_verif_dep and curs_verif_dep[0]
            print('nombre ligne de depense', curs_verif_depense)

            if curs_verif_depense == 0:
                self.env.cr.execute("""INSERT INTO budg_ligne_exe_rec_p 
                (titre_id, section_id, chapitre_id, article_id, parag_id, rub_id, 
                mnt_budgetise,mnt_corrige, reste_a_recouvrer, company_id, x_exercice_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                    (v_titre, v_sec, v_chap, v_art, v_parag,
                                     v_rub, montant, montant, montant, val_struct, val_ex))
            else:
                self.env.cr.execute("""UPDATE budg_ligne_exe_rec_p SET mnt_corrige = coalesce((mnt_corrige),0) + %s, 
                reste_a_recouvrer = coalesce((reste_a_recouvrer),0) + %s
                WHERE titre_id = %s AND section_id = %s AND chapitre_id = %s AND article_id = %s AND parag_id = %s 
                AND rub_id = %s AND x_exercice_id = %s AND company_id = %s """, (montant, montant, v_titre, v_sec,
                v_chap, v_art, v_parag, v_rub, val_ex, val_struct))

    def afficher_rubrique(self):

        for vals in self:
            vals.env.cr.execute("""select titre_id as tit, section_id as sec, chapitre_id as chap,
            article_id as art, parag_id as par, id as rub from budg_param_rub_rec_p 
            order by tit, sec, chap, art, par, id""")
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.rubrique_ids.unlink()
            for line in rows:
                result.append((0, 0,
                               {'section_id': line['sec'], 'titre_id': line['tit'], 'chapitre_id': line['chap'],
                                'article_id': line['art'], 'parag_id': line['par'], 'rub_id': line['rub']}))
            self.rubrique_ids = result


class BudgBudgetRecLineP(models.Model):
    _name = "budg_ligne_budgetaire_rec_p"

    budg_id = fields.Many2one("budg_budget_rec_p", ondelete='cascade')
    titre_id = fields.Many2one("budg_titre_rec_p", "Titre", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_param_chapitre_rec_p", "Chapitre", required=True)
    article_id = fields.Many2one("budg_param_article_rec_p", "Article", required=True)
    parag_id = fields.Many2one("budg_param_paragraphe_rec_p", "Paragraphe", required=True)
    rub_id = fields.Many2one("budg_param_rub_rec_p", "Rubrique", required=True)
    montant = fields.Float("Montant", required=True)


class BudgBudgetDepExeLineP(models.Model):

    _name = "budg_ligne_exe_dep_p"
    section_id = fields.Many2one("budg_section_p", "Section", required=True)
    prog_id = fields.Many2one("budg_param_action_p", "Programme", required=True)
    chapitre_id = fields.Many2one("budg_chapitre_p", "Chapitre", required=True)
    action_id = fields.Many2one("budg_param_action_p", "Action", required=True)
    activite_id = fields.Many2one("budg_param_activite_p", "Activité", required=True)
    article_id = fields.Many2one("budg_param_article_p", "Article", required=True)
    parag_id = fields.Many2one("budg_param_parag_p", "Paragraphe", required=True)
    rub_id = fields.Many2one("budg_param_rub_p", "Rubrique", required=True)
    source_id = fields.Many2one("faarf.source.immo", "Source de financement", required=True)
    mnt_budgetise = fields.Float("Dotation initiale", required=True)
    mnt_corrige = fields.Float("Dotation Corrige", required=True)
    mnt_disponible = fields.Float("Credit Dispo", required=True)
    mnt_engage = fields.Float("Montant Eng", required=True)
    reste_mandat = fields.Float("Reste Mdt", required=True)
    company_id = fields.Many2one('res.company', string="Structure")
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")


class BudgBudgetRecExeLineP(models.Model):

    _name = "budg_ligne_exe_rec_p"
    titre_id = fields.Many2one("budg_section_p", "budg_budget_dep_p", required=True)
    section_id = fields.Many2one("budg_param_section_rec_p", "Section", required=True)
    chapitre_id = fields.Many2one("budg_param_chapitre_rec_p", "Chapitre", required=True)
    article_id = fields.Many2one("budg_param_article_rec_p", "Activité", required=True)
    parag_id = fields.Many2one("budg_param_paragraphe_rec_p", "Paragraphe", required=True)
    #rub_id = fields.Many2one("budg_param_rub_p", "Rubrique", required=True)
    mnt_budgetise = fields.Float("Dotation initiale", required=True)
    mnt_corrige = fields.Float("Dotation Corrige", required=True)
    mnt_emis = fields.Float("Montant emis", required=True)
    reste_a_recouvrer = fields.Float("Reste a recouvrer", required=True)
    company_id = fields.Many2one('res.company', string="Structure")
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
