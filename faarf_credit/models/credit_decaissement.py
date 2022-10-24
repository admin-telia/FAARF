from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CreditCreditRemboursement(models.TransientModel):
    """ """
    _name = "credit_credit_decaissement"
    _description = ""

    credit_id = fields.Many2one('credit_credit', string='Credit', required=False)
    date_dernier_remb = fields.Date(string="Date derniere remboursement", required=False, )
    date = fields.Date(string="Date", required=False, default=fields.Date.context_today)



    montant = fields.Float(string="Principal dû", required=False, digits=(16, 0))
    interet = fields.Float(string="interêt dû", required=False, digits=(16, 0))
    garantie = fields.Float(string="Garantie dû", required=False, digits=(16, 0))
    total = fields.Float(string="Total", required=False, digits=(16, 0))

    montant_p_arriere = fields.Float(string="Principal en arriérés", required=False, digits=(16, 0))
    interet_arriere = fields.Float(string="interêt en arriérés", required=False, digits=(16, 0))
    garantie_arriere = fields.Float(string="Garantie en arriérés", required=False, digits=(16, 0))
    montant_t_arriere = fields.Float(string="Total arriere", required=False, digits=(16, 0))


    montant_total = fields.Float(string="Montant Total", required=False, digits=(16, 0),) #montant total du credit

    montant_p_paye = fields.Float(string="Principal Payé", required=False, digits=(16, 0),)
    interet_paye = fields.Float(string="Interet Payé", required=False, digits=(16, 0),)
    garantie_paye = fields.Float(string="Garantie Payé", required=False, digits=(16, 0),)
    montant_t_paye = fields.Float(string="Montant Payé", required=False, digits=(16, 0),) #montant total deja paye

    solde = fields.Float(string='Solde', required=False, digits=(16, 0),)

    penalite_p = fields.Float(string="Pénalités dues", required=False, digits=(16, 0),
                              compute="compute_a_payer")
    interet_arriere_p = fields.Float(string="interêt en arriérés", required=False, digits=(16, 0),
                                     compute="compute_a_payer")
    montant_p_arriere_p = fields.Float(string="Principal en arriérés", required=False, digits=(16, 0),
                                       compute="compute_a_payer")
    garantie_arriere_p = fields.Float(string="Garantie en arriérés", required=False, digits=(16, 0),
                                      compute="compute_a_payer")
    interet_p = fields.Float(string="interêt dû", required=False, digits=(16, 0),
                             compute="compute_a_payer")
    montant_p = fields.Float(string="Principal dû", required=False, digits=(16, 0),
                             compute="compute_a_payer")
    garantie_p = fields.Float(string="Garantie dû", required=False, digits=(16, 0),
                              compute="compute_a_payer")

    interet_anticipe = fields.Float(string="interêt payé anticipativement", required=False, digits=(16, 0),
                                    compute="compute_a_payer")
    montant_anticipe = fields.Float(string="Principal remboursé anticipativement", required=False, digits=(16, 0),
                                    compute="compute_a_payer")
    garantie_anticipe = fields.Float(string="Garantie remboursé anticipativement", required=False, digits=(16, 0),
                                     compute="compute_a_payer")

    montant_a_payer = fields.Float(string="Montant total à payer", required=False, digits=(16, 0),)

    @api.onchange('credit_id')
    def calcul_solde(self):
        """Cette fonction permet de calculer le montant total du credit le principal, l'interet et la garantie deja
        payé """

        montant_total = 0
        ta = self.env['credit_credit_line'].search([('credit_id.id', '=', self.credit_id.id)])
        for l in ta:
            montant_total += l['total']

        self.montant_total = montant_total

        montant_p_paye = 0
        interet_paye = 0
        garantie_paye = 0
        rembours = self.env['credit_credit_remboursement_line'].search([('credit_id.id', '=', self.credit_id.id)])
        for l in rembours:
            montant_p_paye += l['montant_p']
            interet_paye += l['interet_p']
            garantie_paye += l['garantie_p']
            print(l['garantie_p'])

        print(garantie_paye)
        self.montant_p_paye = montant_p_paye
        self.interet_paye = interet_paye
        self.garantie_paye = garantie_paye
        self.montant_t_paye = montant_p_paye + interet_paye + garantie_paye

        self.solde = self.montant_total - self.montant_t_paye

        self.onchange_date()

    @api.onchange('date')
    def onchange_date(self):
        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])
        principal_total = 0
        interet_total = 0
        garantie_total = 0
        montant_total = 0
        self.penalite = 0

        #arriere
        montant_p_paye = self.montant_p_paye
        is_date = 1
        date = 0
        for l in ta:
            principal_total += l['montant']
            interet_total += l['interet']
            garantie_total += l['garantie']
            montant_total += l['total']

            # calcul de la date l'arriere
            montant_p_paye = montant_p_paye - l['montant']
            if montant_p_paye < 0:
                if is_date:
                    date = l['date']
                    is_date = 0

        result_p = self.montant_p_paye - principal_total
        result_int = self.interet_paye - interet_total
        result_garantie = self.garantie_paye - garantie_total
        result = self.montant_t_paye - montant_total

        self.montant_p_arriere = 0
        if result_p < 0:
            self.montant_p_arriere = result_p * -1

        self.interet_arriere = 0
        if result_int < 0:
            self.interet_arriere = result_int * -1

        self.garantie_arriere = 0
        if result_garantie < 0:
            self.garantie_arriere = result_garantie * -1

        self.montant_t_arriere = 0
        if result < 0:
            self.montant_t_arriere = result * -1

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])

        self.montant = 0
        self.interet = 0
        self.garantie = 0

        for l in ta:
            self.montant += l['montant']
            self.interet += l['interet']
            self.garantie += l['garantie']
            # self.montant_total += l['total']

        if result_int > 0:
            if result_int >= self.interet:
                self.interet = 0
            else:
                self.interet = self.interet - result_int

        if result_p > 0:
            if result_p >= self.montant:
                self.montant = 0
            else:
                self.montant = self.montant - result_p

        if result_garantie > 0:
            if result_garantie >= self.garantie:
                self.garantie = 0
            else:
                self.garantie = self.garantie - result_garantie


        if date and ((self.date - date).days > 30):
            print((self.date - date).days)
            self.datep = (self.date - date).days
            self.penalite = round((self.montant_p_arriere * 1) / 100)

        self.montant_a_payer = (self.penalite
                                + self.interet_arriere + self.montant_p_arriere + self.garantie_arriere
                                + self.interet + self.montant + self.garantie)

    @api.depends('montant_a_payer')
    def compute_a_payer(self):
        """En fonction du montant a payer on procede au paiement"""
        if self.montant_a_payer < 0:
            self.montant_a_payer = 0

        reste = self.montant_a_payer

        #1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        #2- interet Arriere
        if reste == 0:
            self.interet_arriere_p = 0
        elif reste > self.interet_arriere:
            self.interet_arriere_p = self.interet_arriere
            reste = reste - self.interet_arriere
        else:
            self.interet_arriere_p = reste
            reste = 0

        #3- principal Arriere
        if reste == 0:
            self.montant_p_arriere_p = 0
        elif reste > self.montant_p_arriere:
            self.montant_p_arriere_p = self.montant_p_arriere
            reste = reste - self.montant_p_arriere
        else:
            self.montant_p_arriere_p = reste
            reste = 0

        #4- garantie arriere
        if reste == 0:
            self.garantie_arriere_p = 0
        elif reste > self.garantie_arriere:
            self.garantie_arriere_p = self.garantie_arriere
            reste = reste - self.garantie_arriere
        else:
            self.garantie_arriere_p = reste
            reste = 0

        #5 - interet
        if reste == 0:
            self.interet_p = 0
        elif reste > self.interet:
            self.interet_p = self.interet
            reste = reste - self.interet
        else:
            self.interet_p = reste
            reste = 0

        #6- principal
        if reste == 0:
            self.montant_p = 0
        elif reste > self.montant:
            self.montant_p = self.montant
            reste = reste - self.montant
        else:
            self.montant_p = reste
            reste = 0

        # 7- garantie
        if reste == 0:
            self.garantie_p = 0
        elif reste > self.garantie:
            self.garantie_p = self.garantie
            reste = reste - self.garantie
        else:
            self.garantie_p = reste
            reste = 0

        #8- calcul des montant payees anticipe
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<=', self.date)])
        interet = self.interet_paye
        principal = self.montant_p_paye
        garantie = self.garantie_paye
        for l in ta:
            interet = interet - l['interet']
            principal = principal - l['montant']
            garantie = garantie - l['garantie']

        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '>', self.date)])
        self.interet_anticipe = 0
        self.montant_anticipe = 0
        self.garantie_anticipe = 0

        for l in ta:
            l_interet = 0
            l_montant = 0
            l_garantie = 0

            if interet >= l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            elif interet > 0:
                l_interet = l['interet'] - interet
                interet = 0
            else:
                l_interet = l['interet']

            if principal >= l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            elif principal > 0:
                l_montant = l['montant'] - principal
                principal = 0
            else:
                l_montant = l['montant']

            if garantie >= l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            elif garantie > 0:
                l_garantie = l['garantie'] - garantie
                garantie = 0
            else:
                l_garantie = l['garantie']

            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0


            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

    def payer(self):
        interet = self.interet_arriere_p + self.interet_p + self.interet_anticipe
        montant = self.montant_p_arriere_p + self.montant_p + self.montant_anticipe
        garantie = self.garantie_arriere_p + self.garantie_p + self.garantie_anticipe

        if not (interet or montant or garantie):
            raise models.ValidationError("Les montants à payer ne peuvent pas ếtre null")

        num_trans = self.env['ir.sequence'].next_by_code('transaction.sequence.code') or 'New'
        r = self.env['credit_credit_remboursement_line'].create({
            'date': self.date,
            'montant_p': montant,
            'interet_p': interet,
            'garantie_p': garantie,
            'penalite_p': self.penalite_p,
            'transaction': num_trans,
            'credit_id': self.credit_id.id
        })

        self.onchange_date()
        self.penalite = 0
        self.interet_arriere = 0
        self.montant_p_arriere = 0
        self.interet = 0
        self.montant = 0

        if (montant + interet) == self.solde:
            print("Le crédit est soldé")

        self.calcul_solde()
        return self.env.ref('faarf_credit.report_credit_remboursement_recu').report_action(r.id)

    def print_quotation(self):
        return self.env.ref('faarf_credit.report_credit_remboursement_recu').report_action(self)

    def create_notification(self, titre, message):
        ms = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': titre,
                'message': message,
                'type': 'success',  # types: success,warning,danger,info
                'sticky': False,  # True/False will display for few seconds if false
                'fadeout': 'slow',
            }
        }
        return ms


class CreditCreditRemboursement(models.Model):
    """ """
    _name = "credit_credit_remboursement_line"
    _description = ""

    credit_id = fields.Many2one('credit_credit', string='Credit', required=False)
    date = fields.Date(string="Date", required=False, )

    montant_p = fields.Float(string="Montant dû", required=False, digits=(16, 0))
    interet_p = fields.Float(string="interêt dû", required=False, digits=(16, 0))
    garantie_p = fields.Float(string="Garantie dû", required=False, digits=(16, 0))
    penalite_p = fields.Float(string="Pénalité dû", required=False, digits=(16, 0))
    transaction = fields.Char(string='Transaction', required=False)

