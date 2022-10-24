from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _inherit = 'credit_credit'