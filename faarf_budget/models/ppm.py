from odoo import models, fields, api


class FaarfPpmMode(models.Model):
    _name = "faarf.ppm.mode"

    name = fields.Char("Code", required=True)
    libelle = fields.Char("Libellé", required=True)
    active = fields.Boolean("Actif", default=True)


class FaarfTypePpm(models.Model):
    _name = "faarf.type.ppm"

    name = fields.Char("Code", required=True)
    libelle = fields.Char("Libellé", required=True)
    active = fields.Boolean("Actif", default=True)


class FaarfPpmPrestation(models.Model):
    _name = "faarf.ppm.prestation"

    name = fields.Char("Libellé", required=True)
    active = fields.Boolean("Actif", default=True)


class FaarfPpmParamMode(models.Model):
    _name = "faarf.ppm.param.mode"

    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de PPM", required=True)
    type_id = fields.Selection([('F', 'Formelle'), ('NF', 'Non formelle')], string="Type")
    mnt_min = fields.Float("Montant minimum", required=True)
    mnt_max = fields.Float("Montant maximum", required=True)


class FaarfPpm(models.Model):
    _name = "faarf.ppm"

    dte = fields.Date("Date de mise en place", required=True)
    ref = fields.Char("Référence", required=True)
    type_ppm = fields.Many2one("faarf.type.ppm", "Type de PPM", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    state = fields.Selection([('draft', 'Brouillon'), ('AP', 'Avant projet'), ('P', 'Projet'),
                              ('V', 'Approuvé')], string="Etat", required=True, default='draft')
    ppm_ids = fields.One2many("faarf.ppm.line", "ppm_id")

    def name_get(self):
        result = []
        for ppm in self:
            name = 'Plan de passation de marché' + ' ' + 'du' + ' ' + str(ppm.x_exercice_id.no_ex)
            result.append((ppm.id, name))
        return result

    def approuver(self):
        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        v_id = int(self.id)

        self.env.cr.execute("""SELECT l.* FROM faarf_ppm_line l, faarf_ppm p WHERE p.x_exercice_id = %d 
        AND p.company_id = %d AND l.ppm_id = %d""" % (val_ex, val_struct, v_id))
        for line in self.env.cr.dictfetchall():
            v_ref = line['name']
            v_ppm = line['ppm_id']
            v_source = line['source_id']
            v_tit = line['cd_titre_id']
            v_sec = line['cd_section_id']
            v_chap = line['cd_chapitre_id']
            v_art = line['cd_article_id']
            v_par = line['cd_paragraphe_id']
            v_rub = line['cd_rubrique_id']
            v_est = line['montant_estime']
            v_dep = line['montant_dep_eng']
            v_disp = line['disponible']
            v_nat = line['nature']
            v_mod = line['mode_id']
            v_lanc = line['periode_lancement']
            v_rem = line['periode_remise']
            v_eval = line['temps_eval']
            v_dem = line['dte_demarre']
            v_del = line['delai_execution']
            v_stat = line['state']

            resu = self.env['faarf.ppm.line.exe'].search_count([('name', '=', v_ref), ('x_exercice_id', '=', val_ex)])
            if resu == 0:
                self.env.cr.execute("""INSERT INTO faarf_ppm_line_exe (ppm_id, name, source_id, cd_titre_id,
                cd_section_id, cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id, montant_estime, 
                montant_dep_eng, disponible, nature, mode_id, periode_lancement, periode_remise, temps_eval, 
                dte_demarre, delai_execution, state, x_exercice_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                    v_ppm, v_ref, v_source, v_tit, v_sec, v_chap, v_art, v_par, v_rub,
                    v_est, v_dep, v_disp, v_nat, v_mod, v_lanc, v_rem, v_eval, v_dem, v_del, v_stat, val_ex))

            else:
                self.env.cr.execute("""UPDATE faarf_ppm_line_exe SET source_id = %s, cd_titre_id = %s,
                cd_section_id = %s, cd_chapitre_id = %s, cd_article_id = %s, cd_paragraphe_id = %s,
                cd_rubrique_id = %s, montant_estime = %s, montant_dep_eng = %s, disponible = %s, nature = %s, 
                mode_id = %s, periode_lancement = %s, periode_remise = %s, temps_eval = %s, dte_demarre = %s, 
                delai_execution = %s, state = %s where name = %s and x_exercice_id = %s""",
                                    (v_source, v_tit, v_sec, v_chap, v_art, v_par, v_rub, v_est,
                v_dep, v_disp, v_nat, v_mod, v_lanc, v_rem, v_eval, v_dem, v_del, v_stat, v_ref, val_ex))

            self.write({'state': 'V'})

    def valider_avt_projet(self):
        self.write({'state': 'AP'})

    def valider(self):
        self.write({'state': 'P'})

class FaarfPpmLine(models.Model):
    _name = "faarf.ppm.line"

    name = fields.Char("Code", required=True)
    ppm_id = fields.Many2one("faarf.ppm", ondelete='cascade')
    source_id = fields.Many2one("faarf.source.immo", "Source",
                                default=lambda self: self.env['faarf.source.immo'].search([], limit=1), required=True)
    cd_titre_id = fields.Many2one("budg_titre", default=lambda self: self.env['budg_titre'].search([('type_titre', '=', 'D')]), string="Titre", required=True)
    cd_section_id = fields.Many2one("budg_section", string="Section", required=True)
    cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", required=True)
    cd_article_id = fields.Many2one("budg_param_article", string="Article", required=True)
    cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", required=True)
    cd_rubrique_id = fields.Many2one("budg_rubrique", string="Imputation", required=True)
    montant_estime = fields.Float("Mt estimé", required=True)
    montant_dep_eng = fields.Float("Mt Dep Eng")
    disponible = fields.Float("Crédit disponible", readonly=True)
    nature = fields.Text("Nature", required=True)
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode", required=True)
    periode_lancement = fields.Date("Lancement", required=True)
    periode_remise = fields.Date("Remise des offres", required=True)
    temps_eval = fields.Float("Tps éval.", required=True)
    dte_demarre = fields.Date("Démarrage", required=True)
    delai_execution = fields.Integer("Délai Exéc.", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('L', 'Lancé')],
                             string="Etat", readonly=True, default='N')
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")

    _sql_constraints = [('name_ppm_uniq', 'unique (name,ppm_id)',
                         'Vous ne pouvez pas avoir une même référence dans le meme PPM !')]

    @api.onchange("montant_estime")
    def dispo(self):
        for val in self:
            val.disponible = val.montant_estime


class FaarfPpmLineExe(models.Model):
    _name = "faarf.ppm.line.exe"

    ppm_id = fields.Many2one("faarf.ppm", ondelete='cascade')
    name = fields.Char("Référence", readonly=True)
    source_id = fields.Many2one("faarf.source.immo", "Source de financement", required=True)
    cd_titre_id = fields.Many2one("budg_titre", string="Titre", required=True)
    cd_section_id = fields.Many2one("budg_section", string="Section", required=True)
    cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", required=True)
    cd_article_id = fields.Many2one("budg_param_article", string="Article", required=True)
    cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", required=True)
    cd_rubrique_id = fields.Many2one("budg_rubrique", string="Imputation", required=True)
    montant_estime = fields.Float("Montant estimé", required=True)
    montant_dep_eng = fields.Float("Montant Dep Eng")
    disponible = fields.Float("Crédit disponible")
    nature = fields.Text("Nature prestation", required=True)
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", required=True)
    periode_lancement = fields.Date("Période de lancement", required=True)
    periode_remise = fields.Date("Période de remise des offres", required=True)
    temps_eval = fields.Float("Temps évaluation", required=True)
    dte_demarre = fields.Date("Date démarrage", required=True)
    delai_execution = fields.Integer("Délai prévisonnel", required=True)
    dte_fin = fields.Date("Date fin", required=False)
    state = fields.Selection([('N', 'Nouveau'), ('L', 'Lancé'), ('A', 'Attribué')],
                             string="Etat", readonly=True, default='N')
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")


class FaarfPpmMarche(models.Model):
    _name = "faarf.ppm.marche"

    dte = fields.Date(default=fields.Date.context_today, string="Date", required=True)
    name = fields.Many2one("faarf.ppm.line.exe", "Code ligne", required=True,
                           domain=[('state', '=', 'N'), ('x_exercice_id.etat', '=', 1)])
    reference = fields.Char("Référence", readonly=True)
    type_prestation = fields.Many2one("faarf.ppm.prestation", required=True)
    source_id = fields.Many2one("faarf.source.immo", string="Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    periode_lancement = fields.Date("Période de lancement", related='name.periode_lancement')
    periode_remise = fields.Date("Période de remise des offres", required=True, related='name.periode_remise')
    dte_demarre = fields.Date("Date démarrage", related='name.dte_demarre')
    delai_execution = fields.Integer("Délai prévisonnel", related='name.delai_execution')
    montant_estime = fields.Float("Montant estimé", related='name.montant_estime')
    state = fields.Selection([('N', 'Nouveau'), ('L', 'Marché lancé'), ('A', 'Marché attribué'),
                              ('V', 'Visa CG'), ('W', 'Visa Ord.')],
                             string="Etat", readonly=True, default='N')

    @api.onchange('name')
    def valsource(self):
        for val in self:
            val.source_id = val.name.source_id

    def valider(self):
        v_id = int(self.name)
        self.env.cr.execute("update faarf_ppm_line_exe set state ='L' where id = %d" % v_id)
        self.state = 'L'


class FaarfPpmSoumissionnaire(models.Model):
    _name = "faarf.ppm.soumissionnaire"
    _order = "numero asc"

    name = fields.Many2one("faarf.ppm.line.exe", "Référence", required=True,
                           domain=[('state', '=', 'L'), ('x_exercice_id.etat', '=', 1)])
    source_id = fields.Many2one("faarf.source.immo", "Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    fournisseur_id = fields.Many2one("ref_beneficiaire", "Fournisseur", required=True)
    telephone = fields.Char("Téléphone", related='fournisseur_id.tel')
    ifu = fields.Char("N° IFU", related='fournisseur_id.no_ifu')
    dte_recep = fields.Datetime("Date et heure de réception", required=True)
    numero = fields.Char("N°Ordre", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validé')], string="Etat", default='N')
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")

    def valider(self):
        v_ex = int(self.x_exercice_id)
        v_ref = int(self.name)
        self.env.cr.execute(
            "select nosoum from compteur_soum where x_exercice_id = %d and refe = %d" % (v_ex, v_ref))
        eng = self.env.cr.fetchone()
        no_eng = eng and eng[0] or 0
        c1 = int(no_eng) + 1
        c = str(no_eng)
        if c == "0":
            ok = str(c1).zfill(3)
            self.numero = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO compteur_soum(x_exercice_id,refe,nosoum)  VALUES(%d ,%d, %d)""" % (
                v_ex, v_ref, vals))
            self.state = 'V'
        else:
            c1 = int(no_eng) + 1
            ok = str(c1).zfill(3)
            self.numero = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE compteur_soum SET nosoum = %d WHERE x_exercice_id = %d and refe = %d" % (
                vals, v_ex, v_ref))

            self.state = 'V'

    @api.onchange('name')
    def valsource(self):
        for val in self:
            val.source_id = val.name.source_id

class CompteurSoum(models.Model):
    _name = "compteur.soum"

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]), string="Exercice")
    refe = fields.Many2one('faarf.ppm.line.exe')
    nosoum = fields.Integer(default=0)

class FaarfPpmSoumissionnaireRetenu(models.Model):
    _name = "faarf.ppm.soumissionnaire.retenue"

    name = fields.Many2one("faarf.ppm.line.exe", "Référence", required=True,
                           domain=[('state', '=', 'L'), ('x_exercice_id.etat', '=', 1)])
    source_id = fields.Many2one("faarf.source.immo", "Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    retenu_ids = fields.One2many("faarf.ppm.soumissionnaire.retenue.line", "soum_id")
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validé')], string="Etat", default='N')

    def valider(self):
        self.state = 'V'

    def afficher(self):
        for val in self:
            resu = self.env['faarf.ppm.soumissionnaire'].search([('name', '=', val.name.id), ('state', '=', 'V')])
            for x in resu:

                self.env['faarf.ppm.soumissionnaire.retenue.line'].create({
                    'fournisseur_id': x.fournisseur_id.id,
                    'telephone': x.telephone,
                    'ifu': x.ifu,
                    'marche': self.name.id,
                    'soum_id': self.id,
                })

    @api.onchange('name')
    def valsource(self):
        for val in self:
            val.source_id = val.name.source_id


class FaarfPpmSoumissionnaireRetenuLine(models.Model):
    _name = "faarf.ppm.soumissionnaire.retenue.line"
    _rec_name = "fournisseur_id"

    soum_id = fields.Many2one("faarf.ppm.soumissionnaire.retenue", ondelete='cascade')
    fournisseur_id = fields.Many2one("ref_beneficiaire", "Fournisseur", readonly=True)
    telephone = fields.Char("Téléphone", readonly=True)
    ifu = fields.Char("N° IFU", readonly=True)
    state = fields.Selection([('R', 'Retenu'), ('NR', 'Non Retenu')], string='Résultat', required=False)
    marche = fields.Many2one("faarf.ppm.line.exe", "Référence")


class FaarfPpmMarcheSoumissionnaireRetenu(models.Model):
    _name = "faarf.ppm.marche.soumissionnaire.retenue"

    name = fields.Many2one("faarf.ppm.line.exe", "Référence", required=True,
                           domain=[('state', '=', 'L'), ('x_exercice_id.etat', '=', 1)])
    source_id = fields.Many2one("faarf.source.immo", string="Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    soumissionnaire_id = fields.Many2one("faarf.ppm.soumissionnaire.retenue.line",
                                         string='Fournisseur',  required=True)
    telephone = fields.Char("Téléphone", related='soumissionnaire_id.telephone')
    ifu = fields.Char("N° IFU", related='soumissionnaire_id.ifu')
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validé'), ('C', 'Contrat établi')],
                             string="Etat", default='N')
    montant = fields.Float("Montant", required=True)
    reference = fields.Text("Références de la procédure de passation")

    def valider(self):
        v_id = int(self.name)
        self.state = 'V'
        self.env.cr.execute("update faarf_ppm_line_exe set state = 'A' where id = %d" % v_id)

    @api.onchange('name')
    def valsource(self):
        for val in self:
            val.source_id = val.name.source_id


class FaarfPpmApproCg(models.Model):
    _name = "faarf.ppm.appro.cg"

    dte = fields.Date(default=fields.Date.context_today, string="Date", required=True)
    name = fields.Many2one("faarf.ppm.contrat", "Référence", required=True,
                           domain=[('state', '=', 'N')])
    source_id = fields.Many2one("faarf.source.immo", string="Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    soumissionnaire_id = fields.Many2one("faarf.ppm.soumissionnaire.retenue.line",
                                         string='Fournisseur', readonly=True)
    telephone = fields.Char("Téléphone", readonly=True)
    ifu = fields.Char("N° IFU", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Visé'), ('R', 'Réjété')], string="Etat", default='N')
    obs = fields.Text("Observation")

    def valider(self):
        v_id = int(self.name)
        self.state = 'V'
        self.env.cr.execute("update faarf_ppm_contrat set state = 'V' where id = %d" % v_id)

    def rejeter(self):
        self.state = 'R'

    @api.onchange('name')
    def valsource(self):
        for val in self:
            v_id = int(val.name)
            resu = self.env['faarf.ppm.marche.soumissionnaire.retenue'].search([('name.id', '=', v_id)])
            val.soumissionnaire_id = resu.soumissionnaire_id.id
            val.telephone = resu.telephone
            val.ifu = resu.ifu

            val.source_id = val.name.source_id


class FaarfPpmApproOrd(models.Model):
    _name = "faarf.ppm.appro.ord"

    dte = fields.Date(default=fields.Date.context_today, string="Date approbation", required=True)
    name = fields.Many2one("faarf.ppm.contrat", "Référence", required=True,
                           domain=[('state', '=', 'V')])
    source_id = fields.Many2one("faarf.source.immo", string="Source de financement", readonly=True)
    nature = fields.Text("Nature prestation", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    soumissionnaire_id = fields.Many2one("faarf.ppm.soumissionnaire.retenue.line",
                                         readonly=True, string='Fournisseur')
    telephone = fields.Char("Téléphone", readonly=True)
    ifu = fields.Char("N° IFU", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Approuvé')], string="Etat", default='N')

    def valider(self):
        v_id = int(self.name)
        self.state = 'V'
        self.env.cr.execute("update faarf_ppm_contrat set state = 'W' where id = %d" % v_id)

    @api.onchange('name')
    def valsource(self):
        for val in self:
            v_id = int(val.name)
            resu = self.env['faarf.ppm.marche.soumissionnaire.retenue'].search([('name.id', '=', v_id)])
            val.soumissionnaire_id = resu.soumissionnaire_id.id
            val.telephone = resu.telephone
            val.ifu = resu.ifu
            val.source_id = val.name.source_id



class FaarfPpmExecution(models.Model):
    _name = "faarf.ppm.execution"

    dte_deb = fields.Date("Date debut", required=True)
    dte_fin = fields.Date("Date fin", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    ppm_ids = fields.One2many("faarf.ppm.execution.line", "execution_id")

    def chercher(self):
        v_id = int(self.name)


class FaarfPpmExecutionLine(models.Model):
    _name = "faarf.ppm.execution.line"

    execution_id = fields.Many2one("faarf.ppm.execution", ondelete='cascade')
    numero = fields.Char("N°")
    immatriculation = fields.Char("Immatriculation")
    dte_appro = fields.Date("Date approbation")
    reference = fields.Text("Reference")
    nature = fields.Text("Nature")
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", required=True)
    type_prestation = fields.Many2one("faarf.type.prestation", "Type de prestation")
    source_id = fields.Many2one("faarf.source.immo", "Source")
    soummissionnaire = fields.Many2one("faarf.ppm.soumissionnaire.retenue.line", "Nom du titulaire")
    ifu = fields.Char("N° IFU")
    montant = fields.Float("Montant")
    state = fields.Selection([('N', 'En cours'), ('V', 'Marché exécuté, réceptionné et en cours de paiement'),
                              ('W', 'Marché exécuté, réceptionné et payé'), ('A', 'Annulé')], string="Etat d'exécution")


class FaarfPpmContrat(models.Model):
    _name = "faarf.ppm.contrat"

    numero = fields.Char("Code contrat", readonly=True)
    objet = fields.Text("Objet", default="Passé suivant Autorisation", required=True)
    name = fields.Many2one("faarf.ppm.marche.soumissionnaire.retenue", "Référence", required=True,
                           domain=[('state', '=', 'V')])
    source_id = fields.Many2one("faarf.source.immo", string="Financement", readonly=True)
    nature = fields.Text("Objet", related='name.nature')
    mode_id = fields.Many2one("faarf.ppm.mode", "Mode de passation", related='name.mode_id')
    soumissionnaire_id = fields.Many2one("faarf.ppm.soumissionnaire.retenue.line",
                                         related='name.soumissionnaire_id', string='Titulaire', required=True)
    telephone = fields.Char("Téléphone", related='name.telephone')
    ifu = fields.Char("N° IFU", related='name.ifu')
    montant = fields.Float("Montant", related='name.montant')
    dte_appro = fields.Date("Date d'approbation")
    dte_notification = fields.Date("Date de notification")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    state = fields.Selection([('draft', 'Brouillon'), ('N', 'Nouveau'),
                              ('V', 'Visé CG'), ('W', 'Approuvé Ord.')], string="Etat", default='draft')

    def valider(self):
        v_id = int(self.name)
        self.env.cr.execute("""update faarf_ppm_marche_soumissionnaire_retenue 
        set state = 'C' where id = %d""" % v_id)
        self.state = 'N'
