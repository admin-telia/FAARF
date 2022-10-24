from odoo import api, models, fields, _
from datetime import date
from odoo.exceptions import ValidationError


class ComptaPres(models.Model):
    _name = "compta_prestation"
    
    code = fields.Char("Code", required=True)
    name = fields.Char("Libellé", required=True)
    active = fields.Boolean('Actif', default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)



class ComptaModeReg(models.Model):
    _name = "compta_mode_regularisation"

    lb_court = fields.Char("Libellé court")
    name = fields.Char("Libellé long", required=True)


class ComptaPourcentage(models.Model):
    _name = "compta_pourcentage"

    taux = fields.Float("Taux (%)", required=True)
    name = fields.Char("Libellé", required=True)
    imputation = fields.Many2one("compta_plan_lines", string="Imputation", required=True)

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.name, rec.taux)))
        return result


class Compta_Type1OpCpta(models.Model):
    
    _name = 'compta_type1_op_cpta'
    _rec_name = 'lb_long' 
    
    type1_opcpta = fields.Char("Code", size =3, required=True)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65, required=True)
    data_id = fields.Many2one("compta_data", "Type opération")
    active = fields.Boolean('Actif',default=True)
    
  
class Compta_TypeOpCptaline(models.Model):
    
    _name = 'compta_type_op_cpta_line'
    _rec_name = 'type1_opcpta'
    
    type1_opcpta = fields.Many2one("compta_type1_op_cpta", "Libellé de type de base")
    type_opguichet_ids = fields.One2many('compta_type_op_cpta','type_opcpta_id')  
    
    
    
class Compta_TypeOpCpta(models.Model):
    
    _name = 'compta_type_op_cpta'
    
    #type1_opcpta usage pour enregistrememnt unique à enlever si solution groupée trouvée
    reg_op_guichet = fields.Many2one("compta_reg_op_guichet")
    type1_opcpta = fields.Many2one("compta_type1_op_cpta", "Libellé de type de base")
    type_opcpta_id = fields.Many2one("compta_type_op_cpta_line")
    type_opcpta1 = fields.Char("Code", size =5, required=True)
    lb_court = fields.Char("Libellé court", size=50)
    name = fields.Char("Libellé ", required=True)
    fg_pc = fields.Selection([
        ('S', 'Sans'),
        ('P', 'Préalable'),
        ('R', 'Regul'),
        ('I', 'Immédiat'),
        ('U', 'Ultérieur'),
        ('?', '?'),
        ], ' ', default='S', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    fg_term = fields.Selection([
        ('T', 'Y-Terminal'),
        ('N', 'N-Non (ici)'),
        ('L', 'L-Non(Lv)'),
        ], 'Niveau de determination', default='T', required=True)
    col_id = fields.Many2one('compta_colonne_caisse', "Col. brouill caiss",required=True)
    no_imputation = fields.Many2one("compta_plan_lines", 'Imputation',domain="[('company_id','=',company_id)]")
    souscompte_id = fields.Integer()
    list_val = fields.Many2one("compta_table_listnat", 'Nature détaillée')
    no_imp_pc = fields.Char('       ',size=10)
    lb_nature = fields.Char('           ',size=15)
    fg_grant_ac = fields.Boolean("Ac")
    fg_grant_ord = fields.Boolean("ORD")
    fg_facial = fields.Boolean()
    fg_guichet = fields.Boolean("Gui.")
    fg_ch_emis = fields.Boolean("Cheq./Vir.")
    fg_op_relev = fields.Boolean("Rel.")
    fg_retenue = fields.Boolean("Ret.")
    typ2_assign = fields.Char(size=3)
    na_fixe = fields.Char(size=10)
    typebase_id = fields.Many2one("compta_operation_guichet", ondelete='cascade')
    regle_id = fields.Many2one("compta_regle_operation_guichet")
    x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    
    
    @api.onchange('no_imputation')
    def Val_Imput(self):
        for x in self:
            x.souscompte_id = x.no_imputation.souscpte.id
    
class Compta_TypeColonneCaisse(models.Model):
    
    _name = 'compta_colonne_caisse'
    _rec_name = 'lb_long'
    
    cd_col_caise = fields.Char("Code", size =3)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65, required=True)
    active = fields.Boolean('Actif',default=True) 
    #test = fields.Selection(selection = 'function_test')   
    
    _sql_constraints = [
        ('cd_col_caise', 'unique (cd_col_caise)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
    
    """
    @api.model
    def function_test(self):
        nom_vue = str('vue_nature')
        clause_w = str('cd_nat = 2')
        
        #nature = self.env['compta_colonne_caisse'].search([])
        #return [(x.cd_col_caise, x.lb_court) for x in nature]
    
        #self.env.cr.execute("select * from %s where %s" %(nom_vue,clause_w))
        nature = self.env['vue_nature'].search([])
        #nature = self.env.cr.dictfetchall()
        return [(x.cd_nat, x.lb_nat) for x in nature]
        print('valeur nature',nature)
    """
    
class Compta_TypeOpBanque(models.Model):
    
    _name='compta_type_op_banque'
    _rec_name = 'lb_long'
  
  
    #type1_opcpta_id usage pour enregistrememnt unique à enlever si solution groupée trouvée
    reg_op_banque = fields.Many2one("compta_reg_op_banque")
    type1_opcpta = fields.Many2one("compta_type_op_banque_line")
    type_opbq = fields.Char("Code",size=5)
    lb_court = fields.Char("Libellé court", size=50)
    lb_long = fields.Char("Libellé long", size=100)
    lb_comment = fields.Char('Commentaire',size=200)
    no_cpt_deb = fields.Many2one('compta_plan_lines', 'Débit')
    no_cpt_cred = fields.Many2one('compta_plan_lines', 'Crédit')
    cpte_cred = fields.Integer()
    cpte_deb = fields.Integer()
    type_journal_id = fields.Many2one('compta_type_journal', "Type de journal")
    cd_assign = fields.Selection([
        ('ac', 'AC'),
        ('daf', 'DAF'),
        ('struct', 'STRUCT'),
        ], 'Assignataire', index=True, copy=False, track_visibility='always')
    typebase_id = fields.Many2one("compta_operation_banque", ondelete='cascade')
    regle_id = fields.Many2one("compta_regle_operation_banque")
    
    @api.onchange('no_cpt_deb')
    def deb(self):
        if self.no_cpt_deb:
            self.cpte_deb = self.no_cpt_deb.souscpte.id

    @api.onchange('no_cpt_cred')
    def cred(self):
        if self.no_cpt_cred:
            self.cpte_cred = self.no_cpt_cred.souscpte.id

    
class Compta_TypeOpBanqueline(models.Model):
    
    _name = 'compta_type_op_banque_line'
    _rec_name = 'type1_opcpta_id'
    
    type1_opcpta_id = fields.Many2one("compta_type1_op_cpta", "Libellé de type de base")
    type_opbq_ids = fields.One2many('compta_type_op_banque','type1_opcpta')
    
    
class Compta_type_ecriture(models.Model): 
    
    _name='compta_type_ecriture'
    _rec_name = 'lb_long'
    
    type_ecriture = fields.Char("Code", size =1, required=True)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65, required=True)
    active = fields.Boolean('Actif',default=True)

    _sql_constraints = [
        ('type_ecriture', 'unique (type_ecriture)', "Ce code existe déjà. Veuillez changer de code !"),
    ]  
    

class Compta_type_op_ecriture(models.Model): 
    
    _name='compta_type_op_ecriture'
    _rec_name = 'lb_long'
    
    type_op_ecr = fields.Char("Code", size =2)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65)
    active = fields.Boolean('Actif',default=True)

    _sql_constraints = [
        ('type_op_ecr', 'unique (type_op_ecr)', "Ce code existe déjà. Veuillez changer de code !"),
    ] 
    

class Compta_TypeLbLecriture(models.Model):
    
    _name = 'compta_typelblecriture'
    _rec_name = 'lb_long'
    
    type_lblecriture = fields.Char("Code", size =1)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65)
    active = fields.Boolean('Actif',default=True)
    
    _sql_constraints = [
        ('type_lblecriture', 'unique (type_lblecriture)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
    
    
class Compta_TypeJournal(models.Model):
    
    _name='compta_type_journal'
    _rec_name = 'lb_long'
    
    
    type_journal = fields.Char("Code", size =5, required=True)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65, required=True)
    active = fields.Boolean('Actif',default=True)
    
    _sql_constraints = [
        ('type_journal', 'unique (type_journal)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
    

class Compta_TypeQuittance(models.Model):

    _name = "compta_type_quittance"
    _rec_name = 'lb_long'
    
    ty_quittance = fields.Char("Code")
    lb_long = fields.Char("Libellé court",size = 35)
    lb_court = fields.Char("Libellé long",size=100, required=True)
    active = fields.Boolean('Actif',default=True)
    
    _sql_constraints = [
        ('ty_quittance', 'unique (ty_quittance)', "Ce code existe déjà. Veuillez changer de code !"),
        
    ]
    
class Compta_TypeBilletage(models.Model):

    _name = "compta_type_billetage"
    _rec_name = 'lb_long'
    
    type_billetage = fields.Char("Code")
    lb_long = fields.Char("Libellé long",size = 100, required=True)
    lb_court = fields.Char("Libellé court",size=35)
    active = fields.Boolean('Actif',default=True)
    
    _sql_constraints = [
        ('type_billetage', 'unique (type_billetage)', "Ce code existe déjà. Veuillez changer de code !"),
        
    ]
    
    
class Compta_TypePeriode(models.Model):

    _name = "compta_type_periode"
    _rec_name = 'lb_long'
    
    ty_periode = fields.Char("Code")
    lb_long = fields.Char("Libellé long" ,size = 100)
    lb_court = fields.Char("Libellé court" ,size=35)
    active = fields.Boolean('Actif',default=True)


class Compta_Periode(models.Model):
    _name = 'compta_periode'
    _rec_name = 'lb_periode'
    
    cd_type = fields.Many2one("compta_type_periode", 'Type de période',states={'O': [('readonly', True)]}, required=True)
    dt_debut = fields.Date("Date de début", required=True, states={'O': [('readonly', True)],'F': [('readonly', True)]})
    dt_fin = fields.Date("Date de fin",required=True,states={'O': [('readonly', True)]})
    lb_periode = fields.Char("Libellé",required=True,states={'O': [('readonly', True)]})
    numero = fields.Integer("N°",states={'O': [('readonly', True)]})
    active = fields.Boolean('Actif',default=True)
    state = fields.Selection([
        ('draft','Brouillon'),
        ('O','Ouverte'),
        ('A','Arrêtée'),
        ('F','Clotûrée'),
        ], string="Etat", default="draft")

    
    def ouvrir(self):
        self.write({'state': 'O'})
    
    @api.onchange('dt_fin')
    def OnChangeDate(self):
        val_date = date.today()
        
        if self.dt_fin < self.dt_debut:
            raise ValidationError(_('Vérifiez les date'))
        
        #if self.dt_fin > val_date:
            #self.active = False

class Compta_TypeIntervExt(models.Model):
    
    _name = 'compta_type_interv_ext'
    _rec_name = 'lb_long'
    
    type_ivext = fields.Char('Code', size=4)
    lb_court = fields.Char("Libellé court", size=35)
    lb_long = fields.Char("Libellé long", size=65, required=True)
    fg_enc = fields.Boolean()
    fg_dec = fields.Boolean()
    nm_table = fields.Char(size=20)
    ls_col_table = fields.Char(size=50)
    active = fields.Boolean('Actif',default=True)
    
    _sql_constraints = [
        ('type_ivext', 'unique (type_ivext)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
    
class Compta_intervant(models.Model):
    
    _name = "compta_intervenant"
    
    type_op = fields.Many2one("compta_reg_op_guichet_unique", string ="Type d'opération")
    intervenant_id = fields.Many2one("compta_type_interv_ext", string="Libellé usager")
    
class Budg_TypeBordTrans(models.Model):
    
    _inherit = "budg_typebordtrans"
    
    fictif = fields.Char("fictif")
    
    
class Compta_teneur(models.Model):
    _name = 'compta_teneur_cpte'
    _rec_name="no_cpte"
    
    user_id = fields.Many2one('res.users', string='Teneur', required=True)
    no_cpte = fields.Many2one("compta_plan_lines",domain = "[('company_id','=', company_id)]", string="Compte", required=True)
    active = fields.Boolean('Actif',default=True)
    fg_sens = fields.Char("Sens")
    x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class ComptaOperationGuichet(models.Model):
    _name = "compta_operation_guichet"
    _rec_name = "typebase"
    
    data_id = fields.Many2one('compta_data')
    typebase = fields.Many2one("compta_type1_op_cpta", "Opération de base", required=True)
    code = fields.Char("Code", readonly=True)
    operation_guichet_ids = fields.One2many("compta_type_op_cpta", "typebase_id")
    
    @api.onchange('typebase')
    def Code(self):
        if self.typebase:
            self.code = self.typebase.type1_opcpta
            

class ComptaOperationBanque(models.Model):
    _name = "compta_operation_banque"
    _rec_name = "typebase"
    
    typebase = fields.Many2one("compta_type1_op_cpta", "Type de base", required=True)
    code = fields.Char("Code", readonly=True)
    operation_banque_ids = fields.One2many("compta_type_op_banque","typebase_id")
    
    @api.onchange('typebase')
    def Code(self):
        if self.typebase:
            self.code = self.typebase.type1_opcpta


class Categorie(models.Model):
    _name = 'compta_categorie'
    
    code = fields.Char("Code", size=5)
    lb_court = fields.Char("Libellé court")
    name = fields.Char("Libellé", required=True)
    
    
class TypePrestation(models.Model):
    _name = 'compta_type_prestation'
    
    code = fields.Char("Code", size=5)
    lb_court = fields.Char("Libellé court", required=False)
    name = fields.Char("Libellé", required=True)


class Prestation(models.Model):
    _name = 'compta_prestation'
    
    code = fields.Char("Code", size=5)
    lb_court = fields.Char("Libellé court", required=False)
    name = fields.Char("Libellé", required=True)



class Parametre(models.Model):
    _name = "compta_parametre"
    _rec_name = 'designation'
    
    categorie_id = fields.Many2one("compta_categorie", "Catégorie de prestation", required=True)
    type_id = fields.Many2one("compta_type_prestation", "Type de prestation", required=True)
    designation = fields.Many2one("compta_prestation", "Prestation", required=True)
    support = fields.Selection([("tv","Télé"),("radio","Radio")], string="Support de diffusion")
    rtb = fields.Selection([("1","RTB1"),("2","RTB2")], string="Choisir le")
    horaire = fields.Many2one("compta_horaire", "Horaire")
    localite = fields.Many2one("ref_localite", "Localité")
    duree = fields.Integer("Durée (en seconde)")
    prix_unitaire = fields.Integer("Coût", required=True)

class Horaire(models.Model):
    _name = "compta_horaire"
    
    name = fields.Char("Libellé", required=True)
    code = fields.Char("Code")

    
