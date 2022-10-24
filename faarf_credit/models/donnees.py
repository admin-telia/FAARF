from odoo import fields, models, api


class FaarfTypeClient(models.Model):
    """Definir un type de client."""

    _name = "credit_type_client"
    _description = "Faarf Type de client"
    _order = "code"

    name = fields.Char('Nom', required=True)
    code = fields.Char('Code', required=True)
    codification = fields.Char(string='Code', required=False)

    active = fields.Boolean('Actif', default=True, help="Activer un type de client")
    description = fields.Text('Description', help='Description')


class CreditSecteurActivite(models.Model):
    """ secteur d'activite """
    _name = 'credit_secteur_activite'
    _description = "Secteur d'activite"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)
    active = fields.Boolean('Actif', default=True, help="Activer une nature de prêt")
    description = fields.Text('Description', help='Description')


class CreditActivite(models.Model):
    """ domaine activite """
    _name = 'credit_activite'
    _description = "activite"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)
    secteur_id = fields.Many2one('', string='Secteur', required=False)
    active = fields.Boolean('Actif', default=True, help="Activer une nature de prêt")
    description = fields.Text('Description', help='Description')


class CreditObjetEmprunt(models.Model):
    """ Objet de l'emprunt """
    _name = 'credit_objet_emprunt'
    _description = "Objet de l'emprunt"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)
    active = fields.Boolean('Actif', default=True, help="Activer une nature de prêt")
    description = fields.Text('Description', help='Description')


class CreditBailleur(models.Model):
    """ Credit Bailleurs de fonds """
    _name = 'credit_bailleur'
    _description = "Credit Bailleurs de fonds"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)
    active = fields.Boolean('Actif', default=True, help="Activer une nature de prêt")
    description = fields.Text('Description', help='Description')


class CreditFonds(models.Model):
    """ Credit Bailleurs de fonds """
    _name = 'credit_fonds'
    _description = "fonds de credit"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)

    bailleur = fields.Many2one('credit_bailleur', string='Bailleur', required=False)

class CreditFonds(models.Model):
    """ Credit Bailleurs de fonds """
    _name = 'credit_periodicite'
    _description = "Périodicité"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)

class CreditProduit(models.Model):
    """Definition de la table produit credit"""

    _name = "credit_produit"
    _description = "Definition de la table produit credit"

    name = fields.Char(string='Libellé', required=False)


class CreditAssureur(models.Model):
    """ Credit Assureurs """
    _name = 'credit_assureur'
    _description = "Credit Assureurs"
    _order = "code"

    code = fields.Char('Code', required=False)
    name = fields.Char('Libellé', required=True)
    description = fields.Text('Description', help='Description')
