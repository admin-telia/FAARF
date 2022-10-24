from odoo import fields, models, api


class CreditProgDebloc(models.Model):
    """ """
    _name = "credit_prog_deblocage"
    _description = ""
    _order = 'date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Programme deblocage N°', required=False)
    libelle = fields.Char(string='Libellé', required=False)
    date_transfert = fields.Date(string='Date', required=False, default=fields.Date.context_today)
    date = fields.Date(string='Date création', required=False, default=fields.Date.context_today)
    date_deblocage = fields.Date(string='Date prévue déblocage', required=False, default=fields.Date.context_today)
    a_debloque = fields.Integer(string='A debloque', required=False)
    a_debloque = fields.Integer(string='debloque', required=False)

    gestionnaire_id = fields.Many2one('res.users', string='Gestionnaire', default=lambda self: self.env.user)
    superviseur_id = fields.Many2one('res.users', string='Superviseur', related="gestionnaire_id.x_superviseur_id")
    credit_ids = fields.Many2many('credit_credit', string='Credit_ids')

    montant = fields.Float(string="Montant Total", required=False, digits=(16, 0))
    montants = fields.Float(string="Montant Total", required=False, store=True, digits=(16, 0), compute="calcul_mtn")

    nbr_dossier = fields.Integer(string='Nombre de dossier', required=False, compute="calcul_mtn")
    dossier_decaisse = fields.Integer(string='Dossier débloqué', required=False, compute="calcul_mtn")

    commentaires = fields.Html(string='Commentaires', required=False)

    state = fields.Selection(string='Etat', readonly=True, default="N",
                             selection=
                             [('N', 'Brouillon'), ('V', 'Pour validation'),
                              ('PD', 'Pour émission chèque'),
                              ('CE', 'Chèque émis'), ], )

    @api.depends('credit_ids')
    def calcul_mtn(self):
        for val in self:
            m = 0
            i = 0
            for c in val.credit_ids:
                m = m + c.montant_accorde

                if c.state in ('DC', 'RB'):
                    i = i + 1

            val.dossier_decaisse = i
            val.montants = m
            val.nbr_dossier = len(val.credit_ids)

    # def afficher(self):
    #     credit_ids = self.env['credit_credit'].search([
    #         ('state', '=', 'DA'),
    #         ('gestionnaire_id', '=', self.gestionnaire_id.id),
    #     ])
    #     self.credit_ids = [(5, 0, 0)]
    #     self.sudo().write({'credit_ids': credit_ids})
    #     self.credit_ids = credit_ids

    def set_valider(self):
        for c in self.credit_ids:
            c.set_deblocage()
            self.state = 'V'

            self.date_transfert = fields.Date.context_today(self)

    def approuver(self):
        # for c in self.credit_ids:
        #     c.set_deblocage()

        self.date = fields.Date.context_today(self)
        self.state = 'PD'
        num_demande = self.env['ir.sequence'].next_by_code('deblocage.sequence.code') or 'New'
        self.name = num_demande

    # def check_emis(self):
    #     chequier = '1'
    #     cheque = '1236547896541236547'
    #     for c in self.credit_ids:
    #         c.set_cheque_emis(chequier, cheque)
    #     self.state = 'CE'

    def set_cheque_emis(self, chequier, cheque):
        for c in self.credit_ids:
            c.set_cheque_emis(chequier, cheque)
        self.state = 'CE'

    # def set_decaiss(self):
    #     for c in self.credit_ids:
    #         c.set_decaisser()
