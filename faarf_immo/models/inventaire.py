from odoo import fields, models, api
import datetime


class FaarfInventaireEntree(models.Model):
    _name = "faarf.inventaire.entree"
    _rec_name = "type_invent"

    magasin_id = fields.Many2one("faarf.magasin.immo", string="Magasin")
    date_debut = fields.Date(string="Date debut", required=True)
    date_fin = fields.Date(string="Date fin", required=True)
    type_invent = fields.Selection(
        [("1", "Annuel"), ("2", "Semestriel"), ("3", "Trimestriel"), ("4", "Mensuel"), ("5", "Tournant")],
        string="Type Inventaire", store=True, required=True)
    emplacement = fields.Selection([('1', 'Tous les magasins'), ('2', 'Par magasin')], string="Emplacements",
                                   default='1', required=True)
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    compta_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    magasinier = fields.Many2one("budg_signataire",
                                 default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    entree_line_ids = fields.One2many("faarf.inventaire.entree.line", "entree_id", string=" ")
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.onchange("date_debut")
    def calDate(self):

        for val in self:
            if val.type_invent == '1':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=364)
                val.date_fin = new_dte.date()


            elif val.type_invent == '2':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=179)
                val.date_fin = new_dte.date()

            elif val.type_invent == '3':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=89)
                val.date_fin = new_dte.date()

            elif val.type_invent == '4':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=29)
                val.date_fin = new_dte.date()

            else:
                val.date_fin = val.date_fin

    # fonction de remplissage du tableau des biens en service

    def invent_entree(self):
        if self.date_debut and self.date_fin:
            ddbut = str(self.date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.date_fin.strftime("%Y-%m-%d"))
            val_mag = int(self.magasin_id)

            if self.emplacement == "1":

                for vals in self:
                    vals.env.cr.execute(
                        """SELECT s.code as code, s.matiere_id as mat, sum(s.reste) as qte, s.cmu as val
                        FROM faarf_ordre_entree_line l, faarf_stock_immo s where l.matiere_id = s.matiere_id and 
                        s.dte BETWEEN %s and %s group by s.code, s.matiere_id, s.cmu""", (ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result

            else:
                for vals in self:
                    vals.env.cr.execute(
                        """SELECT s.code as code, s.matiere_id as mat, sum(s.reste) as qte, s.cmu as val
                        FROM faarf_ordre_entree_line l, faarf_stock_immo s where l.matiere_id = s.matiere_id 
                        and s.magasin_id = l.magasin_id and s.magasin_id = %s and s.dte BETWEEN %s and %s 
                        group by s.code, s.matiere_id, s.cmu""", (val_mag, ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result


class FaarfInventaireEntreeLine(models.TransientModel):
    _name = "faarf.inventaire.entree.line"

    entree_id = fields.Many2one("faarf.inventaire.entree")
    sous_code = fields.Char(string="Sous code")
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    quant = fields.Float(string="Quantité Théorique", readonly=True)
    quant_phys = fields.Float(string="Quantité physique")
    ecart = fields.Float(string="Ecart", compute='_ecart')
    val_unit = fields.Float(string="Prix unitaire")
    montant = fields.Float(string="Total", compute='_ecart')
    observation = fields.Text(string="Observation")

    @api.depends("quant_phys", "val_unit")
    def _ecart(self):
        for val in self:
            val.ecart = val.quant - val.quant_phys
            val.montant = val.quant * val.val_unit


class FaarfInventaireService(models.Model):
    _name = "faarf.inventaire.service"
    _rec_name = "type_invent"

    direction_id = fields.Many2one("hr.department", string="Direction")
    date_debut = fields.Date(string="Date debut", required=True)
    date_fin = fields.Date(string="Date fin", required=True)
    type_invent = fields.Selection(
        [("1", "Annuel"), ("2", "Semestriel"), ("3", "Trimestriel"), ("4", "Mensuel"), ("5", "Tournant")],
        string="Type Inventaire", store=True, required=True)
    emplacement = fields.Selection([('1', 'Toutes les directions'), ('2', 'Par direction')], string="Emplacements",
                                   default='1', required=True)
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    compta_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    magasinier = fields.Many2one("budg_signataire",
                                 default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    entree_line_ids = fields.One2many("faarf.inventaire.service.line", "entree_id", string=" ")
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.onchange("date_debut")
    def calDate(self):

        for val in self:
            if val.type_invent == '1':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=364)
                val.date_fin = new_dte.date()


            elif val.type_invent == '2':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=179)
                val.date_fin = new_dte.date()

            elif val.type_invent == '3':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=89)
                val.date_fin = new_dte.date()

            elif val.type_invent == '4':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=29)
                val.date_fin = new_dte.date()

            else:
                val.date_fin = val.date_fin

    # fonction de remplissage du tableau des biens en service

    def invent_entree(self):
        if self.date_debut and self.date_fin:
            ddbut = str(self.date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.date_fin.strftime("%Y-%m-%d"))
            val_dir = int(self.direction_id)

            if self.emplacement == "1":

                for vals in self:
                    vals.env.cr.execute(
                        """SELECT s.code as code, s.id_matiere as mat, sum(s.qte) as qte, s.valeur_unitaire as val
                        FROM faarf_affectation_line s, faarf_affectation a where a.dte BETWEEN %s and %s 
                        and a.id = s.affectation_id
                        GROUP BY s.code, s.id_matiere, s.valeur_unitaire""", (ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result

            else:
                for vals in self:
                    vals.env.cr.execute(
                        """SELECT s.code as code, s.id_matiere as mat, sum(s.qte) as qte, s.valeur_unitaire as val
                        FROM faarf_affectation_line s, faarf_affectation a where s.direction_id = %s 
                        and a.dte BETWEEN %s and %s and a.id = s.affectation_id
                        GROUP BY s.code, s.id_matiere, s.valeur_unitaire""", (val_dir, ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result


class FaarfInventaireServiceLine(models.TransientModel):
    _name = "faarf.inventaire.service.line"

    entree_id = fields.Many2one("faarf.inventaire.service")
    sous_code = fields.Char(string="Sous code")
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    quant = fields.Float(string="Quantité Théorique", readonly=True)
    quant_phys = fields.Float(string="Quantité physique")
    val_unit = fields.Float(string="Prix unitaire")
    montant = fields.Float(string="Total", compute='_ecart')
    observation = fields.Text(string="Observation")

    @api.depends("quant_phys", "val_unit")
    def _ecart(self):
        for val in self:
            val.montant = val.quant * val.val_unit


class FaarfInventaireDeclasse(models.Model):
    _name = "faarf.inventaire.declasse"
    _rec_name = "type_invent"

    direction_id = fields.Many2one("ref_direction", string="Direction")
    date_debut = fields.Date(string="Date debut", required=True)
    date_fin = fields.Date(string="Date fin", required=True)
    type_invent = fields.Selection(
        [("1", "Annuel"), ("2", "Semestriel"), ("3", "Trimestriel"), ("4", "Mensuel"), ("5", "Tournant")],
        string="Type Inventaire", store=True, required=True)
    emplacement = fields.Selection([('1', 'Toutes les directions'), ('2', 'Par direction')], string="Emplacements",
                                   default='1', required=False)
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    compta_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    magasinier = fields.Many2one("budg_signataire",
                                 default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    entree_line_ids = fields.One2many("faarf.inventaire.declasse.line", "entree_id", string=" ")
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.onchange("date_debut")
    def calDate(self):

        for val in self:
            if val.type_invent == '1':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=364)
                val.date_fin = new_dte.date()


            elif val.type_invent == '2':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=179)
                val.date_fin = new_dte.date()

            elif val.type_invent == '3':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=89)
                val.date_fin = new_dte.date()

            elif val.type_invent == '4':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=29)
                val.date_fin = new_dte.date()

            else:
                val.date_fin = val.date_fin

    # fonction de remplissage du tableau des biens en service

    def invent_entree(self):
        if self.date_debut and self.date_fin:
            ddbut = str(self.date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.date_fin.strftime("%Y-%m-%d"))

            if self.emplacement == "1":

                for vals in self:
                    vals.env.cr.execute(
                        """SELECT l.code as code, l.id_matiere as mat, count(l.id) as qte, l.valeur_unitaire as val
                        FROM faarf_ordre_sortie_line l where l.dte BETWEEN %s and %s group by l.code, l.id_matiere, l.valeur_unitaire""", (ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result

            else:
                for vals in self:
                    vals.env.cr.execute(
                        """SELECT s.code as code, s.matiere_id as mat, sum(s.sortie) as qte, s.cmu as val
                        FROM faarf_ordre_sortie_line l, faarf_stock_immo s where l.id_matiere = s.matiere_id 
                        and l.dte BETWEEN %s and %s 
                        group by s.code, s.matiere_id, s.cmu""", (ddbut, ddfin))
                    res = vals.env.cr.dictfetchall()
                    result = []

                # delete old ordre entree lines
                vals.entree_line_ids.unlink()
                for line in res:
                    result.append((0, 0, {'sous_code': line['code'], 'quant': line['qte'],
                                          'matiere_id': line['mat'], 'val_unit': line['val']}))
                self.entree_line_ids = result


class FaarfInventaireDeclasseLine(models.TransientModel):
    _name = "faarf.inventaire.declasse.line"

    entree_id = fields.Many2one("faarf.inventaire.declasse")
    sous_code = fields.Char(string="Sous code")
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    quant = fields.Float(string="Quantité Théorique", readonly=True)
    quant_phys = fields.Float(string="Quantité physique")
    val_unit = fields.Float(string="Prix unitaire",readonly=True)
    montant = fields.Float(string="Total", compute='_ecart')
    observation = fields.Text(string="Observation")

    @api.depends("quant_phys", "val_unit")
    def _ecart(self):
        for val in self:
            val.montant = val.quant * val.val_unit


class FaarfFicheInventaireMatiere(models.Model):
    _name = "faarf.fiche.inventaire.matiere"

    _rec_name = "type_invent"

    date_debut = fields.Date(string="Date debut", required=True)
    date_fin = fields.Date(string="Date fin", required=True)
    type_invent = fields.Selection([("1", "Annuel")], string="Type Inventaire", required=True)
    ordre_matiere = fields.Many2one("budg_signataire",
                                    default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    compta_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    magasinier = fields.Many2one("budg_signataire",
                                 default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    entree_line_ids = fields.One2many("faarf.fiche.inventaire.matiere.line", "entree_id")
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.onchange("date_debut")
    def calDate(self):

        for val in self:
            if val.type_invent == '1':
                ddbut = str(val.date_debut)
                vddbut = datetime.datetime.strptime(ddbut, "%Y-%m-%d")
                new_dte = vddbut + datetime.timedelta(days=364)
                val.date_fin = new_dte.date()

    # fonction de remplissage du tableau des biens en service

    def invent_entree(self):
        ddbut = str(self.date_debut.strftime("%Y-%m-%d"))
        ddfin = str(self.date_fin.strftime("%Y-%m-%d"))

        for vals in self:

            resu = self.env['faarf.stock.immo'].search([])
            result = []
            self.entree_line_ids.unlink()
            for line in resu:
                # print(line['code'])
                result.append((0, 0, {'sous_code': line['code'], 'matiere_id': line['matiere_id'].id}))

            self.entree_line_ids = result
            for val in self.entree_line_ids:
                mat = val.matiere_id
                nbre = self.env['faarf.codification'].search_count([('id_matiere', '=', mat.id)])
                val.en_service = nbre

                entree = self.env['faarf.stock.immo'].search([('matiere_id', '=', mat.id)])
                val.affecte_non = entree.entree - val.en_service
                val.total = val.affecte_non + val.en_service


class FaarfFicheInventaireMatiereLine(models.TransientModel):
    _name = "faarf.fiche.inventaire.matiere.line"

    entree_id = fields.Many2one("faarf.fiche.inventaire.matiere")
    sous_code = fields.Char(string="Sous code", readonly=True)
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    affecte_non = fields.Float(string="Matières en attente d'affectation", readonly=True)
    en_service = fields.Float(string="Matières en service", readonly=True)
    en_sortie = fields.Float(string="Matières en sortie provisoire", readonly=True)
    total = fields.Float(string="Total", readonly=True)
    en_plus = fields.Float("En plus")
    en_moins = fields.Float("En moins")
    val_unit = fields.Float(string="Prix unitaire")
    val_en_plus = fields.Float("Val. en plus", readonly=True)
    val_en_moins = fields.Float("Val. en moins", readonly=True)

    @api.depends('en_plus', 'en_moins', 'val_unit')
    def _mnt_total(self):
        for val in self:
            val.val_en_plus = val.en_plus * val.val_unit
            val.val_en_moins = val.en_moins * val.val_unit
