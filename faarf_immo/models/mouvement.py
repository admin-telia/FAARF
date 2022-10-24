from odoo import fields, models, api
from datetime import date


class FaarfAffectation(models.Model):
    _name = "faarf.affectation"

    name = fields.Char("N° Affectation", readonly=True)
    dte = fields.Date("Date affectation", default=fields.Date.context_today, required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('V', 'Validé')], string="Etat", required=True, default='draft')
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    compte_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    magasinier = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    cd_struct = fields.Char("Code Structure", related='company_id.code_struct')
    cd_ministere = fields.Char("Code Ministere", related='company_id.ministere.code_ministere')

    departement_id = fields.Many2one("ref_departement", "Département", required=False)
    cd_departement = fields.Char("Code Département", default='00')

    province_id = fields.Many2one("ref_province", "Province", related='departement_id.ref_province_id')
    cd_province = fields.Char("Code Province", related='province_id.code_province')

    region_id = fields.Many2one("ref_region", "Région", related='province_id.ref_region_id')
    cd_region = fields.Char("Code Région", related='region_id.libcourt')

    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    direction_id = fields.Many2one("hr.department", "Direction", required=True)
    cd_direction = fields.Char("Code Direction", related='direction_id.code')

    service_id = fields.Many2one("hr_service", "Service")
    magasin_id = fields.Many2one("faarf.magasin.immo", "Magasin", required=True)
    line_ids = fields.One2many("faarf.affectation.line", "affectation_id")


    """Compteur d'ordre entrée en matiere"""
    def valider(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select numero from faarf_compteur_aff where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_aff(x_exercice_id,company_id,numero) VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            self.majficheimmo()
            self.state = 'V'
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_aff SET numero = %d WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))
            self.majficheimmo()
            self.state = 'V'

    def majficheimmo(self):
        v_id = int(self.id)

        cd_ministere = self.cd_ministere
        cd_struct = self.cd_struct
        cd_region = '03'
        print("region", cd_region)
        cd_province = '11'
        print("province", cd_province)
        cd_direction = self.cd_direction
        print("direction", cd_direction)
        cd_departement = '00'
        dire = self.direction_id
        dte = self.dte
        self.majstock()


        for val in self.line_ids:

            codification = str(val.code) + "/" + str(cd_ministere) + "/" + str(cd_struct) + "." + str(cd_direction) + "/" + str(cd_region) + "/" + str(cd_province) + "/" + str(cd_departement) + "/" + str(val.annee) + "/" + str(val.num_ordre)
            val.codification = codification
            val.direction_id = dire
            val.state = 'C'

            resu = self.env['faarf.stock.immo'].search([('id', '=', val.matiere_id.id)])
            resu.etat = 'C'
            resu.codification = val.codification

            print("Maa")
            print(val.id_matiere.id)
            self.env['faarf.codification'].create({
                'name': val.codification,
                'id_matiere': val.id_matiere.id,
                'direction_id': self.direction_id.id,
                'valeur_unitaire': val.valeur_unitaire,
                'fournisseur_id': val.fournisseur_id.id,
                'dte_acquisition': val.dte_acquisition,
                'dte_service': dte,
                'source_id': val.source_id.id,
                'type_immo': val.type_immo
            })


    def majstock(self):


        self.env.cr.execute("""select * from faarf_affectation_line where affectation_id = %d
        """ %(self.id))
        for val in self.env.cr.dictfetchall():
            v_mat = val['matiere_id']
            self.env.cr.execute("""update faarf_stock_immo set reste = 0, etat ='C' where id = %d""" % v_mat)
        self.majnum()

    def majnum(self):

        num = 0
        for val in self.line_ids:
            num = num + 1
            ok = str(num).zfill(4)
            val.num_ordre = ok


class FaarfAffectationLine(models.Model):
    _name = "faarf.affectation.line"
    _rec_name = "codification"

    affectation_id = fields.Many2one("faarf.affectation", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", size=4, readonly=True)
    code = fields.Char("Sous Code", readonly=True)
    matiere_id = fields.Many2one("faarf.stock.immo", domain=[('etat', '=', 'NC')], required=True, string="Matière")
    unite_id = fields.Many2one("faarf.format.immo", string="Unité", readonly=True)
    qte = fields.Float("Qté/Nbre", readonly=True, default=1)
    montant = fields.Float("Montant", compute='_mnt_total')
    decompte = fields.Char("Décompte")
    annee = fields.Char("Année")
    observation = fields.Text("Observation")
    utilisateur_id = fields.Many2one("res.users", "Utilisateur", required=True)
    state = fields.Selection([('N', 'Nouveau'), ('C', 'Codifié'), ('D', 'Déclassé')], string="Etat", default='N')


    codification = fields.Char("Code Immo", readonly=True)
    id_matiere = fields.Many2one("faarf.bien.immo", string="Id Matière")
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    direction_id = fields.Many2one("hr.department", "Direction")
    dte_acquisition = fields.Date("Date acquisition")
    fournisseur_id = fields.Many2one("ref_beneficiaire")
    source_id = fields.Many2one("faarf.source.immo")
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'),
                                  ('2', 'Immobilisation incorporelle')], string="Type")

    @api.onchange("matiere_id")
    def date(self):
        v_mat = int(self.matiere_id.matiere_id)
        print("matiere", v_mat)
        for x in self:
            x.code = x.matiere_id.code
            x.unite_id = x.matiere_id.unite_id
            x.id_matiere = x.matiere_id.matiere_id
            x.annee = x.matiere_id.annee

            self.env.cr.execute("""select * from 
            faarf_ordre_entree_line where matiere_id = %d and state = 'V' """ % (x.id_matiere))
            val = self.env.cr.dictfetchall()

            #x.valeur_unitaire = val and val[0]['valeur_unitaire']
            x.fournisseur_id = val and val[0]['fournisseur_id']
            x.dte_acquisition = val and val[0]['dte']
            x.type_immo = val and val[0]['type_immo']
            x.source_id = val and val[0]['source_id']

            self.env.cr.execute("""select cmu from faarf_stock_immo where matiere_id = %d""" % v_mat)
            res = self.env.cr.fetchone()
            x.valeur_unitaire = res and res[0] or 0


    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.montant = val.qte * val.valeur_unitaire


class FaarfCompteurAff(models.Model):
    _name = "faarf.compteur.aff"

    x_exercice_id = fields.Many2one("ref_exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfMutation(models.Model):
    _name = "faarf.mutation"

    name = fields.Char("N° Mutation", readonly=True)
    dte = fields.Date("Date de mutation", default=fields.Date.context_today, required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('V', 'Validé')], string="Etat", required=True, default='draft')
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    compte_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    magasinier = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    direction_dep = fields.Many2one("hr.department", "Direction de départ", required=True)
    direction_arr = fields.Many2one("hr.department", "Direction d'accueil", required=True)
    line_ids = fields.One2many("faarf.mutation.line", "mutation_id")

    """Compteur d'ordre entrée en matiere"""
    def valider(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select numero from faarf_compteur_mut where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_mut(x_exercice_id,company_id,numero) VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            self.state = 'V'
            self.majnum()
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_mut SET numero = %d WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))
            self.state = 'V'
            self.majnum()

    def majnum(self):

        num = 0
        for val in self.line_ids:
            num = num + 1
            ok = str(num).zfill(4)
            val.num_ordre = ok


class FaarfCompteurMut(models.Model):
    _name = "faarf.compteur.mut"

    x_exercice_id = fields.Many2one("ref_exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfMutationLine(models.Model):
    _name = "faarf.mutation.line"
    _rec_name = "matiere_id"

    mutation_id = fields.Many2one("faarf.mutation", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", readonly=True)
    code = fields.Char("Sous Code", readonly=True)
    matiere_id = fields.Many2one("faarf.affectation.line", domain=[('state', '=', 'C')],
                                 required=True, string="Code Immo")
    id_matiere = fields.Many2one("faarf.bien.immo", string="Id Matière")
    matiere = fields.Many2one("faarf.stock.immo", string="Désignation", readonly=True)
    unite_id = fields.Many2one("faarf.format.immo", required=True, string="Unité")
    qte = fields.Float("Qté/Nbre", readonly=True, default=1)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    montant = fields.Float("Montant", compute='_mnt_total')
    decompte = fields.Char("Décompte")
    observation = fields.Text("Observation")
    utilisateur_id = fields.Many2one("res.users", "Utilisateur", required=False)
    codification = fields.Char("Code Immo", readonly=True)

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.montant = val.qte * val.valeur_unitaire

    @api.onchange("matiere_id")
    def date(self):
        v_mat = int(self.id_matiere)
        for x in self:
            x.code = x.matiere_id.code
            x.unite_id = x.matiere_id.unite_id
            x.id_matiere = x.matiere_id.id_matiere
            x.matiere = x.matiere_id.matiere_id
            x.codification = x.matiere_id.codification
            code = x.matiere.id

            self.env.cr.execute("""select cmu from faarf_stock_immo where id = %d""" % code)
            res = self.env.cr.fetchone()
            x.valeur_unitaire = res and res[0] or 0


class FaarfSortieTemp(models.Model):
    _name = "faarf.sortie.temp"

    name = fields.Char("N° Sortie", readonly=True)
    dte = fields.Date("Date de sortie", default=fields.Date.context_today, required=True)
    dte_retour = fields.Date("Date retour eff.",readonly=True)
    dte_retour_pro = fields.Date("Date retour pro.", default=fields.Date.context_today, required=False)

    state = fields.Selection([('draft', 'Brouillon'), ('V', 'Sortie validé'), ('R', 'Retour effectif')], string="Etat", required=True, default='draft')
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    compte_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    motif = fields.Text("Motif", required=True)
    destination_id = fields.Many2one("faarf.destination", "Destination", required=True)
    direction_id = fields.Many2one("hr.department", "Direction (Origine)", required=True)
    line_ids = fields.One2many("faarf.sortie.temp.line", "sortie_id")

    """Compteur d'ordre entrée en matiere"""
    def valider(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select numero from faarf_compteur_st where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_st(x_exercice_id,company_id,numero) VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            self.state = 'V'
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_st SET numero = %d WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))
            self.state = 'V'

    def retour(self):

        self.state = 'R'
        self.dte_retour = date.today()


class FaarfCompteurSt(models.Model):
    _name = "faarf.compteur.st"

    x_exercice_id = fields.Many2one("ref_exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfSortieTempLine(models.Model):
    _name = "faarf.sortie.temp.line"
    _rec_name = "matiere_id"

    sortie_id = fields.Many2one("faarf.sortie.temp", ondelete='cascade')
    code = fields.Char("Code", readonly=True)
    matiere_id = fields.Many2one("faarf.affectation.line", domain=[('state', '=', 'C')],
                                           required=True, string="Code Immo")
    matiere = fields.Many2one("faarf.stock.immo", string="Désignation", readonly=True)
    id_matiere = fields.Many2one("faarf.bien.immo", string="Id Matière")
    qte = fields.Float("Qté/Nbre", readonly=True, default=1)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    montant = fields.Float("Montant", compute='_mnt_total')
    etat = fields.Char("Etat")
    observation = fields.Text("Observation")

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.montant = val.qte * val.valeur_unitaire

    @api.onchange("matiere_id")
    def date(self):
        v_mat = int(self.id_matiere)
        for x in self:
            x.code = x.matiere_id.codification
            x.valeur_unitaire = x.matiere_id.valeur_unitaire
            x.id_matiere = x.matiere_id.id_matiere
            x.matiere = x.matiere_id.matiere_id
            code = x.matiere

            self.env.cr.execute("""select cmu from faarf_stock_immo where id = %d""" % code)
            res = self.env.cr.fetchone()
            x.valeur_unitaire = res and res[0] or 0


class FaarfOrdreSortie(models.Model):
    _name = "faarf.ordre.sortie"

    name = fields.Char("N° Ordre sortie", readonly=True)
    dte = fields.Date("Date sortie", default=fields.Date.context_today, required=True)
    nature_id = fields.Many2one("faarf.type.sortie", "Nature de sortie", domain=[('type_id', '=', '2')], required=True)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('P', 'Projet OSM'), ('V', 'Validé'), ('A', 'Annulé')],
                             string="Etat", required=True, default='draft')
    compte_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    ordre_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    line_ids = fields.One2many("faarf.ordre.sortie.line", "ordre_id")
    observation = fields.Text("Observation")

    def numordre(self):

        num = 0
        for val in self.line_ids:
            num = num + 1
            ok = str(num).zfill(4)
            val.num_ordre = ok

    """Compteur d'ordre entrée en matiere"""

    def valider(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select numero from faarf_compteur_oem where x_exercice_id = %d and company_id = %d" % (
                val_ex, val_struct))
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_oem(x_exercice_id,company_id,numero) VALUES(%d, %d, %d)""" % (
                    val_ex, val_struct, vals))
            self.numordre()
            self.state = 'P'
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_oem SET numero = %d WHERE x_exercice_id = %d and company_id = %d" % (
                    vals, val_ex, val_struct))
            self.numordre()
            self.state = 'P'

    def valider_dfc(self):
        v_id = int(self.id)
        v_dte = self.dte
        v_type = int(self.nature_id)
        v_piece = int(self.piece_id)
        self.env.cr.execute("""select sl.* from faarf_ordre_sortie_line sl, faarf_ordre_sortie s 
        where s.id = sl.ordre_id and sl.ordre_id = %d""" % (v_id))
        for val in self.env.cr.dictfetchall():
            v_mat = val['id_matiere']
            v_qte = val['qte']

            self.env.cr.execute("""update faarf_stock_immo set etat ='S', sortie = coalesce(sortie,0) + %s where id = %s""",
                                (v_qte, v_mat))
            self.env.cr.execute("""update faarf_ordre_sortie_line set
            dte = %s, nature_id = %s, piece_id = %s where ordre_id = %s""", (v_dte, v_type, v_piece, v_id))

        self.state = 'V'


class FaarfOrdreSortieLine(models.Model):
    _name = "faarf.ordre.sortie.line"
    _rec_name = "matiere_id"

    ordre_id = fields.Many2one("faarf.ordre.sortie", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", readonly=True, size=4)
    code = fields.Char("Sous code matière", readonly=True)
    matiere_id = fields.Many2one("faarf.stock.immo", domain=[('etat', '!=', 'S')], required=True, string="Matière")
    id_matiere = fields.Many2one("faarf.bien.immo", string="Id Matière")
    unite_id = fields.Many2one("faarf.format.immo", required=True, string="Unité")
    qte = fields.Float("Quantité", readonly=True, default=1)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    valeur_totale = fields.Float("Valeur totale", compute='_mnt_total')
    decompte = fields.Char("Décompte")
    observation = fields.Text("Observation")
    dte = fields.Date("Date sortie", default=fields.Date.context_today, required=False)
    nature_id = fields.Many2one("faarf.type.sortie", "Nature de sortie", required=False)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", required=False)

    @api.onchange("matiere_id")
    def numcode(self):
        v_mat = int(self.id_matiere)
        for val in self:
            if val.matiere_id:
                val.code = val.matiere_id.code
                val.id_matiere = val.matiere_id.matiere_id
                code = val.matiere_id

                self.env.cr.execute("""select cmu from faarf_stock_immo where id = %d""" % code)
                res = self.env.cr.fetchone()
                val.valeur_unitaire = res and res[0] or 0

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.valeur_totale = val.qte * val.valeur_unitaire
