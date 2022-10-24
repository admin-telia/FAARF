from odoo import fields, api, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from num2words import num2words


# classe type conge
class HrEmployeeRegistre(models.Model):
    _name = 'hr_employee_registre'

    name = fields.Char(string='Name', required=False, default="Registre des employés")
    struct_ids = fields.Many2many(comodel_name='hr.payroll.structure', string='Type employé', required=False)
    department_ids = fields.Many2many(comodel_name='hr.department', string='Direction', required=False)
    x_emploi_ids = fields.Many2many(comodel_name='hr_emploi', string='Emploi', required=False)
    x_fonction_ids = fields.Many2many(comodel_name='hr_fonctionss', string='Fonction', required=False)

    line_ids = fields.One2many(comodel_name='hr_employee_registre_line', inverse_name='line_id',
                               string='Line_ids', required=False)

    def set_afficher(self):
        domain = []
        if self.struct_ids:
            domain.append(('struct_id', 'in', self.struct_ids.ids))
        if self.department_ids:
            domain.append(('department_id', 'in', self.department_ids.ids))
        if self.x_emploi_ids:
            domain.append(('x_emploi_id', 'in', self.x_emploi_ids.ids))
        if self.x_fonction_ids:
            domain.append(('x_fonction_id', 'in', self.x_fonction_ids.ids))

        employees = self.env['hr.employee'].search(domain)

        self.line_ids.unlink()
        ordre = 1
        for e in employees:
            self.env['hr_employee_registre_line'].create({
                'ordre': ordre,
                'name': e.name,
                'matricule_genere': e.matricule_genere,
                'direction': e.department_id.name,
                'type': e.struct_id.name,
                'fonction': e.x_emploi_id.name,
                'emploi': e.x_fonction_id.name,
                'categorie': e.x_categorie_c_id.name,
                'echelle': e.x_echelle_c_id.name,
                'echelon': e.x_echellon_c_id.name,
                'line_id': self.id,
            })
            ordre = ordre + 1


class HrEmployeeRegistreLine(models.Model):
    _name = 'hr_employee_registre_line'

    ordre = fields.Integer(string='Ordre', required=False)
    name = fields.Char(string='Nom et Prénoms', required=False)
    matricule_genere = fields.Char(string="Matricule")
    type = fields.Char(string='Nom et Prénoms', required=False)
    direction = fields.Char(string='Nom et Prénoms', required=False)
    fonction = fields.Char(string="Fonction")
    emploi = fields.Char(string="Emploi")
    categorie = fields.Char(string="Catégorie")
    echelle = fields.Char(string="Echelle")
    echelon = fields.Char(string="Echelon")

    line_id = fields.Many2one(
        comodel_name='hr_employee_registre',
        string='Line_id',
        required=False)
