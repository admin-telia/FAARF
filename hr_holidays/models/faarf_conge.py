from odoo import fields, models, api


class FaarfCongeType(models.Model):
    """Definir un client."""

    _name = "faarf_conge_type"

    name = fields.Char(string='Libellé', required=False)
    code = fields.Char(string='Code', required=False)

class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    x_conge_type_id = fields.Many2one(comodel_name='faarf_conge_type',
                                       string=' Type de congé', required=False)

    x_exercice_id = fields.Many2one('ref_exercice',
                                    string="Exercice",
                                    default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))

    @api.onchange('x_conge_type_id', 'x_exercice_id')
    def calcul_name(self):
        for rec in self:
            if rec.x_conge_type_id.name and rec.x_exercice_id.name:
                rec.name = rec.x_conge_type_id.name + " " + rec.x_exercice_id.name


class HolidaysAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    x_employee_ids = fields.Many2many(
        comodel_name='hr.employee', string='Employés')

    x_decision_fichier = fields.Binary(string="Décision",)

    @api.onchange('holiday_status_id')
    def calcul_name(self):
        for rec in self:
            if rec.holiday_status_id:
                rec.name = rec.holiday_status_id.name

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    x_decision_fichier = fields.Binary(string="Décision", )

