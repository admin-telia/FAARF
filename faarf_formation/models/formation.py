from odoo import fields, models, api


class FaarfProgPrev(models.Model):
    _name = "faarf.prog.prev"

    name = fields.Char(string="Libellé",
                       default="Programme prévisonnel de formation de la clientèle", required=True)
    dte = fields.Date("Date", default=fields.Date.context_today, required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('V', 'Validé')],
                             string="Etat", required=True, default='draft')
    nbre_formation = fields.Integer("Nbre de formations")
    line_ids = fields.One2many("faarf.prog.prev.line", "prog_id")
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")

    def valider(self):
        self.state = 'V'

    @api.constrains('line_ids')
    def _nbre_formation(self):
        for val in self:
            val.nbre_formation = len(val.line_ids)


class FaarfProgPrevLine(models.Model):
    _name = "faarf.prog.prev.line"
    _rec_name = "num_ordre"

    prog_id = fields.Many2one("faarf.prog.prev", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", required=True, size=3)
    date_begin = fields.Date("Date de début", required=True)
    date_end = fields.Date("Date de fin", required=True)
    date_begin_reel = fields.Date("Date de début réelle", required=False)
    date_end_reel = fields.Date("Date de fin réelle", required=False)
    module_id = fields.Many2one("faarf.module", string="Module", required=True)
    nbre = fields.Integer("Nbre de bénéficiaires", required=True)
    region_id = fields.Many2one("ref_region", "Région", required=True)
    province_id = fields.Many2one("ref_province", "Province", required=True)
    province_agent_id1 = fields.Many2one("ref_province", string="Prov. A1", required=False)
    province_agent_id2 = fields.Many2one("ref_province", string="Prov. A2", required=False)
    lieu = fields.Many2one("ref_departement", "Lieu", required=True)
    montant = fields.Float("Total", compute="_montant")
    animatrice_id = fields.Many2one("res.users", string="1ère Animatrice", required=True)
    animatrice_id2 = fields.Many2one("res.users", string="2nde Animatrice",
                                    domain=[('x_user_role_id.code', '=', 'ROLEGEST')])
    superviseur_id = fields.Many2one("res.users", string="Superviseur")

    state = fields.Selection([('P', 'Non budgétisée'), ('B', 'Budgétisée'), ('E', 'Exécutée')],
                             string="Etat", required=True, default='P')
    cout_ids = fields.One2many("faarf.cout.prev", "prog_id")

    def name_get(self):
        result = []
        for formation in self:
            name = 'Formation N°' + ' ' + formation.num_ordre + ' ' + 'du' + ' ' + str(formation.date_begin) + ' ' + 'au' + ' ' + str(formation.date_end) + '/' + formation.region_id.name + '/' + formation.province_id.name + '/' + formation.lieu.name
            result.append((formation.id, name))
        return result

    def valider(self):
        self.state = 'B'

    @api.depends("cout_ids.prix_total")
    def _montant(self):
        self.montant = sum(ligne.prix_total for ligne in self.cout_ids)

    @api.onchange("region_id")
    def supval(self):
        reg = int(self.region_id)
        for val in self:
            self.env.cr.execute("""select distinct u.id from res_users u, ref_user_role rr, ref_region_res_users_rel ru
            where u.id = ru.res_users_id and rr.id = u.x_user_role_id and rr.code = 'ROLESUP' 
            and ru.ref_region_id = %d""" % reg)

            resu = val.env.cr.fetchone()
            val.superviseur_id = resu and resu[0] or 0



class FaarfCoutPrevisionnel(models.Model):
    _name = "faarf.cout.prev"

    prog_id = fields.Many2one("faarf.prog.prev.line", "Session de :", ondelete='cascade')
    element_id = fields.Many2one("faarf.element.budget", "Libellé", required=True)
    prix_unit = fields.Float("Prix unitare", required=True)
    nbre = fields.Float("Nombre", default=1, required=True)
    prix_total = fields.Float("Total", readonly=True)

    _sql_constraints = [('prog_element_uniq', 'unique (prog_id,element_id)',
                         'Vous ne pouvez pas avoir deux lignes pour du même élément !')]

    @api.onchange('prix_unit', 'nbre')
    def total(self):
        for val in self:
            val.prix_total = val.nbre * val.prix_unit


class FaarfFormation(models.Model):
    _name = "faarf.formation"

    name = fields.Many2one("faarf.prog.prev.line", "Formation", required=True)
    date_begin = fields.Date("Date de début", related='name.date_begin')
    date_end = fields.Date("Date de fin", related='name.date_end')
    date_begin_reel = fields.Date("Date de début réelle", required=True)
    date_end_reel = fields.Date("Date de fin réelle", required=True)
    module_id = fields.Many2one("faarf.module", string="Module")
    nbre = fields.Integer("Nbre prévu", related='name.nbre')
    nbre_reel = fields.Integer("Nbre réel", required=True)
    region_id = fields.Many2one("ref_region", "Région", readonly=True)
    province_id = fields.Many2one("ref_province", "Province", readonly=True)
    lieu = fields.Many2one("ref_departement", "Lieu", readonly=True)
    line_ids = fields.One2many("faarf.formation.line", "formation_id")
    fichier_ids = fields.One2many("faarf.formation.fichier", "formation_id")
    state = fields.Selection([('N', 'Nouveau'), ('E', 'Exécutée')],
                             string="Etat", required=True, default='N')
    tot_reliquat = fields.Float("Total reliquat", compute='_totaux_req', store=True)
    tot_reel = fields.Float("Total réel", compute='_totaux_reel', store=True)
    tot_prev = fields.Float("Total prévisionnel", compute='_totaux_prev', store=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.depends("line_ids.cout_prev")
    def _totaux_prev(self):
        self.tot_prev = sum(ligne.cout_prev for ligne in self.line_ids)

    @api.depends("line_ids.mnt_dep")
    def _totaux_reel(self):
        self.tot_reel = sum(ligne.mnt_dep for ligne in self.line_ids)

    @api.depends("line_ids.reliquat")
    def _totaux_req(self):
        self.tot_reliquat = sum(ligne.reliquat for ligne in self.line_ids)

    @api.onchange('name')
    def total(self):
        for val in self:
            val.module_id = val.name.module_id
            val.region_id = val.name.region_id
            val.province_id = val.name.province_id
            val.lieu = val.name.lieu

    def valider(self):
        v_id = int(self.name)
        resu = self.env['faarf.prog.prev.line'].search([('id', '=', v_id)])
        resu.state = 'E'
        self.state = 'E'

    def afficher(self):
        v_id = int(self.name)
        resu = self.env['faarf.cout.prev'].search([('prog_id', '=', v_id)])
        for val in resu:
            self.env['faarf.formation.line'].create({
                'element_id': val.element_id.id,
                'cout_prev': val.prix_total,
                'mnt_recu': val.prix_total,
                'mnt_dep': 0,
                'formation_id': self.id,
            })


class FaarfFormationLine(models.Model):
    _name = "faarf.formation.line"

    formation_id = fields.Many2one("faarf.formation", ondelete="cascade")
    element_id = fields.Many2one("faarf.element.budget", "Libellé", readonly=True)
    cout_prev = fields.Float("Prévisionnel", readonly=True)
    mnt_recu = fields.Float("Montant reçu", required=True)
    mnt_dep = fields.Float("Montant dépensé", required=True)
    reliquat = fields.Float("Réliquat", readonly=True)

    @api.onchange('mnt_recu', 'mnt_dep')
    def total(self):
        for val in self:
            val.reliquat = val.mnt_recu - val.mnt_dep


class FaarfFormationFichier(models.Model):
    _name = "faarf.formation.fichier"

    formation_id = fields.Many2one("faarf.formation", ondelete="cascade")
    libelle = fields.Char("Libellé du fichier", required=True)
    fichier = fields.Binary("Joindre le fichier", attachment=True, required=True)


class FaarfBilanFormation(models.Model):
    _name = "faarf.bilan.formation"

    date_begin = fields.Date("Date du", required=True)
    date_end = fields.Date("Date au", required=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    bilan_ids = fields.One2many("faarf.bilan.formation.line", "bilan_id")

    def name_get(self):
        result = []
        for formation in self:
            name = 'Bilan et côut de formation de la clientèle du' + ' ' \
                   + str(formation.date_begin) + ' ' + 'au' + ' ' + str(formation.date_end)
            result.append((formation.id, name))
        return result

    def afficher(self):
        dd1 = self.date_begin
        dd2 = self.date_end

        # resu = self.env['faarf.formation'].search([
        #     ('date_begin_reel', '>=', dd1), ('date_begin_reel', '=', dd2),
        #     ('date_end_reel', '>=', dd1), ('date_end_reel', '=', dd2), ('state', '=', 'E')])
        # self.bilan_ids.unlink()
        # for val in resu:
        #     self.env['faarf.bilan.formation.line'].create({
        #         'date_begin_reel': val.date_begin_reel,
        #         'date_end_reel': val.date_end_reel,
        #         'module_id': val.module_id,
        #         'region_id': val.region_id.id,
        #         'province_id': val.province_id.id,
        #         'lieu': val.lieu.id,
        #         'nbre_reel': val.nbre_reel,
        #         'bilan_id': self.id,
        #     })

        for vals in self:
            vals.env.cr.execute(
                """select * from faarf_formation where date_begin_reel >= %s and date_begin_reel <= %s
                and date_end_reel >= %s and date_end_reel <= %s and state = 'E' order by date_begin_reel""",
                (dd1, dd2, dd1, dd2))
            res = vals.env.cr.dictfetchall()
            result = []

        # delete old ordre entree lines
        vals.bilan_ids.unlink()
        for line in res:
            result.append((0, 0, {'date_begin_reel': line['date_begin_reel'], 'date_end_reel': line['date_end_reel'],
                                  'module_id': line['module_id'], 'tot_prev': line['tot_prev'],
                                  'tot_reel': line['tot_reel'], 'tot_reliquat': line['tot_reliquat'],
                                  'nbre_reel': line['nbre_reel'], 'region_id': line['region_id'],
                                  'province_id': line['province_id'], 'lieu': line['lieu']}))
        self.bilan_ids = result


class FaarfBilanFormationLine(models.Model):
    _name = "faarf.bilan.formation.line"

    bilan_id = fields.Many2one("faarf.bilan.formation", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre")
    date_begin_reel = fields.Date("Date début", required=True)
    date_end_reel = fields.Date("Date fin", required=True)
    module_id = fields.Many2one("faarf.module", string="Module")
    tot_prev = fields.Float("Coût prévisionnel", readonly=True)
    tot_reel = fields.Float("Coût réel", readonly=True)
    tot_reliquat = fields.Float("Réliquat", readonly=True)
    nbre_reel = fields.Integer("Nbre de femmes formées", readonly=True)
    region_id = fields.Many2one("ref_region", "Région", readonly=True)
    province_id = fields.Many2one("ref_province", "Province", readonly=True)
    lieu = fields.Many2one("ref_departement", "Lieu", readonly=True)


class FaarfBudgetFormation(models.Model):
    _name = "faarf.budget.formation"

    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Année")
    budget_ids = fields.One2many("faarf.budget.formation.line", "budget_id")
    state = fields.Selection([('N', 'Nouveau'), ('E', 'Exécutée')],
                             string="Etat", required=True, default='N')

    def afficher(self):
        v_ex = int(self.x_exercice_id)
        for vals in self:
            vals.env.cr.execute(
                """select count(l.*) as sess, l.module_id as modul, l.province_id as prov, sum(l.nbre) as nbre
                from faarf_prog_prev_line l, faarf_prog_prev p 
                where p.x_exercice_id =%d and p.id = l.prog_id group by l.module_id, l.province_id, l.lieu, l.nbre
                order by l.province_id""" % (v_ex))
            res = vals.env.cr.dictfetchall()
            result = []

        # delete old ordre entree lines
        vals.budget_ids.unlink()
        for line in res:
            result.append((0, 0, {'module_id': line['modul'], 'province_id': line['prov'],
                                  'nbre': line['nbre'], 'nbre_session': line['sess']}))
        self.budget_ids = result

    def name_get(self):
        result = []
        for formation in self:
            name = 'Budget prévisionnel des formations de la clientèle de' + ' ' + str(
                formation.x_exercice_id.no_ex)
            result.append((formation.id, name))
        return result


class FaarfBudgetFormationLine(models.Model):
    _name = "faarf.budget.formation.line"

    budget_id = fields.Many2one("faarf.budget.formation", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre")
    province_id = fields.Many2one("ref_province", "Province", readonly=True)
    module_id = fields.Many2one("faarf.module", string="Module")
    nbre_session = fields.Float("Nbre de sessions", readonly=True)
    nbre = fields.Float("Nbre femmes")
    nbre_reg = fields.Float("Nbre Reg.")
    nbre_dep = fields.Float("Nbre Dep.")
    nbre_prov = fields.Float("Nbre Prov.")
    cout_reg = fields.Float("C.U Reg.")
    cout_dep = fields.Float("C.U Dep.")
    cout_prov = fields.Float("C.U Prov.")
    cout_tot_reg = fields.Float("C.T Reg.")
    cout_tot_dep = fields.Float("C.T Dep.")
    cout_tot_prov = fields.Float("C.T Prov.")
    total = fields.Float("Total")


class FaarfTableauBord(models.Model):
    _name = "faarf.tableau.bord"

    x_exercice_id = fields.Many2one('ref_exercice', string="Année")
    tab_ids = fields.One2many("faarf.tableau.bord.line", "tab_id", readonly=True)

    def name_get(self):
        result = []
        for formation in self:
            name = 'Tableau de bord des formations de la clientèle de' + ' ' + str(
                formation.x_exercice_id.no_ex)
            result.append((formation.id, name))
        return result


    def afficher(self):
        v_ex = int(self.x_exercice_id)
        for vals in self:
            vals.env.cr.execute(
                """select distinct f.region_id, sum(l.nbre) as nbre, f.nbre_reel, 
                l.animatrice_id as anim, l.superviseur_id as sup,
                (l.nbre - f.nbre_reel) as reste, count(l.*) as nbresess,
                coalesce((case when f.state = 'E' then count(f.*) end),0) as nbresesstenu, 
                coalesce((count(l.*) - (case when f.state = 'E' then count(f.*) end)),0) as restesession,
                f.province_id, f.lieu, f.tot_reel, f.tot_prev from faarf_formation f, faarf_prog_prev_line l
                where f.x_exercice_id = %d and l.id = f.name and f.lieu = l.lieu 
                and f.region_id = l.region_id and f.province_id = l.province_id
                group by f.region_id, l.nbre, f.nbre_reel,f.province_id, 
                f.lieu, f.tot_reel, f.tot_prev, f.state,l.animatrice_id,l.superviseur_id 
                """ % (v_ex))
            res = vals.env.cr.dictfetchall()
            result = []

        # delete old ordre entree lines
        vals.tab_ids.unlink()
        for line in res:
            result.append((0, 0, {'superviseur_id': line['sup'], 'gestionnaire_id': line['anim'],
                                  'region_id': line['region_id'], 'province_id': line['province_id'],
                                  'lieu': line['lieu'], 'nbre': line['nbre'], 'nbre_reel': line['nbre_reel'],
                                  'reste_nbre': line['reste'], 'nbre_session': line['nbresess'],
                                  'nbre_session_reel': line['nbresesstenu'], 'nbre_session_nonreel': line['restesession'],
                                  'tot_prev': line['tot_prev'], 'tot_reel': line['tot_reel']}))
        self.tab_ids = result


class FaarfTableauBordLine(models.Model):
    _name = "faarf.tableau.bord.line"

    tab_id = fields.Many2one("faarf.tableau.bord", ondelete='cascade')
    formation_id = fields.Many2one("faarf.prog.prev.line", "Formation")
    tot_prev = fields.Float("Coût prévisionnel", readonly=True)
    tot_reel = fields.Float("Coût réel", readonly=True)
    nbre = fields.Integer("Prev Nbre de femmes à former", readonly=True)
    nbre_reel = fields.Integer("Nbre de femmes formées", readonly=True)
    reste_nbre = fields.Integer("Nbre de femmes formées", readonly=True)
    nbre_session = fields.Integer("Prev Nbre de session", readonly=True)
    nbre_session_reel = fields.Integer("Nbre de sessions réalisées", readonly=True)
    nbre_session_nonreel = fields.Integer("Nbre de formations non réalisées", readonly=True)
    region_id = fields.Many2one("ref_region", "Région", readonly=True)
    province_id = fields.Many2one("ref_province", "Province", readonly=True)
    lieu = fields.Many2one("ref_departement", "Lieu", readonly=True)
    gestionnaire_id = fields.Many2one("res.users", string="Gestionnaire")
    superviseur_id = fields.Many2one("res.users", string="Superviseur")


class FaarfSuggestion(models.Model):
    _name = "faarf.suggestion"

    dte = fields.Date("Date", required=True)
    formation_id = fields.Many2one("faarf.formation", "Formation", required=True)
    suggestion = fields.Text("Suggestion/recommandation", required=True)
