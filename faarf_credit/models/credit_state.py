from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CreditCredit(models.Model):
    """Definition de la table credit"""

    _inherit = 'credit_credit'

    state = fields.Selection([('N', 'N'), ('G', 'G'),
                              ('S', 'S'),
                              ('CR', 'CR.'), ('CC', 'CC'),
                              ('DG', 'DG.'),
                              ('CCA', 'CCA.'),
                              ('DAJ', 'AJ'),  # demande ajournee
                              ('DR', 'REF'),  # demande rejet
                              ('DA', 'AC'),  # demande accord
                              ('PD', 'PD'),  # Programme debloc
                              ('CE', 'CE'),  # Cheque emis
                              ('DC', 'DC'),  # Demande Decaiss
                              ('RB', 'RB'),  # Rembourser

                              # Projet et programme
                              ('RC', 'RC'),  # Reception
                              ('NOT', 'NOT'),  # Notation
                              ('BEN', 'BEN'), # Choix benef

                              # Projet et programme
                              ('AN', 'AN'),  # Annuler
                              ],
                             string='Etat', readonly=True, default="N", )  # track_visibility='always')

    # tracabilite
    date_trans_clientele = fields.Date(string='Retour au service clientèle', required=False, track_visibility='always')
    date_trans_gest = fields.Date(string='Transférer à la gestionnaire', required=False, track_visibility='always')
    date_trans_sup = fields.Date(string='Transférer à la superviseur', required=False, track_visibility='always')
    date_retour_gest = fields.Date(string='Retour à la gestionnaire', required=False, track_visibility='always')
    date_trans_cr = fields.Date(string='Transférer comité régional', required=False, track_visibility='always')
    date_retour_sup = fields.Date(string='Retour à la superviseur', required=False, track_visibility='always')
    date_trans_cc = fields.Date(string='Transférer comité régional', required=False, track_visibility='always')
    date_trans_dg = fields.Date(string='Transférer DG', required=False, track_visibility='always')
    date_trans_cca = fields.Date(string='Transférer CCA', required=False, track_visibility='always')

    date_avis_gestionnaire = fields.Date(string='Date avis du gestionnaire', required=False, track_visibility='always')
    date_avis_commite_antenne = fields.Date(string='Date avis du ', required=False)
    date_avis_commite_credit = fields.Date(string='Date avis du ', required=False)
    date_avis_directrice = fields.Date(string='Date avis du ', required=False)
    date_avis_commite_ca = fields.Date(string='Date avis du', required=False)

    date_accord = fields.Date(string='Date_trans_gest', required=False)
    date_debloc = fields.Date(string='Date_trans_gest', required=False)
    date_cheque = fields.Date(string='Date_trans_gest', required=False)
    chequier = fields.Char(string='Chequier', required=False)
    cheque = fields.Char(string='Chequier', required=False)
    date_decaiss = fields.Date(string='Date_trans_gest', required=False)
    date_rembours = fields.Date(string='Date_trans_gest', required=False)

    is_alert = fields.Boolean(string='Is_alert', required=False, default=False)

    def search_credit(self):
        credits = self.env['credit_credit'].search([('id', '!=', self.id), ('state', 'not in',  ['RB', 'AN', 'DR'])])
        for c in credits:
            if self.type_client_code == 'IND':
                if c.type_client_code == 'IND':
                    if self.cliente_id.nip == c.cliente_id.nip:
                        raise ValidationError(
                            "La sollicitante " + str(self.cliente_id.name) + " a déjà un crédit en cours (Crédit N°:" +
                            str(c.name) + ")")
                else:
                    for m in c.membres_ids:
                        if self.cliente_id.nip == m.membre_id.nip:
                            raise ValidationError(
                                "La sollicitante " + str(
                                    self.cliente_id.name) + " a déjà un crédit en cours (Crédit N°:" +
                                str(c.name) + ")")
            else:
                for m in self.membres_ids:
                    if c.type_client_code == 'IND':
                        if m.membre_id.nip == c.cliente_id.nip:
                            raise ValidationError(
                                "La sollicitante " + str(
                                    m.membre_id.name) + " a déjà un crédit en cours (Crédit N°:" +
                                str(c.name) + ")")
                    else:
                        for ms in c.membres_ids:
                            if m.membre_id.nip == ms.membre_id.nip:
                                raise ValidationError(
                                    "La sollicitante " + str(
                                        m.membre_id.name) + " a déjà un crédit en cours (Crédit N°:" +
                                    str(c.name) + ")")

    # clientele
    def set_trans_gest(self):
        if self.state == 'N':
            # Rechercher si l'utilisateur a un credit encours
            self.search_credit()
            if self.num_demande == '-':
                dem_compteur = self.env['credit_compt_demande'].search(
                    [('type_client.codification', '=', self.cliente_id.type_client.codification)])
                nombre = 1
                if dem_compteur:
                    nombre = dem_compteur.nombre + 1
                    dem_compteur.nombre = nombre
                    nombre = str(nombre).zfill(8)
                else:
                    self.env['credit_compt_demande'].create({
                        'nombre': 1,
                        'type_client': self.cliente_id.type_client.id
                    })
                    nombre = str(nombre).zfill(8)
                num_demande = str(self.cliente_id.type_client.codification) + nombre
                self.write({
                    'state': 'G',
                    'num_demande': num_demande,
                    'date_trans_gest': fields.Date.context_today(self)
                })
            else:
                self.write({
                    'state': 'G',
                    'date_trans_gest': fields.Date.context_today(self)
                })

        # self.is_alert = True
        # self.is_alert = False
        # return self.create_notification("Succès", "Le dossier a été bien transféré")

    # gestionnaire
    def set_renvoi_clientele(self):
        if self.state == 'G':
            self.write({
                'state': 'N',
                'date_trans_clientele': fields.Date.context_today(self)
            })

    def set_trans_sup(self):
        if self.state == 'G':
            # Rechercher si l'utilisateur a un credit encours
            self.search_credit()
            if not len(self.compte_exploit_ids):
                raise ValidationError("Vous ne pouvez pas envoyer une demande sans compte d'exploitation")

            if not self.avis_gestionnaire:
                raise models.ValidationError("Vous devez remplir votre avis avant de transmettre")

            if self.type_client_code == 'ASS':
                if len(self.membres_ids) < self.produit_credit.n_min_membre_ass:
                    raise models.ValidationError("Le nombre de membres minimum est de "
                                                 + str(self.produit_credit.n_min_membre_ass))
                if len(self.membres_ids) > self.produit_credit.n_max_membre_ass:
                    raise models.ValidationError("Le nombre de membres maximum est de "
                                                 + str(self.produit_credit.n_max_membre_ass))

            if self.type_client_code == 'GROUP':
                if len(self.membres_ids) < self.produit_credit.n_min_membre_gs:
                    raise models.ValidationError("Le nombre de membres minimum est de "
                                                 + str(self.produit_credit.n_min_membre_gs))
                if len(self.membres_ids) > self.produit_credit.n_max_membre_gs:
                    raise models.ValidationError("Le nombre de membres maximum est de "
                                                 + str(self.produit_credit.n_max_membre_gs))

            self.sudo().write({
                'state': 'S',
                'date_avis_gestionnaire': fields.Date.context_today(self),
                'date_trans_sup': fields.Date.context_today(self)
            })

    # supeviseur
    def set_renvoi_gest(self):
        if self.state == 'S':
            self.sudo().write({
                'date_retour_gest': fields.Date.context_today(self),
                'state': 'G'
            })

    def set_trans_cr(self):
        if self.state == 'S':
            # if not self.avis_gestionnaire:
            #     raise models.ValidationError("Vous devez remplir votre avis avant de transmettre")
            #
            # if not len(self.compte_exploit_ids):
            #     raise ValidationError("Vous ne pouvez pas envoyer une demande sans compte d'exploitation")

            zone = self.env['ref_zone'].search([('id', '=', self.zone_id.id)])

            if zone.ordre_validation == '1':
                self.sudo().write({
                    'date_trans_cr': fields.Date.context_today(self),
                    'state': 'CR'
                })
            else:
                self.write({
                    'date_trans_cc': fields.Date.context_today(self),
                    'state': 'CC'
                })

    # Comite regional
    def set_trans_cc(self):
        if self.state == 'CR':
            self.write({
                'date_trans_cc': fields.Date.context_today(self),
                'date_avis_commite_antenne': fields.Date.context_today(self),
                'state': 'CC'
            })

    def set_accorde_r(self):
        if self.state == 'CR':
            self.credit_pv_id.add_credit_line(self.id, 'A')
            self.calcul_tableau_amortissement()
            self.genere_num_credit()
            self.sudo().write({
                'state': 'DA',
                'date_avis_commite_antenne': fields.Date.context_today(self),
                'date_accord': fields.Date.context_today(self),
                'avis_commite_antenne': 'Avis favorable',
            })

    def set_refuse_r(self):
        self.credit_pv_id.add_credit_line(self.id, 'R')
        if self.state == 'CR':
            self.write({
                'date_avis_commite_antenne': fields.Date.context_today(self),
                'state': 'DR'
            })

    def set_ajourne_r(self):
        self.credit_pv_id.add_credit_line(self.id, 'AJ')
        if self.state == 'CR':
            self.write({
                'state': 'S',
                'date_retour_sup': fields.Date.context_today(self)
            })

    # Comite rcentral
    def set_trans_dg(self):
        if self.state == 'CC':
            self.write({
                'date_trans_dg': fields.Date.context_today(self),
                'date_avis_commite_credit': fields.Date.context_today(self),
                'state': 'DG'
            })

    def set_accorde_cc(self):
        if self.state == 'CC':
            self.calcul_tableau_amortissement()
            self.genere_num_credit()
            self.sudo().write({
                'state': 'DA',
                'date_avis_commite_antenne': fields.Date.context_today(self),
                'date_accord': fields.Date.context_today(self),
            })

    def set_refuse_cc(self):
        if self.state == 'CC':
            self.write({
                'date_avis_commite_antenne': fields.Date.context_today(self),
                'state': 'DR'
            })

    def set_ajourne_cc(self):
        if self.state == 'CC':
            self.write({
                'state': 'S',
                'date_retour_sup': fields.Date.context_today(self)
            })

    # DG
    def set_trans_cca(self):
        if self.state == 'DG':
            self.write({
                'date_trans_cca': fields.Date.context_today(self),
                'date_avis_directrice': fields.Date.context_today(self),
                'state': 'CCA'
            })

    def set_accorde_dg(self):
        if self.state == 'DG':
            self.calcul_tableau_amortissement()
            self.genere_num_credit()
            self.sudo().write({
                'state': 'DA',
                'date_avis_directrice': fields.Date.context_today(self),
                'date_accord': fields.Date.context_today(self),
            })

    def set_refuse_dg(self):
        if self.state == 'DG':
            self.write({
                'date_avis_directrice': fields.Date.context_today(self),
                'state': 'DR'
            })

    def set_ajourne_dg(self):
        if self.state == 'DG':
            self.write({
                'state': 'S',
                'date_retour_sup': fields.Date.context_today(self)
            })

    # Comite CA
    def set_recp_cca(self):
        self.state = 'RCCA'

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

    def create_rainbow_man(self, message):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': message,
                'type': 'rainbow_man'
            }
        }

    # Comite CA
    def imprime_recepisse(self):
        return self.env.ref('faarf_credit.report_credit_recipisse').report_action(self.id)

    ##deblocage
    def set_deblocage(self):
        if self.state == 'DA':
            date_debloc = fields.Date.context_today(self)
            self.sudo().write({
                'state': 'PD',
                'date_debloc': date_debloc
            })

    def set_cheque_emis(self, chequier, cheque):
        date_cheque = fields.Date.context_today(self)
        self.sudo().write({
            'state': 'CE',
            'date_cheque': date_cheque,
            'chequier': chequier,
            'cheque': cheque
        })

    def set_decaisser(self):
        date_decaiss = fields.Date.context_today(self)
        self.sudo().write({
            'state': 'DC',
            'date_decaiss': date_decaiss
        })

    def set_rembouser(self):
        date_rembours = fields.Date.context_today(self)
        self.sudo().write({
            'state': 'RB',
            'date_rembours': date_rembours
        })
