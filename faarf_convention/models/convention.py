from odoo import fields, models


class FaarfDemandePartenariat(models.Model):
    _name = "faarf.demande.partenariat"

    partenaire_id = fields.Many2one("faarf.partenaire", "Partenaire", required=True)
    name = fields.Char("N° demande", readonly=True)
    objet = fields.Text("Objet", required=True)
    dte_dmde = fields.Date("Date", default=fields.Date.context_today, required=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validée'), ('R', 'Rejétée'), ('C', 'Convention signée')],
                             string="Etat", required=True, default='N')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    fichier_ids = fields.One2many("faarf.demande.partenariat.line", "dmde_id")

    def valider(self):
        val_struct = int(self.company_id)

        self.env.cr.execute(
            "select numero from faarf_compteur_dmde where company_id = %d" % val_struct)
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_dmde(company_id,numero) VALUES(%d, %d)""" % (val_struct, vals))
            self.state = 'V'
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_dmde SET numero = %d WHERE company_id = %d" % (vals, val_struct))
            self.state = 'V'


class FaarfDemandePartenariatLine(models.Model):
    _name = "faarf.demande.partenariat.line"

    dmde_id = fields.Many2one("faarf.demande.partenariat", ondelete='cascade')
    libelle = fields.Char("Libellé", required=True)
    fichier_id = fields.Binary("Fichiers joints", required=True)


#class FaarfVisuPartenariat(models.Model):
#    _name = "faarf.visu.partenariat"


class FaarfConvention(models.Model):
    _name = "faarf.convention"

    name = fields.Char("N° Convention", readonly=True)
    demande_id = fields.Many2one("faarf.demande.partenariat", domain=[('state', '=', 'V')],
                                 string="N° Demande", required=True)
    dte_dmde = fields.Date("Date convention", default=fields.Date.context_today, required=True)
    dte_debut = fields.Date("Date debut", required=True)
    dte_fin = fields.Date("Date fin", required=True)
    resume = fields.Text("Résumé", required=True)
    state = fields.Selection([('N', 'Nouveau'), ('E', 'En cours'), ('R', 'Renouvellé'), ('A', 'Annulée')],
                             string="Etat", required=True, default='N')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    fichier_ids = fields.One2many("faarf.convention.line", "convention_id")

    def valider(self):
        val_struct = int(self.company_id)
        v_id = int(self.demande_id)
        self.env.cr.execute(
            "select numero from faarf_compteur_conv where company_id = %d" % val_struct)
        nu = self.env.cr.fetchone()
        num = nu and nu[0] or 0
        c1 = int(num) + 1
        c = str(num)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO faarf_compteur_conv(company_id,numero) VALUES(%d, %d)""" % (val_struct, vals))
            self.state = 'E'
        else:
            c1 = int(num) + 1
            ok = str(c1).zfill(4)
            self.name = ok
            vals = c1
            self.env.cr.execute(
                "UPDATE faarf_compteur_conv SET numero = %d WHERE company_id = %d" % (vals, val_struct))
            self.state = 'E'

        self.env.cr.execute("update faarf_demande_partenariat set state = 'C' where id = %d" % v_id)

    def renouveller(self):
        self.state = 'E'

    def annuler(self):
        self.state = 'E'


class FaarfConventionLine(models.Model):
    _name = "faarf.convention.line"

    convention_id = fields.Many2one("faarf.convention", ondelete='cascade')
    libelle = fields.Char("Libellé", required=True)
    fichier_id = fields.Binary("Fichiers joints", required=True)


class FaarfCompDmde(models.Model):
    _name = "faarf.compteur.dmde"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfCompConvention(models.Model):
    _name = "faarf.compteur.conv"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    numero = fields.Integer(default=0)


class FaarfHistorisation(models.Model):
    _name = "faarf.historisation"

    name = fields.Many2one("faarf.partenaire", "Partenaire", required=True)
    dte_hist = fields.Date("Date", default=fields.Date.context_today, required=True)
    type_hist = fields.Many2one("faarf.type.historisation", string="Type d'échange", required=True)
    observation = fields.Text("Résumé", required=True)
    state = fields.Selection([('N', 'Nouveau'), ('V', 'Validé')], string="Etat", default='N')

    def valider(self):
        self.state = 'V'
