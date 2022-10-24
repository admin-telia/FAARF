from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCreditAffectation(models.Model):
    """Definition de la table credit"""

    _name = 'credit_user_affectation'
    _rec_name = 'utilisateur'

    utilisateur = fields.Many2one('res.users', string='Utilisateur', required=True)
    x_user_role_id = fields.Many2one('ref_user_role', string='Fonction', required=True)
    role_code = fields.Char("code", related='x_user_role_id.code')
    x_superviseur_id = fields.Many2one('res.users', string='Superviseur', required=False)
    date_affectation = fields.Date(string='Date', required=False)
    affection_doc = fields.Binary(string="Acte",  )

    code_gestionnaire = fields.Char(string='Code Gestionnaire', required=False)
    cpte_gest = fields.Many2one(comodel_name='compta_plan_lines', string='Compte Client')

    x_zone_ids = fields.Many2many(comodel_name='ref_zone', string='Zone', required=False)
    x_region_ids = fields.Many2many(comodel_name='ref_region', string='Region', required=False)
    x_province_ids = fields.Many2many(comodel_name='ref_province', string='Province', required=False)
    x_departement_ids = fields.Many2many(comodel_name='ref_departement', string='Commune/département', required=False)
    x_village_ids = fields.Many2many(comodel_name='ref_village', string='Village/Secteur', required=False)

    state = fields.Selection([('N', 'N'), ('A', 'A'),
                              ],
                             string='Etat', readonly=True, default="N", )  # track_visibility='always')

    def valider(self):
        if self.x_user_role_id.code == 'ROLEGEST':
            users = self.env['res.users'].search(
                [('x_user_role_id.code', '=', 'ROLEGEST'), ('id', '!=', self.utilisateur.id)])
            for u in users:
                for v in u.x_village_ids:
                    if v.id in self.x_village_ids.ids:
                        raise models.ValidationError("Il y'a déja une gestionnaire dans ce secteur/village (" +
                                                     str(u.name) + " : " +
                                                     str(v.name) + ")")
        self.utilisateur.sudo().write({
            'x_user_role_id': self.x_user_role_id,
            'x_zone_ids': self.x_zone_ids,
            'x_region_ids': self.x_region_ids,
            'x_province_ids': self.x_province_ids,
            'x_departement_ids': self.x_departement_ids,
            'x_village_ids': self.x_village_ids,
            # 'cpte_user': self.cpte_gest,
        })

        if self.x_user_role_id.code == 'ROLEGEST':
            if not self.utilisateur.code_gestionnaire:
                gest_compteur = self.env['credit_compteur_gestionnaire'].search([])
                nombre = 1
                if gest_compteur:
                    nombre = gest_compteur.nombre + 1
                    gest_compteur.nombre = nombre
                    nombre = str(nombre).zfill(4)
                else:
                    self.env['credit_compteur_gestionnaire'].create({
                        'nombre': 1,
                        'code': "ROLEGEST"
                    })
                    nombre = str(nombre).zfill(4)

                self.utilisateur.sudo().write({
                    'code_gestionnaire': nombre,
                    'x_superviseur_id': self.x_superviseur_id,
                })

        users = self.env['res.users'].search([('id', '=', self.utilisateur.id)])
        group_id = self.env.ref('faarf_credit.group_service_client')
        group_id.users = [(4, user.id) for user in users]
        # group_id.users = [(3, user.id) for user in users] remove

        self.state = 'A'
        self.date_affectation = fields.Date.context_today(self)

    @api.onchange('utilisateur')
    def onchange_utilisateur(self):
        for val in self:
            val.x_user_role_id = None
            val.x_zone_ids = None
            val.x_region_ids = None
            val.x_province_ids = None
            val.x_departement_ids = None
            val.x_village_ids = None
            if val.utilisateur:
                users = self.env['res.users'].search([('id', '=', val.utilisateur.id)])
                for u in users:
                    val.x_user_role_id = u.x_user_role_id
                    val.x_superviseur_id = u.x_superviseur_id
                    val.x_zone_ids = u.x_zone_ids
                    val.x_region_ids = u.x_region_ids
                    val.x_province_ids = u.x_province_ids
                    val.x_departement_ids = u.x_departement_ids
                    val.x_village_ids = u.x_village_ids



    # @api.onchange('x_zone_ids')
    # def onchange_x_zone_ids(self):
    #     print("onchange_x_zone_ids")
    #     for val in self:
    #         val.x_region_ids = None
    #         val.x_province_ids = None
    #         val.x_departement_ids = None
    #         val.x_village_ids = None
    #
    # @api.onchange('x_region_ids')
    # def onchange_x_region_ids(self):
    #     print("onchange_x_region_ids")
    #     for val in self:
    #         val.x_province_ids = None
    #         val.x_departement_ids = None
    #         val.x_village_ids = None
    #
    # @api.onchange('x_province_ids')
    # def onchange_x_province_ids(self):
    #     for val in self:
    #         val.x_departement_ids = None
    #         val.x_village_ids = None
    #
    # @api.onchange('x_departement_ids')
    # def onchange_x_departement_ids(self):
    #     for val in self:
    #         val.x_village_ids = None