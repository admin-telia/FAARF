from odoo import models, fields, api
from datetime import datetime, date


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # fonction de recherche permettant de retourner l'indemnité d'astreinte en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id', 'x_fonction_id')
    def cal_indem_astr(self):
        for rec in self:
            val_emploi = int(rec.x_emploi_id)
            val_zone = int(rec.x_zone_id)
            val_echel = int(rec.x_echelle_c_id)
            val_cat = int(rec.x_categorie_c_id)
            val_struct = int(rec.company_id)
            val_fonct = int(self.x_fonction_id)

            if rec.struct_id.code == 'FCT_MD':
                val_echel = int(rec.x_echelle_id)
                val_cat = int(rec.x_categorie_id)

            print("Maxx")
            rec.x_indem_astr = 0
            if val_emploi != False:
                if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                    # res = self.env['hr_paramindemniteastr'].search(
                    #     [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                    #      ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])

                    res = self.env['hr_paramindemniteastr'].search(
                        [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone),
                         ('x_fonction_id', '=', val_fonct),
                         ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                    rec.x_indem_astr = res.x_taux

    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_loge(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                # res = self.env['hr_paramindemnitelogement'].search(
                #     [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                #      ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                res = self.env['hr_paramindemnitelogement'].search(
                    [('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_loge = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de technicité en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_techn(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                # res = self.env['hr_paramindemnitetechnicite'].search(
                #     [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone),
                #      ('x_echelle_c_id', '=', val_echel),
                #      ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                res = self.env['hr_paramindemnitetechnicite'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_techn = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité resp financière en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_respfinanciere(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                # res = self.env['hr_paramindemniterespfinanciere'].search(
                #     [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone),
                #      ('x_echelle_c_id', '=', val_echel),
                #      ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                res = self.env['hr_paramindemniterespfinanciere'].search(
                    [('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_finance = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité spécificité GRH en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                # res = self.env['hr_paramindemnitespecifique'].search(
                #     [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone),
                #      ('x_echelle_c_id', '=', val_echel),
                #      ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                res = self.env['hr_paramindemnitespecifique'].search(
                    [('x_emploi_id', '=', val_emploi), ('company_id', '=', val_struct)])
                self.x_indem_specif = res.x_taux

        # fonction de recherche permettant de retourner l'indemnité spécificité IT en fonction des paramètres

    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec_it(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique_it'].search(
                    [('x_emploi_id', '=', val_emploi), ('company_id', '=', val_struct)])
                self.x_indem_spec_inspect_trav = res.x_taux

    @api.onchange('x_fonction_id', 'x_zone_id')
    def indem_resp(self):
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_struct = int(self.company_id)
        if val_fonct != False or val_fonct == False and val_zone != False or val_zone == False and val_struct != False:
            # res = self.env['hr_paramindemniteresp'].search(
            #     [('x_fonction_id', '=', val_fonct), ('x_zone_id', '=', val_zone), ('company_id', '=', val_struct)])
            res = self.env['hr_paramindemniteresp'].search(
                [('x_fonction_id', '=', val_fonct), ('company_id', '=', val_struct)])
            self.x_indem_resp = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de caisse en fonction des paramètres
    @api.onchange('x_fonction_id', 'x_categorie_c_id')
    def indem_caisse(self):
        # val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_fonct != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                # res = self.env['hr_paramindemnitecaisse'].search(
                #     [('x_fonction_id', '=', val_fonct), ('x_categorie_c_id', '=', val_cat),
                #      ('company_id', '=', val_struct)])
                res = self.env['hr_paramindemnitecaisse'].search(
                    [('x_fonction_id', '=', val_fonct), ('company_id', '=', val_struct)])
                self.x_indem_caisse = res.x_taux

# Creation de la classe Indemnie avec ses attributs
class HrParametrageIndemnite(models.Model):
    _name = "hr_paramindemnite"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Char(string='Type indemnité', required=False)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=False)
    x_fonction_id = fields.Many2one("hr_fonctionss", string="Fonction", required=False)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=False)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=False)
    x_taux = fields.Float(string='Taux à servir', required=False)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=False)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')


# Creation de la classe IndemniteAstreinte avec ses attributs
class HrParametrageIndemniteAstreinte(models.Model):
    _name = "hr_paramindemniteastr"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de responsabilité
class HrParametrageIndemniteResponsabilite(models.Model):
    _name = "hr_paramindemniteresp"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de de logement
class HrParametrageIndemniteLogement(models.Model):
    _name = "hr_paramindemnitelogement"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de technicité
class HrParametrageIndemniteTecnicite(models.Model):
    _name = "hr_paramindemnitetechnicite"
    _rec_name = "x_type_indem_id"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités spécifiques GRH
class HrParametrageIndemniteSpecifiqueGRH(models.Model):
    _name = "hr_paramindemnitespecifique"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités spécifiques  IT
class HrParametrageIndemniteSpecifiqueIT(models.Model):
    _name = "hr_paramindemnitespecifique_it"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités spécifiques  IFC (Indemnité Forfaitaire Compensatrice)
class HrParametrageIndemniteSpecifiqueIFC(models.Model):
    _name = "hr_paramindemnitespecifique_ifc"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités spécifiques  IRP (Indemnité Responsabilite Pecunière)
class HrParametrageIndemniteSpecifiqueIRP(models.Model):
    _name = "hr_paramindemnitespecifique_irp"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités spécifiques  ISH (Indemnité Spécifique Harmonisée pour le  Personnel du MENA et du MESRSI)
class HrParametrageIndemniteSpecifiqueISH(models.Model):
    _name = "hr_paramindemnitespecifique_ish"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités spécifiques liées à la fonction
class HrParametrageIndemniteSpecifiques(models.Model):
    _name = "hr_paramindemnitespecifiques"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de transport
class HrParametrageIndemniteTransport(models.Model):
    _name = "hr_paramindemnitetransport"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de Informatique
class HrParametrageIndemniteInformatique(models.Model):
    _name = "hr_paramindemniteinformatique"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de Exploitation reseaux
class HrParametrageIndemniteExploiReseau(models.Model):
    _name = "hr_paramindemniteexploireseau"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités de resp.financière
class HrParametrageIndemniteRespFinanciere(models.Model):
    _name = "hr_paramindemniterespfinanciere"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de garde
class HrParametrageIndemniteGarde(models.Model):
    _name = "hr_paramindemnitegarde"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités de risque de contagion
class HrParametrageIndemniteRisque(models.Model):
    _name = "hr_paramindemniterisquecontagion"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de sujetion de contagion
class HrParametrageIndemniteSujetion(models.Model):
    _name = "hr_paramindemnitesujetion"
    _inherit = 'hr_paramindemnite'

# Classe pour gerer les indemnités de formation spécialisée
class HrParametrageIndemniteFormationSp(models.Model):
    _name = "hr_paramindemniteformation"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités de caisse
class HrParametrageIndemniteCaisse(models.Model):
    _name = "hr_paramindemnitecaisse"
    _inherit = 'hr_paramindemnite'


# Classe pour gerer les indemnités vestimentaire
class HrParametrageIndemniteVestimentaire(models.Model):
    _name = "hr_paramindemnitevest"
    _inherit = 'hr_paramindemnite'
