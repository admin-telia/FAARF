import time
from datetime import datetime
from odoo import fields, models, api, _
from odoo import exceptions
from odoo.exceptions import UserError


class HrAvanaceSalaire(models.Model):
    _name = 'hr_avance_salaire'
    _description = 'Description'

    name = fields.Char(string='Name', readonly=True, default=lambda self: 'AV/')
    employee_id = fields.Many2one('hr.employee', string='Employé', required=True, help="Employé")
    date = fields.Date(string='Date rembourssement', required=True, default=lambda self: fields.Date.today(),
                       help="Submit date")
    reason = fields.Text(string='Raison', help="Raison")
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    advance = fields.Float(string='Avance', required=True)
    mode_paiement = fields.Char(string='Mode de paiement')
    exceed_condition = fields.Boolean(string='Exceed than Maximum',
                                      help="The Advance is greater than the maximum percentage in salary structure")
    state = fields.Selection([('draft', 'Brouillon'),
                              ('submit', 'Envoyé'),
                              ('waiting_approval', 'En attente'),
                              ('approve', 'Approuvé'),
                              ('cancel', 'Annulé'),
                              ('reject', 'Rejeté'),
                              ('paid', 'Remboursé')], string='Status', default='draft', track_visibility='onchange')
    employee_contract_id = fields.Many2one('hr.contract', string='Contract')
    payslip_id = fields.Many2one('hr.payslip', string="Bulletin Ref.", help="Payslip")

    def submit_request(self):
        self.state = 'submit'

    def cancel(self):
        self.state = 'cancel'

    def reject(self):
        self.state = 'reject'

    def approve_request(self):
        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise UserError("L'avance peut être demandée q'une fois par mois.")
        if not self.employee_contract_id:
            raise UserError("Définir un contrat pour l'employé.")

        adv = self.advance
        amt = self.employee_contract_id.x_net_payer
        if adv > amt and not self.exceed_condition:
            raise UserError("Le montant de l'avance est supérieur à celui alloué")

        if not self.advance:
            raise UserError("Vous devez entrer le montant de l'avance sur salaire")
        payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id),
                                                     ('state', '=', 'done'), ('date_from', '<=', self.date),
                                                     ('date_to', '>=', self.date)])
        if payslip_obj:
            raise UserError("Le salaire de ce mois a été déjà calculé")

        self.state = 'approve'
        self.name = self.env['ir.sequence'].get('salary.advance.seq') or ' '


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    avance_salaire_id = fields.Many2one('hr_avance_salaire', string="Avance sur salaire", help="Avance sur salaire")


class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'

    avance_salaire_id = fields.Many2one('hr_avance_salaire', string="Avance sur salaire", help="Avance sur salaire")

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(SalaryRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        adv_salary = self.env['hr_avance_salaire'].search([('employee_id', '=', emp_id.id)])
        for adv_obj in adv_salary:
            current_date = date_from.month
            date = adv_obj.date
            existing_date = date.month
            if current_date == existing_date:
                state = adv_obj.state
                amount = adv_obj.advance
                for result in res:
                    if state == 'approve' and amount != 0 and result.get('code') == 'SAR':
                        result['amount'] = amount
                        self.avance_salaire_id = adv_obj
        return res

    def action_payslip_done(self):
        if self.avance_salaire_id:
            self.avance_salaire_id.state = 'paid'
            self.avance_salaire_id.payslip_id = self
        return super(SalaryRuleInput, self).action_payslip_done()
