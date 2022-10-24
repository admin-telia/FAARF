from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date



class FaarfOrdreEntree(models.Model):
    _name = "faarf.ordre.entree"

    name = fields.Char("N° Ordre entrée", readonly=True)
    dte = fields.Date("Date d'entrée", default=fields.Date.context_today, required=True)
    ref = fields.Char("Référence facture", required=True)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", required=True)
    fournisseur_id = fields.Many2one("ref_beneficiaire", "Fournisseur", required=True)
    mode_id = fields.Many2one("faarf.type.sortie", "Nature d'entrée", domain=[('type_id', '=', '1')], required=True)
    magasin_id = fields.Many2one("faarf.magasin.immo", "Magasin", required=True)
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative", required=True)
    source_id = fields.Many2one("faarf.source.immo", "Source financement", required=True)
    state = fields.Selection([('draft', 'Brouillon'), ('P', 'Projet OEM'), ('V', 'Validé'), ('A', 'Annulé')], string="Etat", required=True, default='draft')
    compte_matiere = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '5')]))
    ordre_matiere = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]), string="Exercice")
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    line_ids = fields.One2many("faarf.ordre.entree.line", "ordre_id")

    def numordre(self):

        num = 0
        for val in self.line_ids:
            num = num + 1
            ok = str(num).zfill(4)
            val.num_ordre = ok


    # Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
    """@api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id"""

    #Compteur d'ordre entrée en matiere
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

        self.env.cr.execute("""update faarf_ordre_entree_line set
        dte = %s where ordre_id = %s""", (self.dte, self.id))

    def valider_dfc(self):
        v_id = int(self.id)
        v_four = int(self.fournisseur_id)
        v_source = int(self.source_id)
        v_dte = self.dte
        v_type = int(self.mode_id)
        v_piece = int(self.piece_id)
        x_annee = str(self.dte.year)
        print("annee", x_annee)
        mag = int(self.magasin_id)


        self.env.cr.execute("""select l.* from faarf_ordre_entree_line l, faarf_ordre_entree e 
        where l.ordre_id = e.id and l.ordre_id = %d and l.state = 'N' """ % (v_id))
        for val in self.env.cr.dictfetchall():
            v_mat = val['matiere_id']
            v_qte = val['qte']
            v_code = val['code']
            v_unit = val['unite_id']
            v_mnt = val['valeur_unitaire']

            qte = int(v_qte + 1)

            for vals in range(1, qte):
                self.env['faarf.stock.immo'].create({
                    'code': v_code,
                    'matiere_id': v_mat,
                    'cmu': v_mnt,
                    'unite_id': v_unit,
                    'reste': 1,
                    'quantite': 1,
                    'magasin_id': mag,
                    'dte': v_dte,
                    'etat': 'NC',
                    'annee': x_annee,
                })
        self.state = 'V'


class FaarfOrdreEntreeLine(models.Model):
    _name = "faarf.ordre.entree.line"
    _rec_name = "matiere_id"

    ordre_id = fields.Many2one("faarf.ordre.entree", ondelete='cascade')
    num_ordre = fields.Char("N° Ordre", readonly=True, size=4)
    code = fields.Char("Sous code matière", readonly=True)
    matiere_id = fields.Many2one("faarf.bien.immo", string="Matière", required=True)
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type Immo.")
    unite_id = fields.Many2one("faarf.format.immo", required=True, string="Unité")
    qte = fields.Float("Quantité", required=True)
    valeur_unitaire = fields.Float("Valeur unitaire", required=True)
    valeur_totale = fields.Float("Valeur totale", compute='_mnt_total')
    decompte = fields.Char("Décompte")
    observation = fields.Text("Observation")
    cmu = fields.Float("CMUP")
    #infos recuperer
    mode_id = fields.Many2one("faarf.type.sortie", "Nature d'entrée")
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative")
    fournisseur_id = fields.Many2one("ref_beneficiaire")
    source_id = fields.Many2one("faarf.source.immo")
    dte = fields.Date("Date acquisition")
    annee = fields.Char("Char")
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validé'), ('D', 'Déclassé')], string="Etat", required=True, default='N')

    @api.onchange("matiere_id")
    def numcode(self):
        for val in self:
            if val.matiere_id:
                val.code = val.matiere_id.concate_code
                val.type_immo = val.matiere_id.type_immo

    @api.depends('qte', 'valeur_unitaire')
    def _mnt_total(self):
        for val in self:
            val.valeur_totale = val.qte * val.valeur_unitaire


class FaarfCompteurOem(models.Model):
    _name = "faarf.compteur.oem"

    x_exercice_id = fields.Many2one("ref_exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfCodification(models.Model):
    _name = "faarf.codification"

    name = fields.Char("Code Immo", readonly=True)
    id_matiere = fields.Many2one("faarf.bien.immo", "Désignation", readonly=True)
    direction_id = fields.Many2one("hr.department", string="Direction", readonly=True)
    valeur_unitaire = fields.Float("Valeur unitaire", readonly=True)
    dte_acquisition = fields.Date("Date acquisition", readonly=True)
    dte_service = fields.Date("Date service", readonly=True)
    fournisseur_id = fields.Many2one("ref_beneficiaire", readonly=True)
    source_id = fields.Many2one("faarf.source.immo", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Généré')], string="Etat", default='N')
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type", readonly=True)



class FaarfFicheImmo(models.Model):
    _name = "faarf.fiche.immo"
    _rec_name = "numero"

    dte_acquisition = fields.Date("Date acquisition", readonly=True)
    dte_service = fields.Date("Date mise service", readonly=True)
    numero = fields.Many2one("faarf.codification", "N° Identification", domain=[('state', '=', 'N')], required=True)
    matiere_id = fields.Many2one("faarf.bien.immo", "Désignation", readonly=True)
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type", readonly=True)
    type_amort = fields.Many2one("faarf.typeamortissement.immo", "Type Amortissement")
    marque_id = fields.Many2one("faarf.marque.immo", "Marque")
    fournisseur_id = fields.Many2one("ref_beneficiaire", "Fournisseur", readonly=True)
    prix_acquisition = fields.Float("Prix acquisition", readonly=True)
    source_id = fields.Many2one("faarf.source.immo", "Source financement", readonly=True)
    dte_sortie = fields.Date("Date de sortie", readonly=True)
    direction_id = fields.Many2one("hr.department", "Direction", readonly=True)
    annee = fields.Char("Année")
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Généré')], string="Etat", required=True, default='N')
    etat = fields.Selection([('NC', 'Non codifié'), ('C', 'Codifié')], string="Etat", required=True, default='NC')
    tableau_ids = fields.One2many("faarf.tableau", "fiche_id")

    @api.onchange('numero')
    def valeur(self):
        for val in self:
            val.dte_acquisition = val.numero.dte_acquisition
            val.dte_service = val.numero.dte_service
            val.matiere_id = val.numero.id_matiere
            val.source_id = val.numero.source_id
            val.fournisseur_id = val.numero.fournisseur_id
            val.direction_id = val.numero.direction_id
            val.type_immo = val.numero.type_immo
            val.prix_acquisition = val.numero.valeur_unitaire


    def valider(self):
        """Cela crée automatiquement le versement que le client doit payer pour
        en fonction de la date de début de paiement et du nombre de versements."""
        for fiche in self:
            if fiche.type_amort == False:
                raise ValidationError(_("Veuillez choissir un type d'amortissement."))
            elif fiche.type_amort.name == "AMORTISSEMENT LINEAIRE":
                print("type amoty", fiche.type_amort)
                fiche.tableau_ids.unlink()
                date_debut = fiche.dte_service
                taux = 100/fiche.matiere_id.duree
                print("taux", taux)
                montant = round(fiche.prix_acquisition * taux)/100
                print("montant", montant)
                j = 12
                i = 0
                while i < fiche.matiere_id.duree:
                    # Increment the added_date by given months
                    added_date = date_debut + relativedelta(months=j)
                    fiche.env.cr.execute(
                        """INSERT INTO faarf_tableau(fiche_id,dte_amort,amort_annuel,amort_cumul)  VALUES(%s,%s,%s,%s)""", (
                        self.id, added_date, montant, 0))

                    i = i + 1
                    j = j + 12

                self.state = 'V'
                self.maj()
            else:
                fiche.tableau_ids.unlink()
                date_debut = fiche.dte_service
                if fiche.matiere_id.duree <= 4:
                    taux = (1/fiche.matiere_id.duree)*1.5
                elif fiche.matiere_id.duree <= 6:
                    taux = (1/fiche.matiere_id.duree) * 2
                else:
                    taux = (1/fiche.matiere_id.duree) * 2.5

                montant = round(fiche.prix_acquisition * taux) / 100

                j = 12
                i = 0
                while i < fiche.matiere_id.duree:
                    # Increment the added_date by given months
                    added_date = date_debut + relativedelta(months=j)
                    fiche.env.cr.execute(
                        """INSERT INTO faarf_tableau(fiche_id,dte_amort,amort_annuel,amort_cumul)  VALUES(%s,%s,%s,%s)""",
                        (self.id, added_date, montant, 0))

                    i = i + 1
                    j = j + 12
                self.maj()
                self.state = 'V'

        return True

    def maj(self):
        num = int(self.numero)
        for x in self:
            x.env.cr.execute("update faarf_codification set state = 'V' where id = %d" %(num))


class FaarfTableau(models.Model):
    _name = "faarf.tableau"

    fiche_id = fields.Many2one("faarf.fiche.immo", ondelete='cascade')
    dte_amort = fields.Date("Date armotissement")
    amort_annuel = fields.Float("Amortissement")
    amort_cumul = fields.Float("Amortissement cumulé")


class FaarfRegistre(models.Model):
    _name = "faarf.registre"

    dte_acquisition = fields.Date("Date acquisition")
    dte_service = fields.Date("Date mise service")
    numero = fields.Char("N° Identif.")
    matiere_id = fields.Many2one("faarf.bien.immo", "Désignation")
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type")
    marque_id = fields.Many2one("faarf.marque.immo", "Marque")
    fournisseur_id = fields.Many2one("ref_fournisseur", "Fournisseur")
    prix_acquisition = fields.Float("Prix acquisition")
    source_id = fields.Many2one("faarf.source.immo", "Source financement")
    dte_sortie = fields.Date("Date de sortie")
    direction_id = fields.Many2one("ref_direction", "Direction")
    service_id = fields.Many2one("ref_service", "Service")
    observation = fields.Text("Observation")


class FaarfStockImmo(models.Model):
    _name = "faarf.stock.immo"
    _rec_name = "matiere_id"

    matiere_id = fields.Many2one("faarf.bien.immo", "Désignation")
    quantite = fields.Float("Quantité")
    montant = fields.Float("CMUP")
    unite_id = fields.Many2one("faarf.format.immo", string="Unité")
    reste = fields.Float("Reste")
    entree = fields.Float("Entrée")
    sortie = fields.Float("Sortie")
    cmu = fields.Float("CMU")
    code = fields.Char("Code")
    magasin_id = fields.Many2one("faarf.magasin.immo", "Magasin")
    piece_id = fields.Many2one("ref_piece_justificatives", "Piece Justificative")
    observation = fields.Text("Observation")
    dte = fields.Date("Date")
    annee = fields.Char()
    codification = fields.Char("Codification")
    etat = fields.Selection([('NC', 'Non codifié'), ('C', 'Codifié'), ('S', 'Sortie')], string="Etat", required=True, default='NC')
