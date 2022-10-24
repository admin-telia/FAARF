from odoo import fields, api, models, tools, _
import string
from datetime import datetime, date
import pdb
import calendar
from calendar import monthrange
from odoo.exceptions import UserError, ValidationError
from math import *


# Creation de la classe fonction avec ses attributs
class HrFonction(models.Model):
    _name = "hr_fonctionss"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe emploi avec ses attributs
class HrEmploi(models.Model):
    _name = "hr_emploi"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    code = fields.Char(string="Code", required=True)


# Creation de la classe service avec ses attributs
class RefService(models.Model):
    _name = "hr_service"
    x_direction_id = fields.Many2one('hr.department', 'Département/Direction', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    est_stock = fields.Selection([
        ('1', 'Oui'),
        ('2', 'Non'),
    ], string="Est Service du Stock ?", default='2', required=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe unité avec ses attributs
class RefUnite(models.Model):
    _name = "hr_unite"
    x_service_id = fields.Many2one('hr_service', 'Service', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe section avec ses attributs
class RefSection(models.Model):
    _name = "hr_section"
    x_unite_id = fields.Many2one('hr_unite', 'Unité', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# heritage type de contrat
class HrTypeContrats(models.Model):
    _name = 'hr_contract_type'

    name = fields.Char(string='Name', required=False)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)


# Creation de la classe nature  precompte avec ses attributs
class HrNature(models.Model):
    _name = "hr_nature"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of nature.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe motif cessation avec ses attributs
class HrMotif(models.Model):
    _name = "hr_motif"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of motif.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# creation table pour contenir le nombre d'année de depart a la retraite des employés
class HrNbreAnnee(models.Model):
    _name = 'hr_nbreannee'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    name = fields.Integer(string="Nombre année", required=True)


# Creation de la classe grille des contractuels du burkina faso avec ses attributs
class HrGrilleSalarialeContractuel(models.Model):
    _name = "hr_grillesalariale_contractuel"
    _rec_name = "x_salbase_ctrt"
    x_class_c_id = fields.Many2one('hr_classe', string='Classe')
    x_indice_c = fields.Float(string="Indice")
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_echellon_c_id = fields.Many2one('hr_echellon', string='Echelon', required=True)
    x_salbase_ctrt = fields.Float(string="Salaire Base", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    active = fields.Boolean(string="Etat", default=True)


# stage
class TypeStage(models.Model):
    _name = 'hr_type_stage'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of stage.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure",
                                 default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

# classe domaine de formation
class DomaineFormation(models.Model):
    _name = 'hr_domaine'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


class HrOrganisme(models.Model):
    _name = 'hr_organisme'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe lieu de stage
class HrLieuStag(models.Model):
    _name = 'hr_lieu'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)

#classe situation de famiille
class HrSituationFamille(models.Model):
    _name = 'hr_situationfamille'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string = "Libéllé court", required = True)
    lib_long = fields.Char(string = "Libellé long", size = 35, required = True)
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string = "Etat", default=True)