from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError

class CreditCompteurDemande(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compt_demande'

    type_client = fields.Many2one('credit_type_client', 'Type de client', required=False)
    nombre = fields.Integer(string='Nombre', required=False)


class CreditCompteurClient(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compteur_client'

    type_client = fields.Many2one('credit_type_client', 'Type de client', required=False)
    nombre = fields.Integer(string='Nombre', required=False)


class CreditCompteurGestionnaire(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compteur_gestionnaire'

    code = fields.Char(string='Code', required=False)
    nombre = fields.Integer(string='Nombre', required=False)


class CreditCompteurCredit(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compteur_credit'

    code_gestionnaire = fields.Char(string='Code Bailleur', required=False)
    nombre = fields.Integer(string='Nombre', required=False)


class CreditCompteurPv(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compteur_pv'

    nombre = fields.Integer(string='Nombre', required=False)


class CreditCompteurClientGarantie(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compt_client_garantie'

    nombre = fields.Integer(string='Nombre', required=False)

class CreditCompteurRemboursmentline(models.Model):
    """Definition de la table credit"""

    _name = 'credit_compt_remb_line'

    nombre = fields.Integer(string='Nombre', required=False)
    annee = fields.Integer(string='Annee', required=False)