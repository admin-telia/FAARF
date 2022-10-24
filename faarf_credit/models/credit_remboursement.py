from odoo import fields, models, api
from odoo.exceptions import ValidationError
from num2words import num2words


class CreditCreditRemboursement(models.TransientModel):
    """ """
    _name = "credit_credit_remboursement"
    _description = ""

    credit_id = fields.Many2one('credit_credit', string='Crédit N°', required=False)
    date_dernier_remb = fields.Date(string="Date derniere remboursement", required=False, )
    date = fields.Date(string="Date", required=False, default=fields.Date.context_today)
    nbr_echeance = fields.Integer(
        string='Nb écheance restante',
        required=False)
    cliente = fields.Char(string='Cliente', required=False, related="credit_id.cliente_id.name")
    is_affiche = fields.Boolean(string='Is_affiche', required=False, default=False)

    datep = fields.Integer(
        string='Retard',
        required=False)

    penalite = fields.Float(string="Pénalités dues", required=False, digits=(16, 0))

    montant = fields.Float(string="Principal dû", required=False, digits=(16, 0))
    interet = fields.Float(string="interêt dû", required=False, digits=(16, 0))
    garantie = fields.Float(string="Garantie dû", required=False, digits=(16, 0))
    total = fields.Float(string="Total", required=False, digits=(16, 0))

    montant_p_arriere = fields.Float(string="Principal en arriérés", required=False, digits=(16, 0))
    interet_arriere = fields.Float(string="interêt en arriérés", required=False, digits=(16, 0))
    garantie_arriere = fields.Float(string="Garantie en arriérés", required=False, digits=(16, 0))
    montant_t_arriere = fields.Float(string="Total arriere", required=False, digits=(16, 0))

    montant_total = fields.Float(string="Montant Total", required=False, digits=(16, 0), )  # montant total du credit

    montant_p_paye = fields.Float(string="Principal Payé", required=False, digits=(16, 0), )
    interet_paye = fields.Float(string="Interet Payé", required=False, digits=(16, 0), )
    garantie_paye = fields.Float(string="Garantie Payé", required=False, digits=(16, 0), )
    montant_t_paye = fields.Float(string="Montant Payé", required=False, digits=(16, 0), )  # montant total deja paye

    solde = fields.Float(string='Solde', required=False, digits=(16, 0), )

    penalite_p = fields.Float(string="Pénalités dues", required=False, digits=(16, 0),
                              compute="compute_a_payer2")
    interet_arriere_p = fields.Float(string="interêt en arriérés", required=False, digits=(16, 0),
                                     compute="compute_a_payer2")
    montant_p_arriere_p = fields.Float(string="Principal en arriérés", required=False, digits=(16, 0),
                                       compute="compute_a_payer2")
    garantie_arriere_p = fields.Float(string="Garantie en arriérés", required=False, digits=(16, 0),
                                      compute="compute_a_payer2")
    interet_p = fields.Float(string="interêt dû", required=False, digits=(16, 0),
                             compute="compute_a_payer2")
    montant_p = fields.Float(string="Principal dû", required=False, digits=(16, 0),
                             compute="compute_a_payer2")
    garantie_p = fields.Float(string="Garantie dû", required=False, digits=(16, 0),
                              compute="compute_a_payer2")

    interet_anticipe = fields.Float(string="interêt payé anticipativement", required=False, digits=(16, 0),
                                    compute="compute_a_payer2")
    montant_anticipe = fields.Float(string="Principal remboursé anticipativement", required=False, digits=(16, 0),
                                    compute="compute_a_payer2")
    garantie_anticipe = fields.Float(string="Garantie remboursé anticipativement", required=False, digits=(16, 0),
                                     compute="compute_a_payer2")

    montant_a_payer = fields.Float(string="Montant versé", required=False, digits=(16, 0), )
    montant_t_a_payer = fields.Float(string="Montant total à payer", required=False, digits=(16, 0), )

    montant_arriere = fields.Float(string="Montant arriere", required=False, digits=(16, 0), )
    date_arriere = fields.Date(string="Date arriere", required=False,)

    @api.onchange('credit_id')
    def calcul_solde(self):
        """Cette fonction permet de calculer le montant total du credit le principal, l'interet et la garantie deja
        payé """

        self.is_affiche = False
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
        self.montant_arriere = 0

        # arriere
        montant_p_paye = self.montant_p_paye
        montant_t_paye = self.montant_t_paye
        is_date = 1
        date = 0
        for l in ta:
            principal_total += l['montant']
            interet_total += l['interet']
            garantie_total += l['garantie']
            montant_total += l['total']

            # calcul de la date l'arriere
            montant_p_paye = montant_p_paye - l['montant']
            montant_t_paye = montant_t_paye - l['total']
            mnt_arriere = 0
            if montant_t_paye < 0:
                if is_date:
                    date = l['date']
                    is_date = 0
                    print(l['date'])

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

        if date and ((self.date - date).days >= 30):
            self.datep = (self.date - date).days
            mois = round((self.date - date).days / 30)
            self.penalite = round((self.montant_p_arriere * 1) / 100) * mois

            print(mois)

        # print((self.date - date).days)
        # arriere
        ta = self.env['credit_credit_line'].search([
            ('credit_id.id', '=', self.credit_id.id),
            ('date', '<', self.date)])
        montant_p_paye = self.montant_p_paye
        interet_paye = self.interet_paye
        garantie_paye = self.garantie_paye
        montant_t_paye = self.montant_t_paye

        tpenalite = 0
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



        if tpenalite > 0:
            self.datep = (self.date - date).days
            mois = round((self.date - date).days / 30)
            self.penalite = round((tpenalite * 1) / 100) * mois

            self.montant_arriere = tpenalite
            self.date_arriere = date
            print(self.montant_arriere)

        self.montant_a_payer = (self.penalite
                                + self.interet_arriere + self.montant_p_arriere + self.garantie_arriere
                                + self.interet + self.montant + self.garantie)

        self.montant_t_a_payer = self.montant_a_payer

    def payer(self):
        self.is_affiche = True
        interet = self.interet_arriere_p + self.interet_p + self.interet_anticipe
        montant = self.montant_p_arriere_p + self.montant_p + self.montant_anticipe
        garantie = self.garantie_arriere_p + self.garantie_p + self.garantie_anticipe

        if not (interet or montant or garantie):
            raise models.ValidationError("Les montants à payer ne peuvent pas ếtre null")

        annee = int(fields.datetime.now().year)
        rb_compteur = self.env['credit_compt_remb_line'].search(
            [('annee', '=', annee)])
        nombre = 1
        if rb_compteur:
            nombre = rb_compteur.nombre + 1
            rb_compteur.nombre = nombre
            nombre = str(nombre).zfill(8)
        else:
            self.env['credit_compt_remb_line'].create({
                'nombre': 1,
                'annee': annee
            })
            nombre = str(nombre).zfill(8)

        r = self.env['credit_credit_remboursement_line'].create({
            'date': self.date,
            'montant_p': montant,
            'interet_p': interet,
            'garantie_p': garantie,
            'penalite_p': self.penalite_p,
            'transaction': nombre,
            'annee': annee,
            'credit_id': self.credit_id.id
        })

        # if garantie:
        #     self.env['credit_client_garantie'].create({
        #         'cliente_id': self.credit_id.cliente_id.id,
        #         'credit_id': self.credit_id.id,
        #         'date': fields.Datetime.now(),
        #         'piece_comptable': num_trans,
        #         'montant': garantie,
        #     })

        self.onchange_date()
        self.penalite = 0
        self.interet_arriere = 0
        self.montant_p_arriere = 0
        self.interet = 0
        self.montant = 0

        if (montant + interet + garantie) == self.solde:
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

    # mohamed
    def ecriture_remboursement(self):

            v_ex = int(self.x_exercice_id)
            v_struct = int(self.company_id)
            dte = self.date
            num_cred = self.credit_id.num_appro

            garantie = self.garantie_arriere_p + self.garantie_p + self.garantie_anticipe
            mt_p = self.montant_p_arriere_p + self.montant_p + self.montant_anticipe
            interet = self.interet_arriere_p + self.interet_p + self.interet_anticipe

            penalite = self.penalite_p
            total = self.montant_a_paye

            cpte_capital = int(self.credit_id.produit_credit.capital.souscpte.id)
            cpte_penalite = int(self.credit_id.produit_credit.cpte_penalite.souscpte.id)

            cpte_membre = int(self.credit_id.produit_credit.cpte_membr.souscpte.id)

            self.env.cr.execute(
                "select no_ecr,no_lecr from compta_compteur_ecr where x_exercice_id = %d and company_id = %d" % (
                    v_ex, v_struct))
            noecr = self.env.cr.dictfetchall()
            no_ecrs = noecr and noecr[0]['no_ecr']
            no_ecrs1 = noecr and noecr[0]['no_lecr']
            no_ecr = no_ecrs
            no_lecrs = no_ecrs1

            for val in self:

                if not no_ecr:
                    no_ecr = 1
                    no_lecrs = 1

                    # Ecriture de remboursement
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'D', 'P') """, (
                        no_ecr, no_lecrs, cpte_membre, num_cred, total, v_ex, v_struct, dte))

                    no_lecrs1 = no_lecrs + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                        (no_ecr, no_lecrs1, cpte_membre, num_cred, interet, v_ex, v_struct, dte))

                    no_lecrs2 = no_lecrs1 + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                        (no_ecr, no_lecrs2, cpte_capital, num_cred, mt_p, v_ex, v_struct, dte))

                    if penalite != 0:
                        no_lecrs3 = no_lecrs2 + 1
                        self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                            (no_ecr, no_lecrs3, cpte_penalite, num_cred, penalite, v_ex, v_struct, dte))

                        self.env.cr.execute(
                            """INSERT INTO compta_compteur_ecr(x_exercice_id,company_id,no_ecr,no_lecr) VALUES(%d, %d, %d,%d)""" % (
                                v_ex, v_struct, no_ecr, no_lecrs3))
                    else:
                        self.env.cr.execute(
                            """INSERT INTO compta_compteur_ecr(x_exercice_id,company_id,no_ecr,no_lecr) VALUES(%d, %d, %d,%d)""" % (
                                v_ex, v_struct, no_ecr, no_lecrs2))
                else:
                    no_ecr = no_ecr + 1
                    no_lecrs = no_lecrs + 1

                    # Ecriture de remboursement
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'D', 'P') """, (
                        no_ecr, no_lecrs, cpte_membre, num_cred, total, v_ex, v_struct, dte))

                    no_lecrs1 = no_lecrs + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                        (no_ecr, no_lecrs1, cpte_membre, num_cred, interet, v_ex, v_struct, dte))

                    no_lecrs2 = no_lecrs1 + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                        (no_ecr, no_lecrs2, cpte_capital, num_cred, mt_p, v_ex, v_struct, dte))

                    if penalite != 0:
                        no_lecrs3 = no_lecrs2 + 1
                        self.env.cr.execute("""INSERT INTO compta_ligne_ecriture (no_ecr, no_lecr, no_souscptes, type_pj, ref_pj, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens,fg_etat) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'C', 'P') """,
                                            (no_ecr, no_lecrs3, cpte_penalite, num_cred, penalite, v_ex, v_struct, dte))

                        self.env.cr.execute(
                            "UPDATE compta_compteur_ecr SET no_ecr = %d, no_lecr = %d WHERE x_exercice_id = %d and company_id = %d" % (
                                no_ecr, no_lecrs3, v_ex, v_struct))
                    else:
                        self.env.cr.execute(
                            "UPDATE compta_compteur_ecr SET no_ecr = %d, no_lecr = %d WHERE x_exercice_id = %d and company_id = %d" % (
                                no_ecr, no_lecrs2, v_ex, v_struct))


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
    annee = fields.Char(string='Annee', required=False)
    caissiere_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    montant_total = fields.Float(string="Montant total", required=False, digits=(16, 0), compute="cal_montant_total")
    mtn_lettre = fields.Char(string='Mtn_lettre',required=False, compute="cal_montant_total")

    @api.depends('montant_p', 'garantie_p', 'interet_p', 'penalite_p')
    def cal_montant_total(self):
        for val in self:
            val.montant_total = val.montant_p + val.interet_p + val.garantie_p + val.penalite_p
            val.mtn_lettre = num2words(val.montant_total, lang='fr')
