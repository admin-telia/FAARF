from odoo import fields, models, api


class CreditProgRestFa(models.Model):
    """ """
    _name = "credit_prog_rest_fa"
    _description = ""
    _order = 'date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Prog restitution N°', required=False)
    libelle = fields.Char(string='Libéllé', required=True)
    date = fields.Date(string='Date', required=False, default=fields.Date.context_today)
    date_deblocage = fields.Date(string='Date prévue restitution', required=False, default=fields.Date.context_today)

    ordre_ids = fields.Many2many(
        comodel_name='credit_garantie',
        string='Ordre')

    montant = fields.Float(string="Montant Total", required=False, digits=(16, 0), store=True, compute="calcul_mtn")

    nbr_dossier = fields.Integer(string='Nombre de dossier', required=False, compute="calcul_mtn")

    state = fields.Selection(string='Etat', readonly=True, default="N",
                             selection=
                             [('N', 'N'), ('PD', 'Programmé pour deblocage'),
                              ('CE', 'Chèque émis'), ], )

    @api.depends('ordre_ids')
    def calcul_mtn(self):
        for val in self:
            m = 0
            for c in val.ordre_ids:
                m = m + c.montant

            val.montant = m
            val.nbr_dossier = len(val.ordre_ids)

    def approuver(self):
        pass


