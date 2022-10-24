from odoo import fields, models, api
import datetime

class FaarfLivreJournal(models.TransientModel):
    _name = "faarf.livre.journal"
    _rec_name = "journal_id"

    dte_deb = fields.Date("Date de début", required=True)
    dte_fin = fields.Date("Date de fin", required=True)
    journal_id = fields.Selection([('1', 'Journal des entrées'), ('2', 'Journal des sorties'),
                                   ('3', 'Les deux')], string="Type journal", default = '1', required=True)
    compte_matiere = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    livre_entree_ids = fields.One2many("faarf.livre.journal.entree", "livre_id")
    livre_sortie_ids = fields.One2many("faarf.livre.journal.sortie", "livre_id")

    def afficher(self):

        dte_b = self.dte_deb
        dte_f = self.dte_fin

        if self.journal_id == '1':
            for vals in self:
                vals.env.cr.execute("""select * from faarf_ordre_entree_line
                where dte between %s and %s""", (dte_b, dte_f))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.livre_entree_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'num_ordre': line['num_ordre'], 'dte': line['dte'], 'code': line['code'],
                                          'matiere_id': line['matiere_id'], 'qte': line['qte'],
                                          'valeur_unitaire': line['valeur_unitaire'],
                                           'nature_id': line['mode_id'],
                                          'piece_id': line['piece_id'], 'observation': line['observation']}))
                self.livre_entree_ids = result

        elif self.journal_id == '2':
            for vals in self:
                vals.env.cr.execute("""select * from faarf_ordre_sortie_line
                where dte between %s and %s""" , (dte_b, dte_f))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.livre_sortie_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'num_ordre': line['num_ordre'], 'dte': line['dte'], 'code': line['code'],
                                          'matiere_id': line['id_matiere'], 'qte': line['qte'],
                                          'valeur_unitaire': line['valeur_unitaire'],
                                          'nature_id': line['nature_id'],
                                          'piece_id': line['piece_id'], 'observation': line['observation']}))
                self.livre_sortie_ids = result
        else:
            for vals in self:
                vals.env.cr.execute("""select * from faarf_ordre_entree_line
                where dte between %s and %s""" , (dte_b, dte_f))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.livre_entree_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'num_ordre': line['num_ordre'], 'dte': line['dte'], 'code': line['code'],
                                          'matiere_id': line['matiere_id'], 'qte': line['qte'],
                                          'valeur_unitaire': line['valeur_unitaire'], 'nature_id': line['mode_id'],
                                          'piece_id': line['piece_id'], 'observation': line['observation']}))
                self.livre_entree_ids = result

            for vals in self:
                vals.env.cr.execute("""select * from faarf_ordre_sortie_line
                        where dte between %s and %s""", (dte_b, dte_f))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.livre_sortie_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'num_ordre': line['num_ordre'], 'dte': line['dte'], 'code': line['code'],
                                          'matiere_id': line['id_matiere'], 'qte': line['qte'],
                                          'valeur_unitaire': line['valeur_unitaire'], 'nature_id': line['nature_id'],
                                          'piece_id': line['piece_id'], 'observation': line['observation']}))
                self.livre_sortie_ids = result


class FaarfLivreJournalEntree(models.TransientModel):
    _name = "faarf.livre.journal.entree"

    livre_id = fields.Many2one("faarf.livre.journal", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", readonly=True)
    dte = fields.Date("Date", readonly=True)
    code = fields.Char("Sous code matière", readonly=True)
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    qte = fields.Float("Quantité", readonly=True)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    valeur_totale = fields.Float("Valeur totale", compute='_mnt_total')
    nature_id = fields.Many2one("faarf.type.sortie", "Nature", readonly=True)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", readonly=True)
    observation = fields.Text("Observation")

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.valeur_totale = val.qte * val.valeur_unitaire


class FaarfLivreJournalSortie(models.TransientModel):
    _name = "faarf.livre.journal.sortie"

    livre_id = fields.Many2one("faarf.livre.journal", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", readonly=True)
    dte = fields.Date("Date", readonly=True)
    code = fields.Char("Sous code matière", readonly=True)
    matiere_id = fields.Many2one("faarf.bien.immo", string="Désignation", readonly=True)
    qte = fields.Float("Quantité", readonly=True)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    valeur_totale = fields.Float("Valeur totale", compute='_mnt_total')
    nature_id = fields.Many2one("faarf.type.sortie", "Nature", readonly=True)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", readonly=True)
    observation = fields.Text("Observation")

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.valeur_totale = val.qte * val.valeur_unitaire


class FaarfFicheStock(models.TransientModel):
    _name = "faarf.fiche.stock"

    dte_deb = fields.Date("Date de début", required=True)
    dte_fin = fields.Date("Date de fin", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string="Exercice")
    magasinier = fields.Many2one("budg_signataire",
                                     default=lambda self: self.env['budg_signataire'].search([('code', '=', '6')]))
    lines_ids = fields.One2many("faarf.fiche.stock.line", "fiche_id", readonly=True)

    def afficher(self):

        dte_b = self.dte_deb
        dte_f = self.dte_fin

        for vals in self:
            vals.env.cr.execute("""select b.concate_code as code, sum(e.qte) as qte_ent, sum(s.qte) as qte_sor, b.id as mat 
            from faarf_ordre_entree_line e, faarf_ordre_sortie_line s, faarf_bien_immo b
            where e.dte between %s and %s and s.dte between %s and %s
            and e.matiere_id = b.id and s.id_matiere = b.id group by b.id, b.concate_code """, (dte_b, dte_f,dte_b, dte_f))
            rows = vals.env.cr.dictfetchall()
            result = []

            vals.lines_ids.unlink()
            for line in rows:
                result.append((0, 0, {'code': line['code'],'matiere_id': line['mat'],
                                      'entree': line['qte_ent'], 'sortie': line['qte_sor']}))
            self.lines_ids = result


class FaarfFicheStockLine(models.TransientModel):
    _name = "faarf.fiche.stock.line"

    fiche_id = fields.Many2one("faarf.fiche.stock")
    code = fields.Char("Code")
    dte_entree = fields.Date("Date entrée")
    dte_sortie = fields.Date("Date sortie")
    matiere_id = fields.Many2one("faarf.bien.immo", "Désignation")
    entree = fields.Float("Entrée")
    sortie = fields.Float("Sortie")
    solde = fields.Float("Solde", compute='_mnt_total')
    observation = fields.Text("Observation")

    @api.depends('entree', 'sortie')
    def _mnt_total(self):
        for val in self:
            val.solde = val.entree - val.sortie
