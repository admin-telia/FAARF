from datetime import date

from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    date_signature = fields.Date(string="Date signature acte/decision d'engagement")

    # # Informations professionnelles
    type_id = fields.Many2one(comodel_name='hr_contract_type', string='Type contrat')  # type contrat
    struct_id = fields.Many2one("hr.payroll.structure", string="Structure Salariale")  # type employe/srtuture salariale
