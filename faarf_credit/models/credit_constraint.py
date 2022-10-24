from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError

class CreditCredit(models.Model):
    """Definition de la table credit"""
    _inherit = 'credit_credit'

    @api.constrains('avis_gestionnaire')
    def _check_avis_gestionnaire(self):
        for rec in self:
            if rec.state == 'G':
                if rec.avis_gestionnaire == '':
                    raise models.ValidationError("Vous devez remplir votre avis avant de transmettre")


# class CreditClient(models.Model):
#     """Definition de la table credit"""
#
#     _inherit = 'credit_clients'

    # @api.constrains('nip')
    # def _check_nip(self):
    #     for rec in self:
    #         credit = self.env['credit_clients'].search([('nip', '=', rec.nip)])
    #         if credit:
    #             raise ValidationError("Le N.I.P doit être unique")
    #
    # @api.constrains('num_piece')
    # def _check_num_piece(self):
    #     for rec in self:
    #         credit = self.env['credit_clients'].search([('num_piece', '=', rec.num_piece)])
    #         if credit:
    #             raise ValidationError("Le numéro de la pièce doit être unique")
    #
    # @api.constrains('num_agrement')
    # def _check_num_agrement(self):
    #     for rec in self:
    #         credit = self.env['credit_clients'].search([('num_agrement', '=', rec.num_agrement)])
    #         if credit:
    #             raise ValidationError("Le numéro d'agrément/récépissé doit être unique")