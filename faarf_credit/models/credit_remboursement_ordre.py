from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CreditCreditRemboursement(models.TransientModel):
    """ """
    _inherit = "credit_credit_remboursement"
    _description = ""

    @api.depends('montant_a_payer')
    def compute_a_payer2(self):
        """En fonction du montant a payer on procede au paiement"""
        if self.montant_a_payer < 0:
            self.montant_a_payer = 0
        self.penalite_p = 0
        self.interet_arriere_p = 0
        self.montant_p_arriere_p = 0
        self.garantie_arriere_p = 0
        self.interet_p = 0
        self.montant_p = 0
        self.garantie_p = 0
        self.interet_anticipe = 0
        self.montant_anticipe = 0
        self.garantie_anticipe = 0

        if self.montant_arriere:
            if self.montant_a_payer <= self.montant_arriere:
                montant_a_payer = self.montant_a_payer
                ta = self.env['credit_credit_line'].search([
                    ('credit_id.id', '=', self.credit_id.id),
                    ('date', '<', self.date)])
                montant_t_paye = self.montant_t_paye

                tpenalite = 0
                i = 0
                for l in ta:
                    if montant_t_paye <= 0:
                        tmp = l['total']
                    elif montant_t_paye > l['total']:
                        tmp = 0
                        montant_t_paye = montant_t_paye - l['total']
                    else:
                        tmp = l['total'] - montant_t_paye
                        montant_t_paye = 0

                    if (self.date - l['date']).days >= 30:
                        tpenalite = tpenalite + tmp

                    if montant_a_payer > 0 and tmp:
                        i = i + 1
                        montant_a_payer = montant_a_payer - tmp

                self.penalite = round((self.montant_a_payer * 1) / 100) * i
            else:
                date = self.date_arriere
                self.datep = (self.date - date).days
                mois = round((self.date - date).days / 30)
                self.penalite = round((self.montant_arriere * 1) / 100) * mois

        if self.credit_id.ordre_remboursment == '1':
            self.garantie_capital_interet()
        elif self.credit_id.ordre_remboursment == '2':
            self.garantie_interet_capital()
        elif self.credit_id.ordre_remboursment == '3':
            self.capital_interet_garantie()
        elif self.credit_id.ordre_remboursment == '4':
            self.capital_garantie_interet()
        elif self.credit_id.ordre_remboursment == '5':
            self.interet_capital_garantie()
        elif self.credit_id.ordre_remboursment == '6':
            self.interet_garantie_capital()
        else:
            self.garantie_capital_interet()

    def garantie_capital_interet(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

            # 3- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

            # 4- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

            # 6- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

            # 7- interet
            interet = l['interet']

            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

        """3- calcul des montant payees anticipe"""
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

        print(principal)
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '>', self.date)])
        self.interet_anticipe = 0
        self.montant_anticipe = 0
        self.garantie_anticipe = 0

        for l in ta:
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0
            print(l['montant'])
            print(principal)
            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

            ## 9 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

            ##10- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

    def garantie_interet_capital(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

            # 3- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

            # 4- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

            # 6- interet
            interet = l['interet']

            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

            # 7- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

        """3- calcul des montant payees anticipe"""
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
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0

            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

            ##9- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

            ## 10 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

    def capital_interet_garantie(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 3- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

            # 4- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 6- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

            # 7- interet
            interet = l['interet']

            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

        """3- calcul des montant payees anticipe"""
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
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0

            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ## 9 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

            ##10- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

    def capital_garantie_interet(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 3- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

            # 4- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 6- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

            # 7- interet
            interet = l['interet']

            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

        """3- calcul des montant payees anticipe"""
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
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0

            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ## 9 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

            ##10- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

    def interet_garantie_capital(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 4- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

            # 3- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 7- interet
            interet = l['interet']

            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

            # 6- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

        """3- calcul des montant payees anticipe"""
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
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0

            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ##10- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0

            ## 9 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

    def interet_capital_garantie(self):
        interet_paye = self.interet_paye
        montant_p_paye = self.montant_p_paye
        garantie_paye = self.garantie_paye

        reste = self.montant_a_payer

        # 1-Penalite
        if reste == 0:
            self.penalite_p = 0
        elif reste > self.penalite:
            self.penalite_p = self.penalite
            reste = reste - self.penalite
        else:
            self.penalite_p = reste
            reste = 0

        """1- on calcul les arrieres"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])

        for l in ta:
            # 4- interet Arriere
            interet_arriere = 0
            if interet_paye == 0:
                interet_arriere = l['interet']
            elif interet_paye > l['interet']:
                interet_arriere = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet_arriere = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_arriere_p = self.interet_arriere_p + 0
            elif reste > interet_arriere:
                self.interet_arriere_p = self.interet_arriere_p + interet_arriere
                reste = reste - interet_arriere
            else:
                self.interet_arriere_p = self.interet_arriere_p + reste
                reste = 0
            ########## fin interet ########

            # 3- principal Arriere
            montant_p_arriere = 0
            if montant_p_paye == 0:
                montant_p_arriere = l['montant']
            elif montant_p_paye > l['montant']:
                montant_p_arriere = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant_p_arriere = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p_arriere_p = self.montant_p_arriere_p + 0
            elif reste > montant_p_arriere:
                self.montant_p_arriere_p = self.montant_p_arriere_p + montant_p_arriere
                reste = reste - montant_p_arriere
            else:
                self.montant_p_arriere_p = self.montant_p_arriere_p + reste
                reste = 0
            ########## fin principal ########

            # 2- garantie arriere
            garantie_arriere = 0
            if garantie_paye == 0:
                garantie_arriere = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie_arriere = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie_arriere = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_arriere_p = self.garantie_arriere_p + 0
            elif reste > garantie_arriere:
                self.garantie_arriere_p = self.garantie_arriere_p + garantie_arriere
                reste = reste - garantie_arriere
            else:
                self.garantie_arriere_p = self.garantie_arriere_p + reste
                reste = 0
            ########## fin garantie ########

        """2- on calcul le montant a payer pour la journee"""
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '=', self.date)])
        for l in ta:
            # 7- interet
            interet = l['interet']
            if interet_paye == 0:
                interet = l['interet']
            elif interet_paye > l['interet']:
                interet = 0
                interet_paye = interet_paye - l['interet']
            else:
                interet = l['interet'] - interet_paye
                interet_paye = 0

            if reste == 0:
                self.interet_p = 0
            elif reste > interet:
                self.interet_p = interet
                reste = reste - interet
            else:
                self.interet_p = reste
                reste = 0
            ########## fin interet ########

            # 6- principal
            montant = l['montant']
            if montant_p_paye == 0:
                montant = l['montant']
            elif montant_p_paye > l['montant']:
                montant = 0
                montant_p_paye = montant_p_paye - l['montant']
            else:
                montant = l['montant'] - montant_p_paye
                montant_p_paye = 0

            if reste == 0:
                self.montant_p = 0
            elif reste > montant:
                self.montant_p = montant
                reste = reste - montant
            else:
                self.montant_p = reste
                reste = 0
            ########## fin principal ########

            # 5- garantie
            garantie = l['garantie']
            if garantie_paye == 0:
                garantie = l['garantie']
            elif garantie_paye > l['garantie']:
                garantie = 0
                garantie_paye = garantie_paye - l['garantie']
            else:
                garantie = l['garantie'] - garantie_paye
                garantie_paye = 0

            if reste == 0:
                self.garantie_p = 0
            elif reste > garantie:
                self.garantie_p = garantie
                reste = reste - garantie
            else:
                self.garantie_p = reste
                reste = 0
            ########## fin garantie ########

        """3- calcul des montant payees anticipe"""
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
            if interet <= 0:
                l_interet = l['interet']
            elif interet > l['interet']:
                l_interet = 0
                interet = interet - l['interet']
            else:
                l_interet = l['interet'] - interet
                interet = 0

            if principal <= 0:
                l_montant = l['montant']
            elif principal > l['montant']:
                l_montant = 0
                principal = principal - l['montant']
            else:
                l_montant = l['montant'] - principal
                principal = 0

            if garantie <= 0:
                l_garantie = l['garantie']
            elif garantie > l['garantie']:
                l_garantie = 0
                garantie = garantie - l['garantie']
            else:
                l_garantie = l['garantie'] - garantie
                garantie = 0

            ##10- interet
            if reste == 0:
                self.interet_anticipe = self.interet_anticipe + 0
            elif reste > l_interet:
                self.interet_anticipe = self.interet_anticipe + l_interet
                reste = reste - l_interet
            else:
                self.interet_anticipe = self.interet_anticipe + reste
                reste = 0

            ## 9 - capital
            if reste == 0:
                self.montant_anticipe = self.montant_anticipe + 0
            elif reste > l_montant:
                self.montant_anticipe = self.montant_anticipe + l_montant
                reste = reste - l_montant
            else:
                self.montant_anticipe = self.montant_anticipe + reste
                reste = 0

            ## 8-garantie
            if reste == 0:
                self.garantie_anticipe = self.garantie_anticipe + 0
            elif reste > l_garantie:
                self.garantie_anticipe = self.garantie_anticipe + l_garantie
                reste = reste - l_garantie
            else:
                self.garantie_anticipe = self.garantie_anticipe + reste
                reste = 0
