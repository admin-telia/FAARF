from odoo import fields, models


class FaarfModule(models.Model):
    _name = "faarf.module"
    _description = "Enregistrement des modules de formation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)


class FaarfElementBudget(models.Model):
    _name = "faarf.element.budget"
    _description = "Enregistrement des element du budget de formation"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")
    active = fields.Boolean("Actif", default=True)
