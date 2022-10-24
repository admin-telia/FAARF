from odoo import fields, models


class FaarfCategorieImmo(models.Model):
    _name = "faarf.categorie.immo"
    _description = "Enregistrement des catégories d'immobilisation"

    name = fields.Char("Libellé", required=True)
    code = fields.Char("Code", size=3, required=True)
    description = fields.Text("Description")
    duree = fields.Integer("Durée", required=False)
    taux = fields.Integer("Taux", required=False)
    active = fields.Boolean("Actif", default=True)
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type Immo.", required=True)


class FaarfMarqueImmo(models.Model):
    _name = "faarf.marque.immo"
    _description = "Enregistrement des marques d'immobilisation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfModeleImmo(models.Model):
    _name = "faarf.modele.immo"
    _description = "Enregistrement des modeles d'immobilisation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfModeAcquisitionImmo(models.Model):
    _name = "faarf.mode.immo"
    _description = "Enregistrement des modes d'acquisition d'immobilisation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfDestinationImmo(models.Model):
    _name = "faarf.destination"
    _description = "Enregistrement des destinations"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfTypeSortie(models.Model):
    _name = "faarf.type.sortie"
    _description = "Enregistrement des types de sorties"

    type_id = fields.Selection([('1','Entrée'), ('2', 'Sortie')], string="Type", required=True)
    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfMagasinImmo(models.Model):
    _name = "faarf.magasin.immo"
    _description = "Enregistrement des magasins d'immobilisation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfTypeAmortissementImmo(models.Model):
    _name = "faarf.typeamortissement.immo"
    _description = "Enregistrement des typs d'amortissement d'acquisition d'immobilisation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfFormatBienImmo(models.Model):
    _name = "faarf.format.immo"
    _description = "Enregistrement des formats de biens"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfUniteImmo(models.Model):
    _name = "faarf.unite.immo"
    _description = "Enregistrement des unités de biens"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfSourceImmo(models.Model):
    _name = "faarf.source.immo"
    _description = "Enregistrement des sources de financement"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfBienImmo(models.Model):
    _name = "faarf.bien.immo"
    _description = "Enregistrement des biens"

    image = fields.Binary("Image")
    name = fields.Char("Libellé", required=True)
    type_immo = fields.Selection([('1', 'Immobilisation corporelle'), ('2', 'Immobilisation incorporelle')],
                                 string="Type Immo.", required=True)
    duree = fields.Integer("Durée (en année)", related='categorie_id.duree')
    categorie_id = fields.Many2one("faarf.categorie.immo", "Catégorie Immo.", required=True)
    concate_code = fields.Char("Sous code", required=True, size=6)
    observation = fields.Text("Note interne")
    active = fields.Boolean("Actif", default=True)
