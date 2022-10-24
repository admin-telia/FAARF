from math import floor

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _inherit = 'credit_credit'

    #Amortissement lineaire
    def ta_normal(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        # date_debut = date_debut + relativedelta(months=1)
        periodicite = int(self.periodicite)

        montant = round(credit.montant_accorde / credit.nbr_tranche)
        interet = round(credit.montant_interet / credit.nbr_tranche)
        garantie = round(credit.montant_garantie / credit.nbr_tranche)
        date_debut = date_debut + relativedelta(months=periodicite)
        num = 1
        for i in range(1, credit.nbr_tranche):
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': garantie,
                'total': montant + interet + garantie,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=periodicite)
            num = num + 1

        montant = round(credit.montant_accorde - (montant * (credit.nbr_tranche - 1)))
        interet = round(credit.montant_interet - (interet * (credit.nbr_tranche - 1)))
        garantie = round(credit.montant_garantie - (garantie * (credit.nbr_tranche - 1)))
        credit.env['credit_credit_line'].create({
            'numero': num,
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': garantie,
            'total': montant + interet + garantie,
            'credit_id': credit.id
        })

    def ta_interet_decaiss(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        # date_debut = date_debut + relativedelta(months=1)
        periodicite = int(self.periodicite)
        garantie = round(credit.montant_garantie)
        interet = round(credit.montant_interet)
        num = 1
        credit.env['credit_credit_line'].create({
            'numero': num,
            'date': date_debut,
            'montant': 0,
            'interet': interet,
            'garantie': 0,
            'total': interet,
            'credit_id': credit.id
        })
        montant = round(credit.montant_accorde / credit.nbr_tranche)
        garantie = round(credit.montant_garantie / credit.nbr_tranche)

        date_debut = date_debut + relativedelta(months=periodicite)
        j = 0
        num = num + 1
        for i in range(1, credit.nbr_tranche):
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': 0,
                'garantie': garantie,
                'total': montant + garantie,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=periodicite)
            j = j + 1
            num = num + 1

        montant = round(credit.montant_accorde - (montant * j))
        garantie = round(credit.montant_garantie - (garantie * j))

        credit.env['credit_credit_line'].create({
            'numero': num,
            'date': date_debut,
            'montant': montant,
            'interet': 0,
            'garantie': garantie,
            'total': montant + garantie,
            'credit_id': credit.id
        })

    def ta_interet_debut(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        periodicite = int(self.periodicite)
        num = 1
        if credit.nbr_tranche == 1:
            date_debut = date_debut + relativedelta(months=periodicite)
            montant = round(credit.montant_accorde)
            interet = round(credit.montant_interet)
            garantie = round(credit.montant_garantie)
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': garantie,
                'total': garantie,
                'credit_id': credit.id
            })
            num = num + 1
        else:
            date_debut = date_debut + relativedelta(months=periodicite)
            garantie = round(credit.montant_garantie)
            interet = round(credit.montant_interet)
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': 0,
                'interet': interet,
                'garantie': 0,
                'total': interet,
                'credit_id': credit.id
            })
            num = num + 1
            montant = round(credit.montant_accorde / (credit.nbr_tranche - 1))
            interet = round(credit.montant_interet / (credit.nbr_tranche - 1))
            garantie = round(credit.montant_garantie / (credit.nbr_tranche - 1))

            date_debut = date_debut + relativedelta(months=periodicite)
            j = 0
            for i in range(1, credit.nbr_tranche - 1):
                credit.env['credit_credit_line'].create({
                    'numero': num,
                    'date': date_debut,
                    'montant': montant,
                    'interet': 0,
                    'garantie': garantie,
                    'total': montant + garantie,
                    'credit_id': credit.id
                })
                date_debut = date_debut + relativedelta(months=periodicite)
                j = j + 1
                num = num + 1

            montant = round(credit.montant_accorde - (montant * j))
            interet = round(credit.montant_interet - (interet * j))
            garantie = round(credit.montant_garantie - (garantie * j))

            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': 0,
                'garantie': garantie,
                'total': montant + garantie,
                'credit_id': credit.id
            })

    def ta_fa_decaiss(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        # date_debut = date_debut + relativedelta(months=1)
        periodicite = int(self.periodicite)
        garantie = round(credit.montant_garantie)
        num = 1
        credit.env['credit_credit_line'].create({
            'numero': num,
            'date': date_debut,
            'montant': 0,
            'interet': 0,
            'garantie': garantie,
            'total': garantie,
            'credit_id': credit.id
        })
        montant = round(credit.montant_accorde / credit.nbr_tranche)
        interet = round(credit.montant_interet / credit.nbr_tranche)

        date_debut = date_debut + relativedelta(months=periodicite)
        j = 0
        num = num + 1
        for i in range(1, credit.nbr_tranche):
            print("maxx")
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=periodicite)
            j = j + 1
            num = num + 1

        montant = round(credit.montant_accorde - (montant * j))
        interet = round(credit.montant_interet - (interet * j))

        credit.env['credit_credit_line'].create({
            'numero': num,
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': 0,
            'total': montant + interet,
            'credit_id': credit.id
        })

    def ta_fa_debut(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        periodicite = int(self.periodicite)
        num = 1
        if credit.nbr_tranche == 1:
            date_debut = date_debut + relativedelta(months=periodicite)
            montant = round(credit.montant_accorde)
            interet = round(credit.montant_interet)
            garantie = round(credit.montant_garantie)
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': garantie,
                'total': garantie,
                'credit_id': credit.id
            })
            num = num + 1
        else:
            date_debut = date_debut + relativedelta(months=periodicite)
            garantie = round(credit.montant_garantie)
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': 0,
                'interet': 0,
                'garantie': garantie,
                'total': garantie,
                'credit_id': credit.id
            })
            num = num + 1
            montant = round(credit.montant_accorde / (credit.nbr_tranche - 1))
            interet = round(credit.montant_interet / (credit.nbr_tranche - 1))

            date_debut = date_debut + relativedelta(months=periodicite)
            j = 0
            for i in range(1, credit.nbr_tranche - 1):
                credit.env['credit_credit_line'].create({
                    'numero': num,
                    'date': date_debut,
                    'montant': montant,
                    'interet': interet,
                    'garantie': 0,
                    'total': montant + interet,
                    'credit_id': credit.id
                })
                date_debut = date_debut + relativedelta(months=periodicite)
                j = j + 1
                num = num + 1

            montant = round(credit.montant_accorde - (montant * j))
            interet = round(credit.montant_interet - (interet * j))

            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })

    def ta_fa_decaiss2(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        # date_debut = date_debut + relativedelta(months=1)
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': 0,
            'interet': 0,
            'garantie': credit.montant_garantie,
            'total': credit.montant_garantie,
            'credit_id': credit.id
        })
        montant = round(credit.montant_accorde / (credit.nbr_tranche - 1))
        interet = round(credit.montant_interet / (credit.nbr_tranche - 1))
        date_debut = date_debut + relativedelta(months=1)
        for i in range(1, credit.nbr_tranche - 1):
            credit.env['credit_credit_line'].create({
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=1)

        montant = round(credit.montant_accorde - (montant * (credit.nbr_tranche - 2)))
        interet = round(credit.montant_interet - (interet * (credit.nbr_tranche - 2)))
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': 0,
            'total': montant + interet,
            'credit_id': credit.id
        })

    def ta_fa_debut2ta_fa_debut(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        date_debut = date_debut + relativedelta(months=1)
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': 0,
            'interet': 0,
            'garantie': credit.montant_garantie,
            'total': credit.montant_garantie,
            'credit_id': credit.id
        })
        montant = round(credit.montant_accorde / (credit.nbr_tranche - 1))
        interet = round(credit.montant_interet / (credit.nbr_tranche - 1))
        date_debut = date_debut + relativedelta(months=1)
        for i in range(1, credit.nbr_tranche - 1):
            credit.env['credit_credit_line'].create({
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=1)

        montant = round(credit.montant_accorde - (montant * (credit.nbr_tranche - 2)))
        interet = round(credit.montant_interet - (interet * (credit.nbr_tranche - 2)))
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': 0,
            'total': montant + interet,
            'credit_id': credit.id
        })

    def ta_unique_normal(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        date_debut = date_debut + relativedelta(months=credit.nbr_tranche)

        montant = credit.montant_accorde
        interet = credit.montant_interet
        garantie = credit.montant_garantie

        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': garantie,
            'total': montant + interet + garantie,
            'credit_id': credit.id
        })

    def ta_unique_fa_decaiss(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        montant = credit.montant_accorde
        interet = credit.montant_interet
        garantie = credit.montant_garantie

        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': 0,
            'interet': 0,
            'garantie': garantie,
            'total': garantie,
            'credit_id': credit.id
        })

        date_debut = date_debut + relativedelta(months=credit.nbr_tranche)
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': garantie,
            'total': montant + interet + garantie,
            'credit_id': credit.id
        })

    def ta_unique_fa_deb(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        montant = credit.montant_accorde
        interet = credit.montant_interet
        garantie = credit.montant_garantie

        date_debut = date_debut + relativedelta(months=1)
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': 0,
            'interet': 0,
            'garantie': garantie,
            'total': garantie,
            'credit_id': credit.id
        })

        date_debut = date_debut + relativedelta(months=credit.nbr_tranche)
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': garantie,
            'total': montant + interet + garantie,
            'credit_id': credit.id
        })

    def ta_unique_interet(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        date_debut = date_debut + relativedelta(months=1)

        montant = credit.montant_accorde
        interet = round(credit.montant_interet / credit.nbr_tranche)
        # garantie = round(credit.montant_garantie / credit.nbr_tranche)
        date_debut = date_debut + relativedelta(months=1)
        for i in range(1, credit.nbr_tranche):
            credit.env['credit_credit_line'].create({
                'date': date_debut,
                'montant': 0,
                'interet': interet,
                'garantie': 0,
                'total':  interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=1)

        interet = round(credit.montant_interet - (interet * (credit.nbr_tranche - 1)))
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': 0,
            'total': montant + interet,
            'credit_id': credit.id
        })

    def ta2(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')

        montant = round(credit.montant_accorde / credit.nbr_tranche)
        interet = round(credit.montant_interet / credit.nbr_tranche)

        date_debut = date_debut + relativedelta(months=1)
        for i in range(1, credit.nbr_tranche):
            credit.env['credit_credit_line'].create({
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=1)

        montant = round(credit.montant_accorde - (montant * (credit.nbr_tranche - 1)))
        interet = round(credit.montant_interet - (interet * (credit.nbr_tranche - 1)))
        credit.env['credit_credit_line'].create({
            'date': date_debut,
            'montant': montant,
            'interet': interet,
            'garantie': 0,
            'total': montant + interet,
            'credit_id': credit.id
        })

    # Amortissement degressif
    def ta_normal_degressif(self, credit):
        date_debut = datetime.strptime(str(credit.date_demande), '%Y-%m-%d')
        periodicite = int(self.periodicite)
        t_mensuel = (credit.taux_int_annuel / 100) / 12
        capital_restant = credit.montant_accorde

        num = 1
        somme_montant = 0
        somme_interet = 0
        for i in range(1, credit.nbr_tranche + 1):
            interet = round(capital_restant * t_mensuel)
            montant = credit.montant_mensualite - interet
            capital_restant = capital_restant - montant
            somme_montant = somme_montant + montant
            somme_interet = somme_interet + interet
            credit.env['credit_credit_line'].create({
                'numero': num,
                'date': date_debut,
                'montant': montant,
                'interet': interet,
                'garantie': 0,
                'total': montant + interet,
                'credit_id': credit.id
            })
            date_debut = date_debut + relativedelta(months=periodicite)
            num = num + 1

        # print(credit.montant_interet)
        # print(somme_interet)
        # montant = round(credit.montant_accorde - somme_montant)
        # interet = round(credit.montant_interet - somme_interet)
        # credit.env['credit_credit_line'].create({
        #     'numero': num,
        #     'date': date_debut,
        #     'montant': montant,
        #     'interet': interet,
        #     'garantie': 0,
        #     'total': montant + interet,
        #     'credit_id': credit.id
        # })