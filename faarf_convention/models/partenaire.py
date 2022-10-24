from odoo import fields, models


class FaarfPartenaire(models.Model):
    _name = "faarf.partenaire"
    _description = "Enregistrement des partenariats"

    name = fields.Char("Nom", required=True)
    domaine_id = fields.Many2one("ref_secteur_activite", string="Domaine d'activité",
                                 required=True)
    adresse = fields.Char("Adresse", required=True)
    type_partenaire = fields.Many2one("faarf.type.partenaire", "Type de partenaire",
                                      required=True)
    telephone = fields.Char("Téléphone", required=True)
    mail = fields.Char("Mail", required=True)
    description = fields.Text("Autres informations")
    active = fields.Boolean("Actif", default=True)


class FaarfTypePartenaire(models.Model):
    _name = "faarf.type.partenaire"
    _description = "Enregistrement des type de partenaires"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfTypeHistorisation(models.Model):
    _name = "faarf.type.historisation"
    _description = "Enregistrement des type de historisations"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)
