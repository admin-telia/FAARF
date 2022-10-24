from odoo import api, models, fields, _, tools
from odoo.exceptions import ValidationError
from datetime import date
from num2words import num2words
from collections import OrderedDict
from builtins import sorted

"""Definitions des différentes classes"""


class BudgTypeAccompte(models.Model):

	_name = "budg_typeaccompte"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_accompte = fields.Char(string="Code", size=2, required=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)

	
class BudgTypeBudget(models.Model):

	_name = "budg_typebudget"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_budget = fields.Char(string="Code", size=2, required=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeBordTrans(models.Model):

	_name = "budg_typebordtrans"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	code = fields.Char(string="Code", size=2)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	type_depart = fields.Selection([('ORD', 'ORD'), ('CF/CG', 'CF/CG'), ('AC', 'AC'), ], string="Départ")
	type_dest = fields.Selection([('ORD', 'ORD'), ('CF', 'CF'), ('AC', 'AC'), ], string="Destinataire")
	active = fields.Boolean('Actif', default=True)


class BudgTypeControle(models.Model):

	_name = "budg_typecontrole"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_controle = fields.Char(string="Code",
								   default=lambda self: self.env['ir.sequence'].next_by_code('cd_type_controle'),
								   readonly=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeContribuable(models.Model):

	_name = "budg_typecontribuable"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_contribuable = fields.Char(string="Code", default=lambda self: self.env['ir.sequence'].next_by_code
	('cd_type_contribuable'), readonly=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeDepense(models.Model):

	_name = "budg_typedepense"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_depense = fields.Char(string="Code", default=lambda self: self.env['ir.sequence'].next_by_code
	('cd_type_contribuable'), readonly=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)
	_sql_constraints = [('cd_type_depense', 'unique (cd_type_depense)', "Ce code existe déjà. Veuillez changer de code !"), ]


class BudgTypeDossierBudg(models.Model):
	_name = "budg_typedossierbudg"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	code = fields.Char(string="Code", readonly=False)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeprocedure(models.Model):
	
	_name = 'budg_typeprocedure'
	_rec_name = 'lb_long'
	
	sequence = fields.Integer(default=10)
	type_procedure = fields.Char(string="Code",
								 default=lambda self: self.env['ir.sequence'].next_by_code('type_procedure'), readonly=True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeEngagement(models.Model):

	_name = "budg_typeengagement"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	type_procedure_id = fields.Many2one('budg_typeprocedure', string="Type procédure")
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypeOrdrePaiement(models.Model):

	_name = "budg_typeordrepaiement"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_ordre_paiement = fields.Char(string="Code",
										 default=lambda self: self.env['ir.sequence'].next_by_code('cd_type_ordre_paiement'), readonly=True)
	type_procedure = fields.Many2one('budg_typeprocedure', string="Type procédure")
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgTypePieceBudget(models.Model):

	_name = "budg_typepiecebudget"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_piece_budget = fields.Char(string="Code",
									   default=lambda self: self.env['ir.sequence'].next_by_code('cd_type_piece_budget'), readonly = True)
	name = fields.Char(string="Libellé court", size=25, required=True)
	lb_long = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)


class BudgPJ(models.Model):
	
	_name = "budg_pj"
	_rec_name = "lb_long"
	
	lb_long = fields.Many2one("ref_piece_justificatives", string="Libellé long", required=True)
	oblige = fields.Boolean("Obligé ?")
	nombre = fields.Integer("Nbre copies(s)")
	ref = fields.Char("Références")
	montant = fields.Integer("Montant")
	param_article_id = fields.Many2one("budg_param_article")
	recette_id = fields.Many2one("budg_titrerecette")
	liq_id = fields.Many2one('budg_liqord')
	mandat_id = fields.Many2one('budg_mandat')
	

class BudgPjRec(models.Model):
	
	_name = "budg_pj_rec"
	_rec_name = "lb_long"
	
	lb_long = fields.Many2one("ref_piece_justificatives", string="Libellé long", size=100, required=True)
	oblige = fields.Boolean("Obligé ?")
	nombre = fields.Integer("Nbre copies(s)")
	ref = fields.Char("Références")
	montant = fields.Integer("Montant")
	nature_rec_id = fields.Many2one("budg_naturerecette")


class Budg_NatureRecette(models.Model):

	_name = "budg_naturerecette"
	_rec_name = "cd_paragraphe_id"

	sequence = fields.Integer(default=10)
	cd_titre_id = fields.Many2one("budg_titre", string="Titre", default=lambda self: self.env['budg_titre'].search([('type_titre','=', 'R')]),readonly=True, required=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", required=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", required=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", required=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", required=True)
	lb_long = fields.Many2one("ref_article", string="Nature de la recette", required=False)
	typebenef = fields.Many2one("ref_typecontribuable", "Type de contribuable", required=False)
	cat_benef = fields.Many2one("ref_categoriecontribuable", "Catégorie de contribuable", required=False)
	pj_ids = fields.One2many("budg_pj_rec", 'nature_rec_id')
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	
	

class Budg_NatureDepense(models.Model):

	_name = "budg_naturedepense"
	_rec_name = "cat_benef"

	sequence = fields.Integer(default=10)
	cd_titre_id = fields.Many2one("budg_titre", string="Titre", default=lambda self: self.env['budg_titre'].search([('type_titre','=', 'D')]),readonly=True, required=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", required=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", required=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", required=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", required=True)
	lb_long = fields.Many2one("ref_article", string="Nature de la dépense", required=False)
	cd_type_dossier_id = fields.Many2one('budg_typedossierbudg', required=True, string="Etape",
										 default=lambda self: self.env['budg_typedossierbudg'].search([('code','=', 'ENG')]))
	type_procedure_id = fields.Many2one('budg_typeprocedure', string="Type de procédure", required=True)
	typebenef = fields.Many2one("ref_typebeneficiaire", "Type de bénéficiaire", required=False)
	cat_benef = fields.Many2one("ref_categoriebeneficiaire", "Catégorie de beneficiaire", required=True)
	pj_ids = fields.One2many("budg_pj_dep", 'nature_dep_id')
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	

class BudgPjDep(models.Model):
	
	_name = "budg_pj_dep"
	_rec_name="lb_long"
	
	lb_long = fields.Many2one("ref_piece_justificatives",string = "Libellé long", size = 100, required=True)
	oblige = fields.Boolean("Obligatoire")
	nombre = fields.Integer("Nbre copies(s)")
	ref = fields.Char("Références")
	montant = fields.Integer("Montant")
	nature_dep_id = fields.Many2one("budg_naturedepense")


class BudgPieceJusti(models.Model):
	
	_name = "budg_piecejustificative"
	_rec_name = "cd_piecejust_id"
	
	sequence = fields.Integer(default=10)
	cd_piecejust_id = fields.Many2one('ref_piece_justificatives', string="Intitulé")
	reference = fields.Char("Références", size = 35)
	datepj = fields.Date('Date')
	active = fields.Boolean("Obligé ?",default=True)
	montant = fields.Integer('Montant', size= 15)
	nombre = fields.Integer("Nbre copies(s)", size = 2)
	eng_id = fields.Many2one('budg_engagement')
	

class BudgTypePJBudget(models.Model):

	_name = "budg_typepjbudget"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_pj_budget = fields.Char(string = "Code ", size = 3)
	name = fields.Char(string = "Libellé court", size = 50, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	lb_ref = fields.Char(string="Ref", size=65)
	active = fields.Boolean('Actif',default=True)


class BudgModeMarche(models.Model):

	_name = "budg_modemarche"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_mode_mp = fields.Char(string = "Mode marché", default=lambda self: self.env['ir.sequence'].next_by_code('cd_mode_mp'), readonly=True) 
	name = fields.Char(string = "Libellé court", size = 25)
	lb_long = fields.Char(string = "Libellé long", size = 65)
	active = fields.Boolean('Actif',default=True)


class BudgTypeTitreBudgetaire(models.Model):

	_name = "budg_typetitrebudgetaire"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_titre_budgetaire = fields.Char(string = "Code", size = 2, required=True)
	name = fields.Char(string = "Libellé court", size = 25, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_titre_budgetaire', 'unique (cd_titre_budgetaire)', "Ce code existe déjà. Veuillez changer de code !"),]


class RefContribuable(models.Model):
	_name = "ref_contribuable"
	_rec_name = 'nm_rs'

	no_contrib = fields.Char(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('no_contrib'), readonly = True)
	type_contribuable_id = fields.Many2one("ref_categoriecontribuable",string="Type de contribuable", required=True)
	nm_rs = fields.Char(string="Raison sociale/Nom")
	nm_rs2 = fields.Char(string="Libellé")
	an_agre = fields.Date(string="Année agrément")
	no_agre = fields.Integer(string="N° Agrément")
	no_ifu = fields.Char(string="N° IFU", size=11)
	cd_citib = fields.Char(string="Cd_CITIB")
	activite = fields.Char(string="Activité", size=50)
	ap_rue = fields.Char(string="Rue")
	ap_bp = fields.Char(string="Boite Postale")
	ap_cd_post = fields.Char(string="Code Postale")
	ap_region = fields.Many2one("ref_region",string="Région")
	ap_ville = fields.Char(string="Ville")
	ap_province = fields.Many2one("ref_province",string="Province")
	ap_pays = fields.Many2one("res.country",string="Pays")
	rf_txt_agre = fields.Char(string="Texte n°")
	dt_txt_agre = fields.Date(string="Du")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bank_id = fields.Many2one("res.partner.bank", string="Banque")
	fg_eng = fields.Char()
	active = fields.Boolean('Actif', default=True)
	agence_bank_id = fields.Char(string="N° Agence")
	acc_number = fields.Char(string="N° compte")
	tel = fields.Char(string="Téléphone")
	mail = fields.Char(string="Mail")
	cpte_client = fields.Many2one("compta_plan_lines", string="Compte tiers", required=True)
	cpte_fournisseur = fields.Many2one("ref_souscompte", string="Compte tiers")


class Budg_TitreRecette(models.Model):

	_name = "budg_titrerecette"
	_rec_name = "cd_titre_recette"

	cd_titre_recette = fields.Char(string = "N° titre recette", readonly=True)
	name = fields.Char()
	no_grpadm = fields.Char()
	cd_titre_id = fields.Many2one("budg_titre",default=lambda self: self.env['budg_titre'].search([('type_titre','=', 'R')]), string = "Titre", required=True, readonly=True)
	cd_section_id = fields.Many2one("budg_section", string = "Section", required=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", required=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", required=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", required=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", required=True)
	titre_id = fields.Char()
	section_id = fields.Char()
	chapitre_id = fields.Char()
	article_id = fields.Char()
	paragraphe_id = fields.Char()
	rubrique_id = fields.Char()
	no_grpadm_pere = fields.Char(size = 4)
	no_rec_pere = fields.Char(size = 4)
	no_bord_prec = fields.Integer(size = 5)
	no_brj_prec = fields.Integer(size =5)
	no_bailleur = fields.Many2one("ref_bailleur",string="Nom")
	contribuable_id = fields.Many2one("ref_contribuable", string="Nom du débiteur", size=65, required=True)
	type_titre = fields.Selection([('N', 'Avant recouvrement'), ('R', 'Régularisation')], string='Type titre recette', required=True)
	categorie_contribuable = fields.Many2one("ref_categoriecontribuable", string="Cat cont", required=False)
	nature_rec = fields.Many2one("ref_article", string="Nature de recette", required=False)
	cd_type_contribuable = fields.Many2one("ref_typecontribuable", string="Type contrib/client", required=True)
	lb_objet = fields.Text(string="Objet", size=250, required=True)
	mnt_init_rec = fields.Float(string="Montant initial recette")
	mnt_rec = fields.Float(string="Montant titre recette", required=True)
	nb_pjust = fields.Integer(size=2)
	piecejust_ids = fields.One2many("budg_piece_recette",'recette_id')
	mnt_lbudg_ap = fields.Float(string="Montant lbudg ap")
	mnt_period_ap = fields.Float()
	mnt_recouvre = fields.Float("Reste à recouvrer",digits = (20,0), readonly=True)
	mnt_vbr = fields.Float()
	mnt_ecr = fields.Float()
	mnt_annule = fields.Float()
	imput = fields.Integer()
	no_imputation = fields.Char()
	no_imput = fields.Integer()
	tx_obj1 = fields.Char(size=15)
	type_budget_id = fields.Many2one("budg_typebudget")
	dt_rec = fields.Date(default=fields.Date.context_today,string="Date", readonly=True)
	dt_app = fields.Date()
	dt_valid = fields.Date()
	dt_visa_ac = fields.Date()
	dt_visa_ord = fields.Date()
	no_cpt_deb = fields.Char(size=3)
	no_scpt_deb = fields.Char(size=11)
	no_cpt_cred = fields.Char(size=3)
	no_scpt_cred = fields.Char(size=11)
	x_exercice_id_lecr = fields.Integer(size=4)
	no_lecr_deb = fields.Integer()
	no_lecr_pc_deb = fields.Integer()
	no_lecr_pc_cred = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cd_mode_mp_id = fields.Many2one("ref_modereglement", string = "Mode de recouvrement")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	et_doss = fields.Selection([
        ('draft', 'Brouillon'),
        ('N', 'Confirmé'),
        ('V', 'Approuvé'),
		('A', 'Annulé'),
		('W', 'Visé CG'),
		('R', 'Rejeté CG'),
		('I', 'Visa AC/DFC'),
		('J', 'Rejét AC/DFC'),
		('E', 'Pris en charge'),
		('F', 'Recouvré'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
	current_users = fields.Many2one('res.users', default = lambda self: self.env.user, readonly =True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	@api.constrains('x_exercice_id')
	def ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" %(no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice"+" "+str(v_ex)+" "+"est clôs. Traitement impossible"))

	
	@api.depends('mnt_rec')
	def amount_to_words(self):
		self.text_amount = num2words(self.mnt_rec, lang='fr')
	
		
	@api.onchange('cd_type_contribuable')
	def onchangeTypeCont(self):
		if self.cd_type_contribuable:
			self.categorie_contribuable = self.cd_type_contribuable.cate_id
			self.imput = self.cd_type_contribuable.cpte_client.souscpte.id
	
	@api.onchange('cd_rubrique_id')
	def onchangeType(self):
		if self.cd_rubrique_id:
			self.no_imputation = str(self.cd_rubrique_id.rubrique) + " " + str(self.cd_rubrique_id.no_imputation.souscpte.lb_long)
			self.no_imput = self.cd_rubrique_id.no_imputation.souscpte.id
			self.rubrique_id = self.cd_rubrique_id.rubrique
	
	@api.onchange('cd_paragraphe_id')
	def onchangePar(self):
		if self.cd_paragraphe_id:
			
				self.paragraphe_id = self.cd_paragraphe_id.paragraphe.cd_paragraphe
	
	@api.onchange('cd_titre_id')
	def onchangeTit(self):
		if self.cd_titre_id:
			
				self.titre_id = self.cd_titre_id.titre.cd_titre
				
	@api.onchange('cd_section_id')
	def onchangeSec(self):
		if self.cd_section_id:
			
				self.section_id = self.cd_section_id.section.cd_section
	
				
	@api.onchange('cd_article_id')
	def onchangeArt(self):
		if self.cd_article_id:
			
				self.article_id = self.cd_article_id.article.cd_article
	
	@api.onchange('cd_chapitre_id')
	def onchangeCha(self):
		if self.cd_chapitre_id:
			
				self.chapitre_id = self.cd_chapitre_id.chapitre.cd_chapitre
	
	

	def action_rec_draft(self):
		self.write({'et_doss': 'draft'})
		
		
	@api.onchange('cd_rubrique_id', 'cd_paragraphe_id')
	def cred_dipso(self):
		
		val_ex = int(self.x_exercice_id.id)
		val_struct = int(self.company_id.id)
		val_para = int(self.cd_paragraphe_id)
		val_rubrique = int(self.cd_rubrique_id)
		
		result = self.env['budg_ligne_exe_rec'].search([('cd_paragraphe_id','=',val_para),('cd_rubrique_id','=',val_rubrique),('company_id','=',val_struct),('x_exercice_id','=',val_ex)])
		self.mnt_recouvre = result.reste_emettre
	


	def action_rec_confirmer(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
	
		self.env.cr.execute("select notitre from budg_compteur_titrerec where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		notitre = self.env.cr.fetchone()
		cd_titre_recette = notitre and notitre[0] or 0
		c1 = int(cd_titre_recette) + 1
		c = str(cd_titre_recette)
		if c == "0":
			ok = str(c1).zfill(4)
			self.cd_titre_recette = ok
			vals = c1			
			self.env.cr.execute("INSERT INTO budg_compteur_titrerec(x_exercice_id,company_id,notitre)  VALUES(%d, %d, %d)" %(val_ex,val_struct,vals))
		else:
			c1 = int(cd_titre_recette) + 1
			c = str(cd_titre_recette)
			ok = str(c1).zfill(4)
			self.cd_titre_recette = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_titrerec SET notitre = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))
			
		self.write({'et_doss': 'N'})
		
		
			

	def action_rec_approuver(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_rub = int(self.cd_rubrique_id)
		val_titre = int(self.cd_titre_id)
		val_sec = int(self.cd_section_id)
		val_par = int(self.cd_paragraphe_id)
		val_chap = int(self.cd_chapitre_id)
		val_rub = int(self.cd_rubrique_id)
		val_art = int(self.cd_article_id)
		v_id = int(self.id)
		
		
		self.env.cr.execute("""UPDATE budg_ligne_exe_rec SET mnt_rec = (select sum(T.mnt_rec) 
		FROM budg_ligne_exe_rec BT, budg_titrerecette T WHERE T.id = %d AND BT.cd_titre_id = %d and 
		BT.cd_section_id = %d and BT.cd_chapitre_id = %d and BT.cd_art_id = %d and BT.cd_paragraphe_id = %d and 
		BT.cd_rubrique_id = %d and BT.x_exercice_id = %d and BT.company_id = %d group by T.mnt_rec) WHERE cd_titre_id = %d and 
		cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d and 
		cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d
		""" %(v_id, val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct,val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct))

	
		self.env.cr.execute("""UPDATE budg_ligne_exe_rec SET reste_emettre = (select (BT.mnt_corrige - sum(T.mnt_rec)) 
		FROM budg_ligne_exe_rec BT, budg_titrerecette T WHERE T.id = %d AND BT.cd_titre_id = %d and 
		BT.cd_section_id = %d and BT.cd_chapitre_id = %d and BT.cd_art_id = %d and BT.cd_paragraphe_id = %d and 
		BT.cd_rubrique_id = %d and BT.x_exercice_id = %d and BT.company_id = %d group by BT.mnt_corrige) WHERE cd_titre_id = %d and 
		cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d and 
		cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d
		""" %(v_id,val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct,val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct))


	
		"""
		self.env.cr.execute("UPDATE budg_ligne_exe_rec SET taux = (select ((sum(T.mnt_rec) * 100) / BR.mnt_corrige)  
		FROM budg_ligne_exe_rec BR, budg_titrerecette T WHERE T.id = %d AND BR.cd_titre_id = %d and 
		BR.cd_section_id = %d and BR.cd_chapitre_id = %d and BR.cd_art_id = %d and BR.cd_paragraphe_id = %d and 
		BR.cd_rubrique_id = %d and BR.x_exercice_id = %d and BR.company_id = %d group by BR.mnt_corrige) WHERE cd_titre_id = %d and 
		cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d and 
		cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d
		%(v_id,val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct,val_titre, val_sec, val_chap, val_art, val_par,val_rub, val_ex,val_struct))
		"""

		self.write({'et_doss': 'V'})
		self.dt_app = date.today()
		

	def action_rec_annuler(self):
		self.write({'et_doss': 'A'})

	def action_rec_viser(self):
		self.write({'et_doss': 'W'})
		self.dt_visa_ord = date.today()

	def action_rec_rejeter(self):
		self.write({'et_doss': 'R'})

	def action_rec_viser_ac(self):
		self.write({'et_doss': 'I'})

	def action_rec_rejeter_ac(self):
		self.write({'et_doss': 'J'})

	def action_rec_pc(self):
		self.write({'et_doss': 'E'})
		
	def afficher_piece(self):
		val_ex = int(self.x_exercice_id)
		categorie = int(self.categorie_contribuable)
		titre = int(self.cd_titre_id)
		section = int(self.cd_section_id)
		chapitre = int(self.cd_chapitre_id)
		article = int(self.cd_article_id)
		paragraphe = int(self.cd_paragraphe_id)

		for vals in self:
			vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, b.nombre as nbr from budg_pj_rec b, budg_naturerecette n where n.cat_benef = %d
			and n.cd_titre_id = %d and n.cd_section_id = %d and n.cd_chapitre_id = %d and n.cd_article_id = %d and n.cd_paragraphe_id = %d 
			and n.x_exercice_id = %d and n.id = b.nature_rec_id""" %(categorie, titre, section, chapitre, article, paragraphe, val_ex))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0,0, {'lb_long' : line['lib'], 'oblige': line['obl'], 'nombre': line['nbr']}))
			self.piecejust_ids = result
	
		
class Budg_Compteur_titrerec(models.Model):
	
	_name = "budg_compteur_titrerec"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	notitre = fields.Integer(default = 0)


class Budg_bord_titre(models.Model):
	
	_name = "budg_bord_titre_recette"
	_rec_name = "no_bord_rec"
	
	name = fields.Char()
	no_bord_rec = fields.Char("N° Bord", readonly=True)
	cd_acteur = fields.Char(string ="Acteur", readonly=True)
	date_emis = fields.Date("Date bordereau", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date()
	num_accuse = fields.Char()
	totaux = fields.Float()
	type_bord_trsm = fields.Char("Type de bordereau", readonly=True)
	cd_acteur_accuse = fields.Char(string ="Acteur accusé")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	recette_ids = fields.Many2many("budg_titrerecette", "budg_detail_bord_recette", string="Liste des titres de recettes", ondelete="restrict")
	et_doss = fields.Selection([
        ('N', 'Nouveau'),
        ('EB', 'Mise en bordereau'),
		('RB', 'Réceptionné par CG'),
        ], 'Etat', default='N', required=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	@api.constrains('x_exercice_id')
	def ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


	def action_reception_bord_daf_cf(self):
		self.write({'et_doss': 'RB'})


	def action_envoi_bord_cf_daf(self):
		self.write({'et_doss': 'EC'})
		

	def action_reception_bord_cf_daf(self):
		self.write({'et_doss': 'RC'})
	

	def action_envoyer_bord_pc(self):
		self.write({'et_doss': 'V'})
	

	def action_reception_bord_pc(self):
		self.write({'et_doss': 'PC'})
		
	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')
		
	

	def action_generer_bord_titre(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_id = int(self.id)
		
			
		self.env.cr.execute("select bordtitre from budg_compteur_bord_titre where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		bordtitre = self.env.cr.fetchone()
		no_bord_titre = bordtitre and bordtitre[0] or 0
		c1 = int(no_bord_titre) + 1
		c = str(no_bord_titre)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_rec = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_titre(x_exercice_id,company_id,bordtitre)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))	
		else:
			c1 = int(no_bord_titre) + 1
			c = str(no_bord_titre)
			ok = str(c1).zfill(4)
			self.no_bord_rec = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_titre SET bordtitre = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))
	
		self.write({'et_doss': 'EB'})
		
		self.env.cr.execute("select lb_long from budg_typebordtrans where code = '13' ")
		val = self.env.cr.fetchone()
		self.type_bord_trsm = val and val[0] or 0
		
		self.env.cr.execute("select type_depart from budg_typebordtrans where code = '13' ")
		val1 = self.env.cr.fetchone()
		self.cd_acteur = val1 and val1[0] or 0
		
		self.env.cr.execute("select type_dest from budg_typebordtrans where code = '13' ")
		val2 = self.env.cr.fetchone()
		self.cd_acteur_accuse = val2 and val2[0] or 0
		
		
		self.env.cr.execute(""" SELECT sum(mnt_rec) FROM budg_titrerecette bt , budg_bord_titre_recette b, budg_detail_bord_recette br
		WHERE b.x_exercice_id = %d AND b.company_id = %d AND br.budg_bord_titre_recette_id = %d 
		AND bt.id = br.budg_titrerecette_id AND br.budg_bord_titre_recette_id = b.id""" %(val_ex,val_struct, val_id))
		res = self.env.cr.fetchone()
		resu = res and res[0] or 0
		if resu <=0:
			raise ValidationError(_("Le bordereau doit contenir au moins un titre de recette approuvé."))
		else:
			self.totaux = resu
			print('montant',self.totaux)

	
"""	
class Budg_TypeBeneficiaire(models.Model):

	_name = "budg_typebeneficiaire"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_beneficiaire = fields.Char(string = "Code", size = 2, required=True)
	name = fields.Char(string = "Libellé court", size = 25, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_type_beneficiaire', 'unique (cd_type_beneficiaire)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
"""

class Budg_TypeFinancement(models.Model):

	_name = "budg_typefinancement"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_financement = fields.Char(string = "Code", size = 2, required=True)
	name = fields.Char(string = "Libellé court", size = 25, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_type_financement', 'unique (cd_type_financement)', "Ce code existe déjà. Veuillez changer de code !"),
    ]


class Budg_TypeRecette(models.Model):

	_name = "budg_typerecette"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_recette = fields.Char(string = "Code", size = 2)
	name = fields.Char(string = "Libellé court", size = 25, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_type_recette', 'unique (cd_type_recette)', "Ce code existe déjà. Veuillez changer de code !"),
    ]



class Budg_TypeFournisseur(models.Model):

	_name = "budg_typefournisseur"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_type_fournisseur = fields.Char(string = "Code", size = 2, required=True)
	name = fields.Char(string = "Libellé court", size = 25, required=True)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_type_fournisseur', 'unique (cd_type_fournisseur)', "Ce code existe déjà. Veuillez changer de code !"),
    ]

"""
class BudgBeneficiaire(models.Model):

	_name = "budg_beneficiaire"
	_rec_name = "nm"
	
	name = fields.Char(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('name'), readonly = True)
	no_beneficiaire = fields.Char(string="Raison sociale", size=65)
	type_beneficiaire_id = fields.Many2one("budg_typebeneficiaire",string="Type de bénéficiaire")
	nm = fields.Char(string="Nom et Prénom", size=20)
	pn = fields.Char(string="Prénom", size=40)
	no_ifu = fields.Char(string="N° IFU", size=20)
	cd_mat = fields.Char(string="Matricule", size=20)
	no_eng = fields.Integer(string="No_Eng")
	ex_last = fields.Integer(string="Ex_last")
	ap_rue = fields.Char(string="Rue", size=35)
	ap_bp = fields.Char(string="Boite postale", size=8)
	ap_cd_post = fields.Char(string="Code postal", size=6)
	ap_ville = fields.Char(string="Ville", size=30)
	ap_pays = fields.Many2one("ref_pays",string="Pays")
	tel = fields.Char(string="Téléphone", size=30)
	nm_officiel = fields.Char(string="Titre officiel", size=50)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	mod_reg_id = fields.Many2one("ref_modereglement", string="Mode") 
	bank_id = fields.Many2one("res.bank", string = "Banque")
	active = fields.Boolean('Actif',default=True)
	fg_bloc = fields.Char()
	cpte_client = fields.Many2one("ref_souscompte", string = "Compte client")
	cpte_fournisseur = fields.Many2one("ref_souscompte", string = "Compte fournisseur")
	agence_bank_id = fields.Char(string = "N° Agence")
	acc_number = fields.Char(string = "N° compte")
	cat_fournisseur = fields.Selection([
		('S', 'Société'),
		('P', 'Particulier')], 'Catégorie ')

	_sql_constraints = [
        ('no_beneficiaire', 'unique (no_beneficiaire)', "Ce code existe déjà. Veuillez changer de code !"),
    ]
"""

class ResPartner(models.Model):
	
	_inherit = "res.partner"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class BudgBailleur(models.Model):

	_name = "budg_bailleur"
	_rec_name = "nm_bail"
	
	name = fields.Char()
	cd_bail = fields.Char(string="Code Bailleur", default=lambda self: self.env['ir.sequence'].next_by_code('cd_bail'), readonly = True)
	type_bailleur = fields.Selection([
        ('P', 'Particulier'),
        ('S', 'Société/Institution'),
        ], string ="Type de bailleur", default='P')
	nm_bail = fields.Char(string="Nom Bailleur", size=60)
	lb_sigle = fields.Char(string="Libellé sigle", size=60)
	na_bail = fields.Char(string="na_bail", size=1)
	cd_categ = fields.Char(string="Catégorie", size=4)
	ap_rue = fields.Char(string="Rue", size=35)
	ap_bp = fields.Char(string="Boite Postale", size=8)
	ap_cd_post = fields.Char(string="Code Postale", size=6)
	ap_ville = fields.Char(string="Ville", size=30)
	ap_pays = fields.Many2one("ref_pays",string="Pays", size=3)
	as_rue = fields.Char(string="Rue 2nd", size=35)
	as_bp = fields.Char(string="Boite Postale 2nd", size=8)
	as_cd_post = fields.Char(string="Code Postale 2nd", size=6)
	as_ville = fields.Char(string="Ville 2nd", size=30)
	as_pays = fields.Many2one("ref_pays",string="Pays 2nd", size=8)
	tel = fields.Char(string="Téléphone", size=30)
	mail = fields.Char(string="Mail", size=50)
	site = fields.Char(string="Site WEB", size=50)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bank_id = fields.Many2one("res.bank", string = "Banque")
	acc_bank_id = fields.Char(string = "N° Compte", size=30)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_bail', 'unique (cd_bail)', "Ce code existe déjà. Veuillez changer de code !"),
    ]


class BudgFournisseur(models.Model):

	_name = "budg_fournisseur"
	_rec_name = 'nm_rs'
	
	
	no_four = fields.Char(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('no_four'), readonly = True)
	type_fournisseur_id = fields.Many2one("budg_typebeneficiaire",string="Type de fournisseur")
	nm_rs = fields.Char(string="Raison sociale ou Nom")
	nm_rs2 = fields.Char(string=" ")
	an_agre = fields.Date(string="Année agrément")
	no_agre = fields.Integer(string="N° Agrément")
	no_ifu = fields.Char(string="N° IFU", size=11)
	cd_citib = fields.Char(string="Cd_CITIB")
	activite = fields.Char(string="Activité", size  = 50)
	ap_rue = fields.Char(string="Rue")
	ap_bp = fields.Char(string="Boite Postale")
	ap_cd_post = fields.Char(string="Code Postale")
	ap_region = fields.Many2one("ref_region",string="Région")
	ap_ville = fields.Char(string="Ville")
	ap_province = fields.Many2one("ref_province",string="Province")
	ap_pays = fields.Many2one("ref_pays",string="Pays")
	rf_txt_agre = fields.Char(string="Texte n°")
	dt_txt_agre = fields.Date(string="Du")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bank_id = fields.Many2one("res.bank", string = "Banque")
	fg_eng = fields.Char()
	active = fields.Boolean('Actif',default=True)
	agence_bank_id = fields.Char(string = "N° Agence")
	acc_number = fields.Char(string = "N° compte")
	tel = fields.Char(string="Téléphone")
	mail = fields.Char(string="Mail")

	_sql_constraints = [
        ('no_four', 'unique (no_four)', "Ce code existe déjà. Veuillez changer de code !"),
    ]

class BudgContribuable(models.Model):

	_name = "budg_contribuable"
	_rec_name = 'nm_rs'
	
	
	no_contrib = fields.Char(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('no_contrib'), readonly = True)
	type_contribuable_id = fields.Many2one("budg_typecontribuable",string="Type de contribuable")
	nm_rs = fields.Char(string="Raison sociale ou Nom")
	nm_rs2 = fields.Char(string=" ")
	an_agre = fields.Date(string="Année agrément")
	no_agre = fields.Integer(string="N° Agrément")
	no_ifu = fields.Char(string="N° IFU", size=11)
	cd_citib = fields.Char(string="Cd_CITIB")
	activite = fields.Char(string="Activité", size  = 50)
	ap_rue = fields.Char(string="Rue")
	ap_bp = fields.Char(string="Boite Postale")
	ap_cd_post = fields.Char(string="Code Postale")
	ap_region = fields.Many2one("ref_region",string="Région")
	ap_ville = fields.Char(string="Ville")
	ap_province = fields.Many2one("ref_province",string="Province")
	ap_pays = fields.Many2one("ref_pays",string="Pays")
	rf_txt_agre = fields.Char(string="Texte n°")
	dt_txt_agre = fields.Date(string="Du")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bank_id = fields.Many2one("res.partner.bank", string = "Banque")
	fg_eng = fields.Char()
	active = fields.Boolean('Actif',default=True)
	agence_bank_id = fields.Char(string = "N° Agence")
	acc_number = fields.Char(string = "N° compte")
	tel = fields.Char(string="Téléphone")
	mail = fields.Char(string="Mail")

	_sql_constraints = [
        ('no_contrib', 'unique (no_contrib)', "Ce code existe déjà. Veuillez changer de code !"),
    ]


# Définitions des classes du menu paramètre

class Budg_Certification(models.Model):

	_name = "budg_certification"
	_rec_name = "lb_long"

	sequence = fields.Integer(default=10)
	cd_certification = fields.Char(string = "Code", size = 2)
	name = fields.Char(string = "Libellé court", size = 25)
	lb_long = fields.Char(string = "Libellé long", size = 65, required=True)
	active = fields.Boolean('Actif',default=True)

	_sql_constraints = [
        ('cd_certification', 'unique (cd_certification)', "Ce code existe déjà. Veuillez changer de code !"),
    ]


class BudgRubrique(models.Model):
	_name = "budg_rubrique"
	_order = "concate_rubrique"

	sequence = fields.Integer(default=10)
	
	concate_rubrique = fields.Char()
	cd_titre_id = fields.Many2one("budg_titre", string = "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section", string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string ="Paragraphe", required=True)
	rubrique_id = fields.Many2one("ref_rubrique",string="Rubrique")
	rubrique = fields.Char(string="Code Rubrique", required=True)
	lb_court = fields.Char("Libellé court", size = 75, required=False)
	lb_long = fields.Char("Libellé long", size = 200, required=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	active = fields.Boolean('Terminal',default=True)
	no_imputation = fields.Many2one("compta_plan_lines", string = "Imputation Cptble", required=True)

	def name_get(self):
		result = []
		for val in self:
			if val.rubrique:
				result.append((val.id, '%s - %s' % (val.rubrique, val.lb_long)))
		return result
   
	@api.onchange('cd_paragraphe_id')
	def Rub(self):

		for x in self:
			self.cd_titre_id = self.cd_paragraphe_id.cd_titre_id
			self.cd_section_id = self.cd_paragraphe_id.cd_section_id
			self.cd_chapitre_id = self.cd_paragraphe_id.cd_chapitre_id
			self.cd_article_id = self.cd_paragraphe_id.cd_article_id

# Définitions des classes du menu marché & contrat

class BudgAppelOffre(models.Model):
	
	_name = "budg_appeloffre"
	_rec_name = "name"

	
	name = fields.Integer(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('name'), required=True)
	ref_ao = fields.Char(string="Référence A.O", size = 25, required=True)	
	cd_titre_id = fields.Many2one("budg_titre",string="Titre",default=lambda self: self.env['budg_titre'].search([('titre', '=', 2)]))
	cd_section_id = fields.Many2one("budg_section",string="Section")
	cd_nature_depense_id = fields.Many2one("budg_naturedepense", string="Nature",required=True)
	cd_mode_mp_id = fields.Many2one("budg_modemarche", string="Mode")
	cd_bailleur_id = fields.Many2one("budg_bailleur", string="Financement")
	objet_ao = fields.Text(string="Objet", size = 300)
	prix_dossier = fields.Integer(string="Prix du dossier",required=True)
	dt_publication = fields.Date(string="Date de publication")
	dt_depouillement = fields.Date(string="Date de dépouillement")
	dt_resultat = fields.Date(string="Date probable des résultats")
	typ_dest = fields.Char(string="Type destinataire")
	id_dest = fields.Char(string="Identifiant destinataire")
	dt_delai = fields.Date(string="Delai d'exécution")
	nb_j_delai = fields.Integer(string="Nombre de jour", size = 2)
	nb_s_delai = fields.Integer(string="Nombre de semaine", size = 2)
	nb_m_delai = fields.Integer(string="Nombre de mois", size = 2)
	nb_a_delai = fields.Integer(string="Nombre d'année", size = 2)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	_sql_constraints = [
        ('name', 'unique (name)', "Ce code existe déjà. Veuillez changer de code !"),
    ]	


class BudgMarche(models.Model):

	_name = "budg_marche"
	_rec_name = "ref_mp"

	name = fields.Char()
	id_mp = fields.Char(string="Identifiant du marché", default=lambda self: self.env['ir.sequence'].next_by_code('id_mp'), readonly = True)
	ref_mp = fields.Char(string="Référence", required=True)
	id_ao = fields.Many2one("budg_appeloffre", string="Identifiant Appel offre", required=True)
	objet_marche = fields.Text(string = "Objet", size=300)
	cd_titre_id = fields.Many2one("budg_titre", string="Titre", default=lambda self: self.env['budg_titre'].search([('titre','=', 2)]))
	cd_section_id = fields.Many2one("budg_section", string="Section")
	cd_fournisseur_id = fields.Many2one("ref_beneficiaire", string="Bénéficiaire")
	mnt_mp = fields.Integer(string="Montant du marché", size=15, required=True)
	mnt_eng_cf = fields.Integer(string="Montant engagé CF", size=15)
	mnt_liq_cf = fields.Integer(string="Montant liquidé CF", size=15)
	dt_notif = fields.Date(string="Date de notification")
	dt_sign = fields.Date(string="Date de signature (Approuvé le)")
	dt_clot = fields.Date(string="Date de cloture")
	id_dest = fields.Char(string="ID destinataire", size = 6)
	typ_dest = fields.Char(string="Type destinataire", size = 1)
	no_ifu = fields.Char(string="N° IFU", size = 11)
	mnt_vbp = fields.Integer(string ="Montant VBP", size = 15)
	mnt_ecp = fields.Integer(string ="Montant ECP", size = 15)
	mnt_ord = fields.Integer(string ="Montant ORD", size = 15)
	mnt_ex_tresor = fields.Integer(string ="Montant Exo Tresor", size = 15)
	ty_ap = fields.Char(string="Type ap")
	bank_id = fields.Many2one("res.partner.bank", string = "Banque")
	agence_bank_id = fields.Char(string = "N° Agence")
	acc_number = fields.Many2one("res.partner.bank", string = "N° compte")
	nm_titulaire = fields.Many2one("res.partner.bank", string = "Titulaire du comp")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one("ref_structure") 
	cd_mode_mp_id = fields.Many2one("budg_modemarche",  string ="Mode")
	flag_actif = fields.Char(string = "Actif" )
	dt_delai = fields.Date(string="Delai d'exécution")
	nb_j_delai = fields.Integer(string="Nombre jours")
	nb_s_delai = fields.Integer(string="Nombre semaine")
	nb_m_delai = fields.Integer(string="Nombre mois")
	nb_a_delai = fields.Integer(string="Nombre année")
	dt_visa_dmp = fields.Date()
	dt_visa_daf = fields.Date()
	dt_visa_cf = fields.Date()
	dt_visa_ord = fields.Date()	
	cd_type_beneficiaire_id = fields.Many2one("ref_typebeneficiaire", string="Type de bénéficiaire")
	cd_type_financement_id = fields.Many2one("ref_bailleur", "Financement")
	beneficiaire_id = fields.Many2one("ref_beneficiaire", string="Bénéficiaire")
	#cd_nature_depense_id = fields.Many2one("budg_naturedepense", string="Nature")
	state = fields.Selection([
        ('draft', 'Brouillon'),
        ('N', 'Confirmé'),
        ('V', 'Approuvé par DMP'),
		('A', 'Annulé'),
		('W', 'Visé par DAF'),
		('WCF', 'Visé par CF'),
		('WORD', 'Visé par ORD'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
	
	_sql_constraints = [
        ('ref_mp', 'unique (ref_mp)', "Ce code existe déjà. Veuillez changer de code !"),
    ]


	def action_marche_draft(self):
		self.write({'state': 'draft'})


	def action_marche_confirmer(self):
		self.write({'state': 'N'})
		

	def action_marche_approuver_dmp(self):
		self.write({'state': 'V'})
		

	def action_marche_annuler(self):
		self.write({'state': 'A'})
		

	def action_marche_viser_daf(self):
		self.write({'state': 'W'})
		

	def action_marche_viser_cf(self):
		self.write({'state': 'WCF'})
		

	def action_marche_viser_ord(self):
		self.write({'state': 'WORD'})

	@api.onchange('id_ao')

	def id_ao_on_change(self):

		if self.id_ao:
			self.ref_mp = self.id_ao.ref_ao
			self.cd_section_id = self.id_ao.cd_section_id
			#self.cd_nature_depense_id = self.id_ao.cd_nature_depense_id
			self.cd_type_financement_id = self.id_ao.cd_bailleur_id
			self.cd_mode_mp_id = self.id_ao.cd_mode_mp_id
			
			
class BudgContratService(models.Model):
	
	_name = 'budg_contrat_service'
	
	origine = fields.Char("Origine contrat")
	reference = fields.Char("Référence")
	nature_contrat = fields.Char("Nature contrat")
	#nature_depense = fields.Many2one("budg_naturedepense", "Nature dépense")
	mnt_disponible = fields.Integer("Info créd. dispo")
	mnt_contrat = fields.Integer("Montant contrat")
	id_appel = fields.Many2one("budg_appeloffre", "Identifiant Appel/Demande")
	mode_passation = fields.Many2one("budg_modemarche", "Mode de passation")
	financement_id = fields.Many2one("ref_bailleur", "Financement")
	type_beneficiaire = fields.Many2one("ref_typebeneficiaire", "Type Bénéficiaire")
	beneficiaire_id = fields.Many2one("ref_beneficiaire", string="Identité")
	cd_titre_id = fields.Many2one("budg_titre", string = "Titre", required=True)
	cd_section_id = fields.Many2one("budg_section", string = "Section", required=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", required=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", required=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", required=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", required=True)
	objet_contrat = fields.Text("Objet contrat")
	dt_notif = fields.Date(string="Notifié le")
	dt_sign = fields.Date(string="Signé le")
	dt_clot = fields.Date(string="Clôturé le")
	dt_exec = fields.Date(string="Exécuté le")
	nb_j_delai = fields.Integer(string="Nombre jours")
	nb_s_delai = fields.Integer(string="Nombre semaine")
	nb_m_delai = fields.Integer(string="Nombre mois")
	nb_a_delai = fields.Integer(string="Nombre année")
	etat = fields.Selection([
        ('draft', 'Brouillon'),
        ('N', 'Confirmé'),
        ('V', 'Approuvé par DMP'),
		('A', 'Annulé'),
        ], 'Etat', default='draft')
	

	def action_draft(self):
		self.write({'etat': 'draft'})


	def action_confirmer(self):
		self.write({'etat': 'N'})
		

	def action_approuver(self):
		self.write({'etat': 'V'})
		

	def action_annuler(self):
		self.write({'etat': 'A'})
	

class BudgBudget(models.Model):

	_name = "budg_budget"
	_rec_name = "refp"

	name = fields.Char(string="Nom")
	typebudget_id = fields.Many2one("budg_typebudget", string="Type de Budget", required=True)
	cd_type_piece_budget = fields.Many2one("budg_typepiecebudget", string="Type de Pièce", required=True)
	refp = fields.Char(string = "Ref.Piece", required=True)
	date_to = fields.Date(string = "Date de mise en place", required=True)	
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	dots_titre1 = fields.Float("RECETTES", compute="compute_dotation_titre1")
	dots_titre2 = fields.Float("DEPENSES", compute="compute_dotation_titre2")
	ecarts = fields.Float("ECART", compute="compute_ecart")
	dot_titre1section1 = fields.Float("Recettes/Fonctionnement", compute="compute_dotation_titre1section1")
	dot_titre1section2 = fields.Float("Recettes/Investissements", compute="compute_dotation_titre1section2")
	dot_titre2section1 = fields.Float("Dépenses/Fonctionnement", compute="compute_dotation_titre2section1")
	dot_titre2section2 = fields.Float("Dépenses/Investissements", compute="compute_dotation_titre2section2")
	dot_titre1section1chapitre = fields.Float("Titre I/Sect I/Chap", compute="compute_dotation_titre1section1chapitre")
	sum_titre = fields.Float("TITRES")
	dot_titre1section2chapitre = fields.Float("Titre I/Sect II/Chap")
	fichier_joint = fields.Binary(string="Joindre l'acte", attachment=True)
	rubrique_ids = fields.One2many("budg_ligne_budgetaire", "budg_id", states={'E': [('readonly', True)]})
	state = fields.Selection([
        ('AP', 'Avant projet'), ('N', 'Projet'), ('E', 'Exécutoire')
        ], 'Etat', default='AP', index=True, required=True, readonly=True, copy=False, track_visibility='always')
	date_execution = fields.Date("Date execution")

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")

	"""
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id"""
	

	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0 :
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))
	
	#fonction de controle du type de budget	pour empecher la double saisie du budget primitif
	@api.onchange('typebudget_id')
	def controle_type_budget(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		self.env.cr.execute("select count(b.id) FROM budg_budget b, budg_typebudget t, ref_exercice r WHERE b.x_exercice_id = %d AND b.company_id = %d and t.id = b.typebudget_id AND t.cd_type_budget = 'BI' " %(val_ex, val_struct))
		res = self.env.cr.fetchone()
		val = res and res[0]
		if val > 0 and self.typebudget_id.cd_type_budget == 'BI':
			raise ValidationError(_('Le budget initial' + " " +  str(self.x_exercice_id.no_ex) + " " + 'est déjà saisi.'))
		
	
		
	#fonction de validation et réaménagement budgetaire
	def validation_budget(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_budg = int(self.id)
	
		
		#recuperation des données des recettes
		self.env.cr.execute("""SELECT l.cd_titre_id, l.cd_section_id, l.cd_chapitre_id, l.cd_article_id, l.cd_paragraphe_id, l.cd_rubrique_id, 
		coalesce((l.mnts_budgetise),0) as mnts_budgetise FROM budg_ligne_budgetaire l, budg_titre t WHERE l.x_exercice_id = %d AND l.company_id = %d 
		AND l.budg_id = %d AND l.cd_titre_id = t.id AND t.type_titre = 'R' """ %(val_ex, val_struct, val_budg))
		for line in self.env.cr.dictfetchall():
			#print('ligne', line['mnts_budgetise'])
				
			v_titre = line['cd_titre_id']
			v_section = line['cd_section_id']
			v_chap = line['cd_chapitre_id']
			v_article =  line['cd_article_id']
			v_para = line['cd_paragraphe_id']
			v_rub =  line['cd_rubrique_id']
			mnt_budgetise = line['mnts_budgetise']
			
			#curseur pour compter le nombre de ligne de depense dans la ligne executoire des dépenses
			self.env.cr.execute("""SELECT coalesce(count(*),0) FROM budg_ligne_exe_rec 
				WHERE cd_titre_id = %s AND cd_section_id = %s AND cd_chapitre_id = %s AND cd_art_id = %s AND
				cd_paragraphe_id = %s AND cd_rubrique_id = %s AND x_exercice_id = %s AND company_id = %s """ ,(v_titre,v_section,v_chap,v_article,v_para,v_rub,val_ex,val_struct))
			curs_verif_recette = self.env.cr.fetchone()[0] or 0
			print('nombre ligne de recette',curs_verif_recette)
				
			if curs_verif_recette == 0:
				self.env.cr.execute("""INSERT INTO budg_ligne_exe_rec (cd_titre_id, cd_section_id, cd_chapitre_id, cd_art_id, cd_paragraphe_id, cd_rubrique_id, mnt_budgetise,mnt_corrige, reste_emettre, company_id, x_exercice_id, budg_id) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
				""" ,(v_titre, v_section, v_chap, v_article, v_para, v_rub, mnt_budgetise, mnt_budgetise,mnt_budgetise, val_struct, val_ex, val_budg))				
				
				#self.env.cr.execute("""INSERT INTO compta_cg_rec_line (cd_titre_id, cd_section_id, cd_chapitre_id, cd_art_id, cd_paragraphe_id, cd_rubrique_id, mnt_budgetise,mnt_corrige,rest_recouvrer, company_id, x_exercice_id, budg_id) 
				#VALUES (%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)  
				#""" %(v_titre, v_section, v_chap, v_article, v_para, v_rub, mnt_budgetise, mnt_budgetise,mnt_budgetise, val_struct, val_ex, val_budg))				
			else:
				self.env.cr.execute("""UPDATE budg_ligne_exe_rec SET mnt_corrige = coalesce((mnt_corrige),0) + %s, reste_emettre = coalesce((reste_emettre),0) + %s
				WHERE cd_titre_id = %s AND cd_section_id = %s AND  cd_chapitre_id = %s and  cd_art_id = %s and
				cd_paragraphe_id = %s AND cd_rubrique_id = %s AND x_exercice_id = %s AND company_id = %s """
				,(mnt_budgetise,mnt_budgetise,v_titre,v_section,v_chap,v_article,v_para,v_rub,val_ex,val_struct))			
		
				#self.env.cr.execute("""UPDATE compta_cg_rec_line SET mnt_corrige = mnt_corrige + %d
				#WHERE cd_titre_id = %d AND cd_section_id = %d AND  cd_chapitre_id = %d and  cd_art_id = %d and
				#cd_paragraphe_id = %d AND cd_rubrique_id = %d AND x_exercice_id = %d AND company_id = %d """
				#%(mnt_budgetise,v_titre,v_section,v_chap,v_article,v_para,v_rub,val_ex,val_struct))			
		
		#recuperation des données des dépenses
		self.env.cr.execute("""SELECT  l.cd_titre_id, l.cd_section_id, l.cd_chapitre_id, l.cd_article_id, l.cd_paragraphe_id, l.cd_rubrique_id, 
		coalesce((l.mnts_budgetise),0) as mnts_budgetise FROM budg_ligne_budgetaire l, budg_titre t WHERE l.x_exercice_id = %d AND l.company_id = %d 
		and l.budg_id = %d AND l.cd_titre_id = t.id AND t.type_titre = 'D' """ %(val_ex, val_struct, val_budg))	
		for line in self.env.cr.dictfetchall():
				
			v_titre1 = line['cd_titre_id']
			v_section1 = line['cd_section_id']
			v_chap1 = line['cd_chapitre_id']
			v_article1 = line['cd_article_id']
			v_para1 = line['cd_paragraphe_id']
			v_rub1 = line['cd_rubrique_id']
			mnt_budgetise1 = line['mnts_budgetise']
		
			#curseur pour compter le nombre de ligne de depense dans la ligne executoire des dépenses
			self.env.cr.execute("""SELECT coalesce(count(*),0) FROM budg_ligne_exe_dep 
				WHERE cd_titre_id = %s AND cd_section_id = %s AND cd_chapitre_id = %s AND cd_art_id = %s AND
				cd_paragraphe_id = %s AND cd_rubrique_id = %s AND x_exercice_id = %s AND company_id = %s """ ,(v_titre1,v_section1,v_chap1,v_article1,v_para1,v_rub1,val_ex,val_struct))
			curs_verif_depense = self.env.cr.fetchone()[0] or 0
			#curs_verif_depense = curs_verif_dep and curs_verif_dep[0]
			print('nombre ligne de depense',curs_verif_depense)
			
			if curs_verif_depense == 0:
				self.env.cr.execute("""INSERT INTO budg_ligne_exe_dep (cd_titre_id, cd_section_id, cd_chapitre_id, cd_art_id, cd_paragraphe_id, cd_rubrique_id, mnt_budgetise,mnt_corrige, mnt_disponible, reste_mandat, company_id, x_exercice_id, budg_id) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
				""" ,(v_titre1, v_section1, v_chap1, v_article1, v_para1, v_rub1, mnt_budgetise1, mnt_budgetise1, mnt_budgetise1,mnt_budgetise1, val_struct, val_ex, val_budg))					
				
				#self.env.cr.execute("""INSERT INTO compta_cg_dep_line (cd_titre_id, cd_section_id, cd_chapitre_id, cd_art_id, cd_paragraphe_id, cd_rubrique_id, mnt_budgetise,mnt_corrige, company_id, x_exercice_id, budg_id) 
				#VALUES (%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d) 
				#""" %(v_titre1, v_section1, v_chap1, v_article1, v_para1, v_rub1, mnt_budgetise1, mnt_budgetise1, val_struct, val_ex, val_budg))					
			else:
				self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_corrige = coalesce((mnt_corrige),0) + %s, mnt_disponible = coalesce((mnt_disponible),0) + %s, reste_mandat = coalesce((reste_mandat),0) + %s
				WHERE cd_titre_id = %s AND cd_section_id = %s AND  cd_chapitre_id = %s AND  cd_art_id = %s AND
				cd_paragraphe_id = %s AND cd_rubrique_id = %s AND x_exercice_id = %s AND company_id = %s """
				,(mnt_budgetise1,mnt_budgetise1,mnt_budgetise1,	v_titre1,v_section1,v_chap1,v_article1,v_para1,v_rub1,val_ex,val_struct))
				
				#self.env.cr.execute("""UPDATE compta_cg_dep_line SET mnt_corrige = mnt_corrige + %d
				#WHERE cd_titre_id = %d AND cd_section_id = %d AND  cd_chapitre_id = %d AND  cd_art_id = %d AND
				#cd_paragraphe_id = %d AND cd_rubrique_id = %d AND x_exercice_id = %d AND company_id = %d """
				#%(mnt_budgetise1,v_titre1,v_section1,v_chap1,v_article1,v_para1,v_rub1,val_struct,val_ex))
	

	def valider_avt_projet(self):
		self.write({'state': 'N'})
				

	def budget_valider(self):
		
		if (self.dots_titre1 - self.dots_titre2 == 0):
			self.validation_budget()
			self.date_execution = date.today()
			self.write({'state': 'E'})
		else:
			raise ValidationError(_('Vous ne pouvez pas valider le budget car les dépenses et les recettes ne sont pas équilibrées.'))
	

	def compute_dotation_titre1(self):
		
		val_budg = (self.id)
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			val.env.cr.execute("select sum(l.mnts_budgetise) from ref_titre t, budg_titre bt, budg_ligne_budgetaire l where t.cd_titre = 'I' and t.id = bt.titre and bt.id = l.cd_titre_id  and l.x_exercice_id = %d and l.company_id = %d and budg_id = %d group by t.cd_titre" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dots_titre1 = res and res[0]

	def compute_dotation_titre2(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			val.env.cr.execute("select sum(l.mnts_budgetise) from ref_titre t, budg_titre bt, budg_ligne_budgetaire l where t.cd_titre = 'II' and t.id = bt.titre and bt.id = l.cd_titre_id  and l.x_exercice_id = %d and l.company_id = %d and budg_id = %d group by t.cd_titre" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dots_titre2 = res and res[0]

	def compute_ecart(self):
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
			
			self.ecarts = self.dots_titre1 - self.dots_titre2

	def compute_dotation_titre1section1(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			val.env.cr.execute("select sum(l.mnts_budgetise) from ref_exercice e,ref_titre t ,ref_section s INNER JOIN budg_ligne_budgetaire l ON s.id = l.cd_section_id where s.cd_section = 'I' and l.cd_titre_id =  t.id and t.cd_titre = 'I' and e.etat = 1 and l.x_exercice_id = %d and l.company_id = %d and budg_id = %s group by cd_section,l.cd_titre_id" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dot_titre1section1 = res and res[0]
		

	def compute_dotation_titre1section2(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			self.env.cr.execute("select sum(l.mnts_budgetise) from ref_exercice e,ref_titre t ,ref_section s INNER JOIN budg_ligne_budgetaire l ON s.id = l.cd_section_id where s.cd_section = 'II' and l.cd_titre_id =  t.id and t.cd_titre = 'I'and e.etat = 1 and l.x_exercice_id = %d and l.company_id = %d and budg_id = %s group by cd_section,l.cd_titre_id" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dot_titre1section2 = res and res[0]
		

	def compute_dotation_titre2section1(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			self.env.cr.execute("select sum(l.mnts_budgetise) from ref_exercice e,ref_titre t ,ref_section s INNER JOIN budg_ligne_budgetaire l ON s.id = l.cd_section_id where s.cd_section = 'I' and l.cd_titre_id =  t.id and t.cd_titre = 'II'and e.etat = 1 and l.x_exercice_id = %d and l.company_id = %d and budg_id = %s group by cd_section,l.cd_titre_id" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dot_titre2section1 = res and res[0]

	def compute_dotation_titre2section2(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			self.env.cr.execute("select sum(l.mnts_budgetise) from ref_exercice e,ref_titre t ,ref_section s INNER JOIN budg_ligne_budgetaire l ON s.id = l.cd_section_id where s.cd_section = 'II' and l.cd_titre_id =  t.id and t.cd_titre = 'II' and e.etat = 1 and l.x_exercice_id = %d and l.company_id = %d and budg_id = %s group by cd_section,l.cd_titre_id" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dot_titre2section2 = res and res[0]

	def compute_dotation_titre1section1chapitre(self):
		
		val_budg = (self.id)
		
		for val in self:
		
			val_ex = int(self.x_exercice_id.id)
			val_struct = int(self.company_id.id)
				
			self.env.cr.execute("""select sum(l.mnts_budgetise) 
			from ref_exercice e,ref_titre t,ref_section s, ref_chapitre c INNER JOIN l ON c.id = l.cd_chapitre_id where s.id = c.cd_section_id 
			and s.cd_section = 'I'and t.id = s.cd_titre_id and t.cd_titre = 'I' and e.etat = 1 and l.x_exercice_id = %d and l.company_id = %d and budg_id = %s group by l.cd_chapitre_id""" %(val_ex,val_struct, val_budg))
			res = self.env.cr.fetchone()
			self.dot_titre1section1chapitre = res and res[0]
	
	
	def AfficherRubrique(self):
		
		v_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("""select cd_titre_id as tit, cd_section_id as sec, cd_chapitre_id as chap, cd_paragraphe_id as par, cd_article_id as art, id as rub
			from budg_rubrique where company_id = %d order by tit, sec, chap, par, art, id""" %(v_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
            
			vals.rubrique_ids.unlink()
			for line in rows:
				result.append((0,0, {'cd_titre_id' : line['tit'],'cd_section_id' : line['sec'],'cd_chapitre_id' : line['chap'],'cd_paragraphe_id' : line['par'],'cd_article_id' : line['art'],'cd_rubrique_id' : line['rub']}))
			self.rubrique_ids = result

			self.ValeurExercice()
	
	#Fonction impression de façon groupé
	def get_report_values(self):
		
		budg_id = int(self.id)
		print("budget",budg_id)
		company_id = int(self.company_id)
		print("struct",company_id)
		x_exercice_id = int(self.x_exercice_id)
		print("exercice",x_exercice_id)
	

		doctitre = []
		self.env.cr.execute("SELECT cd_titre, lb_long, coalesce(somtitre,0) as somtitre, coalesce(an1,0) as an1, coalesce(an1exe,0) as an1exe, coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe FROM vue_titre WHERE budg_id = %d and company_id = %d and x_exercice_id = %d" %(budg_id, company_id, x_exercice_id))
		for line in self.env.cr.dictfetchall():
			
			v_titre = line['cd_titre']
			print("titr",v_titre)

			v_mnttit = int(line['somtitre'])
			print("mnttit",v_mnttit)

			v_mnttitan1 = line['an1']
			v_mnttitan1exe = line['an1exe']

			v_mnttitan2 = line['an2']
			v_mnttitan2exe = line['an2exe']

			v_mnttitprec = line['prec']
			v_mnttitprecexe = line['precexe']

			libtitre = line['lb_long']
			print("libelle",libtitre)
			

			#Boucle 2
			docsection=[]
			self.env.cr.execute("SELECT cd_titre, cd_section, lb_long, coalesce(somsection,0) as somsection , coalesce(an1,0) as an1 , coalesce(an1exe,0) as an1exe , coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe FROM vue_section WHERE budg_id = %s and cd_titre = '%s' and company_id = %s and x_exercice_id = %s" %(budg_id,v_titre, company_id, x_exercice_id))
			for line in self.env.cr.dictfetchall():
				
				v_section = line['cd_section']
				print("sect",v_section)
				v_mntsec = int(line['somsection'])
				print("mntsec",v_mntsec)
				v_mntsecan1 = line['an1']
				v_mntsecan1exe = line['an1exe']
				print("mntpar",v_mntsecan1)
				v_mntsecan2 = line['an2']
				v_mntsecan2exe = line['an2exe']
				print("mntpar",v_mntsecan2)
				v_mntsecprec = line['prec']
				v_mntsecprecexe = line['precexe']
				print("mntpar",v_mntsecprec)
				libsec = line['lb_long']
				print("libelle",libsec)
				
				

				#Boucle 3
				docchapitre=[]
				self.env.cr.execute("SELECT cd_titre, cd_section,cd_chapitre, lb_long, coalesce(somchapitre,0) as som, coalesce(an1,0) as an1, coalesce(an1exe,0) as an1exe, coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe FROM vue_chapitre WHERE cd_titre = '%s' and cd_section = '%s' and budg_id = %s and company_id = %s and x_exercice_id = %s" %(v_titre, v_section,budg_id, company_id, x_exercice_id))
				for line in self.env.cr.dictfetchall():
				
					v_chapitre = line['cd_chapitre']
					print("chap",v_chapitre)

					v_mntchap = int(line['som'])
					print("mntchap",v_mntchap)

					v_mntchapan1 = line['an1']
					v_mntchapan1exe = line['an1exe']
					print("mntpar",v_mntchapan1)
					v_mntchapan2 = line['an2']
					v_mntchapan2exe = line['an2exe']
					print("mntpar",v_mntchapan2)
					v_mntchapprec = line['prec']
					v_mntchapprecexe = line['precexe']
					print("mntpar",v_mntchapprec)
					libchap = line['lb_long']
					print("libelle", libchap)
					

					#Boucle 4
					docarticle=[]
					self.env.cr.execute("SELECT cd_titre, cd_section,cd_chapitre,cd_article, lb_long, coalesce(somarticle,0) as somarticle, coalesce(an1,0) as an1, coalesce(an1exe,0) as an1exe, coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe FROM vue_article WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and company_id = %s and x_exercice_id = %s" %(budg_id,v_titre, v_section, v_chapitre, company_id, x_exercice_id))
					for line in self.env.cr.dictfetchall():

						v_article = line['cd_article']
						print("art",v_article)
						v_mntart = int(line['somarticle'])
						print("mntart",v_mntart)
						v_mntartan1 = line['an1']
						v_mntartan1exe = line['an1exe']
						print("mntpar",v_mntartan1)
						v_mntartan2 = line['an2']
						v_mntartan2exe = line['an2exe']
						print("mntpar",v_mntartan2)
						v_mntartprec = line['prec']
						v_mntartprecexe = line['precexe']
						print("mntpar",v_mntartprec)
						libart = line['lb_long']
						print("libelle",libart)



						#Boucle 4
						docparagraphe=[]
						self.env.cr.execute("SELECT cd_titre, cd_section,cd_chapitre,cd_article,cd_paragraphe, lb_long, coalesce(somparagraphe,0) as somparagraphe, coalesce(an1,0) as an1, coalesce(an1exe,0) as an1exe, coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe FROM vue_paragraphe WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and company_id = %s and x_exercice_id = %s" %(budg_id,v_titre, v_section, v_chapitre, v_article, company_id, x_exercice_id))
						for line in self.env.cr.dictfetchall():

							v_paragraphe = line['cd_paragraphe']
							print("par",v_paragraphe)
							v_mntpar = int(line['somparagraphe'])
							print("mntpar",v_mntpar)
							v_mntparan1 = line['an1']
							v_mntparan1exe = line['an1exe']
							print("mntpar",v_mntparan1)
							v_mntparan2 = line['an2']
							v_mntparan2exe = line['an2exe']
							print("mntpar2",v_mntparan2)

							v_mntparprec = line['prec']
							v_mntparprecexe = line['precexe']
							print("mntparprec",v_mntparprec)
							libpar = line['lb_long']
							print("libelle",libpar)

							docrubrique=[]
							self.env.cr.execute("""SELECT cd_titre, cd_section,cd_chapitre,cd_article,cd_paragraphe,rubrique, coalesce(somrubrique,0) as somrubrique, lb_long, coalesce(an1,0) as an1, coalesce(an1exe,0) as an1exe, coalesce(an2,0) as an2, coalesce(an2exe,0) as an2exe, coalesce(prec,0) as prec, coalesce(precexe,0) as precexe
							FROM vue_rubrique WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and cd_paragraphe = '%s' and company_id = %s and x_exercice_id = %s""" %(budg_id, v_titre, v_section, v_chapitre, v_article, v_paragraphe,company_id, x_exercice_id))
							for rubs in self.env.cr.dictfetchall():


								v_rubrique =  rubs['rubrique']
								print("rubrique",v_rubrique)
								v_mntrub = int(rubs['somrubrique'])
								print("mntrub",v_mntrub)
								v_ruban1 = rubs['an1']
								v_ruban1exe = rubs['an1exe']
								print("ruban1",v_ruban1)
								v_ruban2 = rubs['an2']
								v_ruban2exe = rubs['an2exe']
								print("ruban2",v_ruban2)
								v_rubprec = rubs['prec']
								v_rubprecexe = rubs['precexe']
								print("rubprec",v_rubprec)
								librub = rubs['lb_long']
								print("libelle",librub)

								erubriq = {v_rubrique : [v_ruban2, v_ruban2exe, v_ruban1, v_ruban1exe, v_rubprec, v_rubprecexe, v_mntrub, librub]}
								erubri = OrderedDict(sorted(erubriq.items(), key=lambda t:t[0]))
								docrubrique.append(erubri)

							eparagraphes = {v_paragraphe : [v_mntparan2, v_mntparan2exe, v_mntparan1, v_mntparan1exe, v_mntparprec,v_mntparprecexe, v_mntpar, libpar],'rubrique':docrubrique}
							eparagraphe = OrderedDict(sorted(eparagraphes.items(), key=lambda t:t[0]))
							docparagraphe.append(eparagraphe)

						earticles={v_article : [v_mntartan2, v_mntartan2exe, v_mntartan1, v_mntartan1exe, v_mntartprec, v_mntartprecexe, v_mntart, libart], "paragraphe":docparagraphe}
						earticle = OrderedDict(sorted(earticles.items(), key=lambda t:t[0]))
						docarticle.append(earticle)

					echapitres = {v_chapitre: [v_mntchapan2, v_mntchapan2exe, v_mntchapan1, v_mntchapan1exe, v_mntchapprec, v_mntchapprecexe, v_mntchap, libchap], "article": docarticle}
					echapitre = OrderedDict(sorted(echapitres.items(), key=lambda t:t[0]))
					docchapitre.append(echapitre)
					
				esections = {v_section : [v_mntsecan2,v_mntsecan2exe, v_mntsecan1, v_mntsecan1exe, v_mntsecprec, v_mntsecprecexe, v_mntsec, libsec], "chapitre": docchapitre}
				esection = OrderedDict(sorted(esections.items(), key=lambda t:t[0]))
				docsection.append(esection)
				
			etitres = {v_titre : [v_mnttitan2 ,v_mnttitan2exe, v_mnttitan1, v_mnttitan1exe, v_mnttitprec, v_mnttitprecexe, v_mnttit, libtitre], "section": docsection}
			etitre = OrderedDict(sorted(etitres.items(), key=lambda t:t[0]))
			doctitre.append(etitre)
			print("result",doctitre)
			
		return doctitre

	def ValeurExercice(self):
		budg = int(self.id)
		v_exercice = int(self.x_exercice_id)
		v_exe = int(self.x_exercice_id.no_ex)
		v_exe1 = int(v_exe) - 1
		v_ex = int(v_exe1)
		v_exe2 = int(v_exe) - 2
		v_ex2 = int(v_exe2)
		v_exe3 = int(v_exe) - 3
		v_ex3 = int(v_exe3)
		v_com = int(self.company_id)

		self.env.cr.execute("""SELECT l.cd_titre_id, l.cd_section_id, l.cd_chapitre_id, l.cd_article_id, l.cd_paragraphe_id, l.cd_rubrique_id, 
		coalesce((l.mnts_budgetise),0) as mnts_budgetise FROM budg_ligne_budgetaire l WHERE l.x_exercice_id = %d AND l.company_id = %d 
		and l.budg_id = %d """ % (v_exercice, v_com, budg))

		for line in self.env.cr.dictfetchall():
			v_titre = line['cd_titre_id']
			v_section = line['cd_section_id']
			v_chap = line['cd_chapitre_id']
			v_art = line['cd_article_id']
			v_para = line['cd_paragraphe_id']
			v_rub = line['cd_rubrique_id']

			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex))

			mnt = self.env.cr.fetchone()
			mnts_prec = mnt and mnt[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex))

			mntexe = self.env.cr.fetchone()
			mnts_precexe = mntexe and mntexe[0] or 0

			self.env.cr.execute("""update budg_ligne_budgetaire set mnts_precedent = %d, mnts_precedentexe = %d where cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d
			and cd_article_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (mnts_prec,mnts_precexe,
			v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_exercice))



			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex2))

			mnt2 = self.env.cr.fetchone()
			mnts_ant2 = mnt2 and mnt2[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex2))

			mnt2exe = self.env.cr.fetchone()
			mnts_ant2exe = mnt2exe and mnt2exe[0] or 0

			self.env.cr.execute("""update budg_ligne_budgetaire set mnts_ant2 = %d, mnts_ant2exe = %d where cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d
			and cd_article_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
			mnts_ant2, mnts_ant2exe, v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_exercice))




			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and l.company_id = %d and cast(r.no_ex as int) = %d""" % (
			v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex3))

			mnt1 = self.env.cr.fetchone()
			mnts_ant1 = mnt1 and mnt1[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex3))

			mnt1exe = self.env.cr.fetchone()
			mnts_ant1_exe = mnt1exe and mnt1exe[0] or 0

			self.env.cr.execute("""update budg_ligne_budgetaire set mnts_ant1 = %d, mnts_ant1exe = %d where cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d
			and cd_article_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
			mnts_ant1, mnts_ant1_exe, v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_exercice))




class BudgLigneBudgetaire(models.Model):

	_name = "budg_ligne_budgetaire"

	budg_id = fields.Many2one("budg_budget", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", string = "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section", string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", required=False)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", required=False)
	mnts_ant1 = fields.Float(string = "Ex n-3 Prévision", readonly=True)
	mnts_ant1exe = fields.Float(string = "Ex n-3 Exécution", readonly=True)
	mnts_ant2 = fields.Float(string = "EX n-2 Prévision", readonly=True)
	mnts_ant2exe = fields.Float(string = "Ex n-2 Exécution", readonly=True)
	mnts_precedent = fields.Float(string = "Ex n-1 Prévision", readonly=True)
	mnts_precedentexe = fields.Float(string = "Ex n-1 Exécution", readonly=True)
	mnts_budgetise = fields.Float("Montant budgétisé", required=False)
	mnt_ant1 = fields.Float(string = "Ex n-3")
	mnt_ant2 = fields.Float(string = "EX n-2")
	mnt_precedent = fields.Float(string = "Ex n-1")
	mnt_budgetise = fields.Float("Montant budgétisé")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	fg_rea = fields.Boolean('OK ?', default = False)
	
	@api.onchange('cd_titre_id', 'cd_section_id', 'cd_chapitre_id','cd_article_id','cd_paragraphe_id','cd_rubrique_id')
	def valprec(self):
		v_titre = int(self.cd_titre_id)
		v_section = int(self.cd_section_id)
		v_chap = int(self.cd_chapitre_id)
		v_art = int(self.cd_article_id)
		v_para = int(self.cd_paragraphe_id)
		v_rub = int(self.cd_rubrique_id)
		v_exercice = int(self.x_exercice_id)
		v_exe = int(self.x_exercice_id.no_ex)
		v_exe1 = int(v_exe) - 1
		v_ex = int(v_exe1)
		v_exe2 = int(v_exe) - 2
		v_ex2 = int(v_exe2)
		v_exe3 = int(v_exe) - 3
		v_ex3 = int(v_exe3)
		v_com = int(self.company_id)
		
		for record in self:
		
			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" %(v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex))
	
			mnt = self.env.cr.fetchone()
			self.mnts_precedent = mnt and mnt[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex))

			mntexe = self.env.cr.fetchone()
			self.mnts_precedentexe = mntexe and mntexe[0] or 0
			
		
		for record in self:
		
			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" %(v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex2))
			
			mnt = self.env.cr.fetchone()
			self.mnts_ant2 = mnt and mnt[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" % (v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex2))

			mnt2exe = self.env.cr.fetchone()
			self.mnts_ant2exe = mnt2exe and mnt2exe[0] or 0

		
		for record in self:
		
			self.env.cr.execute("""select coalesce(sum(mnts_budgetise),0) from budg_ligne_budgetaire l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_article_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and 
			l.company_id = %d and cast(r.no_ex as int) = %d""" %(v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex3))
	
			mnt = self.env.cr.fetchone()
			self.mnts_ant1 = mnt and mnt[0] or 0

			self.env.cr.execute("""select coalesce(sum(mnt_engage),0) from budg_ligne_exe_dep l, ref_exercice r where l.cd_titre_id = %d and cd_section_id = %d and l.cd_chapitre_id = %d
			and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and l.company_id = %d and cast(r.no_ex as int) = %d""" % (
			v_titre, v_section, v_chap, v_art, v_para, v_rub, v_com, v_ex3))

			mnt1exe = self.env.cr.fetchone()
			self.mnts_ant1exe = mnt1exe and mnt1exe[0] or 0
	
	
	@api.onchange('cd_paragraphe_id')
	def Rub(self):

		for x in self:
			x.cd_titre_id = x.cd_paragraphe_id.cd_titre_id
			x.cd_section_id = x.cd_paragraphe_id.cd_section_id
			x.cd_chapitre_id = x.cd_paragraphe_id.cd_chapitre_id
			x.cd_article_id = x.cd_paragraphe_id.cd_article_id
			#x.cd_paragraphe_id = x.cd_rubrique_id.cd_paragraphe_id
	
			

class BudgActReamenagement(models.Model):
	_name = "budg_act_reamenagement"
	
	name = fields.Char("")

class BudgPieceEng(models.Model):
	_name = "budg_piece_engagement"

	sequence = fields.Integer(default=10)
	lb_long = fields.Many2one("ref_piece_justificatives", "Libellé", required=True)
	oblige = fields.Boolean("Obligatoire")
	nombre = fields.Integer("Nombre")
	ref = fields.Char("Référence", required=True)
	montant = fields.Integer("Montant")
	dte = fields.Date("Date")
	eng_id = fields.Many2one("budg_engagement", ondelete='cascade')
	x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	

class BudgPieceLiq(models.Model):
	_name = "budg_piece_liq"

	sequence = fields.Integer(default=10)
	lb_long = fields.Many2one("ref_piece_justificatives", "Libellé")
	oblige = fields.Boolean("Obligé")
	nombre = fields.Integer("Nombre")
	ref = fields.Char("Référence")
	montant = fields.Integer("Montant")
	dte = fields.Date("Date")
	liq_id = fields.Many2one("budg_liqord", ondelete='cascade')
	x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	

class BudgPieceOrd(models.Model):
	_name = "budg_piece_ord"

	sequence = fields.Integer(default=10)
	lb_long = fields.Many2one("ref_piece_justificatives", "Libellé")
	oblige = fields.Boolean("Obligé")
	nombre = fields.Integer("Nombre")
	ref = fields.Char("Référence")
	dte = fields.Date("Date")
	montant = fields.Integer("Montant")
	mandat_id = fields.Many2one("budg_mandat", ondelete='cascade')
	x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	

class BudgPieceRec(models.Model):
	_name = "budg_piece_recette"
	
	lb_long = fields.Many2one("ref_piece_justificatives", "Libellé")
	oblige = fields.Boolean("Obligé")
	nombre = fields.Integer("Nombre")
	ref = fields.Char("Référence")
	montant = fields.Integer("Montant")
	recette_id = fields.Many2one("budg_titrerecette", ondelete='cascade')
	x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	

class BudgEngagement(models.Model):

	_name = "budg_engagement"
	_rec_name = "no_eng"
	_order = " id desc"

	no_eng = fields.Char(string="N° engagement", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", default=lambda self: self.env['budg_titre'].search([('type_titre','=', 'D')]), string = "Titre", required=True, readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", required=True,
									states={'R': [('readonly', True)],'W': [('readonly', True)], 'V': [('readonly', True)],'L': [('readonly', True)],'O': [('readonly', True)]})
	lbsection = fields.Char()
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", required=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	cd_article_id = fields.Many2one("budg_param_article", string="Article", required=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", required=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", required=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", required=True, states={'R': [('readonly', True)],'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	type_budget_id = fields.Many2one("budg_typebudget", string="Type de budget", states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", required=True, string="Catégorie Benef./Four.", states={'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	no_beneficiaire = fields.Many2one("ref_beneficiaire", required=True, string="Identité Benef./Four.", states={'V': [('readonly', True)], 'L': [('readonly', True)], 'O': [('readonly', True)]})
	typedossier = fields.Many2one("budg_typedossierbudg", default=lambda self: self.env['budg_typedossierbudg'].search([('code','=', 'ENG')]), string="Type de dossier", readonly=True)
	lb_obj = fields.Text(string="Objet", size=300, required=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)], 'O': [('readonly', True)]})
	mnt_init_eng = fields.Float(string="Montant initiale engagé", digits=(20, 0), compute="mnt_init_eng")
	credit_eng = fields.Float(string="Montant initiale engagé sur l'engagement", digits=(20, 0))
	mnt_eng = fields.Float(string="Montant engagement", digits=(20, 0), required=True, states={'R': [('readonly', True)],
							'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	mnt_liq = fields.Float(string="Montant liquidé", digits=(20, 0))
	credit_dispo = fields.Float(string="Crédit disponible", digits=(20, 0), readonly=True, states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]})
	piecejust_ids = fields.One2many("budg_piece_engagement", 'eng_id')
	dt_visa_cf = fields.Date(string="Date Visa")
	cpte_benef = fields.Char('compte')
	imput_benef = fields.Many2one("ref_souscompte", "imput beneficiaire")
	cpte_rub = fields.Char('compte rub')
	modereg = fields.Many2one('ref_modereglement', 'Mode de règlement')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]},required=True)
	mnt_lbudg_ap = fields.Float(string="Nouveau disponible", compute='mnt_nvo_dispo')
	mnt_annule = fields.Float(string="Montant annulé", digits=(20, 0))
	mnt_tot_eng = fields.Float(string="Montant total engagé", digits=(20, 0))
	cumul = fields.Float(string='Cumul des engagement antérieurs')
	ref_mp = fields.Many2one("faarf.ppm.contrat", string="Réf. Marché")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
		('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
		('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
	bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
	acc_number = fields.Char(string="N° Compte", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	user_id = fields.Many2one('res.users', string='user', track_visibilty='onchange', readonly=True,  default=lambda self: self.env.user)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	state = fields.Selection([('draft', 'Brouillon'), ('N', 'Confirmé'), ('V', 'Approuvé'), ('A', 'Annulé'),
		('W', 'Visé'), ('R', 'Rejeté'),('LC', 'Liquidation partielle'), ('L', 'Liquidé'), ],
							 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
	credit_disponible = fields.Float("Crédit disponible avant", compute='credits_disponible')
	envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], default='N')
	reste = fields.Integer()
	nature_depense = fields.Selection([('1','Dépenses du personnel'), ('2','Autres dépenses')],
									string="Nature de dépense", states={'R': [('readonly', True)], 'W': [('readonly', True)], 'V': [('readonly', True)], 'L': [('readonly', True)],'O': [('readonly', True)]},required=True)
	bordereau_id = fields.Many2one("hr_bordereau_paie", "Bordereau de paie",domain=[('state', '=', 'E')])
	signataire_1 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '1')]))
	signataire_2 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	@api.onchange('bordereau_id')
	def natureDepense(self):
		for val in self:
			if val.bordereau_id:
				val.cd_section_id = val.bordereau_id.section_id
				val.cd_chapitre_id = val.bordereau_id.chapitre_id
				val.cd_article_id = val.bordereau_id.article_id
				val.cd_paragraphe_id = val.bordereau_id.paragraphe_id
				val.cd_rubrique_id = val.bordereau_id.rubrique_id
				val.mnt_eng = val.bordereau_id.montant


	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id', 'mnt_eng')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

			if record.mnt_eng <= 0:
				raise ValidationError(_("Le montant de l'engagement doit être supérieur à 0."))
			elif record.mnt_eng > record.credit_dispo:
				raise ValidationError(_("Le montant de l'engagement doit être inférieur ou égal au crédit disponible."))


	@api.onchange('cd_section_id')
	def OnchangeSection(self):
		
		if self.cd_section_id:
			self.lbsection = self.cd_section_id.section.lb_court
	
	@api.depends('mnt_eng')
	def amount_to_words(self):
		self.text_amount = num2words(self.mnt_eng, lang='fr')

	def afficher_piece(self):

		val_ex = int(self.x_exercice_id)
		categorie = int(self.categorie_beneficiaire_id)
		val_proc = int(self.type_procedure)
		val_doc = int(self.typedossier)
		titre = int(self.cd_titre_id)
		section = int(self.cd_section_id)
		chapitre = int(self.cd_chapitre_id)
		article = int(self.cd_article_id)
		paragraphe = int(self.cd_paragraphe_id)
		
		for vals in self:
			vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, b.nombre as nbr from budg_pj_dep b, budg_naturedepense n where n.cd_type_dossier_id = %d and n.type_procedure_id = %d and n.cat_benef = %d
			and n.cd_titre_id = %d and n.cd_section_id = %d and n.cd_chapitre_id = %d and n.cd_article_id = %d and n.cd_paragraphe_id = %d 
			and n.id = b.nature_dep_id""" %(val_doc, val_proc, categorie, titre, section, chapitre, article, paragraphe))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0,0, {'lb_long': line['lib'], 'oblige': line['obl'], 'nombre': line['nbr']}))
			self.piecejust_ids = result

	@api.onchange('no_beneficiaire')
	def cpte(self):
		self.cpte_benef = self.no_beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
		self.imput_benef = self.no_beneficiaire.cpte_fournisseur.souscpte.id
		self.bank_id = self.no_beneficiaire.bank_id
		self.acc_number = self.no_beneficiaire.acc_number
	
	@api.onchange('cd_rubrique_id')
	def cpterub(self):
		self.cpte_rub = self.cd_rubrique_id.no_imputation.souscpte.concate_souscpte

	def action_eng_confirmer(self):
		
		val_ex = int(self.x_exercice_id.id)
		val_struct = int(self.company_id.id)
		val_rub = int(self.cd_rubrique_id.id)
		val_par = int(self.cd_paragraphe_id.id)
		val_art = int(self.cd_article_id.id)
		val_sec = int(self.cd_section_id.id)
		val_chap = int(self.cd_chapitre_id.id)
		val_titre = int(self.cd_titre_id.id)
		v_id = int(self.id)
		
		self.write({'state': 'N'})
		
	
		self.env.cr.execute("select noeng from budg_compteur_eng where x_exercice_id = %d and company_id = %d" %(val_ex, val_struct))
		eng = self.env.cr.fetchone()
		no_eng = eng and eng[0] or 0
		c1 = int(no_eng) + 1
		c = str(no_eng)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_eng = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_eng(x_exercice_id,company_id,noeng)  VALUES(%d ,%d, %d)""" %(val_ex, val_struct, vals))
		else:
			c1 = int(no_eng) + 1
			c = str(no_eng)
			ok = str(c1).zfill(4)
			self.no_eng = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_eng SET noeng = %d WHERE x_exercice_id = %d and company_id = %d" %(vals, val_ex, val_struct))
		
		self.env.cr.execute("""select distinct l.mnt_disponible from budg_ligne_exe_dep l where l.cd_titre_id = %d and l.cd_section_id = %d and l.cd_chapitre_id = %d and l.cd_art_id = %d and l.cd_paragraphe_id = %d and l.cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d"""
		%(val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct))
		res = self.env.cr.fetchone()[0] or 0
		
		if self.mnt_eng > res:
			raise ValidationError(_("Le montant de l'engagement est supérieur au montant budgétisé"))
	
		else:

			engagement = self.env['budg_engagement'].search([('cd_titre_id', '=', val_titre), ('cd_section_id', '=', val_sec),
															 ('cd_chapitre_id', '=', val_chap), ('cd_article_id', '=', val_art),
															 ('cd_paragraphe_id', '=', val_par), ('cd_rubrique_id', '=', val_rub),
															 ('x_exercice_id', '=', val_ex), ('company_id', '=', val_struct),
															 ('state','!=', ['draft', 'A', 'R'])])
			montant_engagement = 0
			for e in engagement:
				montant_engagement = montant_engagement + e.mnt_eng
				print('---montant total engagement---')
				print(montant_engagement)

			resultat = self.env['budg_ligne_exe_dep'].search(
				[('cd_titre_id', '=', val_titre), ('cd_section_id', '=', val_sec),
				 ('cd_chapitre_id', '=', val_chap), ('cd_art_id', '=', val_art),
				 ('cd_paragraphe_id', '=', val_par), ('cd_rubrique_id', '=', val_rub),
				 ('x_exercice_id', '=', val_ex), ('company_id', '=', val_struct)])
			corrige = resultat.mnt_corrige
			print('---montant corrige---')
			print(corrige)
			resultat.update({'mnt_engage': montant_engagement, 'mnt_disponible': corrige - montant_engagement})



			self.reste = self.mnt_eng

			self.credit_ouvert()
			self.cumul_anterieur()
			self.mnt_nvo_dispo()
			self.mnt_sum_eng()
				
	#Crédit ouvert sur la ligne
	def credit_ouvert(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_rub = int(self.cd_rubrique_id)
		val_par = int(self.cd_paragraphe_id)
		val_art = int(self.cd_article_id)
		val_sec = int(self.cd_section_id)
		val_chap = int(self.cd_chapitre_id)
		val_titre = int(self.cd_titre_id)
		
		self.env.cr.execute("""select mnt_corrige from budg_ligne_exe_dep where cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d
		and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d"""
		%(val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_struct, val_ex))
		
		res = self.env.cr.fetchone()
		self.credit_eng = res and res[0] or 0
		
	#cumul des engagements antérieurs
	def cumul_anterieur(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_rub = int(self.cd_rubrique_id)
		val_para = int(self.cd_paragraphe_id)
		v_eng = str(self.no_eng)

		self.env.cr.execute("""select coalesce(sum(e.mnt_eng),0) FROM budg_engagement e
		where cd_paragraphe_id = %s and cd_rubrique_id = %s and company_id = %s
		and x_exercice_id = %s and no_eng <> %s and state not in ('draft','A','R') """ ,(val_para, val_rub, val_struct, val_ex, v_eng))
		
		res1 = self.env.cr.fetchone()
		r2 = res1 and res1[0] or 0
		
		self.cumul = r2
		
	# Récupération du nouveau disponible
	@api.depends('credit_disponible', 'mnt_eng')
	def mnt_nvo_dispo(self):

		self.mnt_lbudg_ap = self.credit_disponible - self.mnt_eng


	def mnt_sum_eng(self):

		self.mnt_tot_eng = self.cumul + self.mnt_eng



	@api.depends('credit_eng','cumul')
	def credits_disponible(self):
		self.credit_disponible = self.credit_eng - self.cumul


	def action_eng_approuver(self):
		if self.type_procedure.type_procedure == '001':
			self.write({'state': 'V'})
		else:
			self.write({'state': 'W'})
	

	def action_eng_viser(self):
		self.write({'state': 'W'})
		

	def action_eng_rejeter(self):
		
		#if self.motif_rejet == '1':
		self.write({'state': 'R'})
		

	@api.onchange('cd_rubrique_id','cd_paragraphe_id')
	def cred_dipso(self):
		
		val_ex = int(self.x_exercice_id.id)
		print("ex",val_ex)
		val_struct = int(self.company_id.id)
		print("struc", val_struct)
		val_tit = int(self.cd_titre_id)
		print("tit", val_tit)
		val_sec = int(self.cd_section_id)
		print("sec", val_sec)
		val_chap = int(self.cd_chapitre_id)
		print("chap", val_chap)
		val_art = int(self.cd_article_id)
		print("art", val_art)
		val_para = int(self.cd_paragraphe_id)
		print("para", val_para)
		val_rubrique = int(self.cd_rubrique_id)
		print("rub", val_rubrique)
		
		result = self.env['budg_ligne_exe_dep'].search([('cd_titre_id.id', '=', val_tit), ('cd_section_id.id', '=', val_sec),
														('cd_chapitre_id.id', '=', val_chap), ('cd_art_id.id', '=', val_art),
														('cd_paragraphe_id.id', '=',val_para), ('cd_rubrique_id.id','=',val_rubrique),
														('company_id.id', '=', val_struct), ('x_exercice_id.id', '=', val_ex)])
		print("resut", result)
		self.credit_dispo = result.mnt_disponible
		print("-----------------------")
		print("Disponible", self.credit_dispo)
		
		
class Budg_Compteur_enga(models.Model):
	
	_name = "budg_compteur_eng"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	noeng = fields.Integer(default=0)


class BudgLexedepense(models.Model):

	_name = "budg_ligne_exe_dep"

	cd_titre_id = fields.Many2one("budg_titre", string="Titre")
	cd_section_id = fields.Many2one("budg_section", string="Section")
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre")
	cd_art_id = fields.Many2one("budg_param_article", string="Article")
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe")
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique")
	mnt_budgetise = fields.Float(string = "Dotation initiale")
	mnt_corrige = fields.Float(string = "Dotation corrigée")
	mnt_engage= fields.Float(string = "Engagement")
	mnt_cf = fields.Float(string = "Montant CF")
	mnt_liquide = fields.Float(string = "Montant liquidé")
	mnt_mandate = fields.Float(string = "Mandatement")
	mnt_vbp = fields.Float(string = "Montant vbp")
	mnt_ecp = fields.Float(string = "Montant ecp")
	mnt_paye = fields.Float(string = "Montant payé")
	mnt_max_engage= fields.Float(string = "Montant maximum engagé")
	fg_bloc = fields.Selection([('oui','Oui'), ('non','Non')])
	dt_bloc = fields.Date()
	dt_fin_bloc = fields.Date()
	no_period = fields.Integer()
	mnt_period = fields.Integer()
	mnt_bloque = fields.Integer()
	fg_mnt_bloque = fields.Char()
	dt_deb_mnt_bloque = fields.Date()
	dt_fin_mnt_bloque = fields.Date()
	mnt_disponible = fields.Float("Disponible")
	reste_mandat = fields.Float("Reste à mandater")
	taux = fields.Float("Taux de réalisation(%)")
	mnt_precedent = fields.Float()
	mnt_anterieur1 = fields.Float()
	mnt_anterieur2 = fields.Float()
	budg_id = fields.Many2one("budg_budget")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	
class BudgLexerecette(models.Model):

	_name = "budg_ligne_exe_rec"


	cd_titre_id = fields.Many2one("budg_titre",string = "Titre")
	cd_section_id = fields.Many2one("budg_section",string = "Section")
	cd_chapitre_id = fields.Many2one("budg_chapitre",string = "Chapitre")
	cd_art_id = fields.Many2one("budg_param_article", string = "Article")
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe")
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique")
	mnt_budgetise = fields.Float(string = "Dotation initiale")
	mnt_corrige = fields.Float(string = "Dotation corrigée")
	mnt_emis= fields.Float(string = "Emission")
	mnt_cf = fields.Float(string = "Montant CF")
	mnt_liquide = fields.Float(string = "Montant ordonnancé")
	mnt_ord = fields.Float(string = "Montant mandaté")
	mnt_vbr = fields.Float(string = "Montant vbp")
	mnt_ecr = fields.Float(string = "Montant ecp")
	mnt_rec = fields.Float(string = "Titre émis")
	reste_emettre = fields.Float(string = "Reste à recouvrer")
	mnt_max_engage= fields.Float(string = "Montant maximum engagé",)
	taux = fields.Float("Taux de réalisation(%)")
	no_period = fields.Float()
	mnt_period = fields.Float()
	mnt_precedent = fields.Float()
	mnt_anterieur1 = fields.Float()
	mnt_anterieur2 = fields.Float()
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	budg_id = fields.Many2one("budg_budget")


class BudgLiqOrd(models.Model):

	_name = "budg_liqord"
	_rec_name = "no_lo"
	_order = " id desc"

	type_procedure = fields.Many2one('budg_typeprocedure',string="Type de procédure", readonly=True)
	no_eng = fields.Many2one("budg_engagement", "Engagement", required=True,domain=['|',('state', '=', 'W'),('state', '=', 'LC')],  states={'N': [('readonly', True)], 'L': [('readonly', True)], 'A' :[('readonly', True)]})
	no_lo = fields.Char(string="N°liquidation", states={'N': [('readonly', True)], 'L': [('readonly', True)], 'V' :[('readonly', True)], 'A' :[('readonly', True)]}, readonly=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	res_liq = fields.Integer(string="Reste à liquider",compute = "_mnt_restant", store = True)
	mnt_ord = fields.Integer(string="Montant ordonnancé")
	mnt_paye = fields.Integer(string="Montant à liquider", states={'N': [('readonly', True)], 'L': [('readonly', True)], 'V' :[('readonly', True)], 'A' :[('readonly', True)]})
	mnt_eng = fields.Integer(string="Reste Montant Eng.", readonly=True)
	
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	
	nb_pjust = fields.Integer()
	typedossier = fields.Many2one("budg_typedossierbudg",default=lambda self: self.env['budg_typedossierbudg'].search([('code','=', 'LIQ')]), string = "Type de dossier",  readonly=True,)
	modereg = fields.Many2one('ref_modereglement','Mode de règlement',readonly=True)
	piecejust_line_ids = fields.One2many("budg_piece_liq",'liq_id')
	agence_bank_id = fields.Char(string = "N° Agence")
	dt_visa_cf = fields.Integer(string = "Date Visa Cf")
	dt_visa_ord = fields.Integer(string = "Date Visa Ord")
	dt_visa_ac = fields.Integer(string = "Date Visa Ac")
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date liquidation", required = True, states={'L': [('readonly', True)], 'A' :[('readonly', True)]})
	dispo_engs = fields.Float()
	total_liq_engs = fields.Float()
	cpte_benef = fields.Char('compte')
	cpte_rub = fields.Char('cpte rub')
	imput_benef = fields.Many2one('ref_souscompte','imput')
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	categorie_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", string="Caté de bénéf/four", readonly=True)
	cd_type_accompte = fields.Many2one("budg_typeaccompte", string="Type d'accompte", required=True, states={'N': [('readonly', True)], 'L': [('readonly', True)], 'A' :[('readonly', True)]})
	no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", readonly=True)
	ref_mp = fields.Char('Réf. Marché', readonly=True)
	lb_obj = fields.Text(string="Objet", readonly=True)
	rf_mp = fields.Many2one("budg_marche")
	typ_budg_id = fields.Many2one("budg_typebudget")
	certif_id = fields.Many2one("budg_certification", "Motif de certification", states={'L': [('readonly', True)], 'A': [('readonly', True)]})
	dt_demande = fields.Date()
	motif_rejet = fields.Char(string="Motif rejet")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([('draft', 'Brouillon'), ('N', 'Nouveau'), ('L', 'Liquidée'), ('A', 'Annulée'),
		], string='Etat', default='draft', index=True, readonly=True, copy=False, track_visibility='always')
	active = fields.Boolean(default=True)
	etat = fields.Char(default="En cours")
	signataire_2 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
	acc_number = fields.Char(string="N° Compte", readonly=True)

	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id', 'mnt_paye')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

			if record.mnt_paye <= 0:
				raise ValidationError(_("Le montant de la liquidation doit être supérieur à 0."))

	@api.depends('mnt_paye')
	def amount_to_words(self):
		self.text_amount = num2words(self.mnt_paye, lang='fr')

	def action_liquidation_confirmer(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
				
		self.env.cr.execute("select noliq from budg_compteur_liq where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		lo = self.env.cr.fetchone()
		no_lo = lo and lo[0] or 0
		c1 = int(no_lo) + 1
		c = str(no_lo)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_lo = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_liq(x_exercice_id,company_id,noliq)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))	
		else:
			c1 = int(no_lo) + 1
			c = str(no_lo)
			ok = str(c1).zfill(4)
			self.no_lo = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_liq SET noliq = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))
		
		self.write({'state': 'N'})


	def afficher_piece(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		eng = int(self.no_eng)

		for vals in self:
			vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, b.nombre as nbr, dte as dt, ref as ref, montant as montant from budg_piece_engagement b where b.x_exercice_id = %d and b.company_id = %d
			and b.eng_id = %d order by b.id""" % (val_ex, val_struct, eng))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piecejust_line_ids.unlink()
			for line in rows:
				result.append((0, 0, {'lb_long': line['lib'], 'oblige': line['obl'], 'nombre': line['nbr'],
									  'ref': line['ref'], 'dte': line['dt'], 'montant': line['montant']}))
			self.piecejust_line_ids = result

	def action_liquidation_liquider(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_eng = self.no_eng.no_eng
		mnt_paye = int(self.mnt_paye)

		if self.cd_type_accompte.cd_type_accompte == "AU":
			self.env.cr.execute("UPDATE budg_engagement SET state = 'L', reste = reste - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s" ,(mnt_paye, val_eng, val_ex, val_struct))
		
			self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()
		else:
			self.env.cr.execute("UPDATE budg_engagement SET state = 'LC', reste = reste - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s" ,(mnt_paye, val_eng, val_ex, val_struct))
			
			self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()

	def dispo_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = self.no_eng

		self.env.cr.execute("""select (sum(l.mnt_eng) - l.mnt_paye) FROM budg_liqord l, budg_engagement e
		WHERE e.id = %d and e.id = l.no_eng and l.company_id = %d and l.x_exercice_id = %d group by l.mnt_eng, l.mnt_paye""" % (
		v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		self.dispo_engs = res and res[0] or 0

	def total_liq_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = int(self.no_eng)

		self.env.cr.execute("""select sum(l.mnt_paye) FROM budg_liqord l, budg_engagement e
		WHERE e.id = l.no_eng and l.no_eng = %d and l.company_id = %d and l.x_exercice_id = %d 
		and l.state not in ('A') group by l.mnt_paye""" % (v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		self.total_liq_engs = res and res[0] or 0



	def action_liquidation_certifier(self):
		self.write({'state': 'V'})
		

	def action_liquidation_annuler(self):
		self.write({'state': 'A'})
	
	@api.onchange('cd_type_accompte')
	def compute_mnt_paye(self):
		if self.cd_type_accompte.cd_type_accompte != "AU":
			self.mnt_paye = 0
			#self.no_eng.active = False
		else:
			self.mnt_paye = self.mnt_eng
		
	@api.depends('mnt_eng','mnt_paye')
	def _mnt_restant(self):
		for x in self:
			x.res_liq = x.mnt_eng - x.mnt_paye
		

	@api.onchange('no_eng')
	def no_eng_on_change(self):

		if self.no_eng:
			self.cd_titre_id = self.no_eng.cd_titre_id
			self.cd_section_id = self.no_eng.cd_section_id
			self.cd_chapitre_id = self.no_eng.cd_chapitre_id
			self.cd_article_id = self.no_eng.cd_article_id
			self.cd_paragraphe_id = self.no_eng.cd_paragraphe_id
			self.cd_rubrique_id = self.no_eng.cd_rubrique_id
			self.mnt_eng = self.no_eng.reste
			self.type_procedure = self.no_eng.type_procedure
			self.categorie_beneficiaire_id = self.no_eng.type_beneficiaire_id
			self.type_beneficiaire_id = self.no_eng.type_beneficiaire_id
			self.no_beneficiaire = self.no_eng.no_beneficiaire
			self.lb_obj = self.no_eng.lb_obj
			self.cpte_benef = self.no_eng.cpte_benef
			self.cpte_rub = self.no_eng.cpte_rub
			self.imput_benef = self.no_eng.imput_benef
			self.ref_mp = self.no_eng.ref_mp
			self.modereg = self.no_eng.modereg.id
			self.bank_id = self.no_eng.bank_id
			self.acc_number = self.no_eng.acc_number

	
class Budg_Compteur_liq(models.Model):
	
	_name = "budg_compteur_liq"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	noliq = fields.Integer()


class BudgMandat(models.Model):

	_name = "budg_mandat"
	_rec_name = "no_mandat"
	_order = " id desc"

	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", readonly= True)
	no_eng = fields.Many2one("budg_engagement",string="N° engagement", readonly=True)
	no_mandat = fields.Char(string="N° Ordonnance", readonly=True)
	no_lo = fields.Many2one("budg_liqord", string="Liquidation",
							domain=[('state', '=', 'L'), ('etat', '=', 'En cours')], states={'N': [('readonly', True)], 'A': [('readonly', True)], 'O': [('readonly', True)],'V': [('readonly', True)], 'R': [('readonly', True)] ,'I': [('readonly', True)], 'J': [('readonly', True)] , 'E': [('readonly', True)] , 'F': [('readonly', True)]}, required=True)
	mnt_eng = fields.Integer(string="Montant", readonly=True)
	typedossier = fields.Many2one("budg_typedossierbudg", default=lambda self: self.env['budg_typedossierbudg'].search([('code','=', 'LIQ')]), string = "Type de dossier",  readonly=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cpte_benef = fields.Char('compte')
	cpte_rub = fields.Char('compte rub')
	imput_benef = fields.Many2one('ref_souscompte','imput')
	mnt_annule = fields.Integer( default=0)
	mnt_ord = fields.Integer(string="Montant", readonly=True)
	mnt_paye = fields.Integer(string="Montant payé")
	ac_cf = fields.Selection([('AC', 'AC'), ('CF', 'CF')], string='Banque')
	agence_id = fields.Many2one("ref_banque_agence", string="Banque")
	num_compte = fields.Char(string="N° Compte")
	piecejust_ids = fields.One2many("budg_piece_ord", 'mandat_id')
	bank_id = fields.Many2one("res.bank", string="Banque", readonly=True)
	agence_bank_id = fields.Char(string="N° Agence")
	acc_number = fields.Char(string="N° compte", readonly=True)
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date mandat", required=True, states={'A': [('readonly', True)], 'O': [('readonly', True)],'V': [('readonly', True)], 'R': [('readonly', True)] ,'I': [('readonly', True)], 'J': [('readonly', True)] , 'E': [('readonly', True)] , 'F': [('readonly', True)]})
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie Four.")
	categorie_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", string="Caté de bénéf/four", readonly=True)
	no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", readonly=True)
	no_beneficiaires = fields.Many2one("ref_beneficiaire", string="Id Benef", readonly=True)
	obj = fields.Text(string="Objet mandat", readonly=True)
	modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
	type_accompte_id = fields.Many2one("budg_typeaccompte",string="Type d'accompte", readonly=True)
	typ_budg_id = fields.Many2one("budg_typebudget")
	commentaire = fields.Text()
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([
		('draft', 'Brouillon'), ('N', 'Confirmé'),
		('A', 'Annulé'), ('O', 'Ordonnancé'),
		('I', 'Visé par DFC'), ('J', 'Rejété par DFC'),
		('E', 'Pris en charge'), ('F', 'Payé'),
	], 'Etat', default='draft', index=True, readonly=True, copy=False, track_visibility='always')
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	active = fields.Boolean(default="False")
	envoyer_daf = fields.Selection([('Y','Oui'),('N','Non')], default='N')
	signataire_1 = fields.Many2one("budg_signataire",default=lambda self: self.env['budg_signataire'].search([('code', '=', '1')]))
	signataire_2 = fields.Many2one("budg_signataire",default=lambda self: self.env['budg_signataire'].search([('code', '=', '4')]))
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.depends('mnt_ord')
	def amount_to_words(self):
		self.text_amount = num2words(self.mnt_ord, lang='fr')

	def action_mandat_brouillon(self):
		self.write({'state': 'draft'})

	def action_mandat_confirme(self):
		
		val_ex = int(self.x_exercice_id)
		v_id = int(self.no_lo.no_eng.id)
		val_struct = int(self.company_id)
		val_lo = int(self.no_lo)
		
		self.env.cr.execute("select nomand from budg_compteur_mand where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		mandat = self.env.cr.fetchone()
		no_mandat = mandat and mandat[0] or 0
		c1 = int(no_mandat) + 1
		c = str(no_mandat)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_mandat = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_mand(x_exercice_id,company_id,nomand)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))	
		else:
			c1 = int(no_mandat) + 1
			c = str(no_mandat)
			ok = str(c1).zfill(4)
			self.no_mandat = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_mand SET nomand = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))

		self.write({'state': 'N'})

		self.env.cr.execute("UPDATE budg_liqord set etat = 'Terminé' where id = %d and x_exercice_id = %d and company_id = %d" %(val_lo, val_ex, val_struct))

	def action_mandat_ordonnance(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_eng = int(self.no_eng)
		val_lo = self.no_lo.no_lo
		
		val_titre = int(self.no_eng.cd_titre_id.id)
		val_chap = int(self.no_eng.cd_chapitre_id.id)
		val_sec = int(self.no_eng.cd_section_id.id)
		val_art = int(self.no_eng.cd_article_id.id)
		val_par = int(self.no_eng.cd_paragraphe_id.id)
		val_rub = int(self.no_eng.cd_rubrique_id.id)

		mandatement = self.env['budg_mandat'].search(
			[('cd_titre_id', '=', val_titre), ('cd_section_id', '=', val_sec),
			 ('cd_chapitre_id', '=', val_chap), ('cd_article_id', '=', val_art),
			 ('cd_paragraphe_id', '=', val_par), ('cd_rubrique_id', '=', val_rub),
			 ('x_exercice_id', '=', val_ex), ('company_id', '=', val_struct),
			 ('no_eng', '=', val_eng), ('state', '!=', ['draft', 'A', 'J'])])

		montant_mandat = 0
		for m in mandatement:
			montant_mandat = montant_mandat + m.mnt_ord
			print('---montant total engagement---')
			print(montant_mandat)

		resultat = self.env['budg_ligne_exe_dep'].search(
			[('cd_titre_id', '=', val_titre), ('cd_section_id', '=', val_sec),
			 ('cd_chapitre_id', '=', val_chap), ('cd_art_id', '=', val_art),
			 ('cd_paragraphe_id', '=', val_par), ('cd_rubrique_id', '=', val_rub),
			 ('x_exercice_id', '=', val_ex), ('company_id', '=', val_struct)])
		engage = resultat.mnt_engage
		print('---montant engage---')
		print(engage)
		resultat.update({'mnt_mandate': montant_mandat, 'reste_mandat': engage - montant_mandat})

		self.write({'state': 'O'})

	def afficher_piece(self):
		val_liq = int(self.no_lo)

		for vals in self:
			vals.env.cr.execute("""select b.lb_long as lib, b.oblige as obl, 
			montant as mnt, b.dte as dte, b.nombre as nbr, b.ref as ref 
			from budg_piece_liq b where liq_id = %d""" %(val_liq))
			rows = vals.env.cr.dictfetchall()
			result = []
			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0,0, {'lb_long' : line['lib'], 'oblige': line['obl'], 'dte': line['dte'], 'nombre': line['nbr'],'montant': line['mnt'],'ref': line['ref']}))
			self.piecejust_ids = result

	#Annulation de l'engagement
	def action_mandat_annule(self):

		self.write({'state': 'A'})
		self.mnt_annule = self.mnt_ord

	def action_mandat_visa_ac(self):
		self.write({'state': 'I'})

	def action_mandat_rejeter_ac(self):
		self.write({'state': 'J'})

	#Chargement de la liquidation choisie
	@api.onchange('no_lo')
	def no_lo_on_change(self):

		if self.no_lo:
			self.type_accompte_id = self.no_lo.cd_type_accompte
			self.mnt_eng = self.no_lo.mnt_eng
			self.mnt_ord = self.no_lo.mnt_paye
			self.no_eng = self.no_lo.no_eng
			self.obj = self.no_lo.lb_obj
			self.type_procedure = self.no_lo.type_procedure
			self.cd_titre_id = self.no_lo.cd_titre_id
			self.cd_section_id = self.no_lo.cd_section_id
			self.cd_chapitre_id = self.no_lo.cd_chapitre_id
			self.cd_article_id = self.no_lo.cd_article_id
			self.cd_paragraphe_id = self.no_lo.cd_paragraphe_id
			self.cd_rubrique_id = self.no_lo.cd_rubrique_id
			self.categorie_beneficiaire_id = self.no_lo.categorie_beneficiaire_id
			self.type_beneficiaire_id = self.no_lo.type_beneficiaire_id
			self.no_beneficiaire = self.no_lo.no_beneficiaire
			self.cpte_benef = self.no_lo.cpte_benef
			self.cpte_rub = self.no_lo.cpte_rub
			self.imput_benef = self.no_lo.imput_benef
			#self.ref_mp = self.no_lo.ref_mp
			self.modereg = self.no_lo.modereg
			self.bank_id = self.no_lo.bank_id
			self.acc_number = self.no_lo.acc_number


class Budg_Compteur_mand(models.Model):
	
	_name = "budg_compteur_mand"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	nomand = fields.Integer(default=0)
	
	
class BudgBordEng(models.Model):

	_name = "budg_bordereau_engagement"
	_rec_name = "no_bord_en"
	_order = " id desc"

	name = fields.Char()
	no_bord_eng = fields.Char(string='N° Bord. Eng',default=lambda self: self.env['ir.sequence'].next_by_code('no_bord_eng'))
	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau",default ="Bordereau de Transmission d'engagement pour CG",  readonly=True)
	cd_acteur = fields.Char(string ="Acteur", default='DFC', readonly=True)
	date_emis = fields.Date("Date d'émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de réception")
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	cd_acteur_accuse = fields.Char(string ="Acteur")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_ids = fields.Many2many("budg_engagement", "eng_id", string="Liste des engagements", ondelete="restrict")
	state = fields.Selection([
        ('N', 'Nouveau'),
		('T', 'Envoyé à CG'),
		('R', 'Réceptionné par CG'),
		('TR', 'Traité'),
        ], 'Etat', default='N', required=True, readonly=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	signataire_2 = fields.Many2one("budg_signataire",default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
	signataire_3 = fields.Many2one("budg_signataire",default=lambda self: self.env['budg_signataire'].search([('code', '=', '3')]))

	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')

	def action_generer_bord_eng(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_id = int(self.id)

		self.env.cr.execute("select bordeng from budg_compteur_bord_eng where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))	
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_eng SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))

		
		self.env.cr.execute(""" SELECT sum(mnt_eng) FROM budg_engagement e , budg_bordereau_engagement b, eng_id be
		WHERE e.state = 'V' and b.x_exercice_id = %d AND b.company_id = %d AND be.budg_bordereau_engagement_id = %d 
		AND e.id = be.budg_engagement_id AND be.budg_bordereau_engagement_id = b.id""" %(val_ex,val_struct, val_id))
		res = self.env.cr.fetchone()
		resu = res and res[0] or 0
		if resu <= 0:
			raise ValidationError(_("Le bordereau doit contenir uniquement que des engagements approuvés."))
		else:
			self.totaux = resu
		
			self.env.cr.execute(""" SELECT sum(totaux) FROM budg_bordereau_engagement b	
			WHERE b.x_exercice_id = %d AND b.company_id = %d and b.id != %d """ %(val_ex,val_struct, val_id))
			res1 = self.env.cr.fetchone()
			self.total_prec = res1 and res1[0] or 0

			self.write({'state': 'T'})

	def action_receptionner_bord(self):
		self.write({'state': 'R'})

	def action_traiter_bord(self):
		self.write({'state': 'TR'})
		

class Budg_Compteur_bord_eng(models.Model):
	
	_name = "budg_compteur_bord_eng"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default = 0)
	

class Budg_Compteur_bord_titre(models.Model):
	
	_name = "budg_compteur_bord_titre"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordtitre = fields.Integer(default = 0)
	

class BudgBordLiq(models.Model):

	_name = "budg_bordereau_liquidation"
	_rec_name="no_bord_liq1"

	no_lo = fields.Many2one("budg_bordereau_liquidation")
	no_bord_liq1 = fields.Char("Bord. N°", readonly=True)
	no_bord_liq = fields.Char(string='N° Bord. Liq',default=lambda self: self.env['ir.sequence'].next_by_code('no_bord_liq'))
	type_bord_trsm = fields.Char("Type de bordereau", readonly=True)
	cd_acteur = fields.Char(string ="Acteur", readonly=True)
	date_emis = fields.Date("Date d'émission", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cd_acteur_accuse = fields.Char(string ="Acteur")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	liquidation_ids = fields.Many2many("budg_liqord", "budg_detail_bord_liq", string="Liste des liquidations")
	state = fields.Selection([('N', 'Nouveau'), ('V', 'Transmis'), ('R', 'Receptionner'),
							  ], 'Etat', default='N', index=True, required=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')

	def action_misebordereau_bord_liq(self):
		
		val_ex = int(self.x_exercice_id.id)
		val_struct = int(self.company_id.id)
		val_id = self.id
		
		self.env.cr.execute("select bordliq from budg_compteur_bord_liq where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
		bordliq = self.env.cr.fetchone()
		no_bord_liq1 = bordliq and bordliq[0] or 0
		c1 = int(no_bord_liq1) + 1
		c = str(no_bord_liq1)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_liq1 = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_liq(x_exercice_id,company_id,bordliq)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))
		else:
			c1 = int(no_bord_liq1) + 1
			c = str(no_bord_liq1)
			ok = str(c1).zfill(4)
			self.no_bord_liq1 = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_liq SET bordliq = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))
			
		self.write({'state': 'V'})
		
		
		self.env.cr.execute("select lb_long from budg_typebordtrans where code = '03' ")
		val = self.env.cr.fetchone()
		self.type_bord_trsm = val and val[0] or 0
		
		self.env.cr.execute("select type_depart from budg_typebordtrans where code = '03' ")
		val1 = self.env.cr.fetchone()
		self.cd_acteur = val1 and val1[0] or 0
		
		self.env.cr.execute("select type_dest from budg_typebordtrans where code = '03' ")
		val2 = self.env.cr.fetchone()
		self.cd_acteur_accuse = val2 and val2[0] or 0
		
		
		self.env.cr.execute(""" SELECT sum(mnt_paye) FROM budg_liqord l , budg_bordereau_liquidation b, budg_detail_bord_liq bl
		WHERE b.x_exercice_id = %s AND b.company_id = %s AND bl.budg_bordereau_liquidation_id = %s
		AND l.id = bl.budg_liqord_id AND bl.budg_bordereau_liquidation_id = b.id""" %(val_ex,val_struct, val_id))
		res = self.env.cr.fetchone()
		self.totaux = res and res[0]
		print('montant')

	def action_receptionbordereau_bord_liq(self):
		self.write({'state': 'R'})
		self.date_recus = date.today()

		self.env.cr.execute("select lb_long from budg_typebordtrans where code = '04' ")
		val = self.env.cr.fetchone()
		self.type_bord_trsm = val and val[0] or 0
		
		self.env.cr.execute("select type_depart from budg_typebordtrans where code = '04' ")
		val1 = self.env.cr.fetchone()
		self.cd_acteur = val1 and val1[0] or 0
		
		self.env.cr.execute("select type_dest from budg_typebordtrans where code = '04' ")
		val2 = self.env.cr.fetchone()
		self.cd_acteur_accuse = val2 and val2[0] or 0
		
	
class Budg_Compteur_bord_liq(models.Model):
	
	_name = "budg_compteur_bord_liq"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordliq = fields.Integer(default = 0)


class BudgBordMan(models.Model):

	_name = "budg_bordereau_mandatement"
	_rec_name = "no_bord_mandat"
	_order = 'id desc'

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau',default='Bordereau de Transmission de Mandat pour CG',readonly=True)
	cd_acteur = fields.Char(string ="De",default="DAF/DFC", readonly=True)
	date_emis = fields.Date(string="Date d'émission",default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cd_acteur_accuse = fields.Char(string ="Vers ",default="CG", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.Many2many("budg_mandat", "budg_detail_bord_mandat", string="Liste des mandats")
	et_doss = fields.Selection([
        ('N', 'Nouveau'),
        ('V', 'Envoyé à CG'),
        ('R', 'Réceptionné par CG')
        ], 'Etat', default='N', required=True, readonly=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	signataire_2 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')

	#Fonction pour générer le numero du bordereau, calculer le montant du precedent et present bordereau et affecter les acteurs et type de bordreau

	def action_genererbordereau_bord_mandat(self):
		for vals in self:
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)
			val_id = int(self.id)

			self.env.cr.execute("select bordmand from budg_compteur_bord_mand where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng",type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("""INSERT INTO budg_compteur_bord_mand(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("UPDATE budg_compteur_bord_mand SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))


			self.write({'et_doss': 'V'})


			self.env.cr.execute("""SELECT sum(mnt_ord) FROM budg_mandat m, budg_bordereau_mandatement b, budg_detail_bord_mandat bm
			WHERE b.x_exercice_id = %d AND b.company_id = %d AND bm.budg_bordereau_mandatement_id = %d
			AND m.id = bm.budg_mandat_id AND bm.budg_bordereau_mandatement_id = b.id""" %(val_ex,val_struct, val_id))
			res = self.env.cr.fetchone()
			resu = res and res[0] or 0
			if resu <= 0:
				raise ValidationError(_("Le bordereau doit contenir au moins un mandat approuvé."))
			else:
				self.totaux = resu

				self.env.cr.execute("""SELECT sum(totaux) FROM budg_bordereau_mandatement b
				WHERE b.x_exercice_id = %d AND b.company_id = %d AND b.id != %d""" %(val_ex,val_struct, val_id))
				res1 = self.env.cr.fetchone()
				self.total_prec = res1 and res1[0] or 0
	

class Budg_Compteur_bord_mand(models.Model):
	
	_name = "budg_compteur_bord_mand"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default = 0)
			

class Ordre_Paiement(models.Model):
	
	_name = "budg_op"
	_rec_name = "no_op"
	
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	no_op = fields.Char(string="OP N°", readonly=True)
	no_mandat = fields.Many2one("budg_mandat", string="N° Mandat")
	type_operation = fields.Many2one("budg_typeordrepaiement", string="Type de paiement", required=True)
	imput_benef = fields.Many2one("compta_plan_lines", string="Compte de tiers", required=True)
	imput_benefs = fields.Integer()
	date_emis = fields.Date(string="Date", default=fields.Date.context_today, readonly=True)
	date_etat = fields.Date()
	mnt_op =fields.Float("Montant", required=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	md_reglement = fields.Many2one("ref_modereglement", string="Mode de paiement")
	lb_obj = fields.Text("Objet", size=350, required=True)
	mnt_paye = fields.Integer()
	cd_certif = fields.Many2one("budg_certification", string="Motif certification")
	type_beneficiaire = fields.Many2one("ref_categoriebeneficiaire", string="Catégorie", required=True)
	no_beneficiaire = fields.Many2one("ref_beneficiaire", string="Bénéficiaire", required=True)
	motif_rejet = fields.Text("Motif de rejet", size=240)
	piece_ids = fields.Many2one("ref_piece_justificatives", "Pièce Justificative")
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	et_doss = fields.Selection([
        ('draft', 'Brouillon'), ('N', 'Confirmer'), ('C', 'Certifier'), ('F', 'Payé'),
        ], 'Etat', default='draft', required=True, readonly=True, copy=False, track_visibility='always')
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.depends('mnt_op')
	def amount_to_words(self):
		self.text_amount = num2words(self.mnt_op, lang='fr')

	@api.onchange('imput_benef')
	def Imput(self):
		for val in self:
			val.imput_benefs = val.imput_benef.souscpte.id

	def action_op_confirmer(self):
		for vals in self:
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			vals.env.cr.execute("select op from budg_compteur_ordre_paiement where x_exercice_id = %d and company_id = %d" %(val_ex,val_struct) )
			ope = self.env.cr.fetchone()
			no_op = ope and ope[0] or 0
			c1 = int(no_op) + 1
			c = str(no_op)
			#print("la val eng",type(ope))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_op = ok
				vals = c1
				self.env.cr.execute("""INSERT INTO budg_compteur_ordre_paiement(x_exercice_id,company_id,op)  VALUES(%d, %d, %d)""" %(val_ex,val_struct,vals))
			else:
				c1 = int(no_op) + 1
				c = str(no_op)
				ok = str(c1).zfill(4)
				self.no_op = ok
				vals = c1
				self.env.cr.execute("UPDATE budg_compteur_ordre_paiement SET op = %d  WHERE x_exercice_id = %d and company_id = %d" %(vals,val_ex,val_struct))

			self.write({'et_doss': 'N'})
		

	def action_op_certifier(self):
		self.write({'et_doss': 'C'})
	
class Budg_compteur_ordre_paiement(models.Model):
	
	_name = "budg_compteur_ordre_paiement"
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	op = fields.Integer(default = 0)	
	

class Budg_Balance(models.Model):
	@api.depends('type','dt_debut', 'dt_fin')
	def _concate(self):
		for test in self:
			test.concate = "BALANCE DES" + " " + " " + str(test.type)+ " " + "DU" + " " +str(test.dt_debut)+ " " + "AU" + " " +str(test.dt_fin)
		
	_name = 'budg_balance'
	_rec_name = 'concate'
	
	concate = fields.Char(compute = '_concate')
	type = fields.Selection([
		('DEPENSES', 'Dépense'),
		('RECETTES', 'Recette')], string = "Balance",default="DEPENSES", readonly=True, required = True)
	dt_debut = fields.Date("Date début",required = True)
	dt_fin = fields.Date("Date fin", required = True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	balance_lines = fields.One2many("budg_balance_line", "balance_id", readonly=True)
	total_budget = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	total_engagement = fields.Integer()
	total_mandat = fields.Integer()



	@api.onchange('dt_fin')
	def change_dt_fin(self):
		
		if self.dt_fin < self.dt_debut:
			raise ValidationError(_('La date de début ne peut être supérieure à la date de fin'))
	
	
	def remplir_balance(self):

		val_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("""select br.id as ids, br.rubrique as code, br.lb_long as libelle
			from budg_rubrique br, budg_titre bt
			where bt.id = br.cd_titre_id and bt.type_titre = 'D' and br.company_id = %d order by br.rubrique""" %(val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.balance_lines.unlink()
			for line in rows:
				result.append((0,0, {'val' : line['ids'],'numero_compte' : line['code'], 'libelle': line['libelle']}))
			self.balance_lines = result

			self.Calcul()

	def Calcul(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = self.dt_debut
		val_fin = self.dt_fin
		balance_id = self.id

		self.env.cr.execute("select distinct val from budg_balance_line where x_exercice_id = %d and company_id = %d and balance_id = %d" %(val_ex, val_struct, balance_id))
		for val in self.env.cr.dictfetchall():
			cpte = val['val']

			self.env.cr.execute("""UPDATE budg_balance_line SET montant_budgetise = (select coalesce(sum(mnt_corrige),0) from budg_ligne_exe_dep where cd_rubrique_id = cast(%s as int)
			and company_id = %s and x_exercice_id = %s ) WHERE val = %s and company_id = %s and x_exercice_id = %s and balance_id = %s""",(cpte, val_struct, val_ex, cpte, val_struct, val_ex, balance_id))

			self.env.cr.execute("""UPDATE budg_balance_line SET montant_engagement = (select coalesce(sum(mnt_eng),0) from budg_engagement where cd_rubrique_id = cast(%s as int)
			and company_id = %s and x_exercice_id = %s and state not in ('A','R') and dt_etat between %s and %s)
			WHERE val = %s and company_id = %s and x_exercice_id = %s and balance_id = %s""" ,(cpte, val_struct, val_ex, val_deb, val_fin, cpte, val_struct, val_ex, balance_id))

			self.env.cr.execute("""UPDATE budg_balance_line SET montant_mandatement = (select coalesce(sum(mnt_ord),0) from budg_mandat where cd_rubrique_id = cast(%s as int)
			and company_id = %s and x_exercice_id = %s and state not in ('A','R') and dt_etat between %s and %s)
			WHERE val = %s and company_id = %s and x_exercice_id = %s and balance_id = %s""",(cpte, val_struct, val_ex, val_deb, val_fin, cpte, val_struct, val_ex, balance_id))


class Budg_balance_line(models.Model):
	_name = 'budg_balance_line'
	
	balance_id = fields.Many2one("budg_balance", ondelete='cascade')
	val = fields.Char("ids")
	numero_compte = fields.Char("Numéro compte")
	libelle = fields.Char("Libellé")
	montant_budgetise = fields.Float("Budget")
	montant_engagement = fields.Float("Engagements")
	montant_mandatement = fields.Float("Mandats")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)



class Budg_BalanceRecette(models.Model):
	@api.depends('type','dt_debut', 'dt_fin')
	def _concate(self):
		for test in self:
			test.concate = "BALANCE DES" + " " + " " + str(test.type)+ " " + "DU" + " " +str(test.dt_debut)+ " " + "AU" + " " +str(test.dt_fin)
		
	_name = 'budg_balance_recette'
	_rec_name = 'concate'
	
	concate = fields.Char(compute = '_concate')
	type = fields.Selection([
		('DEPENSES', 'Dépense'),
		('RECETTES', 'Recette')], string = "Balance", default= 'RECETTES',readonly=True, required = True)
	dt_debut = fields.Date("Date début",required = True)
	dt_fin = fields.Date("Date fin", required = True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	balance_lines = fields.One2many("budg_balance_line_recette", "balance_id", readonly=True)
	total_budget = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	total_engagement = fields.Integer()
	total_mandat = fields.Integer()


	@api.onchange('dt_fin')
	def change_dt_fin(self):
		
		if self.dt_fin < self.dt_debut:
			raise ValidationError(_('La date de début ne peut être supérieure à la date de fin'))
	
	
	def remplir_balance(self):
		val_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("""select br.id as ids, br.rubrique as code, br.lb_long as libelle from budg_rubrique br, budg_titre bt
			where bt.id = br.cd_titre_id and bt.type_titre = 'R' and br.company_id = %d order by br.rubrique """ %(val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.balance_lines.unlink()
			for line in rows:
				result.append((0,0, {'val' : line['ids'],'numero_compte' : line['code'], 'libelle': line['libelle']}))
			self.balance_lines = result

			self.Calcul()

	def Calcul(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = self.dt_debut
		val_fin = self.dt_fin
		balance_id = self.id

		self.env.cr.execute("select distinct val from budg_balance_line_recette where x_exercice_id = %d and company_id = %d and balance_id = %d" % (val_ex, val_struct, balance_id))
		for val in self.env.cr.dictfetchall():
			cpte = val['val']

			self.env.cr.execute("""UPDATE budg_balance_line_recette SET montant_budgetise = (select coalesce(sum(mnt_corrige),0) from budg_ligne_exe_rec where cd_rubrique_id = cast(%s as int)
			and company_id = %s and x_exercice_id = %s ) WHERE val = %s and company_id = %s and x_exercice_id = %s and balance_id = %s""",(cpte, val_struct, val_ex, cpte, val_struct, val_ex, balance_id))

			self.env.cr.execute("""UPDATE budg_balance_line_recette SET montant_recette = (select coalesce(sum(mnt_rec),0) from budg_titrerecette where cd_rubrique_id = cast(%s as int)
			and company_id = %s and x_exercice_id = %s and et_doss not in ('A','R') and dt_rec between %s and %s)
			WHERE val = %s and company_id = %s and x_exercice_id = %s and balance_id = %s""", (cpte, val_struct, val_ex, val_deb, val_fin, cpte, val_struct, val_ex, balance_id))


class Budg_balance_line_recette(models.Model):
	_name = 'budg_balance_line_recette'
	
	balance_id = fields.Many2one("budg_balance_recette", ondelete='cascade')
	val = fields.Char("ids")
	numero_compte = fields.Char("Numéro compte")
	libelle = fields.Char("Libellé")
	montant_budgetise = fields.Float("Budget")
	montant_recette = fields.Float("Recette")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class Budg_fiche_compte(models.Model):
	_name = 'budg_fiche_compte'
	_rec_name = 'numero_compte'
	
	numero_compte = fields.Many2one("budg_rubrique", "N° et intitulé Compte", required=True)
	budget_initial = fields.Float("Budget initial", readonly=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	ouverture = fields.Float("Ouverture", readonly=True)
	annulation = fields.Float("Annulation", readonly=True)
	budget_corrige = fields.Float("Budget corrigé", readonly=True)
	fiche_lines = fields.One2many("budg_fiche_compte_line", "fiche_id")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	@api.onchange('numero_compte')	
	def compte(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_rub = int(self.numero_compte)
		
		if self.numero_compte:
			self.env.cr.execute("""select l.mnt_budgetise from budg_ligne_exe_dep l where l.cd_rubrique_id = %s and l.x_exercice_id = %s and l.company_id = %s""" ,(val_rub,val_ex,val_struct))
				
			res = self.env.cr.fetchone()
			self.budget_initial = res and res[0] or 0
			
			self.env.cr.execute("""select l.mnt_corrige from budg_ligne_exe_dep l where l.cd_rubrique_id = %s and l.x_exercice_id = %s and l.company_id = %s""" ,(val_rub,val_ex,val_struct))
				
			res1 = self.env.cr.fetchone()
			self.budget_corrige = res1 and res1[0] or 0
		
	
	def fiche_compte(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_rub = int(self.numero_compte)
		for vals in self:
			vals.env.cr.execute("""select e.dt_etat as dte, concat(e.no_eng, '/', bm.no_mandat) as noeng, e.mnt_eng as eng, e.mnt_annule as ann1, (e.mnt_eng - e.mnt_annule) as cumul1, bm.mnt_ord as ord, bm.mnt_annule as ann2,
			(bm.mnt_ord - bm.mnt_annule) as cumul2 from budg_engagement e, budg_mandat bm 
			where e.cd_rubrique_id = %s and e.no_eng = bm.no_eng and e.x_exercice_id = %s and e.company_id = %s""",(val_rub,val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
			vals.fiche_lines.unlink()
			for line in rows:
				result.append((0, 0, {'date_eng': line['dte'], 'numero_eng': line['noeng'], 'montant_eng': line['eng'], 'montant_ann': line['ann1'],
									 'cumul_eng': line['cumul1'], 'montant_mand': line['ord'], 'montant_mand_ann': line['ann2'], 'cumul_mand': line['cumul2']}))
			self.fiche_lines = result
			for x in vals.fiche_lines:
				x.cumulg = x.cumul_eng + x.cumul_mand

class BudgFicheCompteLine(models.Model):
	_name = 'budg_fiche_compte_line'
	
	fiche_id = fields.Many2one('budg_fiche_compte', ondelete='cascade')
	date_eng = fields.Date("Date")
	journal = fields.Char("JNL")
	folio = fields.Char("Folio")
	numero_eng = fields.Char("N° Eng/N° Mdt")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	montant_eng = fields.Float("Emission Eng.(1)")
	montant_ann = fields.Float("Annulation Eng.(2)")
	cumul_eng = fields.Float("Cumul(3=1-2)")
	montant_mand = fields.Float("Emission Mdt.(4)")
	montant_mand_ann = fields.Float("Annulation Mdt.(5)")
	cumul_mand = fields.Float("Cumul(6=4-5)")
	cumulg = fields.Float("Cumuls généraux(7=6+3)")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class Budg_fiche_compteRec(models.Model):
	_name = 'budg_fiche_compte_rec'
	_rec_name = 'numero_compte'
	
	numero_compte = fields.Many2one("budg_paragraphe", "N° et intitulé Compte", required=True)
	libelle = fields.Char("Libellé")
	budget_initial = fields.Float("Budget initial", readonly=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	ouverture = fields.Float("Ouverture", readonly=True)
	annulation = fields.Float("Annulation", readonly=True)
	budget_corrige = fields.Float("Budget corrigé", readonly=True)
	fiche_lines = fields.One2many("budg_fiche_compte_line_rec", "fiche_id")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


	@api.onchange('numero_compte')	
	def compte(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_para = int(self.numero_compte)
		
		if self.numero_compte:
			self.env.cr.execute("""select l.mnt_budgetise from budg_ligne_exe_rec l where l.cd_paragraphe_id = %s and l.x_exercice_id = %s and l.company_id = %s""" ,(val_para,val_ex,val_struct))
				
			res = self.env.cr.fetchone()
			self.budget_initial = res and res[0] or 0
		
	
	def fiche_compte_rec(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_para = int(self.numero_compte)

		for vals in self:
			vals.env.cr.execute("""select bt.dt_rec as dte, bt.cd_titre_recette as titre, bt.mnt_rec as mnt, bt.mnt_annule as annule, (bt.mnt_rec - bt.mnt_annule) as cumul 
			from budg_titrerecette bt where bt.cd_paragraphe_id = %s and bt.x_exercice_id = %s and bt.company_id = %s""",(val_para,val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
			vals.fiche_lines.unlink()
			for line in rows:
				result.append((0,0, {'date_rec' : line['dte'], 'numero_titre': line['titre'], 'montant_rec': line['mnt'], 'montant_ann': line['annule'], 'cumul': line['cumul']}))
			self.fiche_lines = result


class BudgFicheCompteLinerec(models.Model):
	_name = 'budg_fiche_compte_line_rec'
	
	fiche_id = fields.Many2one('budg_fiche_compte_rec', ondelete='cascade')
	date_rec = fields.Date("Date")
	numero_titre = fields.Char("N° Titre")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	montant_rec = fields.Float("Emission(1)")
	montant_ann = fields.Float("Annulation(2)")
	cumul = fields.Float("Cumul(3=1-2)")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class BudgSynthese(models.Model):
	_name = 'budg_synthese_rubrique'

	name = fields.Char("Nom", default="Consultation des engagements")
	cd_titre_id = fields.Many2one("budg_titre",default=lambda self: self.env['budg_titre'].search([('cd_titre','=', 'II')]), string = "Titre", required=False)
	cd_section_id = fields.Many2one("budg_section", "Section", required=False)
	cd_chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", required=False)
	cd_article_id = fields.Many2one("budg_param_article", "Article", required=False)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", "Paragraphe", required=False)
	cd_rubrique_id = fields.Many2one("budg_rubrique", "Rubrique", required=False)
	dt_appro_deb = fields.Date("Date debut", required=False)
	dt_appro_fin = fields.Date("Date fin", required=False)
	tout = fields.Boolean("Tous les engagements")
	etat = fields.Selection([
		('L', 'Engagement liquidé'),
		('N', 'Engagement à état nouveau'),
		('O', 'Engagement ordonnancé'),
		('R', 'Engagement rejeté par CF/CG'),
		('V', 'Engagement approuvé par DAF/DFC'),
		('W', 'Engagement visé par CF/CG'),
		], 'Etat')
	rubrique_lines = fields.One2many("budg_synthese_rubrique_line", 'synthese_id', readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	def remplir_synthese(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)
		synthese_id = self.id
		val_etat = str(self.etat)
		rub = int(self.cd_rubrique_id)

		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant,
			e.cd_rubrique_id as rub, e.no_beneficiaire as benef FROM budg_engagement e WHERE e.x_exercice_id = %d AND e.company_id = %d order by e.no_eng """ %(val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.rubrique_lines.unlink()
			for line in rows:
				result.append((0, 0, {'noeng': line['numero'], 'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
			self.rubrique_lines = result

		if self.cd_rubrique_id:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant,e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_engagement e WHERE e.cd_rubrique_id = %s AND 
				e.x_exercice_id = %s AND e.company_id = %s order by e.no_eng""" ,(rub,val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_lines.unlink()
				for line in rows:
					result.append((0,0, {'noeng' : line['numero'], 'dte': line['dte'],'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.rubrique_lines = result

		elif self.cd_rubrique_id and self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_engagement e WHERE e.cd_rubrique_id = %s AND e.state = %s e.x_exercice_id = %s AND e.company_id = %s order by e.no_eng""",(rub, val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noeng': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.rubrique_lines = result

		elif self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_engagement e WHERE e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_eng""" ,(val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noeng': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.rubrique_lines = result

		elif self.cd_rubrique_id and self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_engagement e WHERE e.cd_rubrique_id = %s and e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_eng""" ,(rub, val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noeng': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.rubrique_lines = result

		elif self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_eng as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_eng as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_engagement e WHERE e.state = %s and e.x_exercice_id = %s AND e.company_id = %s order by e.no_eng""",(val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noeng': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.rubrique_lines = result


class BudgSyntheseLine(models.Model):
	_name = 'budg_synthese_rubrique_line'
	
	synthese_id = fields.Many2one('budg_synthese_rubrique', ondelete='cascade')
	noeng = fields.Char("N° eng", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	montant = fields.Integer("Montant", readonly=True)
	dte = fields.Date("Date", readonly=True)
	rubrique = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	beneficiaire_id = fields.Many2one("ref_beneficiaire", "Bénéficiaire")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class Budg_synthese_liq(models.Model):
	_name = 'budg_synthese_liq_rubrique'
	
	name = fields.Char("Nom", default="Consultation des liquidations")
	cd_titre_id = fields.Many2one("budg_titre",default=lambda self: self.env['budg_titre'].search([('cd_titre','=', 'II')]), string = "Titre", required=False)
	cd_section_id = fields.Many2one("budg_section", "Section", required=False)
	cd_chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", required=False)
	cd_article_id = fields.Many2one("budg_param_article", "Article", required=False)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", "Paragraphe", required=False)
	cd_rubrique_id = fields.Many2one("budg_rubrique", "Rubrique", required=False)
	dt_appro_deb = fields.Date("Date d'approbation", required=False)
	dt_appro_fin = fields.Date(required=False)
	etat = fields.Selection([
		('N', 'Nouveau'),
		('L', 'Liquidé'),
		('A', 'Annulé'),
		], 'Etat', required=False)
	rubrique_liq_lines = fields.One2many("budg_synthese_liq_rubrique_line", 'synthese_liq_id', readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	def remplir_synthese_liq(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)
		synthese_id = self.id
		val_etat = str(self.etat)
		rub = int(self.cd_rubrique_id)

		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant,
			e.cd_rubrique_id as rub, e.no_beneficiaire as benef FROM budg_liqord e WHERE e.x_exercice_id = %d AND e.company_id = %d order by e.no_lo """ % (
			val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.rubrique_liq_lines.unlink()
			for line in rows:
				result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
									  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],
									  'montant': line['montant']}))
			self.rubrique_liq_lines = result

		if self.cd_rubrique_id:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant,e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_liqord e WHERE e.cd_rubrique_id = %s AND e.x_exercice_id = %s AND e.company_id = %s order by e.no_lo""", (rub, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
										  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],
										  'montant': line['montant']}))
				self.rubrique_liq_lines = result

		elif self.cd_rubrique_id and self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_liqord e WHERE e.cd_rubrique_id = %s AND e.state = %s e.x_exercice_id = %s AND e.company_id = %s order by e.no_lo""",
									(rub, val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
										  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],'montant': line['montant']}))
				self.rubrique_liq_lines = result

		elif self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_liqord e WHERE e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_lo""",(val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
										  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],
										  'montant': line['montant']}))
				self.rubrique_liq_lines = result

		elif self.cd_rubrique_id and self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_liqord e WHERE e.cd_rubrique_id = %s and e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_lo""",
									(rub, val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
										  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],
										  'montant': line['montant']}))
				self.rubrique_liq_lines = result

		elif self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_lo as numero, e.dt_etat as dte, e.lb_obj as objet, e.mnt_paye as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_liqord e WHERE e.state = %s and e.x_exercice_id = %s AND e.company_id = %s order by e.no_lo""",
									(val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.rubrique_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'noliq': line['numero'], 'dte': line['dte'], 'objet': line['objet'],
										  'beneficiaire_id': line['benef'], 'rubrique': line['rub'],
										  'montant': line['montant']}))
				self.rubrique_liq_lines = result


class BudgSyntheseLiqLine(models.Model):
	_name = 'budg_synthese_liq_rubrique_line'
	
	synthese_liq_id = fields.Many2one('budg_synthese_liq_rubrique', ondelete='cascade')
	dte = fields.Date("Date")
	noeng = fields.Char("N° eng")
	noliq = fields.Char("N° liq")
	objet = fields.Char("Objet")
	etat = fields.Char("Etat")
	beneficiaire_id = fields.Char("Bénéficiaire")
	montant = fields.Integer("Montant")
	rubrique = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class Budg_synthese_mdt(models.Model):
	_name = 'budg_synthese_mdt_rubrique'

	
	name = fields.Char("Nom", default="Consultation des mandats")
	cd_titre_id = fields.Many2one("budg_titre",default=lambda self: self.env['budg_titre'].search([('cd_titre','=', 'II')]), string = "Titre", required=False)
	cd_section_id = fields.Many2one("budg_section", "Section", required=False)
	cd_chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", required=False)
	cd_article_id = fields.Many2one("budg_param_article", "Article", required=False)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", "Paragraphe", required=False)
	cd_rubrique_id = fields.Many2one("budg_rubrique", "Rubrique", required=False)
	dt_appro_deb = fields.Date("Date d'approbation", required=False)
	dt_appro_fin = fields.Date(required=False)
	etat = fields.Selection([
		('N', 'Nouveau'),
		('O', 'Ordonnancé'),
		('A', 'Annulé'),
		('V', 'Visé CG'),
		('I', 'Visé DFC/AC'),
		('J','Rejeté DFC/AC'),
		('E', 'Pris en charge'),
		('F', 'Payé'),
		], 'Etat', required=False)
	mandat_liq_lines = fields.One2many("budg_synthese_mdt_rubrique_line", 'synthese_mdt_id', readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	
	def remplir_mdt_liq(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)
		synthese_id = self.id
		val_etat = str(self.etat)
		rub = int(self.cd_rubrique_id)


		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant,
			e.cd_rubrique_id as rub, e.no_beneficiaire as benef FROM budg_mandat e WHERE e.x_exercice_id = %d AND e.company_id = %d order by e.no_mandat """ %(val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_liq_lines.unlink()
			for line in rows:
				result.append((0, 0, {'nomdt': line['numero'], 'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
			self.mandat_liq_lines = result

		if self.cd_rubrique_id:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant,e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_mandat e WHERE e.cd_rubrique_id = %s AND e.x_exercice_id = %s AND e.company_id = %s order by e.no_mandat""" ,(rub,val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_liq_lines.unlink()
				for line in rows:
					result.append((0,0, {'nomdt' : line['numero'], 'dte': line['dte'],'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.mandat_liq_lines = result

		elif self.cd_rubrique_id and self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_mandat e WHERE e.cd_rubrique_id = %s AND e.state = %s and e.x_exercice_id = %s AND e.company_id = %s order by e.no_mandat""",(rub, val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'nomdt': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.mandat_liq_lines = result


		elif self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_mandat e WHERE e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_mandat""" ,(val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'nomdt': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.mandat_liq_lines = result

		elif self.cd_rubrique_id and self.dt_appro_deb and self.dt_appro_fin:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_mandat e WHERE e.cd_rubrique_id = %s and e.x_exercice_id = %s AND e.company_id = %s AND e.dt_etat BETWEEN %s and %s order by e.no_mandat""" ,(rub, val_ex, val_struct, val_deb, val_fin))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'nomdt': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.mandat_liq_lines = result

		elif self.etat:

			for vals in self:
				vals.env.cr.execute("""SELECT DISTINCT e.no_mandat as numero, e.dt_etat as dte, e.obj as objet, e.mnt_ord as montant, e.cd_rubrique_id as rub, e.no_beneficiaire as benef
				FROM budg_mandat e WHERE e.state = %s and e.x_exercice_id = %s AND e.company_id = %s order by e.no_mandat""",(val_etat, val_ex, val_struct))
				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_liq_lines.unlink()
				for line in rows:
					result.append((0, 0, {'nomdt': line['numero'],  'dte': line['dte'], 'objet': line['objet'],'beneficiaire_id': line['benef'], 'rubrique': line['rub'], 'montant': line['montant']}))
				self.mandat_liq_lines = result


class Budg_synthese_mdt_line(models.Model):
	_name = 'budg_synthese_mdt_rubrique_line'
	
	synthese_mdt_id = fields.Many2one('budg_synthese_mdt_rubrique', ondelete='cascade')
	nomdt = fields.Char("N° mandat")
	objet = fields.Char("Objet")
	etat = fields.Char("Etat")
	dte = fields.Date("Date")
	montant = fields.Integer("Montant")
	rubrique = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	beneficiaire_id = fields.Char("Bénéficiaire")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class Budg_synthese_rec(models.Model):
	@api.depends('cd_rubrique_id')
	def _concatenate(self):
		for test in self:
			test.visu ="Synthèse de la rubrique"+ " " +str(test.cd_rubrique_id.concate_rubrique)
	_name = 'budg_synthese_rec'
	_rec_name = "visu"
	
	visu = fields.Char(compute="_concatenate")
	cd_titre_id = fields.Many2one("budg_titre",default=lambda self: self.env['budg_titre'].search([('cd_titre','=', 'I')]), string = "Titre", required=True)
	cd_section_id = fields.Many2one("budg_section", "Section", required=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", required=True)
	cd_article_id = fields.Many2one("budg_param_article", "Article", required=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", "Paragraphe", required=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", "Rubrique", required=True)
	dt_appro_deb = fields.Date("Date d'approbation", required=True)
	dt_appro_fin = fields.Date(required=True)
	etat = fields.Selection([
		('N', 'Nouveau'),
		('V', 'Approuvé'),
		('W', 'Validé'),
		], 'Etat', required=True)
	recette_lines = fields.One2many("budg_synthese_recette_line", 'synthese_rec_id')
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	
	def remplir_synthese_rec(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)
		val_titre = int(self.cd_titre_id)
		val_section = int(self.cd_section_id)
		val_chap = int(self.cd_chapitre_id)
		val_art = int(self.cd_article_id)
		val_para = int(self.cd_paragraphe_id)
		val_rub = int(self.cd_rubrique_id)
		val_struct = int(self.company_id)
		val_etat = str(self.etat)
		
		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT t.cd_titre_recette as numero,  t.lb_objet as objet, t.mnt_rec as montant
			FROM budg_titrerecette t
			WHERE t.cd_titre_id = %s AND t.cd_section_id = %s AND
			t.cd_chapitre_id = %s AND t.cd_article_id = %s AND
			t.cd_paragraphe_id = %s AND t.cd_rubrique_id = %s AND 
			t.x_exercice_id = %s AND t.company_id = %s AND t.et_doss = %s
			AND t.dt_rec BETWEEN %s AND %s """ ,(val_titre, val_section, val_chap, val_art, val_para, val_rub, val_ex, val_struct, val_etat,val_deb, val_fin))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.recette_lines.unlink()
			for line in rows:
				result.append((0,0, {'notitre' : line['numero'], 'objet': line['objet'], 'montant': line['montant']}))
			self.recette_lines = result

class Budg_synthese_rec_line(models.Model):
	_name = 'budg_synthese_recette_line'
	
	synthese_rec_id = fields.Many2one('budg_synthese_rec', ondelete='cascade')
	notitre = fields.Char("N° titre")
	objet = fields.Char("Objet")
	montant = fields.Float("Montant")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


	
class Budg_journal_eng(models.Model):
	@api.depends('dt_appro_deb', 'dt_appro_fin')
	def _concatenate(self):
		for test in self:
			test.visu ="JOURNAL DES ENGAGEMENTS DU" + " " +str(test.dt_appro_deb)+ " " + "AU " + " " +str(test.dt_appro_fin)
	_rec_name = "visu"
	_name = 'budg_journal_eng'
	
	visu = fields.Char(compute='_concatenate')
	dt_appro_deb = fields.Date("Du", required=True)
	dt_appro_fin = fields.Date(required=True)
	jnl_eng_lines = fields.One2many("budg_journal_eng_line", "jnl_eng_id",readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	
	
	@api.onchange('dt_appro_fin')
	def change_dt_fin(self):
		
		if self.dt_appro_fin < self.dt_appro_deb:
			raise ValidationError(_('La date de début ne peut être supérieure à la date de fin'))
	
	
	def remplir_jnl_eng(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)

		
		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.dt_etat as periode, e.no_beneficiaire as creancier,e.no_eng as eng, m.no_mandat as nomandat, e.mnt_eng as engagement, e.cd_rubrique_id as imputation, 
			m.mnt_ord as mandat, (e.mnt_eng - m.mnt_ord) as solde FROM budg_engagement e, budg_mandat m
			WHERE e.x_exercice_id = m.x_exercice_id and e.x_exercice_id = %s AND e.company_id = m.company_id and e.company_id = %s AND e.dt_etat BETWEEN %s and %s AND e.no_eng = m.no_eng""" ,(val_ex, val_struct,val_deb, val_fin))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.jnl_eng_lines.unlink()
			for line in rows:
				result.append((0,0, {'date_deb' : line['periode'], 'creancier': line['creancier'], 'ref_eng': line['eng'], 'no_mandat': line['nomandat'], 'mnt_eng': line['engagement'], 'imputation': line['imputation'], 'mnt_mand': line['mandat'], 'solde': line['solde']}))
			self.jnl_eng_lines = result
		
	
	
class Budg_journal_line(models.Model):
	_name = 'budg_journal_eng_line'
	
	jnl_eng_id = fields.Many2one("budg_journal_eng", ondelete='cascade')
	date_deb = fields.Date('Date', readonly=True)
	creancier = fields.Many2one("ref_beneficiaire","Bénéficiare", readonly=True)
	ref_eng = fields.Char("Ref. eng.", readonly=True)
	no_mandat = fields.Char("N° Mandat", readonly=True)
	imputation = fields.Many2one("budg_rubrique", "Imputation", readonly=True)
	mnt_eng = fields.Float("Engagement", readonly=True)
	mnt_deg = fields.Float("Dégagement", readonly=True)
	mnt_mand = fields.Float("Mandat", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	solde = fields.Integer("Solde", readonly=True)
	

class Budg_journal_mdt(models.Model):
	@api.depends('dt_appro_deb', 'dt_appro_fin')
	def _concatenate(self):
		for test in self:
			test.visu ="JOURNAL DES DEPENSES DU "+ " " +str(test.dt_appro_deb)+ " AU" + " "  +str(test.dt_appro_fin)
	_rec_name = "visu"
	_name = 'budg_journal_mdt'
	
	visu = fields.Char(compute='_concatenate')
	dt_appro_deb = fields.Date("Date d'approbation", required=True)
	dt_appro_fin = fields.Date(required=True)
	jnl_mdt_lines = fields.One2many("budg_journal_mdt_line", "jnl_mdt_id", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	
	
	@api.onchange('dt_appro_fin')
	def change_dt_fin(self):
		
		if self.dt_appro_fin < self.dt_appro_deb:
			raise ValidationError(_('La date de début ne peut être supérieure à la date de fin'))
	
	
	def remplir_jnl_mdt(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)

		
		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.dt_etat as periode, e.no_beneficiaire as creancier, m.no_mandat as nomandat,
			e.cd_rubrique_id as imputation, m.mnt_ord as emission, m.mnt_annule as annule, m.mnt_ord - m.mnt_annule as solde
			FROM budg_engagement e, budg_mandat m WHERE e.x_exercice_id = %s AND e.company_id = %s 
			AND e.dt_etat BETWEEN %s and %s AND e.no_eng = m.no_eng and m.state != 'A' and e.state not in ('R', 'A') """ ,(val_ex, val_struct,val_deb, val_fin))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.jnl_mdt_lines.unlink()
			for line in rows:
				result.append((0,0, {'date_deb' : line['periode'], 'creancier': line['creancier'], 'no_mandat': line['nomandat'], 'imputation': line['imputation'], 'mnt_emis': line['emission'], 'mnt_annule': line['annule'], 'solde': line['solde']}))
			self.jnl_mdt_lines = result
		
	
class Budg_journal_mdt_line(models.Model):
	_name = 'budg_journal_mdt_line'
	
	jnl_mdt_id = fields.Many2one("budg_journal_mdt", ondelete='cascade')
	date_deb = fields.Date('Date')
	creancier = fields.Many2one("ref_beneficiaire","Créancier")
	ref_bord = fields.Char("Ref. Bord.")
	no_mandat = fields.Char("N° Mandat")
	imputation = fields.Many2one("budg_rubrique","Imputation")
	mnt_emis = fields.Float("Emission")
	mnt_annule = fields.Float("Annulation")
	solde = fields.Float("Solde")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)


class Budg_journal_rec(models.Model):
	@api.depends('dt_appro_deb', 'dt_appro_fin')
	def _concatenate(self):
		for test in self:
			test.visu ="Journal des titres de recettes du" + " " +str(test.dt_appro_deb)+ "au" + " " +str(test.dt_appro_fin)
	_rec_name = "visu"
	_name = 'budg_journal_rec'
	
	visu = fields.Char(compute='_concatenate')
	dt_appro_deb = fields.Date("Date d'approbation", required=True)
	dt_appro_fin = fields.Date(required=True)
	jnl_rec_lines = fields.One2many("budg_journal_rec_line", "jnl_rec_id")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	def remplir_jnl_mdt(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)

		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.dt_rec as periode, e.contribuable_id as creancier, e.cd_titre_recette as recette,
			e.cd_rubrique_id as imputation, e.mnt_rec as emission, e.mnt_annule as annule, e.mnt_rec - e.mnt_annule as solde
			FROM budg_titrerecette e WHERE e.x_exercice_id = %s AND e.company_id = %s 
			AND e.dt_rec BETWEEN %s and %s""",(val_ex, val_struct, val_deb, val_fin))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.jnl_rec_lines.unlink()
			for line in rows:
				result.append((0, 0, {'date_deb': line['periode'], 'debiteur': line['creancier'],
									  'no_titre': line['recette'], 'imputation': line['imputation'],
									  'mnt_emis': line['emission'], 'mnt_annule': line['annule'],
									  'solde': line['solde']}))
			self.jnl_rec_lines = result
	
	
class Budg_journal_rec_line(models.Model):
	_name = 'budg_journal_rec_line'
	
	jnl_rec_id = fields.Many2one("budg_journal_rec", ondelete='cascade')
	date_deb = fields.Date('Date')
	debiteur = fields.Many2one("ref_contribuable",'Débiteur')
	no_titre = fields.Char("N° Titre")
	imputation = fields.Many2one("budg_rubrique","Imputation")
	mnt_emis = fields.Float("Emission")
	mnt_annule = fields.Float("Annulation")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	solde = fields.Integer("Solde")


class BudgTypeSignataire(models.Model):
	_name = 'budg_type_signataire'
	
	code = fields.Char("Code", required=True)
	name = fields.Char("Libellé", required=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)	

			
class  BudgJustDepense(models.Model):
	_name ='budg_just_depense'
	
	param_article_id = fields.Many2one("budg_param_article")
	lb_long = fields.Char("Libellé")
	oblige = fields.Boolean("Obligé")
	nombre = fields.Integer("Référence")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class  BudgJustRecette(models.Model):
	_name ='budg_just_recette'
	
	param_article_id = fields.Many2one("budg_param_article")
	lb_long = fields.Char("Libellé")
	oblige = fields.Boolean("Obligé")
	nombre = fields.Integer("Référence")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
		


class BudgCategoriePrecompte(models.Model):
	_name = "budg_categorie_precompte"
	_rec_name = "lb_long"

	lb_court = fields.Char("Libellé court")
	lb_long = fields.Char("Libellé long")
	active = fields.Boolean("Actif")

class BudgTypePrecompte(models.Model):
	_name = "budg_type_precompte"
	_rec_name = "lb_long"
	
	categorie_id = fields.Many2one("budg_categorie_precompte", "Catégorie de précompte")
	lb_court = fields.Char("Libellé court")
	lb_long = fields.Char("Libellé long")
	no_imputation = fields.Many2one("compta_plan_lines", "Imputation")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	

class BudgPrecompte(models.Model):
	_name = "budg_precompte"
	_rec_name = "no_precompte"
	
	no_precompte = fields.Char("N° Précompte")
	type_precompte = fields.Many2one("budg_type_precompte","Type de précompte", required=True)
	mnt_precompte = fields.Float("Montant précompte")
	reste = fields.Float("Reste")
	imput_budg = fields.Char("Imput Budg.", readonly=True)
	mnt_mandat = fields.Float("Montant", readonly=True)
	dt_mandat = fields.Date('Date', readonly=True)
	no_mdt = fields.Many2one('budg_mandat', "Référence mandat")
	no_lo = fields.Char('N° Liq', readonly=True)
	no_eng = fields.Char('N° Eng', readonly=True)
	objet = fields.Text('Objet', readonly=True)
	modereg = fields.Char("Mode de règlement", readonly=True)
	dt_precompte = fields.Date("Date précompte")
	objet_precompte = fields.Text("Objet du précompte", required=True)
	cpte_deb = fields.Many2one("compta_plan_lines", "Cpte Débit", readonly=True)
	cpte_deb_id = fields.Integer()
	cpte_cred = fields.Many2one("compta_plan_lines", "Cpte Crédit", readonly=True)
	cpte_cred_id = fields.Integer()
	dt_visa = fields.Date()
	state = fields.Selection([
		('N', 'Nouveau'),
		('P', 'Provisoire'),
		], string="Etat", default='N')
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class BudgReimputationDepense(models.Model):
	_name = 'budg_reimputation_depense'
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	reimputation_depense_ids = fields.One2many("budg_reimputation_depense_line","reimputationdep_id")

class BudgReimputationDepenseLine(models.Model):
	_name = 'budg_reimputation_depense_line'
	
	reimputationdep_id = fields.Many2one("budg_reimputation_depense")
	dte_mandat = fields.Date("Date de mandat")
	numero_mandat = fields.Many2one("budg_mandat", "Numéro Mdt")
	numero_bord = fields.Many2one("budg_bordereau_mandatement", "N° Bordereau")
	nature_depense = fields.Char("Nature dépense")
	imput_init = fields.Char("Imputation initiale")
	imput_def = fields.Char("Imputation définitive")
	montant = fields.Float("Montant")
	observation = fields.Text("Observation")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	

class BudgReimputationRecette(models.Model):
	_name = 'budg_reimputation_recette'
	
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	reimputation_recette_ids = fields.One2many("budg_reimputation_recette_line","reimputationrec_id")

class BudgReimputationRecetteLine(models.Model):
	_name = 'budg_reimputation_recette_line'
	
	reimputationrec_id = fields.Many2one("budg_reimputation_recette")
	dte_titre = fields.Date("Date de titre")
	numero_titre = fields.Many2one("budg_titrerecette", "Numéro Titre")
	numero_bord = fields.Many2one("budg_bord_titre_recette", "N° Bordereau")
	nature_titre = fields.Char("Nature titre")
	imput_init = fields.Char("Imputation initiale")
	imput_def = fields.Char("Imputation définitive")
	montant = fields.Float("Montant")
	observation = fields.Text("Observation")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	

class BudgEtatDepEng(models.Model):
	_name = 'budg_etat_depense_engage'
	_rec_name="section_id"
	
	dt_appro_deb = fields.Date("Du", required=True)
	dt_appro_fin = fields.Date("Au", required=True)
	section_id = fields.Char("Section",default="Fonctionnement", readonly=True)
	etadep_ids = fields.One2many("budg_etat_depense_engage_line", "etat_dep_id",readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	
	
	def rechercher(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_deb = str(self.dt_appro_deb)
		val_fin = str(self.dt_appro_fin)

		
		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT e.no_eng as eng, e.no_beneficiaire as creancier, e.mnt_eng as montant,e.dt_etat as dte, e.cd_rubrique_id as imputation
			FROM budg_engagement e WHERE e.x_exercice_id = %s AND e.company_id = %s AND e.state not in ('A','draft','R')
			AND e.dt_etat BETWEEN %s and %s AND e.lbsection = 'FONCT' order by e.no_eng""" ,(val_ex, val_struct,val_deb, val_fin))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.etadep_ids.unlink()
			for line in rows:
				result.append((0,0, {'no_eng' : line['eng'], 'creancier': line['creancier'], 'imputation': line['imputation'], 'dte': line['dte'], 'montant': line['montant']}))
			self.etadep_ids = result

class BudgEtatDepEngLine(models.Model):
	_name ="budg_etat_depense_engage_line"
	
	
	etat_dep_id = fields.Many2one("budg_etat_depense_engage", ondelete='cascade')
	no_eng = fields.Char("N° Acte d'Eng.")
	creancier = fields.Many2one('ref_beneficiaire','Créancier')
	imputation = fields.Many2one("budg_rubrique","Imputation")
	dte = fields.Date("Date")
	montant = fields.Float("Montant engagé non mandaté")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	

class BudgEtatRest(models.Model):
	_name = 'budg_etat_rest'
	_rec_name= "section_id"
	
	section_id = fields.Char("Section",default="Investissement", readonly=True)
	rest_ids = fields.One2many("budg_etat_rest_line", "rest_id")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	
	def rechercher(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		
		for vals in self:
			vals.env.cr.execute("""SELECT DISTINCT l.cd_rubrique_id as nature, l.mnt_corrige as budget, l.mnt_engage as realiser, (l.mnt_corrige - l.mnt_engage) as rest FROM budg_ligne_exe_dep l, budg_engagement e, ref_section rs, budg_section bs 
			WHERE rs.id = bs.section and bs.id = l.cd_section_id and rs.lb_court = 'INVEST' AND l.x_exercice_id = %d AND l.company_id = %d order by l.cd_rubrique_id""" %(val_ex, val_struct))
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.rest_ids.unlink()
			for line in rows:
				result.append((0,0, {'nature' : line['nature'], 'budget': line['budget'], 'realisation': line['realiser'], 'reste': line['rest']}))
			self.rest_ids = result
			
			for x in vals.rest_ids:
				x.reste = x.budget - x.realisation

class BudgEtatRestLine(models.Model):
	_name ="budg_etat_rest_line"

	rest_id = fields.Many2one("budg_etat_rest", ondelete='cascade')
	nature = fields.Many2one("budg_rubrique", "Nature de l'investissement", readonly=True)
	budget = fields.Float('Budget', readonly=True)
	realisation = fields.Float("Réalisation", readonly=True)
	reste = fields.Float("Reste à réaliser", readonly=True)
	observation = fields.Text("Proposition de l'ordonnateur")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	
class BudgAnnulMandat(models.Model):
	_name = 'budg_mandat_annule'
	_rec_name = 'mandat_id'
	
	mandat_id = fields.Many2one('budg_mandat', "Ordonnance à annuler", domain=[('state', 'in', ['N', 'O', 'J'])], required=True)
	montant = fields.Float('Montant', readonly=True)
	dte_mandat = fields.Date("Date Ordonnance", readonly=True)
	dte_annulation = fields.Date("Date d'annulation", required=True)
	titre_id = fields.Many2one("budg_titre","Titre", readonly=True)
	section_id = fields.Many2one("budg_section","Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre","Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article","Article", readonly=True)
	paragraphe_id = fields.Many2one("budg_paragraphe","Paragraphe", readonly=True)
	rubrique_id = fields.Many2one("budg_rubrique","Rubrique", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	typebenef = fields.Many2one("ref_categoriebeneficiaire","Catégorie", readonly=True)
	nom = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	motif = fields.Text("Motif d'annulation", required=True)
	no_lo = fields.Many2one("budg_liqord","Liquidation", readonly=True)
	no_engs = fields.Many2one("budg_engagement", "Eng", readonly=True)
	state = fields.Selection([
		('N', 'Nouveau'), ('A', 'Annulé'),], string='Etat', default='N')
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.onchange('mandat_id')
	def OnChangeMdt(self):
		if self.mandat_id:
			self.montant = self.mandat_id.mnt_ord
			self.dte_mandat = self.mandat_id.dt_etat
			self.objet = self.mandat_id.obj
			self.typebenef = self.mandat_id.type_beneficiaire_id
			self.nom = self.mandat_id.no_beneficiaire
			self.titre_id = self.mandat_id.cd_titre_id
			self.section_id = self.mandat_id.cd_section_id
			self.chapitre_id = self.mandat_id.cd_chapitre_id
			self.article_id = self.mandat_id.cd_article_id
			self.paragraphe_id = self.mandat_id.cd_paragraphe_id
			self.rubrique_id = self.mandat_id.cd_rubrique_id
			self.no_lo = self.mandat_id.no_lo
			self.no_engs = self.mandat_id.no_eng
	
	
	def annuler(self):
		
		v_ex = int(self.x_exercice_id)
		v_struct = int(self.company_id)
		v_mdt = int(self.mandat_id)
		v_nolo = int(self.no_lo)
		v_eng = int(self.no_engs)
		v_mnt = int(self.montant)

		for val in self:

			self.env.cr.execute("""UPDATE budg_mandat SET state = 'A', mnt_annule = %s WHERE x_exercice_id = %s AND company_id = %s AND id = %s""" ,(v_mnt,v_ex, v_struct, v_mdt))
			self.env.cr.execute("""UPDATE budg_liqord SET state = 'A' WHERE x_exercice_id = %d AND company_id = %s AND id = %d""" %(v_ex, v_struct, v_nolo))
			self.env.cr.execute("""UPDATE budg_engagement SET state = 'V' WHERE x_exercice_id = %d AND company_id = %s AND id = %d""" %(v_ex, v_struct, v_eng))
			self.action_mandat_annuler()


	def action_mandat_annuler(self):
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_mdt = int(self.mandat_id)

		val_titre = int(self.titre_id)
		val_chap = int(self.chapitre_id)
		val_sec = int(self.section_id)
		val_art = int(self.article_id)
		val_par = int(self.paragraphe_id)
		val_rub = int(self.rubrique_id)


		self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_mandate = (select DISTINCT sum(BM.mnt_ord) - BM.mnt_ord
			FROM budg_ligne_exe_dep BE, budg_mandat BM WHERE BM.id = %d AND 
			BE.cd_titre_id = %d and BE.cd_section_id = %d and BE.cd_chapitre_id = %d and BE.cd_art_id = %d and BE.cd_paragraphe_id = %d and 
			BE.cd_rubrique_id = %d and BE.x_exercice_id = %d and BE.company_id = %d group by  BM.mnt_ord) WHERE cd_titre_id = %d and 
			cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d and 
			cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (v_mdt,val_titre, val_sec, val_chap, val_art,
			val_par, val_rub, val_ex, val_struct, val_titre, val_sec, val_chap,val_art, val_par, val_rub, val_ex, val_struct))

		self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET reste_mandat = (mnt_corrige - mnt_mandate) + mnt_mandate
			WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d 
			and cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (
		val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct))

		self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET taux = ((mnt_mandate * 100) / mnt_corrige)
			WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d 
			and cd_paragraphe_id = %d and cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (
		val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct))

		self.write({'state': 'A'})


class BudgBordManAnnul(models.Model):

	_name = "budg_bordereau_mandat_annule"
	_rec_name = "type_bord_trsm"

	type_bord_trsm = fields.Char('Type de bordereau', readonly=True)
	cd_acteur = fields.Char(string ="Acteur", readonly=True)
	date_emis = fields.Date(string="Date d'émission",default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cd_acteur_accuse = fields.Char(string ="Acteur", readonly=True)
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.Many2many("budg_mandat_annule", "budg_detail_bord_mandat_annule", string="Liste des mandats annulés")
	state = fields.Selection([
        ('N', 'Nouveau'),
        ('V', 'Mise en bordereau'),
        ('R', 'Reception Bord. Annul.'),
        ('ED', 'Renvoi bord. CF/CG'),
        ('RD', 'Reception bord CF/CG'),
        ], 'Etat', default='N', required=True, readonly=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


	def MiseBord(self):
		
		val_struct = int(self.company_id)
		val_ex = int(self.x_exercice_id)
		val_id = int(self.id)
		
		self.env.cr.execute("""SELECT sum(montant) FROM budg_mandat_annule m, budg_bordereau_mandat_annule b, budg_detail_bord_mandat_annule bm
		WHERE b.x_exercice_id = %d AND b.company_id = %d AND bm.budg_bordereau_mandat_annule_id = %d
		AND m.id = bm.budg_mandat_annule_id AND bm.budg_bordereau_mandat_annule_id = b.id""" %(val_ex,val_struct, val_id))
		res = self.env.cr.fetchone()
		self.totaux = res and res[0]

		self.env.cr.execute("select lb_long from budg_typebordtrans where code = '10' ")
		val = self.env.cr.fetchone()
		self.type_bord_trsm = val and val[0] or 0
		
		self.env.cr.execute("select type_depart from budg_typebordtrans where code = '10' ")
		val1 = self.env.cr.fetchone()
		self.cd_acteur = val1 and val1[0] or 0
		
		self.env.cr.execute("select type_dest from budg_typebordtrans where code = '10' ")
		val2 = self.env.cr.fetchone()
		self.cd_acteur_accuse = val2 and val2[0] or 0

		
		self.write({'state': 'V'})
		

	def RecBord(self):
		self.write({'state': 'R'})
		

	def RenBord(self):
		self.write({'state': 'ED'})
	

	def ReceBord(self):
		self.write({'state': 'RD'})
		
	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')
		

class BudgRecetteAnnule(models.Model):
	_name = 'budg_recette_annule'
	_rec_name = "recette_id"
	
	recette_id = fields.Many2one('budg_titrerecette', "Titre à annuler ou à réduire", required=True)
	montant = fields.Float('Montant', readonly=True)
	dte_titre = fields.Date("Date d'émission du titre de recette", readonly=True)
	dte_annulation = fields.Date("Date d'annulation ou de réduction", required=True)
	titre_id = fields.Char("Titre", readonly=True)
	section_id = fields.Char("Section", readonly=True)
	chapitre_id = fields.Char("Chapitre", readonly=True)
	article_id = fields.Char("Article", readonly=True)
	paragraphe_id = fields.Char("Paragraphe", readonly=True)
	rubrique_id = fields.Char("Rubrique", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	typedebiteur = fields.Char("Type de débiteur", readonly=True)
	nom = fields.Char("Nom débiteur", readonly=True)
	motif = fields.Text("Motif d'annulation", required=True)
	no_lo = fields.Integer()
	state = fields.Selection([
		('N', 'Nouveau'),
		('A', 'Annulé'),
		('W', 'Visa CF'),
		], string= 'Etat', default='N')
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	@api.onchange('recette_id')
	def OnChangerec(self):
		if self.recette_id:
			self.montant = self.recette_id.mnt_rec
			self.dte_titre = self.recette_id.dt_rec
			self.objet = self.recette_id.lb_objet
			self.typedebiteur = self.recette_id.cd_type_contribuable.lb_long
			self.nom = self.recette_id.contribuable_id.nm_rs
			self.titre_id = self.recette_id.cd_titre_id.titre.titre
			self.section_id = self.recette_id.cd_section_id.section.section
			self.chapitre_id = self.recette_id.cd_chapitre_id.chapitre.chapitre
			self.article_id = self.recette_id.cd_article_id.article.article
			self.paragraphe_id = self.recette_id.cd_paragraphe_id.paragraphe.paragraphe
			self.rubrique_id = self.recette_id.cd_rubrique_id.concate_rubrique
			
	def annuler(self):
		
		v_ex = int(self.x_exercice_id)
		v_struct = int(self.company_id)
		v_rec = int(self.recette_id)
		self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss = 'A' WHERE x_exercice_id = %s AND company_id = %s AND id = %d""" %(v_ex, v_struct, v_rec))
	
		self.write({'state': 'A'})


class Budg_bord_titreAnnule(models.Model):
	
	_name = "budg_bord_titre_recette_annule"
	_rec_name = "no_bord_rec"
	
	name = fields.Char()
	no_bord_rec = fields.Char("N° Bord", readonly=True)
	cd_acteur = fields.Selection([('ORD', 'ORD'), ('CF', 'CF'), ('AC', 'AC'),
        ], string="Acteur", default="ORD")
	date_emis = fields.Date("Date bordereau", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date()
	num_accuse = fields.Char()
	totaux = fields.Float()
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau d'annulation Titre de recette", readonly=True)
	cd_acteur_accuse = fields.Selection([('ORD', 'ORD'), ('CF', 'CF'), ('AC', 'AC'),
        ], string ="Acteur accusé")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	recette_ids = fields.Many2many("budg_recette_annule", "budg_detail_bord_recette_annule", string="Liste des titres de recettes", ondelete="restrict")
	state = fields.Selection([('N', 'Nouveau'), ('V', 'Mise en bordereau'),('R', 'Réception bord. Annul.'),
							  ('ED', 'Envoi bord. CF/CG'),('RD', 'Réception bord. CF/CG'),
							  ], 'Etat', default='N', required=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


	def MiseBord(self):
		self.write({'state': 'V'})
		

	def RecBord(self):
		self.write({'state': 'R'})
		

	def RenBord(self):
		self.write({'state': 'ED'})
	

	def ReceBord(self):
		self.write({'state': 'RD'})
		
	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')


class RefTypeContribuable(models.Model):
	_name = "ref_typecontribuable"
	_rec_name = "cate_id"
	sequence = fields.Integer(default=10)
	cd_type_contribuable = fields.Char(string = "Code", default=lambda self: self.env['ir.sequence'].next_by_code('cd_type_contribuable'), readonly = True)
	lb_long = fields.Char(string = "Libellé court", size = 25, required=False)
	name = fields.Char(string = "Libellé long", size = 100, required=False)
	active = fields.Boolean('Actif',default=True)
	cate_id = fields.Many2one("ref_categoriecontribuable", required=True,string = "Catégorie de contribuable")
	cpte_client = fields.Many2one("compta_plan_lines",string = "Compte tiers", required=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	_sql_constraints = [('cd_type_contribuable', 'unique (cd_type_contribuable)', "Ce code existe déjà. Veuillez changer de code !"),]



class ref_TypeBeneficiaire(models.Model):
	_name = "ref_typebeneficiaire"
	_rec_name = "cat_id"
	sequence = fields.Integer(default=10)
	cd_type_beneficiaire = fields.Char(string = "Code", size = 2)
	name = fields.Char(string = "Libellé court", size = 25, required=False)
	lb_long = fields.Char(string = "Libellé long", size = 100, required=False)
	cat_id = fields.Many2one("ref_categoriebeneficiaire", string = "Catégorie de bénéficiaire", required=True)
	cpte_client = fields.Many2one("compta_plan_lines",string = "Compte tiers", required=True)
	active = fields.Boolean('Actif',default=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	_sql_constraints = [('cd_type_beneficiaire', 'unique (cd_type_beneficiaire)', "Ce code existe déjà. Veuillez changer de code !"),]
 

class RefBeneficiaire(models.Model):
	_name = "ref_beneficiaire"
	_rec_name = "nm"
	name = fields.Char(string="Identifiant", default=lambda self: self.env['ir.sequence'].next_by_code('name'), readonly = True)
	no_beneficiaire = fields.Char(string="Raison sociale", size=65)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire",string="Catégorie", required=True)
	nm = fields.Char(string="Intitulé", required=True)
	pn = fields.Char(string="Prénom", size=40)
	no_ifu = fields.Char(string="N° IFU", size=30, required=True)
	domaine_id = fields.Many2one('ref_secteur_activite', "Domaine d'activité", required=False)
	cd_mat = fields.Char(string="Matricule", size=20)
	no_eng = fields.Integer(string="No_Eng")
	ex_last = fields.Integer(string="Ex_last")
	ap_rue = fields.Char(string="Rue", size=35)
	ap_bp = fields.Char(string="Boite postale", size=50)
	ap_cd_post = fields.Char(string="Code postal", size=50)
	ap_ville = fields.Char(string="Ville", size=30)
	ap_pays = fields.Many2one("ref_pays",string="Pays")
	tel = fields.Char(string="Téléphone", size=30)
	nm_officiel = fields.Char(string="Titre officiel", size=50)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bank_id = fields.Many2one("res.bank", string="Banque")
	active = fields.Boolean('Actif', default=True)
	fg_bloc = fields.Char()
	cpte_client = fields.Many2one("ref_souscompte", string="Compte tiers")
	cpte_fournisseur = fields.Many2one("compta_plan_lines", string="Compte tiers", required=True)
	agence_bank_id = fields.Char(string="N° Agence")
	acc_number = fields.Char(string="N° compte")
	cat_fournisseur = fields.Selection([
        ('S', 'Société'),
        ('P', 'Particulier')], 'Catégorie')


class BudgBordEngCtrl(models.Model):
	_name = "budg_bordereau_engagement_controle"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Reception d'Engagement de DAF-DFC/DCMEF-CG", readonly=True)
	cd_acteur = fields.Char(string ="Acteur", default="CG", readonly=True)
	date_emis = fields.Date("Date d'émision", readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	date_recep = fields.Date("Date de réception par DAF/DFC", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	bord_recu = fields.Many2one("budg_bordereau_engagement", "N° Bord. reçu", required=True, domain=[('state','=','T')])
	cd_acteur_accuse = fields.Char(string ="Acteur")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_ids = fields.One2many("budg_liste_engagment", "bord_id")
	state = fields.Selection([
        ('N', 'Nouveau'),
        ('R', 'Réceptionner bordereau'),
        ], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.id as eng, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
			b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement b, budg_bordereau_engagement bb, eng_id i
			where bb.id = %d and i.budg_engagement_id = b.id and i.budg_bordereau_engagement_id = bb.id and b.company_id = %d and b.x_exercice_id = %d and b.state = 'V' """ %(id_bord, val_struct, val_ex))
			
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.engagement_ids.unlink()
			for line in rows:
				result.append((0,0, {'dt_etat' : line['dte'], 'no_eng': line['eng'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
									'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
									'no_beneficiaire': line['benef'],'lb_obj': line['obj'],'mnt_eng': line['mnt']}))
			self.engagement_ids = result
	
	def receptionner(self):
		
		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)


		self.env.cr.execute("select bordeng from budg_compteur_bord_eng_ctrl where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng_ctrl(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_eng_ctrl SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))
		
		self.date_recus = date.today()

		self.env.cr.execute("""UPDATE budg_bordereau_engagement SET state ='R', date_recus = %s WHERE id = '%s' and x_exercice_id = %s and company_id = %s""" ,(self.date_recus,bord, val_ex, val_struct))

		self.afficher()
		
		self.write({'state': 'R'})
	
	
	def envoyer(self):
		
		self.write({'state': 'E'})

		self.date_emis = date.today()
		
	

class BudgListeEngagement(models.Model):
	_name = 'budg_liste_engagment'
	
	
	bord_id = fields.Many2one('budg_bordereau_engagement_controle', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly =True)
	no_eng = fields.Many2one("budg_engagement" ,string="N° engagement", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre',readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one("budg_typeprocedure", string = "Type de procédure", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string = "Identité")
	lb_obj = fields.Text(string = "Objet",size=300, readonly=True)
	mnt_eng = fields.Float(string = "Montant engagement", readonly=True)
	piecejust_ids = fields.One2many("budg_liste_piece_eng",'eng_id', readonly=True)
	dt_visa_cf = fields.Date(string = "Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
		('2','Erreur Montant'),('3','Erreur Pièce'),('4','Erreur Bénéficiaire'),
		('5','Erreur Objet')],string = "Motif du rejet")
	x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('V','Approuvé'),
		('W', 'Visé'),
		('R', 'Rejeté'),
        ], default='V', string='Etat',index=True,readonly=True, track_visibility='always')
	credit_disponible = fields.Integer()
	envoyer_daf = fields.Selection([('Y','Oui'),('N','Non')], string='Envoyé ?', default='N')
	observation = fields.Text("Observation")
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	"""@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	 Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))"""

	def viser(self):
		
		for vals in self:
		
			eng = int(vals.no_eng)
			val_ex = int(vals.x_exercice_id)
			val_strcut = int(vals.company_id)

			self.env.cr.execute("""UPDATE budg_engagement SET state ='W', envoyer_daf = 'Y' WHERE id = %d and company_id = %d""" %(eng, val_strcut))

			self.write({'state': 'W'})
	
	def rejeter(self):
		
		eng = int(self.no_eng)
		val_ex = int(self.x_exercice_id)
		val_strcut = int(self.company_id)

		val_rejet = self.motif_rejet
		
		self.env.cr.execute("""UPDATE budg_engagement SET state ='R', motif_rejet = %s WHERE id = %s and company_id = %s""" ,(val_rejet,eng, val_strcut ))
		
		self.write({'state': 'R'})
			
	
	
	def afficher_piece(self):
		
		eng = int(self.no_eng)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("select lb_long as lib, oblige as obl, ref as re, montant as mnt,  dte as dte, nombre as nbr from budg_piece_engagement where eng_id = %d and company_id = %d" %(eng, val_struct))
		
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0,0, {'lib' : line['lib'], 'oblige': line['obl'], 'dte': line['dte'], 'ref': line['re'], 'mnt': line['mnt'], 'nbr': line['nbr']}))
			self.piecejust_ids = result
			
	
class BudgListePieceEng(models.Model):
	_name = "budg_liste_piece_eng"
	
	eng_id = fields.Many2one("budg_liste_engagment", ondelete='cascade')
	lib = fields.Many2one("ref_piece_justificatives","Libellé", readonly=True)
	oblige = fields.Boolean("Obligatoire", readonly=True)
	ref = fields.Char("Référence", readonly=True)
	dte = fields.Date("Date", readonly=True)
	nbr = fields.Integer("Nombre", readonly=True)
	mnt = fields.Integer("Montant", readonly=True)
	

#Reception du bordereau envoyer par CG
class BudgBordEngRecepCtrl(models.Model):

	_name = "budg_bordereau_engagement_recep_controle"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Reception d'Engagement de DMCEF/CG", readonly=True)
	cd_acteur = fields.Char(string ="Acteur", default='DAF/DFC', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_engagement_renvoi_daf","N° Bord. réçu",required=True, domain=[('state','=','E')])
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	cd_acteur_accuse = fields.Char(string ="Acteur")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_ids = fields.Many2many("budg_liste_engagment_recu", "bord_id", string="Liste des engagements", ondelete="restrict")
	state = fields.Selection([
		('E', 'Bordereau envoyé par CG'),
		('R', 'Réceptionné bordereau CG'),
        ], 'Etat', default='E', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		if self.bord_recu:
		
			for vals in self:
				vals.env.cr.execute("""select b.dt_etat as dte, b.no_eng as eng, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
				b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
				b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement_renvoi b 
				where b.bord_id = %d and b.company_id = %d and b.state = 'W' and b.envoyer = 'Y' """ %(id_bord, val_struct))
				
				rows = vals.env.cr.dictfetchall()
				result = []
				
				vals.engagement_ids.unlink()
				for line in rows:
					result.append((0,0, {'dt_etat' : line['dte'], 'no_eng': line['eng'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
										'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
										'no_beneficiaire': line['benef'],'lb_obj': line['obj'],'mnt_eng': line['mnt']}))
				self.engagement_ids = result

	
	def receptionner(self):
		
		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.date_recus = date.today()
		
		self.env.cr.execute("""UPDATE budg_bordereau_engagement_controle SET state ='R', date_recep = '%s' WHERE id = %s and x_exercice_id = %s and company_id = %s""" %(self.date_recus, bord, val_ex, val_struct))

		self.env.cr.execute("select bordeng from budg_compteur_bord_eng_recep where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng_recep(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_eng_recep SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

		self.afficher()
		
		self.write({'state': 'R'})

	

class BudgListeEngagementRecu(models.Model):
	_name = 'budg_liste_engagment_recu'
	
	
	bord_id = fields.Many2one('budg_bordereau_engagement_recep_controle', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly =True)
	no_eng = fields.Many2one("budg_engagement" ,string="N° engagement", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre',readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one("budg_typeprocedure", string = "Type de procédure", v=True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string = "Identité")
	lb_obj = fields.Text(string = "Objet",size=300, readonly=True)
	mnt_eng = fields.Float(string = "Montant engagement", readonly=True)
	dt_visa_cf = fields.Date(string = "Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
		('2','Erreur Montant'),('3','Erreur Pièce'),('4','Erreur Bénéficiaire'),
		('5','Erreur Objet')],string = "Motif du rejet")
	#x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('V','Approuvé'),
		('W', 'Visé'),
		('R', 'Rejeté'),
        ], default='V', string='Etat',index=True,readonly=True, track_visibility='always')
	credit_disponible = fields.Integer()
	envoyer_daf = fields.Selection([('Y','Oui'),('N','Non')], string='Envoyé ?', default='Y')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


class BudgBordEngRenvoiDaf(models.Model):
	_name = "budg_bordereau_engagement_renvoi_daf"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Transmission d'Engament pour DFC", readonly=True)
	cd_acteur = fields.Char(string ="Acteur", default='CG', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_engagement_controle","N° Bord.",required=False, domain=[('state','=','R')])
	date_emis = fields.Date("Date d'émision", readonly=True)
	date_recus = fields.Date("Date de réception")
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words" )
	cd_acteur_accuse = fields.Char(string ="Acteur")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_ids = fields.One2many("budg_liste_engagment_renvoi", "bord_id", string="Liste des engagements")
	state = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Bordereau envoyé à DAF/DFC'),
		('R', 'Bordereau réceptionné par DAF/DFC'),
        ], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	signataire_2 = fields.Many2one("budg_signataire",
								   default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
	signataire_3 = fields.Many2one("budg_signataire",
								   default=lambda self: self.env['budg_signataire'].search([('code', '=', '3')]))

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.id as eng, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
				b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
				b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement b 
				where b.x_exercice_id = %d and b.company_id = %d and b.state = 'W' and b.envoyer_daf = 'N' """ %(val_ex, val_struct))
			
			rows = vals.env.cr.dictfetchall()
			result = []
			
			vals.engagement_ids.unlink()
			for line in rows:
				result.append((0,0, {'dt_etat' : line['dte'], 'no_eng': line['eng'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
									'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
									'no_beneficiaire': line['benef'],'lb_obj': line['obj'],'mnt_eng': line['mnt']}))
			self.engagement_ids = result
	
	
	def envoyer(self):
		
		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.env.cr.execute("""select * from budg_liste_engagment_renvoi r, budg_bordereau_engagement_renvoi_daf d 
		where r.bord_id = d.id and r.bord_id = %d and r.company_id = %d and r.envoyer = 'Y'""" %(bord, val_struct))
		for val in self.env.cr.dictfetchall():
			envo = val['envoyer']
		
			self.env.cr.execute("""UPDATE budg_liste_engagment SET envoyer_daf ='Y' WHERE id = %d and x_exercice_id = %d and
			company_id = %d""" %(envo, val_ex, val_struct))

		self.env.cr.execute("select bordeng from budg_compteur_bord_eng_renvoi where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng_renvoi(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_eng_renvoi SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))
		
		self.date_emis = date.today()

		self.write({'state': 'E'})

	def action_receptionner(self):
		self.date_recus = date.today()
		self.write({'state': 'R'})

	

class BudgListeEngagementRenvoi(models.Model):
	_name = 'budg_liste_engagment_renvoi'
	
	
	bord_id = fields.Many2one('budg_bordereau_engagement_renvoi_daf', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly =True)
	no_eng = fields.Many2one("budg_engagement" ,string="N° engagement", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre',readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one("budg_typeprocedure", string = "Type de procédure", v=True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string = "Identité")
	lb_obj = fields.Text(string = "Objet",size=300, readonly=True)
	mnt_eng = fields.Float(string = "Montant engagement", readonly=True)
	dt_visa_cf = fields.Date(string = "Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
		('2','Erreur Montant'),('3','Erreur Pièce'),('4','Erreur Bénéficiaire'),
		('5','Erreur Objet')],string = "Motif du rejet")
	#x_exercice_id = fields.Many2one("ref_exercice",  default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('V','Approuvé'),
		('W', 'Visé'),
		('R', 'Rejeté'),
        ], default='W', string='Etat',index=True,readonly=True, track_visibility='always')
	envoyer = fields.Selection([('Y','Oui'),('N','Non')], default="Y", string="Envoyé ?")
	credit_disponible = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


class BudgBordMdtControle(models.Model):
	_name = "budg_bordereau_mandatement_controle_a_viser"
	_rec_name = "no_bord_mandat"
	_order = " id desc"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau',default='Bordereau de Réception de Mandats de DAF/ORD', readonly=True)
	cd_acteur = fields.Char(string="Acteur", default="CG",readonly=True)
	date_emis = fields.Date(string="Date d'émission", readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	date_recep = fields.Date("Date de reception par DAF/DFC", readonly=True)
	num_accuse = fields.Char()
	bord_recu = fields.Many2one("budg_bordereau_mandatement", required=True, domain=[('et_doss','=','V')])
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur",  default="DAF/DFC", readonly=True)
	#x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_liste_mandatement", "liste_id")
	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('R', 'Receptionné'),
		('E', 'Envoyé à DAF/DFC '),
		('BR', 'Réceptionné par DAF/DFC'),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		if self.bord_recu:
		
			for vals in self:
				vals.env.cr.execute("""select m.dt_etat as dte,m.no_lo as liq, m.id as mdt, m.cd_titre_id as titre, m.cd_section_id as sec, m.cd_chapitre_id as chap,
				m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.type_procedure as proc, m.type_beneficiaire_id as typeb,
				m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m, budg_bordereau_mandatement bb, budg_detail_bord_mandat i
				where bb.id = %d and i.budg_mandat_id = m.id and i.budg_bordereau_mandatement_id = bb.id and m.company_id = %d
				and m.state = 'O' """ %(id_bord, val_struct))
				
				rows = vals.env.cr.dictfetchall()
				result = []
				
				vals.mandat_ids.unlink()
				for line in rows:
					result.append((0,0, {'dt_etat' : line['dte'], 'no_lo': line['liq'], 'no_mandat': line['mdt'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
										'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
										'no_beneficiaire': line['benef'],'obj': line['obj'],'mnt_ord': line['mnt']}))
				self.mandat_ids = result

	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')
	
	def receptionner(self):

		for vals in self:
			bord = int(vals.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)
			val_id = int(self.id)

			self.date_recus = date.today()

			self.env.cr.execute("""UPDATE budg_bordereau_mandatement SET et_doss ='R', date_recus = %s WHERE id = %s and x_exercice_id = %s and
			company_id = %s""" ,(self.date_recus, bord, val_ex, val_struct))

			self.env.cr.execute("select bordmand from budg_compteur_bord_mand_a_viser where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("""INSERT INTO budg_compteur_bord_mand_a_viser(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("UPDATE budg_compteur_bord_mand_a_viser SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

			self.env.cr.execute(""" SELECT sum(mnt_ord) FROM budg_liste_mandatement e , budg_bordereau_mandatement_controle_a_viser b
					WHERE b.x_exercice_id = %d AND b.company_id = %d AND b.id = e.liste_id AND e.id = %d""" % (val_ex, val_struct, val_id))
			res = self.env.cr.fetchone()
			resu = res and res[0] or 0
			self.totaux = resu


			self.afficher()

			self.write({'et_doss': 'R'})
	
	def envoyer(self):

		self.date_emis = date.today()
		
		self.write({'et_doss': 'E'})

	
class BudgListeMdt(models.Model):
	_name = "budg_liste_mandatement"
	
	liste_id = fields.Many2one("budg_bordereau_mandatement_controle_a_viser", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one('budg_typeprocedure',string="Type de procédure", readonly= True)
	no_eng = fields.Char(string="N° engagement", readonly= True)
	no_mandat = fields.Many2one("budg_mandat",string="N° Mandat",readonly=True)
	no_lo = fields.Many2one("budg_liqord", string="Liquidation", readonly= True)
	mnt_ord = fields.Integer(string="Montant", readonly= True)
	piecejust_ids = fields.One2many("budg_liste_piece_mdt",'mdt_id')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date mandat", readonly = True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Char( string ="Bénéficiaire", readonly= True)
	obj = fields.Text(string="Objet", readonly= True)
	envoyer = fields.Selection([('Y','Oui'),('N','Non')], string="Envoyé ?", default='Y')
	modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
	commentaire = fields.Text("Commentaire")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([
        ('N', 'Nouveau'),
		('V', 'Visé par CG'),
		('R', 'Rejété par CG'),
        ], 'Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def viser(self):
		
		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_strcut = int(self.company_id)
		for vals in self:
			if self.envoyer == 'Y':
				self.env.cr.execute("""UPDATE budg_mandat SET state ='V', envoyer_daf = 'Y' WHERE id = %d and company_id = %d """ %(mdt, val_strcut))
		
			self.write({'state': 'V'})
	
	def rejeter(self):
		
		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_strcut = int(self.company_id)
		motif = self.motif_rejet
		commentaire = self.commentaire
		
		self.env.cr.execute("""UPDATE budg_mandat SET state ='R', motif_rejet = %s, commentaire = %s WHERE id = %s and company_id = %s""",(motif,commentaire, mdt, val_strcut ))
		
		self.write({'state': 'R'})

	def afficher_piece(self):

		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute(
				"select lb_long as lib, oblige as obl, ref as re, montant as mnt, nombre as nbr from budg_piece_ord where mandat_id = %d and company_id = %d" % (
				mdt, val_struct))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'ref': line['re'], 'mnt': line['mnt'],
									  'nbr': line['nbr']}))
			self.piecejust_ids = result



class BudgListePieceMdt(models.Model):
	_name = "budg_liste_piece_mdt"

	mdt_id = fields.Many2one("budg_liste_mandatement", ondelete='cascade')
	lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
	oblige = fields.Boolean("Obligatoire ?", readonly=True)
	ref = fields.Char("Référence", readonly=True)
	nbr = fields.Integer("Nombre", readonly=True)
	mnt = fields.Integer("Montant", readonly=True)


#Renvoi bordereau de mandat DAF / DFC
class BudgBordMdtRenvoiDaf(models.Model):
	_name = "budg_bordereau_mandatement_renvoi_daf"
	_rec_name = "no_bord_mandat"
	_order = " id desc"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau',default="Bordereau de Transmission de Mandat pour DAF/DFC", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default="CG",readonly=True)
	date_emis = fields.Date(string="Date d'émission", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	bord_recu = fields.Many2one("budg_bordereau_mandatement_controle_a_viser", required=True, domain=[('et_doss','=','R')])
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur",  default="DAF/DFC", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_liste_mandatement_renvoi", "liste_id")
	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Envoyé à la DAF/DFC'),
		('R', 'Receptionné par DAF/DFC'),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		
		if self.bord_recu:
		
			for vals in self:
				vals.env.cr.execute("""select m.dt_etat as dte,m.no_lo as liq, m.no_mandat as mdt, m.cd_titre_id as titre, m.cd_section_id as sec, m.cd_chapitre_id as chap,
				m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.type_procedure as proc, m.type_beneficiaire_id as typeb,
				m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_liste_mandatement m
				where  m.liste_id = %d and m.company_id = %d
				and m.x_exercice_id = %d and m.state = 'V' and m.envoyer = 'Y' """ %(id_bord, val_struct, val_ex))
				
				rows = vals.env.cr.dictfetchall()
				result = []
				
				vals.mandat_ids.unlink()
				for line in rows:
					result.append((0,0, {'dt_etat' : line['dte'], 'no_lo': line['liq'], 'no_mandat': line['mdt'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
										'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
										'no_beneficiaire': line['benef'],'obj': line['obj'],'mnt_ord': line['mnt']}))
				self.mandat_ids = result
	
	def envoyer(self):

		for vals in self:
			bord = int(vals.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			self.env.cr.execute("""UPDATE budg_bordereau_mandatement_controle_a_viser SET et_doss ='E' WHERE id = %d and x_exercice_id = %d and
			company_id = %d""" %(bord, val_ex, val_struct))

			self.env.cr.execute("select bordmand from budg_compteur_bord_mand_daf where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("""INSERT INTO budg_compteur_bord_mand_daf(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("UPDATE budg_compteur_bord_mand_daf SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

			#self.afficher()

			self.write({'et_doss': 'E'})
	

	
class BudgListeMdtRenvoi(models.Model):
	_name = "budg_liste_mandatement_renvoi"
	
	liste_id = fields.Many2one("budg_bordereau_mandatement_renvoi_daf", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one('budg_typeprocedure',string="Type de procédure", readonly= True)
	no_eng = fields.Char(string="N° engagement", readonly= True)
	no_mandat = fields.Many2one("budg_mandat",string="N° Mandat",readonly=True)
	no_lo = fields.Many2one("budg_liqord", string="Liquidation", readonly= True)
	mnt_ord = fields.Integer(string="Montant", readonly= True)
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date mandat", readonly = True)
	type_beneficiaire_id = fields.Many2one("ref_typebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Char( string ="Bénéficiaire", readonly= True)
	obj = fields.Text(string="Objet", readonly= True)
	envoyer = fields.Selection([('Y','Oui'),('N','Non')], string="Envoyer ?", default='Y')
	modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
	motif_rejet = fields.Selection([('1','Erreur Montant'),('2','Erreur')],string="Motif rejet")
	#x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([
        ('N', 'Nouveau'),
		('V', 'Visé par CG'),
		('R', 'Rejété par CG'),
        ], 'Etat', default='V', index=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


#Reception bordereau envoyer par CG
class BudgBordMdtRecepDcmef(models.Model):
	_name = "budg_bordereau_mandatement_recep_dcmef"
	_rec_name = "no_bord_mandat"
	_order = " id desc"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau',default="Bordereau de Transmission de prise en charge", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default="DAF/DFC",readonly=True)
	date_emis = fields.Date(string="Date d'émission", readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	date_envoi = fields.Date("Date d'émission PeC", readonly=True)
	date_recep = fields.Date("Date réception pour PeC", readonly=True)
	num_accuse = fields.Char()
	bord_recu = fields.Many2one("budg_bordereau_mandatement_controle_a_viser", required=False)
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur",  default="DAF/DFC", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_liste_mandatement_recep", "liste_id")
	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('PC', 'Envoyé pour PeC'),
		('RP','Réceptionné pour PeC'),
		('TR', 'Traité')
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	signataire_2 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '2')]))
	total_gle = fields.Integer(string="Total gle", readonly=True)


	def MntPre(self):

		for val in self:

			val_id = int(val.id)
			val_ex = int(val.x_exercice_id)
			val_struct = int(val.company_id)

			val.env.cr.execute("""SELECT sum(mnt_ord) FROM budg_liste_mandatement_recep e,budg_bordereau_mandatement_recep_dcmef m
			WHERE e.envoyer = True AND m.company_id = %d AND e.liste_id = %d AND e.liste_id = m.id""" % (val_struct, val_id))
			res = val.env.cr.fetchone()
			resu = res and res[0] or 0
			val.totaux = resu

			val.env.cr.execute("""SELECT sum(totaux) FROM budg_bordereau_mandatement_recep_dcmef b	
			WHERE b.x_exercice_id = %d AND b.company_id = %d and b.id != %d and et_doss in ('PC','RP') """ % (val_ex, val_struct, val_id))
			res1 = val.env.cr.fetchone()
			val.total_prec = res1 and res1[0] or 0

			val.total_gle = val.totaux + val.total_prec

	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')


	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select m.dt_etat as dte, m.no_mandat as mdt, m.cd_titre_id as titre, m.no_lo as liq, m.cd_section_id as sec, m.cd_chapitre_id as chap,
			m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.type_beneficiaire_id as typeb,m.type_procedure as proc,
			m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m
			where m.company_id = %d and m.x_exercice_id = %d and m.state = 'O' and m.envoyer_daf = 'N' """ %(val_struct,val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_ids.unlink()
			for line in rows:
				result.append((0,0, {'dt_etat' : line['dte'], 'no_mandat': line['mdt'], 'no_lo': line['liq'], 'type_procedure': line['proc'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
									'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_beneficiaire_id': line['typeb'],
									'no_beneficiaire': line['benef'],'obj': line['obj'],'mnt_ord': line['mnt']}))
			self.mandat_ids = result

	def approuver(self):
		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		v_id = int(self.id)

		self.env.cr.execute("""SELECT l.* FROM budg_liste_mandatement_recep l, budg_bordereau_mandatement_recep_dcmef m where l.liste_id = m.id and m.id = %d and 
		 l.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

		for val in self.env.cr.dictfetchall():
			mdt = val['no_mandat']
			sec = val['cd_section_id']
			chap = val['cd_chapitre_id']
			art = val['cd_article_id']
			par = val['cd_paragraphe_id']
			rub = val['cd_rubrique_id']
			approuver = val['envoyer']

			if approuver == True:
				self.env.cr.execute("""UPDATE budg_mandat SET envoyer_daf = 'Y' WHERE id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_article_id = %s
				and cd_paragraphe_id = %s and cd_rubrique_id = %s and company_id = %s""" % (mdt, sec, chap, art, par, rub, struct))


	def envoyer(self):

		for vals in self:
			bord = int(vals.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			self.date_envoi = date.today()

			self.env.cr.execute(
				"select bordmand from budg_compteur_bord_mand_cf where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"""INSERT INTO budg_compteur_bord_mand_cf(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"UPDATE budg_compteur_bord_mand_cf SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

			self.MntPre()
			self.approuver()
			self.write({'et_doss': 'PC'})

	def receptionner(self):
		self.write({'et_doss': 'RP'})
		self.date_recep = date.today()

	def traiter(self):
		self.write({'et_doss': 'TR'})
	

	
class BudgListeMdtRecep(models.Model):
	_name = "budg_liste_mandatement_recep"
	
	liste_id = fields.Many2one("budg_bordereau_mandatement_recep_dcmef", ondelete='cascade',readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one('budg_typeprocedure',string="Type de procédure", readonly= True)
	no_eng = fields.Char(string="N° engagement", readonly= True)
	no_mandat = fields.Many2one("budg_mandat",string="N° Ordonnance",readonly=True)
	no_lo = fields.Many2one("budg_liqord", string="Liquidation", readonly= True)
	mnt_ord = fields.Integer(string="Montant", readonly= True)
	dt_etat = fields.Date(string="Date Ordonnance", readonly = True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string = "Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire", string ="Bénéficiaire", readonly= True)
	obj = fields.Text(string="Objet", readonly= True)
	envoyer = fields.Boolean("Envoyer ?",readonly=False)
	modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
	motif_rejet = fields.Selection([('1','Erreur Montant'),('2','Erreur')],string="Motif rejet",readonly=True)
	commentaire = fields.Text("Commentaire")
	x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice",readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id,readonly=True)
	state = fields.Selection([('N', 'Nouveau'), ('V', 'Visé'), ('R', 'Rejété'),],
							 string='Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	piece_ids = fields.One2many("budg_liste_piece_mdt_pc", "mdt_id")


	def PrendreEnCharge(self):

		mdt = int(self.no_mandat)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_mandat SET state ='I' WHERE id = %s and company_id = %s""",
							(mdt, val_struct))

		self.write({'state': 'V'})

	def rejeter(self):

		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		com = self.commentaire
		mo = self.motif_rejet
		if self.motif_rejet == False:
			raise ValidationError(_("Veuillez préciser le motif de rejet d'abord !"))
		else:
			self.env.cr.execute(
				"""UPDATE budg_mandat SET state ='J', motif_rejet = %s, commentaire = %s WHERE id = %s and company_id = %s""",
				(mo, com, mdt, val_struct))

			self.write({'state': 'R'})
			self.write({'etat': 'MR'})

	def afficher_piece(self):

		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute(
				"select lb_long as lib, oblige as obl, ref as re, montant as mnt, nombre as nbr from budg_piece_ord where mandat_id = %d" % (
					mdt))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piece_ids.unlink()
			for line in rows:
				result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'ref': line['re'], 'mnt': line['mnt'],
									  'nbr': line['nbr']}))
			self.piece_ids = result


class BudgListePieceMdtPc(models.Model):
	_name = "budg_liste_piece_mdt_pc"

	mdt_id = fields.Many2one("budg_liste_mandatement_recep", ondelete='cascade')
	lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
	oblige = fields.Boolean("Obligatoire ?", readonly=True)
	ref = fields.Char("Référence", readonly=True)
	nbr = fields.Integer("Nombre", readonly=True)
	mnt = fields.Integer("Montant", readonly=True)


class BudgBordMdtControleviser(models.Model):
	_name = "budg_bordereau_mandatement_controle_viser"
	_rec_name = "no_bord_mandat"
	_order = " id desc"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau',default="Bordereau de Reception Prise en Charge", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='DAF',  readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_mandatement_recep_dcmef",required=True,domain=[('et_doss','=','PC')])
	date_emis = fields.Date(string="Date d'émission", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception",default=fields.Date.context_today, readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_liste_mandatement_pc", "liste_id", string="Liste des mandats")

	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('T', 'Envoyé pour prise en charge'),
		('PC', 'Réceptionné pour prise en charge'),
        ], 'Etat', default='T', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def receptionner(self):
		for vals in self:
			bord = int(self.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			self.date_recus = date.today()

			self.env.cr.execute("""UPDATE budg_bordereau_mandatement_recep_dcmef SET et_doss ='RP', date_recep = %s  WHERE id = %s and x_exercice_id = %s and
			company_id = %s""" ,(self.date_recus, bord, val_ex, val_struct))


			vals.env.cr.execute("select bordmand from budg_compteur_bord_mand_viser where x_exercice_id = %d and company_id = %d" %(val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("""INSERT INTO budg_compteur_bord_mand_viser(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute("UPDATE budg_compteur_bord_mand_viser SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

		self.write({'et_doss': 'PC'})

		self.afficher()



	def afficher(self):
		
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		id_bord = int(self.bord_recu)
		
		for vals in self:
			vals.env.cr.execute("""select distinct m.no_mandat as mdt, m.dt_etat as dte,m.no_lo as liq, m.cd_titre_id as titre, m.cd_section_id as sec, m.cd_chapitre_id as chap,
			m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.type_procedure as proc, m.type_beneficiaire_id as typeb,
			m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_liste_mandatement_recep m
			where m.liste_id = %d and m.company_id = %d and m.envoyer = True """ %(id_bord,val_struct))
			
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_ids.unlink()


			for line in rows:
				result.append((0,0, {'dt_etat' : line['dte'], 'no_lo': line['liq'], 'no_mandat': line['mdt'], 'cd_titre_id': line['titre'], 'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],'cd_article_id': line['art'],
									'cd_paragraphe_id': line['par'],'cd_rubrique_id': line['rub'],'type_procedure': line['proc'],'type_beneficiaire_id': line['typeb'],
									'no_beneficiaire': line['benef'],'obj': line['obj'],'mnt_ord': line['mnt']}))
			self.mandat_ids = result



class BudgListeMdtPc(models.Model):
	_name = "budg_liste_mandatement_pc"
	
	liste_id = fields.Many2one("budg_bordereau_mandatement_controle_viser", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section",string = "Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string = "Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string = "Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string = "Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string = "Rubrique", readonly=True)
	type_procedure = fields.Many2one('budg_typeprocedure',string="Type de procédure", readonly=True)
	no_eng = fields.Char(string="N° engagement", readonly= True)
	no_mandat = fields.Many2one("budg_mandat",string="N° Ordonnance",readonly=True)
	no_lo = fields.Many2one("budg_liqord", string="Liquidation", readonly= True)
	mnt_ord = fields.Integer(string="Montant", readonly= True)
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date Ordonnance", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire",string="Identité", readonly=True)
	obj = fields.Text(string="Objet", readonly=True)
	etat = fields.Selection([('MR', 'Mise pour rejet'),('R', 'Réjeté')])
	modereg = fields.Many2one("ref_modereglement", 'Mode de règlement', readonly=True)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
	commentaire = fields.Text("Commentaire")
	piece_ids = fields.One2many("budg_liste_piece_mdt_pc", "mdt_id")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('N', 'Nouveau'), ('I', 'Pris en charge'), ('J', 'Rejéter')],
							 'Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")


	def PrendreEnCharge(self):
		
		mdt = int(self.no_mandat)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_mandat SET state ='I' WHERE id = %s and company_id = %s""" ,(mdt, val_struct))
		
		self.write({'state': 'I'})
	
	def rejeter(self):
		
		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		com = self.commentaire
		mo = self.motif_rejet
		if self.motif_rejet == False:
			raise ValidationError(_("Veuillez préciser le motif de rejet d'abord !"))
		else:
			self.env.cr.execute("""UPDATE budg_mandat SET state ='J', motif_rejet = %s, commentaire = %s WHERE id = %s and company_id = %s""" ,(mo, com, mdt, val_struct ))
		
			self.write({'state': 'J'})
			self.write({'etat': 'MR'})


	def afficher_piece(self):

		mdt = int(self.no_mandat)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("select lb_long as lib, oblige as obl, ref as re, montant as mnt, nombre as nbr from budg_piece_ord where mandat_id = %d" % (mdt))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piece_ids.unlink()
			for line in rows:
				result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'ref': line['re'], 'mnt': line['mnt'],
									  'nbr': line['nbr']}))
			self.piece_ids = result


class BudgListePieceMdtPc(models.Model):
	_name = "budg_liste_piece_mdt_pc"

	mdt_id = fields.Many2one("budg_liste_mandatement_pc", ondelete='cascade')
	lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
	oblige = fields.Boolean("Obligatoire ?", readonly=True)
	ref = fields.Char("Référence", readonly=True)
	nbr = fields.Integer("Nombre", readonly=True)
	mnt = fields.Integer("Montant", readonly=True)


class Budg_Compteur_bord_mandPc(models.Model):
	_name = "budg_compteur_bord_mand_pc"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)


class Budg_Compteur_bordMandAViser(models.Model):
	_name = "budg_compteur_bord_mand_a_viser"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)


class Budg_CompteurBordEngCtrl(models.Model):
	_name = "budg_compteur_bord_eng_ctrl"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class Budg_CompteurBordRecCtrl(models.Model):
	_name = "budg_compteur_bord_rec_ctrl"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class Budg_CompteurBordRecViser(models.Model):
	_name = "budg_compteur_bord_rec_viser"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)


class Budg_CompteurBordEngRecep(models.Model):
	_name = "budg_compteur_bord_eng_recep"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)

class Budg_CompteurBordEngRenvoi(models.Model):
	_name = "budg_compteur_bord_eng_renvoi"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)
	
class Budg_Compteur_bord_mandViser(models.Model):
	_name = "budg_compteur_bord_mand_viser"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)

class Budg_Compteur_bord_RecRenvoi(models.Model):
	_name = "budg_compteur_bord_rec_renvoi"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)

class Budg_Compteur_bordMandDaf(models.Model):
	_name = "budg_compteur_bord_mand_daf"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)
	
class Budg_Compteur_bordMandCf(models.Model):
	_name = "budg_compteur_bord_mand_cf"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)

class Budg_Compteur_bordMRecCf(models.Model):
	_name = "budg_compteur_bord_rec_cf"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)



class BudgApprobation(models.Model):
	_name = "budg_approbation"
	_rec_name = "eng_id"

	eng_id = fields.Many2one("budg_engagement", "N° Engagement", required=True,domain=[('state','=','N')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	#x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('N','Confirmé'),('V','Approuvé')], default='N', string="Etat", required=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	#Récuperer les elements de l'engagement choisi
	@api.onchange("eng_id")
	def Valeur(self):
		for vals in self:
			if vals.eng_id:
				self.titre_id = self.eng_id.cd_titre_id
				self.section_id = self.eng_id.cd_section_id
				self.chapitre_id = self.eng_id.cd_chapitre_id
				self.article_id = self.eng_id.cd_article_id
				self.para_id = self.eng_id.cd_paragraphe_id
				self.rub_id = self.eng_id.cd_rubrique_id
				self.mnt = self.eng_id.mnt_eng
				self.beneficiaire = self.eng_id.no_beneficiaire
				self.objet = self.eng_id.lb_obj
		
	
	#Permet de mettre l'engagement à l'etat V si procedure normale et W si simplifiée par le DFC
	def Approuver(self):

		for val in self:
			eng = int(val.eng_id)
			sec = int(val.section_id)
			chap = int(val.chapitre_id)
			art = int(val.article_id)
			par = int(val.para_id)
			rub = int(val.rub_id)
			no_ex = int(val.x_exercice_id)
			struct = int(val.company_id)

			if self.eng_id.type_procedure.type_procedure == '001':
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'V' WHERE id = %d  and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
				and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" %(eng, sec, chap, art, par, rub, struct, no_ex))
			else:
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'W' WHERE id = %d  and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
				and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (eng, sec, chap, art, par, rub, struct, no_ex))

			self.write({'state': 'V'})


class BudgCertification(models.Model):
	_name = "budg_certification_liq"
	_rec_name = "liq_id"

	liq_id = fields.Many2one("budg_liqord", "N° liquidation", required=True,domain=[('state','=','N')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Char("Bénéficiaire", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('N','Confirmé'),('L','Approuvé')],default='N', string="Etat", required=True)

	#Récuperer les elements de la liquidation choisie
	@api.onchange("liq_id")
	def Valeur(self):
		for vals in self:
			if vals.liq_id:
				self.titre_id = self.liq_id.cd_titre_id
				self.section_id = self.liq_id.cd_section_id
				self.chapitre_id = self.liq_id.cd_chapitre_id
				self.article_id = self.liq_id.cd_article_id
				self.para_id = self.liq_id.cd_paragraphe_id
				self.rub_id = self.liq_id.cd_rubrique_id
				self.mnt = self.liq_id.mnt_paye
				self.beneficiaire = self.liq_id.no_beneficiaire
				self.objet = self.liq_id.lb_obj

	def Certifier(self):

		for val in self:
			liq = int(val.liq_id)
			sec = int(val.section_id)
			chap = int(val.chapitre_id)
			art = int(val.article_id)
			par = int(val.para_id)
			rub = int(val.rub_id)
			no_ex = int(val.x_exercice_id)
			struct = int(val.company_id)

			self.env.cr.execute("""UPDATE budg_liqord SET state = 'L' WHERE id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
			and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
			liq, sec, chap, art, par, rub, struct, no_ex))

			self.action_liquidation_liquider()

			self.write({'state': 'L'})


	def action_liquidation_liquider(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_eng = self.liq_id.no_eng.no_eng
		mnt_paye = int(self.liq_id.mnt_paye)

		if self.liq_id.cd_type_accompte.cd_type_accompte == "AU":
			self.env.cr.execute("""UPDATE budg_engagement SET state = 'L', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))

			#self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()
		else:
			if self.liq_id.res_liq == 0 and self.liq_id.cd_type_accompte.cd_type_accompte != "AU":
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'L', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))
			elif self.liq_id.res_liq != 0 and self.liq_id.cd_type_accompte.cd_type_accompte != "AU":
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'LC', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))


			#self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()

	def dispo_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = int(self.liq_id)

		self.env.cr.execute("""select (sum(l.mnt_eng) - l.mnt_paye) FROM budg_liqord l, budg_engagement e
		WHERE e.id = %s and e.id = l.no_eng and l.company_id = %s and l.x_exercice_id = %s group by l.mnt_eng, l.mnt_paye""" , (v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		dispo = res and res[0] or 0

		self.env.cr.execute("""UPDATE budg_liqord SET dispo_engs = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",(dispo,v_eng, val_ex, val_struct))

	def total_liq_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = int(self.liq_id)

		self.env.cr.execute("""select sum(l.mnt_paye) FROM budg_liqord l, budg_engagement e WHERE e.id = l.no_eng and l.no_eng = %d and l.company_id = %d and l.x_exercice_id = %d group by l.mnt_paye""" % (v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		total_liq = res and res[0] or 0

		self.env.cr.execute("""UPDATE budg_liqord SET total_liq_engs = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",(total_liq, v_eng, val_ex, val_struct))
	
	
class BudgApproMdt(models.Model):
	_name = "budg_appro_mdt"
	_rec_name = "mdt_id"

	mdt_id = fields.Many2one("budg_mandat", "N° Mandat", required=True,domain=[('state','=','N')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	#x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('N','Confirmé'),('O','Ordonnancé')], default='N',strin= "Etat", required=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id


	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	#Récuperer les elements de lu mandat choisi
	@api.onchange("mdt_id")
	def Valeur(self):
		for vals in self:
			if vals.mdt_id:
				self.titre_id = self.mdt_id.cd_titre_id
				self.section_id = self.mdt_id.cd_section_id
				self.chapitre_id = self.mdt_id.cd_chapitre_id
				self.article_id = self.mdt_id.cd_article_id
				self.para_id = self.mdt_id.cd_paragraphe_id
				self.rub_id = self.mdt_id.cd_rubrique_id
				self.mnt = self.mdt_id.mnt_ord
				#self.beneficiaire = self.mdt_id.no_beneficiaire
				self.objet = self.mdt_id.obj

	def ApproMdt(self):

		for val in self:
			mdt = int(val.mdt_id)
			sec = int(val.section_id)
			chap = int(val.chapitre_id)
			art = int(val.article_id)
			par = int(val.para_id)
			rub = int(val.rub_id)
			no_ex = int(val.x_exercice_id)
			struct = int(val.company_id)

			val_ex = int(self.x_exercice_id)
			val_struct = int(self.company_id)
			val_eng = str(self.mdt_id.no_lo.no_eng.no_eng)
			val_lo = self.mdt_id.no_lo.no_lo

			val_titre = int(self.mdt_id.no_lo.no_eng.cd_titre_id)
			val_chap = int(self.mdt_id.no_lo.no_eng.cd_chapitre_id)
			val_sec = int(self.mdt_id.no_lo.no_eng.cd_section_id)
			val_art = int(self.mdt_id.no_lo.no_eng.cd_article_id)
			val_par = int(self.mdt_id.no_lo.no_eng.cd_paragraphe_id)

			val_rub = int(self.mdt_id.no_lo.no_eng.cd_rubrique_id)


			self.env.cr.execute("""UPDATE budg_mandat SET state = 'O' WHERE id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
			and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
			mdt, sec, chap, art, par, rub, struct, no_ex))

			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_mandate = (select sum(BM.mnt_ord) 
					FROM budg_ligne_exe_dep BE, budg_engagement E, budg_mandat BM WHERE E.no_eng = BM.no_eng AND BE.cd_titre_id = E.cd_titre_id 
					and BE.cd_section_id = E.cd_section_id and BE.cd_chapitre_id = E.cd_chapitre_id and BE.cd_art_id = E.cd_article_id and
					BE.cd_paragraphe_id = E.cd_paragraphe_id and BE.cd_rubrique_id = E.cd_rubrique_id and
					BE.cd_titre_id = %d and BE.cd_section_id = %d and BE.cd_chapitre_id = %d and BE.cd_art_id = %d and BE.cd_paragraphe_id = %d and 
					BE.cd_rubrique_id = %d and BE.x_exercice_id = %d and BE.company_id = %d) WHERE cd_titre_id = %d and 
					cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d and 
					cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (
			val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct, val_titre, val_sec, val_chap,
			val_art, val_par, val_rub, val_ex, val_struct))

			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET reste_mandat = (mnt_corrige - mnt_mandate) 
					WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d and cd_paragraphe_id = %d 
					and cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (
			val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct))

			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET taux = ((mnt_mandate * 100) / mnt_corrige)
					WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_art_id = %d 
					and cd_paragraphe_id = %d and cd_rubrique_id = %d and x_exercice_id = %d and company_id = %d""" % (
			val_titre, val_sec, val_chap, val_art, val_par, val_rub, val_ex, val_struct))

			self.write({'state': 'O'})


class BudgAnnulationEngagement(models.Model):
	_name = "budg_annulation_engagement"
	_rec_name = "eng_id"
	
	eng_id = fields.Many2one("budg_engagement", "N° Engagement",required=True,domain=['|','|',('state','=','R'),('state','=','V'),('state','=','N')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	#x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('V','Approuvé'),('A','Annulé')],default='V', string="Etat", required=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id


	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	#Récuperer les elements de l'engagement choisi
	@api.onchange("eng_id")
	def Valeur(self):
		for vals in self:
			if vals.eng_id:
				self.titre_id = self.eng_id.cd_titre_id
				self.section_id = self.eng_id.cd_section_id
				self.chapitre_id = self.eng_id.cd_chapitre_id
				self.article_id = self.eng_id.cd_article_id
				self.para_id = self.eng_id.cd_paragraphe_id
				self.rub_id = self.eng_id.cd_rubrique_id
				self.mnt = self.eng_id.mnt_eng
				self.beneficiaire = self.eng_id.no_beneficiaire
				self.objet = self.eng_id.lb_obj

	#Annulation Engagement et restauration du crédit
	def AnnulerEngagement(self):
		
		for val in self:
			eng = int(val.eng_id)
			tit = int(val.titre_id)
			sec = int(val.section_id)
			chap = int(val.chapitre_id)
			art = int(val.article_id)
			par = int(val.para_id)
			rub = int(val.rub_id)
			no_ex = int(val.x_exercice_id)
			struct = int(val.company_id)
			mnt = int(val.mnt)
		
			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_disponible = mnt_disponible + %d
			WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and 
			cd_art_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" %(mnt, tit, sec, chap, art, par, rub, struct, no_ex))

			
			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_engage = mnt_engage - %d
						WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and 
						cd_art_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
			mnt, tit, sec, chap, art, par, rub, struct, no_ex))

			self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET taux = (mnt_engage / mnt_corrige) * 100
									WHERE cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and 
									cd_art_id = %d and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" % (
				tit, sec, chap, art, par, rub, struct, no_ex))

			self.env.cr.execute("""UPDATE budg_engagement SET state = 'A' WHERE id = %d and x_exercice_id = %d and company_id = %d""" %(eng, no_ex, struct))
			
			self.write({'state': 'A'})
	

class BudgCorrectionEngagementApprobation(models.Model):
	_name = "budg_correction_engagement_approbation"
	_rec_name = "eng_id"

	eng_id = fields.Many2one("budg_engagement", "N° Engagement",required=True, domain=[('state', '=', 'V')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=False)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
	imput_benef = fields.Many2one("ref_souscompte",string="Imput benef")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('V', 'Approuvé'), ('C', 'Corrigé')], default='V', string="Etat", required=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id


	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	#Récuperer les elements de l'engagement choisi
	@api.onchange("eng_id")
	def Valeur(self):
		for vals in self:
			if vals.eng_id:
				self.titre_id = self.eng_id.cd_titre_id
				self.section_id = self.eng_id.cd_section_id
				self.chapitre_id = self.eng_id.cd_chapitre_id
				self.article_id = self.eng_id.cd_article_id
				self.para_id = self.eng_id.cd_paragraphe_id
				self.rub_id = self.eng_id.cd_rubrique_id
				self.mnt = self.eng_id.mnt_eng
				self.beneficiaire = self.eng_id.no_beneficiaire
				self.objet = self.eng_id.lb_obj
	
	#Correction de l'engagement
	def corriger(self):
		for val in self:
			benef = int(val.beneficiaire)
			obj = str(val.objet)
			print("---objet----")
			print(obj)
			eng = int(val.eng_id)
			no_ex = int(val.x_exercice_id)
			struct = int(val.company_id)

			
			if self.beneficiaire:
				self.imput_benef = self.beneficiaire.cpte_fournisseur.souscpte
				imput = int(self.imput_benef)
				print("---imput benef----")
				print(imput)
				cpte_benef = self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
				print("---cpte benef----")
				print(cpte_benef)

				self.env.cr.execute("""UPDATE budg_engagement SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""" ,(benef, imput, cpte_benef, eng, no_ex, struct))
				self.env.cr.execute("""UPDATE budg_liqord SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(benef, imput, cpte_benef, eng, no_ex, struct))
				self.env.cr.execute("""UPDATE budg_mandat SET no_beneficiaire = %s, imput_benef = %s, cpte_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(benef, imput, cpte_benef, eng, no_ex, struct))

				self.write({'state': 'C'})

			if self.objet:
				obj = str(val.objet)
				print("---objet ok maj----")
				print(obj)
				self.env.cr.execute("""UPDATE budg_engagement SET lb_obj = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""" ,(obj, eng, no_ex, struct))
				self.env.cr.execute("""UPDATE budg_liqord SET lb_obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(obj, eng, no_ex, struct))
				self.env.cr.execute("""UPDATE budg_mandat SET obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(obj, eng, no_ex, struct))

				self.write({'state': 'C'})
			else:
				raise ValidationError(_("Pas de données à corriger."))




class BudgApprobationGroupEng(models.Model):
	_name = 'budg_appro_group_eng'
	_rec_name = 'dte'
	
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True, string='Structure')
	dte = fields.Date("Date", default=fields.Date.context_today, readonly=True)
	appro_ids = fields.One2many("budg_appro_group_eng_line", "appro_id")
	state = fields.Selection([('A','A approuver'), ('V','Approuvés')], default='A', string="Etat")

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id


	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		val_struct = int(self.company_id)
		val_ex = int(self.x_exercice_id)

		
		for vals in self:
			vals.env.cr.execute(""" SELECT * from budg_engagement e where e.state = 'N' and e.company_id = %d and 
            e.x_exercice_id = %d order by no_eng desc""" %(val_struct, val_ex))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.appro_ids.unlink()
			for line in rows:
				result.append((0,0, {'eng_id': line['id'], 'titre_id': line['cd_titre_id'], 'section_id': line['cd_section_id'], 'chapitre_id': line['cd_chapitre_id'], 'article_id': line['cd_article_id'], 'para_id': line['cd_paragraphe_id'], 'rub_id': line['cd_rubrique_id'],
									'x_exercice_id': line['x_exercice_id'], 'company_id': line['company_id'], 'mnt': line['mnt_eng'], 'objet': line['lb_obj'], 'typeprocedure': line['type_procedure']}))
			self.appro_ids = result
	
	
	def approuver(self):

		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		v_id = int(self.id)

		self.env.cr.execute("""SELECT l.* FROM budg_appro_group_eng_line l, budg_appro_group_eng e WHERE l.appro_id = e.id and e.id = %d
		 and e.company_id = %d and l.x_exercice_id = %d""" %(v_id, struct,no_ex))

		for val in self.env.cr.dictfetchall():
			eng = val['eng_id']
			tit = val['titre_id']
			sec = val['section_id']
			chap = val['chapitre_id']
			art = val['article_id']
			par = val['para_id']
			rub = val['rub_id']
			procedure = val['typeprocedure']
			approuver = val['approuver']

			if approuver == True:

				if procedure == 1:
					self.env.cr.execute("""UPDATE budg_engagement SET state = 'V' WHERE id = %d and cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
					and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" %(eng, tit, sec, chap, art, par, rub, struct, no_ex))
					self.write({'state': 'V'})
				else:
					self.env.cr.execute("""UPDATE budg_engagement SET state = 'W', envoyer_daf = 'Y' WHERE id = %d and cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d
					and cd_paragraphe_id = %d and cd_rubrique_id = %d and company_id = %d and x_exercice_id = %d""" %(eng, tit, sec, chap, art, par, rub, struct, no_ex))
	
					self.write({'state': 'V'})
	


class BudgApprobationGroupLine(models.Model):
	_name = 'budg_appro_group_eng_line'
	
	appro_id = fields.Many2one("budg_appro_group_eng", ondelete='cascade')
	eng_id = fields.Many2one("budg_engagement", "N° Eng",readonly=True)
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Paragraphe", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	typeprocedure = fields.Many2one("budg_typeprocedure", "Type de procédure")
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", readonly=True, string="Exercice")
	company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.user.company_id.id)
	approuver = fields.Boolean("Approuver ?")


class BudgApprobationGroupMdt(models.Model):
	_name = 'budg_appro_group_mdt'
	_rec_name = 'dte'
	
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True, string='Structure')
	dte = fields.Date("Date", default=fields.Date.context_today,readonly=True)
	appro_ids = fields.One2many("budg_appro_group_mdt_line", "appro_id")
	state = fields.Selection([('A','A approuver'), ('V','Approuvés')], default='A', string="Etat")

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):
		
		val_struct = int(self.company_id)
		val_ex = int(self.x_exercice_id)
		
		for vals in self:
			vals.env.cr.execute(""" SELECT * from budg_mandat m
            where state = 'N' and m.company_id = %d and 
            m.x_exercice_id = %d""" %(val_struct, val_ex))
			rows = vals.env.cr.dictfetchall()
			result = []
            
			vals.appro_ids.unlink()
			for line in rows:
				result.append((0,0, {'mdt_id' : line['id'], 'titre_id': line['cd_titre_id'], 'section_id': line['cd_section_id'], 'chapitre_id': line['cd_chapitre_id'], 'article_id': line['cd_article_id'], 'para_id': line['cd_paragraphe_id'], 'rub_id': line['cd_rubrique_id'],
									'x_exercice_id': line['x_exercice_id'], 'company_id': line['company_id'], 'mnt': line['mnt_eng'], 'objet': line['obj']}))
			self.appro_ids = result
	
	
	def approuver(self):
		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		v_id = int(self.id)

		self.env.cr.execute("""SELECT l.* FROM budg_appro_group_mdt_line l, budg_appro_group_mdt m 
		where l.appro_id = m.id and m.id = %d and 
		 l.company_id = %d and l.x_exercice_id = %d""" %(v_id, struct, no_ex))

		for val in self.env.cr.dictfetchall():
			mdt = val['mdt_id']
			tit = val['titre_id']
			sec = val['section_id']
			chap = val['chapitre_id']
			art = val['article_id']
			par = val['para_id']
			rub = val['rub_id']
			approuver = val['approuver']
			
			if approuver == True:

				self.env.cr.execute("""UPDATE budg_mandat SET state = 'O' WHERE id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_article_id = %s
				and cd_paragraphe_id = %s and cd_rubrique_id = %s and company_id = %s""" % (mdt, sec, chap, art, par, rub, struct))
	
				self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET mnt_mandate = (select sum(BM.mnt_ord) 
						FROM budg_ligne_exe_dep BE, budg_engagement E, budg_mandat BM WHERE E.id = BM.no_eng AND BE.cd_titre_id = E.cd_titre_id 
						and BE.cd_section_id = E.cd_section_id and BE.cd_chapitre_id = E.cd_chapitre_id and BE.cd_art_id = E.cd_article_id and
						BE.cd_paragraphe_id = E.cd_paragraphe_id and BE.cd_rubrique_id = E.cd_rubrique_id and
						BE.cd_titre_id = %s and BE.cd_section_id = %s and BE.cd_chapitre_id = %s and BE.cd_art_id = %s and BE.cd_paragraphe_id = %s and 
						BE.cd_rubrique_id = %s and BE.x_exercice_id = %s and BE.company_id = %s) WHERE cd_titre_id = %s and 
						cd_section_id = %s and cd_chapitre_id = %s and cd_art_id = %s and cd_paragraphe_id = %s and 
						cd_rubrique_id = %s and x_exercice_id = %s and company_id = %s""" ,(tit, sec, chap, art, par, rub, no_ex, struct, tit, sec, chap,art, par, rub, no_ex, struct))
	
				self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET reste_mandat = (mnt_corrige - mnt_mandate) 
						WHERE cd_titre_id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_art_id = %s and cd_paragraphe_id = %s 
						and cd_rubrique_id = %s and x_exercice_id = %s and company_id = %s"""  ,(tit, sec, chap, art, par, rub, no_ex, struct))
	
				self.env.cr.execute("""UPDATE budg_ligne_exe_dep SET taux = ((mnt_mandate * 100) / mnt_corrige)
						WHERE cd_titre_id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_art_id = %s
						and cd_paragraphe_id = %s and cd_rubrique_id = %s and x_exercice_id = %s and company_id = %s""" ,(tit, sec, chap, art, par, rub, no_ex, struct))

		self.write({'state': 'V'})


class BudgApprobationGroupMdtLine(models.Model):
	_name = 'budg_appro_group_mdt_line'
	
	appro_id = fields.Many2one("budg_appro_group_mdt", ondelete='cascade')
	mdt_id = fields.Many2one("budg_mandat", "N° Ordonnance",readonly=True)
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Paragraphe", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", readonly=True, string="Exercice")
	company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.user.company_id.id)
	approuver = fields.Boolean("Approuver ?")



class BudgCertifLiq(models.Model):
	_name = 'budg_certif_group_liq'
	_rec_name = 'dte'
	
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True, string='Structure')
	dte = fields.Date("Date", default=fields.Date.context_today,readonly=True)
	certif_ids = fields.One2many("budg_certif_liq_line", "certif_id")
	
	
	def afficher(self):
		
		val_struct = int(self.company_id)
		val_ex = int(self.x_exercice_id)
		
		for vals in self:
			vals.env.cr.execute(""" SELECT * from budg_liqord l
            where l.state = 'N' and l.company_id = %d and 
            l.x_exercice_id = %d""" %(val_struct, val_ex))
			rows = vals.env.cr.dictfetchall()
			result = []
            
			vals.appro_ids.unlink()
			for line in rows:
				result.append((0,0, {'liq_id' : line['id'], 'titre_id': line['cd_titre_id'], 'section_id': line['cd_section_id'], 'cd_chapitre_id': line['chapitre_id'], 'article_id': line['cd_article_id'], 'para_id': line['cd_paragraphe_id'], 'rub_id': line['cd_rubrique_id'], 
									'x_exercice_id': line['x_exercice_id'], 'company_id': line['company_id'], 'mnt': line['mnt_eng'], 'objet': line['lb_obj']}))
			self.appro_ids = result
	
	
	def Certifier(self):

		v_id = int(self.id)
		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)

		self.env.cr.execute("""SELECT l.* FROM budg_certif_liq_line l, budg_certif_group_liq m where l.certif_id = m.id and m.id = %d and 
		l.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

		for val in self.env.cr.dictfetchall():
			liq = val['liq_id']
			tit = val['titre_id']
			sec = val['section_id']
			chap = val['chapitre_id']
			art = val['article_id']
			par = val['para_id']
			rub = val['rub_id']
			approuver = val['approuver']


			self.env.cr.execute("""UPDATE budg_liqord SET state = 'L' WHERE id = %s and cd_titre_id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_article_id = %s
			and cd_paragraphe_id = %s and cd_rubrique_id = %s and company_id = %s and x_exercice_id = %s""" % (
			liq, tit, sec, chap, art, par, rub, struct, no_ex))

			self.action_liquidation_liquider()

			self.write({'state': 'L'})


	def action_liquidation_liquider(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		val_eng = self.liq_id.no_eng.no_eng
		mnt_paye = int(self.liq_id.mnt_paye)

		#for x in self.certif_ids:

		if self.liq_id.cd_type_accompte.cd_type_accompte == "AU":
			self.env.cr.execute("""UPDATE budg_engagement SET state = 'L', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))

			#self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()
		else:
			if self.liq_id.res_liq == 0 and self.liq_id.cd_type_accompte.cd_type_accompte != "AU":
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'L', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))
			elif self.liq_id.res_liq != 0 and self.liq_id.cd_type_accompte.cd_type_accompte != "AU":
				self.env.cr.execute("""UPDATE budg_engagement SET state = 'LC', reste = mnt_eng - %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""" ,(mnt_paye, val_eng, val_ex, val_struct))


			#self.write({'state': 'L'})
			self.dispo_eng()
			self.total_liq_eng()

	def dispo_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = int(self.liq_id)

		self.env.cr.execute("""select (sum(l.mnt_eng) - l.mnt_paye) FROM budg_liqord l, budg_engagement e
		WHERE e.id = %s and e.id = l.no_eng and l.company_id = %s and l.x_exercice_id = %s group by l.mnt_eng, l.mnt_paye""" , (v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		dispo = res and res[0] or 0

		self.env.cr.execute("""UPDATE budg_liqord SET dispo_engs = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",(dispo,v_eng, val_ex, val_struct))

	def total_liq_eng(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		v_eng = int(self.liq_id)

		self.env.cr.execute("""select sum(l.mnt_paye) FROM budg_liqord l, budg_engagement e WHERE e.id = l.no_eng and l.no_eng = %d and l.company_id = %d and l.x_exercice_id = %d group by l.mnt_paye""" % (v_eng, val_struct, val_ex))
		res = self.env.cr.fetchone()
		total_liq = res and res[0] or 0

		self.env.cr.execute("""UPDATE budg_liqord SET total_liq_engs = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",(total_liq, v_eng, val_ex, val_struct))




class BudgCertifLiqLine(models.Model):
	_name = "budg_certif_liq_line"

	
	certif_id = fields.Many2one("budg_certif_group_liq", ondelete="cascade")
	liq_id = fields.Many2one("budg_liqord", "N° liquidation", readonly=True,domain=[('state','=','N')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Article", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Char("Bénéficiaire", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('N','Confirmé'),('L','Approuvé')],default='N', string="Etat", required=True)
	certifier = fields.Boolean("Certifier ?")


class BudgApprobationGroupRec(models.Model):
	_name = 'budg_appro_group_rec'
	_rec_name = 'dte'

	#x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,
								 string='Structure')
	dte = fields.Date("Date", default=fields.Date.context_today, readonly=True)
	appro_ids = fields.One2many("budg_appro_group_rec_line", "appro_id")
	state = fields.Selection([('A', 'A approuver'), ('V', 'Approuvés')], default='A', string="Etat")

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id


	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		val_struct = int(self.company_id)
		val_ex = int(self.x_exercice_id)

		for vals in self:
			vals.env.cr.execute(""" SELECT * from budg_titrerecette e
            where e.et_doss = 'N' and e.company_id = %d and 
            e.x_exercice_id = %d""" % (val_struct, val_ex))
			rows = vals.env.cr.dictfetchall()
			result = []

			vals.appro_ids.unlink()
			for line in rows:
				result.append((0, 0, {'rec_id': line['id'], 'titre_id': line['cd_titre_id'],
									  'section_id': line['cd_section_id'], 'chapitre_id': line['cd_chapitre_id'],
									  'article_id': line['cd_article_id'], 'para_id': line['cd_paragraphe_id'],
									  'rub_id': line['cd_rubrique_id'],
									  'x_exercice_id': line['x_exercice_id'], 'company_id': line['company_id'],
									  'mnt': line['mnt_rec'], 'objet': line['lb_objet'],
									  }))
			self.appro_ids = result

	def approuver(self):

		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		v_id = int(self.id)

		self.env.cr.execute("""SELECT l.* FROM budg_appro_group_rec_line l, budg_appro_group_rec e WHERE l.appro_id = e.id and e.id = %d
		 and e.company_id = %d and l.x_exercice_id = %d""" % (v_id, struct, no_ex))

		for val in self.env.cr.dictfetchall():
			rec = val['rec_id']
			tit = val['titre_id']
			sec = val['section_id']
			chap = val['chapitre_id']
			art = val['article_id']
			par = val['para_id']
			rub = val['rub_id']
			approuver = val['approuver']

			if approuver == True:

				self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss = 'V' WHERE id = %s and cd_titre_id = %s and cd_section_id = %s and cd_chapitre_id = %s and cd_article_id = %s
				and cd_paragraphe_id = %s and cd_rubrique_id = %s and company_id = %s and x_exercice_id = %s""",
									(rec, tit, sec, chap, art, par, rub, struct, no_ex))
				self.write({'state': 'V'})



class BudgApprobationGroupRecLine(models.Model):
	_name = 'budg_appro_group_rec_line'

	appro_id = fields.Many2one("budg_appro_group_rec", ondelete='cascade')
	rec_id = fields.Many2one("budg_titrerecette", "N° Titre", readonly=True)
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Paragraphe", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", readonly=True, string="Exercice")
	company_id = fields.Many2one('res.company', readonly=True, default=lambda self: self.env.user.company_id.id)
	approuver = fields.Boolean("Approuver ?")


class BudgBordRecCtrl(models.Model):
	_name = "budg_bordereau_titrerecette_controle"
	_rec_name = "no_bord_en"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Reception de titre de DAF/DFC",
								 readonly=True)
	cd_acteur = fields.Char(string="Acteur", default="CG", readonly=True)
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date()
	num_accuse = fields.Char()
	totaux = fields.Integer()
	bord_recu = fields.Many2one("budg_bord_titre_recette", "N° Bord. reçu", required=True,
								domain=[('et_doss', '=', 'EB')])
	cd_acteur_accuse = fields.Char(string="Acteur")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	recette_ids = fields.One2many("budg_liste_recette", "bord_id")
	state = fields.Selection([
		('N', 'Nouveau'),
		('R', 'Réceptionner bordereau'),
		('E', 'Envoyer à DAF/DFC'),
		('BR', 'Bordereau réceptionné par DAF/DFC'),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select b.dt_rec as dte, b.id as rec, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.cd_type_contribuable as typeb,
			b.contribuable_id as benef, b.lb_objet as obj, b.mnt_rec as mnt from budg_titrerecette b, budg_bord_titre_recette bb, budg_detail_bord_recette i
			where bb.id = %d and i.budg_titrerecette_id = b.id and i.budg_bord_titre_recette_id = bb.id and b.company_id = %d and b.x_exercice_id = %d and b.et_doss = 'V' """ % (
			id_bord, val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.recette_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_rec': line['rec'], 'cd_titre_id': line['titre'],
									  'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
									  'cd_article_id': line['art'],
									  'cd_paragraphe_id': line['par'], 'cd_rubrique_id': line['rub'],
									  'type_beneficiaire_id': line['typeb'],
									  'no_beneficiaire': line['benef'], 'lb_obj': line['obj'], 'mnt_rec': line['mnt']}))
			self.recette_ids = result

	def receptionner(self):

		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_bord_titre_recette SET et_doss ='RB' WHERE id = %d and x_exercice_id = %d and
		company_id = %d""" % (bord, val_ex, val_struct))

		self.env.cr.execute(
			"select bordeng from budg_compteur_bord_rec_ctrl where x_exercice_id = %d and company_id = %d" % (
			val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"""INSERT INTO budg_compteur_bord_rec_ctrl(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
				val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"UPDATE budg_compteur_bord_rec_ctrl SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
				vals, val_ex, val_struct))

		# self.afficher()

		self.write({'state': 'R'})

	def envoyer(self):

		self.write({'state': 'E'})


class BudgListeRecette(models.Model):
	_name = 'budg_liste_recette'

	bord_id = fields.Many2one('budg_bordereau_titrerecette_controle', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
	no_rec = fields.Many2one("budg_titrerecette", string="N° Titre Recette", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre', readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_typecontribuable", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_contribuable", readonly=True, string="Identité")
	lb_obj = fields.Text(string="Objet", size=300, readonly=True)
	mnt_rec = fields.Float(string="Montant titre", readonly=True)
	piecejust_ids = fields.One2many("budg_liste_piece_rec", 'rec_id', readonly=True)
	dt_visa_cf = fields.Date(string="Date Visa")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('V', 'Approuvé'),
		('W', 'Visé'),
		('R', 'Rejeté'),
	], default='V', string='Etat', index=True, readonly=True, track_visibility='always')
	credit_disponible = fields.Integer()
	envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def viser(self):

		for vals in self:

			rec = int(vals.no_rec)
			val_ex = int(vals.x_exercice_id)
			val_strcut = int(vals.company_id)
			if self.envoyer_daf == 'Y':
				self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss ='W' WHERE id = %d and company_id = %d and
				x_exercice_id = %d""" % (rec, val_strcut, val_ex))

			self.write({'state': 'W'})

	def rejeter(self):

		rec = int(self.no_rec)
		val_ex = int(self.x_exercice_id)
		val_strcut = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss ='R' WHERE id = %d and x_exercice_id = %d and
		company_id = %d""" % (rec, val_ex, val_strcut))

		self.write({'state': 'R'})

	def afficher_piece(self):

		rec = int(self.no_rec)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute(
				"select lb_long as lib, oblige as obl, ref as re, montant as mnt, nombre as nbr from budg_piece_recette where recette_id = %d and company_id = %d and x_exercice_id = %d" % (
				rec, val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.piecejust_ids.unlink()
			for line in rows:
				result.append((0, 0, {'lib': line['lib'], 'oblige': line['obl'], 'ref': line['re'], 'mnt': line['mnt'],
									  'nbr': line['nbr']}))
			self.piecejust_ids = result


class BudgListePieceRec(models.Model):
	_name = "budg_liste_piece_rec"

	rec_id = fields.Many2one("budg_liste_rec", ondelete='cascade')
	lib = fields.Many2one("ref_piece_justificatives", "Libellé", readonly=True)
	oblige = fields.Boolean("Obligatoire", readonly=True)
	ref = fields.Char("Référence", readonly=True)
	nbr = fields.Integer("Nombre", readonly=True)
	mnt = fields.Integer("Montant", readonly=True)


class BudgBordRecRenvoiDaf(models.Model):
	_name = "budg_bordereau_recette_renvoi_daf"
	_rec_name = "no_bord_en"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Transmission d'Engament pour DAF/DFC",
								 readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='CG', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_titrerecette_controle", "N° Bord.", required=True,
								domain=[('state', '=', 'R')])
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date()
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	cd_acteur_accuse = fields.Char(string="Acteur")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	recette_ids = fields.One2many("budg_liste_recette_renvoi", "bord_id", string="Liste des recettes")
	state = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Envoyé bordereau à DAF/DFC'),
		('R', 'Bordereau receptionné par DAF/DFC'),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.no_rec as rec, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_beneficiaire_id as typeb,
			b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_rec as mnt from budg_liste_recette b 
			where b.bord_id = %d and b.company_id = %d and b.state = 'W' """ % (id_bord, val_struct))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.recette_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_rec': line['rec'], 'cd_titre_id': line['titre'],
									  'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
									  'cd_article_id': line['art'],'cd_paragraphe_id': line['par'],
									  'cd_rubrique_id': line['rub'],'type_beneficiaire_id': line['typeb'],
									  'no_beneficiaire': line['benef'], 'lb_obj': line['obj'], 'mnt_rec': line['mnt']}))
			self.recette_ids = result

	def envoyer(self):

		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_bordereau_titrerecette_controle SET state ='BR' WHERE id = %d and x_exercice_id = %d and
		company_id = %d""" % (bord, val_ex, val_struct))

		self.env.cr.execute(
			"select bordeng from budg_compteur_bord_rec_renvoi where x_exercice_id = %d and company_id = %d" % (
			val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"""INSERT INTO budg_compteur_bord_rec_renvoi(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
				val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"UPDATE budg_compteur_bord_rec_renvoi SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
				vals, val_ex, val_struct))

		# self.afficher()

		self.write({'state': 'E'})


class BudgListeRecetteRenvoi(models.Model):
	_name = 'budg_liste_recette_renvoi'

	bord_id = fields.Many2one('budg_bordereau_recette_renvoi_daf', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
	no_rec = fields.Many2one("budg_titrerecette", string="N° Titre", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre', readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_typecontribuable", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_contribuable", readonly=True, string="Identité")
	lb_obj = fields.Text(string="Objet", size=300, readonly=True)
	mnt_rec = fields.Float(string="Montant recette", readonly=True)
	dt_visa_cf = fields.Date(string="Date Visa")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('V', 'Approuvé'),
		('W', 'Visé'),
		('R', 'Rejeté'),
	], default='W', string='Etat', index=True, readonly=True, track_visibility='always')
	envoyer = fields.Selection([('Y', 'Oui'), ('N', 'Non')], default="Y", string="Envoyé ?")
	credit_disponible = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


class BudgBordRecRecepDcmef(models.Model):
	_name = "budg_bordereau_recette_recep_dcmef"
	_rec_name = "no_bord_mandat"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de Transmisson de prise en charge",
								 readonly=True)
	cd_acteur = fields.Char(string="Acteur", default="CG", readonly=True)
	date_emis = fields.Date(string="Date d'émission", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	bord_recu = fields.Many2one("budg_bordereau_recette_renvoi_daf", required=True, domain=[('state', '=', 'E')])
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur", default="DAF/DFC", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	recette_ids = fields.One2many("budg_liste_titre_renv", "liste_id")
	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Envoyé par CG'),
		('R', 'Réceptionné'),
		('PC', 'Envoyé pour PC'),
		('RP', 'Réceptionné pour PC')
	], 'Etat', default='E', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		if self.bord_recu:

			for vals in self:
				vals.env.cr.execute("""select m.dt_etat as dte, m.no_rec as rec, m.cd_titre_id as titre, m.cd_section_id as sec, m.cd_chapitre_id as chap,
				m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.type_beneficiaire_id as typeb,
				m.no_beneficiaire as benef, m.lb_obj as obj, m.mnt_rec as mnt from budg_liste_recette_renvoi m
				where  m.bord_id = %d and m.company_id = %d and m.state = 'W' and m.envoyer = 'Y' """ % (id_bord, val_struct))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.recette_ids.unlink()
				for line in rows:
					result.append((0, 0, {'dt_etat': line['dte'], 'no_rec': line['rec'],
										  'cd_titre_id': line['titre'], 'cd_section_id': line['sec'],
										  'cd_chapitre_id': line['chap'], 'cd_article_id': line['art'],
										  'cd_paragraphe_id': line['par'], 'cd_rubrique_id': line['rub'],
										  'type_beneficiaire_id': line['typeb'],'no_beneficiaire': line['benef'],
										  'obj': line['obj'],'mnt_rec': line['mnt']}))
				self.recette_ids = result

	def receptionner(self):

		for vals in self:
			bord = int(vals.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			self.env.cr.execute("UPDATE budg_bordereau_recette_renvoi_daf SET state ='R' WHERE id = %d and x_exercice_id = %d and company_id = %d" % (bord, val_ex, val_struct))

			self.env.cr.execute(
				"select bordmand from budg_compteur_bord_rec_cf where x_exercice_id = %d and company_id = %d" % (
				val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"INSERT INTO budg_compteur_bord_rec_cf(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)" % (
					val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"UPDATE budg_compteur_bord_rec_cf SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (
					vals, val_ex, val_struct))

			self.afficher()

			self.write({'et_doss': 'R'})

	def envoyer(self):

		self.write({'et_doss': 'PC'})

class BudgListeTitreRenv(models.Model):
	_name = 'budg_liste_titre_renv'
	
	liste_id = fields.Many2one("budg_bordereau_recette_recep_dcmef", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	no_rec = fields.Many2one("budg_titrerecette", string="N° Recette", readonly=True)
	mnt_rec = fields.Integer(string="Montant", readonly=True)
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_typecontribuable", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_contribuable", "Identité", readonly=True)
	obj = fields.Text(string="Objet", readonly=True)
	envoyer = fields.Boolean("Envoyer ?")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([
		('N', 'Nouveau'),
		('V', 'Visé par CG'),
		('R', 'Rejété par CG'),
	], 'Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


class BudgBordRecetteControle(models.Model):
	_name = "budg_bordereau_recette_controle_viser"
	_rec_name = "no_bord_mandat"

	name = fields.Char()
	no_bord_mandat = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de Reception Prise en Charge", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_recette_recep_dcmef", required=True,
								domain=[('et_doss', '=', 'PC')])
	date_emis = fields.Date(string="Date d'émission", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de reception", default=fields.Date.context_today, readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	recette_ids = fields.One2many("budg_liste_recette_pc", "liste_id", string="Liste des titres")
	et_doss = fields.Selection([
		('N', 'Nouveau'),
		('T', 'Envoyé pour prise en charge'),
		('PC', 'Réceptionné pour prise en charge'),
	], 'Etat', default='T', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	#Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def receptionner(self):
		for vals in self:
			bord = int(self.bord_recu)
			val_ex = int(vals.x_exercice_id.id)
			val_struct = int(vals.company_id.id)

			self.env.cr.execute("""UPDATE budg_bordereau_recette_recep_dcmef SET et_doss ='RP' WHERE id = %d and x_exercice_id = %d and
			company_id = %d""" % (bord, val_ex, val_struct))

			vals.env.cr.execute(
				"select bordmand from budg_compteur_bord_rec_viser where x_exercice_id = %d and company_id = %d" % (
				val_ex, val_struct))
			bordmand = self.env.cr.fetchone()
			no_bord_mandat = bordmand and bordmand[0] or 0
			c1 = int(no_bord_mandat) + 1
			c = str(no_bord_mandat)
			print("la val eng", type(bordmand))
			if c == "0":
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"""INSERT INTO budg_compteur_bord_rec_viser(x_exercice_id,company_id,bordmand)  VALUES(%d, %d, %d)""" % (
					val_ex, val_struct, vals))
			else:
				c1 = int(no_bord_mandat) + 1
				c = str(no_bord_mandat)
				ok = str(c1).zfill(4)
				self.no_bord_mandat = ok
				vals = c1
				self.env.cr.execute(
					"UPDATE budg_compteur_bord_rec_viser SET bordmand = %d  WHERE x_exercice_id = %d and company_id = %d" % (
					vals, val_ex, val_struct))

			self.afficher()

			self.write({'et_doss': 'PC'})

	def envoyer(self):

		self.write({'et_doss': 'T'})

	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select distinct m.id as rec, m.dt_rec as dte, m.cd_titre_id as titre, m.cd_section_id as sec, m.cd_chapitre_id as chap,
			m.cd_article_id as art, m.cd_paragraphe_id as par, m.cd_rubrique_id as rub, m.cd_type_contribuable as typeb,
			m.contribuable_id as benef, m.lb_objet as obj, m.mnt_rec as mnt from budg_titrerecette m
			where m.company_id = %d and m.x_exercice_id = %d and m.et_doss = 'V' """ % (
			val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.recette_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_rec': line['rec'],
									  'cd_titre_id': line['titre'], 'cd_section_id': line['sec'],
									  'cd_chapitre_id': line['chap'], 'cd_article_id': line['art'],
									  'cd_paragraphe_id': line['par'], 'cd_rubrique_id': line['rub'],
									 'type_beneficiaire_id': line['typeb'],
									  'no_beneficiaire': line['benef'], 'obj': line['obj'], 'mnt_rec': line['mnt']}))
			self.recette_ids = result


class BudgListeRecPc(models.Model):
	_name = "budg_liste_recette_pc"

	liste_id = fields.Many2one("budg_bordereau_recette_controle_viser", ondelete='cascade')
	cd_titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	no_rec = fields.Many2one("budg_titrerecette", string="N° Titre", readonly=True)
	mnt_rec = fields.Integer(string="Montant", readonly=True)
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
	type_beneficiaire_id = fields.Many2one("ref_typecontribuable", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_contribuable", "Identité", readonly=True)
	obj = fields.Text(string="Objet", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([
		('N', 'Nouveau'),
		('I', 'Pris en charge'),
		('J', 'Rejéter'),
	], 'Etat', default='N', index=True, readonly=True, copy=False, track_visibility='always')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def PrendreEnCharge(self):
		mdt = int(self.no_rec)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss ='I' WHERE id = %d and company_id = %d and
		x_exercice_id = %d""" % (mdt, val_struct, val_ex))

		self.write({'state': 'I'})

	def rejeter(self):
		mdt = int(self.no_rec)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.env.cr.execute("""UPDATE budg_titrerecette SET et_doss ='J' WHERE id = %d and x_exercice_id = %d and
		company_id = %d""" % (mdt, val_ex, val_struct))

		self.write({'state': 'J'})


class BudgCompteurBordMandPc(models.Model):
	_name = "budg_compteur_bord_rec_pc"

	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordmand = fields.Integer(default=0)


class RefCategorieContribualbe(models.Model):
	_name = "ref_categoriecontribuable"

	sequence = fields.Integer(default=10)
	lb_court = fields.Char(string="Libellé court", size=25)
	name = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class RefCategorieBeneficiaire(models.Model):
	_name = "ref_categoriebeneficiaire"

	sequence = fields.Integer(default=10)
	lb_court = fields.Char(string="Libellé court", size=25)
	name = fields.Char(string="Libellé long", size=100, required=True)
	active = fields.Boolean('Actif', default=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class BudgViewTitre(models.Model):
	_name="view_titre"
	_auto=False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id,readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre', string="Titre", readonly=True)
	somtitre = fields.Float('', readonly=True)

	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'view_titre')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_titre AS (select company_id,x_exercice_id, budg_id,cd_titre_id,SUM(mnts_budgetise) as somtitre FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_titre_id)")


class BudgViewSection(models.Model):
	_name = "view_section"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
										default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
										string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre', string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	somsection = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'view_section')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_section AS (select company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,SUM(mnts_budgetise) as somsection FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_section_id,cd_titre_id)")


class BudgViewChapitre(models.Model):
	_name = "view_chapitre"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	somchapitre = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'view_chapitre')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_chapitre AS (select company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,SUM(mnts_budgetise) as somchapitre FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id)")


class BudgViewArticle(models.Model):
	_name = "view_article"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	somarticle = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'view_article')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_article AS (select company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id,SUM(mnts_budgetise) as somarticle FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id)")


class BudgViewParagraphe(models.Model):
	_name = "view_paragraphe"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	sompara = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'view_paragraphe')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_paragraphe AS (select company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id,SUM(mnts_budgetise) as sompara FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id)")


class BudgViewRubrique(models.Model):
	_name = "view_rubrique"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one('budg_rubrique', string="Rubrique", readonly=True)
	somrub = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'view_rubrique')

		self.env.cr.execute("CREATE OR REPLACE VIEW view_rubrique AS (select company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id,cd_rubrique_id,SUM(mnts_budgetise) as somrub FROM budg_ligne_budgetaire GROUP by  company_id,x_exercice_id, budg_id,cd_titre_id,cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id,cd_rubrique_id)")

		

class Test(models.Model):
	_name = "test"
	
	budg_id = fields.Many2one("budg_budget", required=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	
	def get_report_values(self):
		
		budg_id = int(self.budg_id)
		print("budget",budg_id)
		company_id = int(self.company_id)
		print("struct",company_id)
		x_exercice_id = int(self.x_exercice_id)
		print("exercice",x_exercice_id)
	
		doctitre = []
		
		
	
		self.env.cr.execute("SELECT cd_titre_id, somtitre FROM view_titre WHERE budg_id = %d and company_id = %d and x_exercice_id = %d" %(budg_id, company_id, x_exercice_id))
		for line in self.env.cr.dictfetchall():
			
			v_titre = line['cd_titre_id']
			print("titr",v_titre)
			v_mnttit = line['somtitre']
			print("mnttit",v_mnttit)
			
			
			#Boucle 2
			docsection=[]
			self.env.cr.execute("""SELECT cd_titre_id, cd_section_id,somsection
			FROM view_section WHERE budg_id = %d and cd_titre_id = %d and company_id = %d and x_exercice_id = %d""" %(budg_id,v_titre, company_id, x_exercice_id))
			for line in self.env.cr.dictfetchall():
				
				v_section = line['cd_section_id']
				print("sect",v_section)
				v_mntsec = line['somsection']
				print("mntsec",v_mntsec)
				
				
			
				#Boucle 3
				docchapitre=[]
				self.env.cr.execute("""SELECT cd_titre_id, cd_section_id,cd_chapitre_id,somchapitre
				FROM view_chapitre WHERE cd_titre_id = %d and cd_section_id = %d and budg_id = %d and company_id = %d and x_exercice_id = %d""" %(v_titre, v_section,budg_id, company_id, x_exercice_id))
				for line in self.env.cr.dictfetchall():
				
					v_chapitre = line['cd_chapitre_id']
					print("chap",v_chapitre)
					v_mntchap = line['somchapitre']
					print("mntchap",v_mntchap)
					
					
					
					#Boucle 3
					docarticle=[]
					self.env.cr.execute("""SELECT cd_titre_id, cd_section_id,cd_chapitre_id,cd_article_id,somarticle
					FROM view_article WHERE budg_id = %d and cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and company_id = %d and x_exercice_id = %d""" %(budg_id,v_titre, v_section, v_chapitre, company_id, x_exercice_id))
					for line in self.env.cr.dictfetchall():
				
						v_article = line['cd_article_id']
						print("art",v_article)
						v_mntart = line['somarticle']
						print("mntart",v_mntart)
						
						
						
						#Boucle 4
						docparagraphe=[]
						self.env.cr.execute("""SELECT cd_titre_id, cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id,sompara
						FROM view_paragraphe WHERE budg_id = %d and cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d and company_id = %d and x_exercice_id = %d""" %(budg_id,v_titre, v_section, v_chapitre, v_article, company_id, x_exercice_id))
						for line in self.env.cr.dictfetchall():
				
							v_paragraphe = line['cd_paragraphe_id']
							print("par",v_paragraphe)
							v_mntpar = line['sompara']
							print("mntpar",v_mntpar)
							
							#eparagraphe = {v_paragraphe : v_mntpar}
							#docparagraphe.append(eparagraphe)
							docrubrique=[]							
							self.env.cr.execute("""SELECT cd_titre_id, cd_section_id,cd_chapitre_id,cd_article_id,cd_paragraphe_id,cd_rubrique_id,somrub
							FROM view_rubrique WHERE budg_id = %d and cd_titre_id = %d and cd_section_id = %d and cd_chapitre_id = %d and cd_article_id = %d and cd_paragraphe_id = %d and company_id = %d and x_exercice_id = %d """ %(budg_id, v_titre, v_section, v_chapitre, v_article, v_paragraphe,company_id, x_exercice_id))
							for rubs in self.env.cr.dictfetchall():
							
							
								v_rubrique =  rubs['cd_rubrique_id']
								print("rubrique",v_rubrique)
								v_mntrub = rubs['somrub']
								print("mntrub",v_mntrub)
								erubri= {v_rubrique : v_mntrub}
								docrubrique.append(erubri)
							
							eparagraphe = {v_paragraphe : v_mntpar,'rubrique':docrubrique}
							docparagraphe.append(eparagraphe)
							
						earticle={v_article : v_mntart, "paragraphe":docparagraphe}
						docarticle.append(earticle)
					
					echapitre = {v_chapitre : v_mntchap, "article": docarticle}
					docchapitre.append(echapitre)
					
				esection = {v_section : v_mntsec, "chapitre": docchapitre}
				docsection.append(esection)
				
			etitre = {v_titre : v_mnttit, "section": docsection}
			doctitre.append(etitre)
			
		
		
		for x in doctitre:
			
			for y,z in x.items():
				print("resultat",(y,z))
			
		return doctitre



class VueTitre(models.Model):
	_name="vue_titre"
	_auto=False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id,readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	somtitre=fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_titre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_titre AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre, rt.lb_long, SUM(l.mnts_budgetise) as somtitre, SUM(l.mnts_ant1) as an1,SUM(l.mnts_ant1exe) as an1exe, SUM(l.mnts_ant2) as an2,SUM(l.mnts_ant2exe) as an2exe, SUM(l.mnts_precedent) as prec, SUM(l.mnts_precedentexe) as precexe
		FROM budg_ligne_budgetaire l, budg_titre bt, ref_titre rt WHERE bt.id = l.cd_titre_id and rt.id = bt.titre GROUP by company_id,x_exercice_id, budg_id,rt.cd_titre, rt.lb_long
		order by rt.cd_titre)""")




class VueSection(models.Model):
	_name = "vue_section"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
										default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
										string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	somsection = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_section')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_section AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section, rs.lb_long, SUM(l.mnts_budgetise) as somsection, SUM(l.mnts_ant1) as an1, SUM(l.mnts_ant1exe) as an1exe, 
		SUM(l.mnts_ant2) as an2, SUM(l.mnts_ant2exe) as an2exe, SUM(l.mnts_precedent) as prec, SUM(l.mnts_precedentexe) as precexe FROM budg_ligne_budgetaire l, budg_titre bt, ref_titre rt, budg_section bs, ref_section rs 
		WHERE bt.id = l.cd_titre_id and rt.id = bt.titre and bs.id = l.cd_section_id and rs.id = bs.section GROUP by company_id,x_exercice_id, budg_id,rt.cd_titre,rs.cd_section, rs.lb_long
		order by rt.cd_titre,rs.cd_section)""")


class VueChapitre(models.Model):
	_name = "vue_chapitre"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	somchapitre = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_chapitre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_chapitre AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre, rc.lb_long, SUM(l.mnts_budgetise) as somchapitre, cast(coalesce(SUM(l.mnts_ant1),0) as int) as an1,cast(coalesce(SUM(l.mnts_ant1exe),0) as int) as an1exe,
		cast(coalesce(SUM(l.mnts_ant2),0) as int) as an2, cast(coalesce(SUM(l.mnts_ant2exe),0) as int) as an2exe, cast(coalesce(SUM(l.mnts_precedent),0) as int) as prec,cast(coalesce(SUM(l.mnts_precedentexe),0) as int) as precexe
		FROM budg_ligne_budgetaire l, budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc 
		WHERE bt.id = l.cd_titre_id and rt.id = bt.titre and bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre GROUP by company_id,x_exercice_id, budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre, rc.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre)""")


class VueArticle(models.Model):
	_name = "vue_article"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	somarticle = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_article')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_article AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long, SUM(l.mnts_budgetise) as somarticle, SUM(l.mnts_ant1) as an1,SUM(l.mnts_ant1exe) as an1exe, SUM(l.mnts_ant2) as an2 , SUM(l.mnts_ant2exe) as an2exe, SUM(l.mnts_precedent) as prec, SUM(l.mnts_precedentexe) as precexe
		FROM budg_ligne_budgetaire l, budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra 
		WHERE bt.id = l.cd_titre_id and rt.id = bt.titre and bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_article_id and ra.id = ba.article GROUP by company_id,x_exercice_id, budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article)""")


class VueParagraphe(models.Model):
	_name = "vue_paragraphe"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	sompara = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_paragraphe')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_paragraphe AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long, SUM(l.mnts_budgetise) as somparagraphe, SUM(l.mnts_ant1) as an1,SUM(l.mnts_ant1exe) as an1exe, SUM(l.mnts_ant2) as an2,SUM(l.mnts_ant2exe) as an2exe, SUM(l.mnts_precedent) as prec,SUM(l.mnts_precedentexe) as precexe
		FROM budg_ligne_budgetaire l, budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp 
		WHERE bt.id = l.cd_titre_id and rt.id = bt.titre and bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_article_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe GROUP by company_id,x_exercice_id, budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe )""")


class VueRubrique(models.Model):
	_name = "vue_rubrique"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one('budg_rubrique', string="Rubrique", readonly=True)
	somrub = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_rubrique')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rubrique AS 
		(select l.company_id,l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long,SUM(l.mnts_budgetise) as somrubrique, SUM(l.mnts_ant1) as an1,SUM(l.mnts_ant1exe) as an1exe, SUM(l.mnts_ant2) as an2, SUM(l.mnts_ant2exe) as an2exe, SUM(l.mnts_precedent) as prec, SUM(l.mnts_precedentexe) as precexe
		FROM budg_ligne_budgetaire l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp, budg_rubrique br 
		WHERE bt.id = l.cd_titre_id and rt.id = bt.titre and bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_article_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe and br.id = l.cd_rubrique_id GROUP by l.company_id,
		l.x_exercice_id, l.budg_id,rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique)""")

	
class BudgEditionBudget(models.Model):
	_name = "budg_edition_budget"
	_rec_name = "budg_id"
	
	budg_id = fields.Many2one("budg_budget", "Budget", required=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=False, required=True, string="Structure")
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	def get_report_values(self):
		
		budg_id = int(self.budg_id)
		print("budget",budg_id)
		company_id = int(self.company_id)
		print("struct",company_id)
		x_exercice_id = int(self.x_exercice_id)
		print("exercice",x_exercice_id)
	
		
		doctitre = []
		self.env.cr.execute("SELECT cd_titre, lb_long, somtitre, an1, an1exe, an2, an2exe, prec, precexe FROM vue_titre WHERE budg_id = %d and company_id = %d and x_exercice_id = %d" %(budg_id, company_id, x_exercice_id))
		for line in self.env.cr.dictfetchall():
			
			v_titre = line['cd_titre']
			print("titr",v_titre)
			v_mnttit = int(line['somtitre'])
			print("mnttit",v_mnttit)
			v_mnttitan1 = line['an1']
			v_mnttitan1exe = line['an1exe']
			v_mnttitan2 = line['an2']
			v_mnttitan2exe = line['an2exe']
			v_mnttitprec = line['prec']
			v_mnttitprecexe = line['precexe']
			libtitre = line['lb_long']
			print("libelle",libtitre)


			#Boucle 2
			docsection=[]
			self.env.cr.execute("""SELECT cd_titre, cd_section, lb_long, somsection, an1, an1exe, an2, an2exe, prec, precexe 
			FROM vue_section WHERE budg_id = %s and cd_titre = '%s' and company_id = %s and x_exercice_id = %s""" %(budg_id,v_titre, company_id, x_exercice_id))
			for line in self.env.cr.dictfetchall():

				v_section = line['cd_section']
				print("sect",v_section)
				v_mntsec = int(line['somsection'])
				print("mntsec",v_mntsec)
				v_mntsecan1 = line['an1']
				v_mntsecan1exe = line['an1exe']
				v_mntsecan2 = line['an2']
				v_mntsecan2exe = line['an2exe']
				v_mntsecprec = line['prec']
				v_mntsecprecexe = line['precexe']
				print("mntpar",v_mntsecprec)
				libsec = line['lb_long']
				print("libelle",libsec)



				#Boucle 3
				docchapitre=[]
				self.env.cr.execute("""SELECT cd_titre, cd_section,cd_chapitre, lb_long, somchapitre, an1, an1exe, an2, an2exe, prec, precexe 
				FROM vue_chapitre WHERE cd_titre = '%s' and cd_section = '%s' and budg_id = %s and company_id = %s and x_exercice_id = %s""" %(v_titre, v_section,budg_id, company_id, x_exercice_id))
				for line in self.env.cr.dictfetchall():

					v_chapitre = line['cd_chapitre']
					print("chap",v_chapitre)
					v_mntchap = int(line['somchapitre'])
					print("mntchap",v_mntchap)
					v_mntchapan1 = line['an1']
					v_mntchapan1exe = line['an1exe']
					v_mntchapan2 = line['an2']
					v_mntchapan2exe = line['an2exe']
					v_mntchapprec = line['prec']
					v_mntchapprecexe = line['precexe']
					print("mntpar",v_mntchapprec)
					libchap = line['lb_long']
					print("libelle",libchap)



					#Boucle 3
					docarticle=[]
					self.env.cr.execute("""SELECT cd_titre, cd_section,cd_chapitre,cd_article, lb_long, somarticle, an1, an1exe, an2, an2exe, prec, precexe 
					FROM vue_article WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and company_id = %s and x_exercice_id = %s""" %(budg_id,v_titre, v_section, v_chapitre, company_id, x_exercice_id))
					for line in self.env.cr.dictfetchall():

						v_article = line['cd_article']
						print("art",v_article)
						v_mntart = int(line['somarticle'])
						print("mntart",v_mntart)
						v_mntartan1 = line['an1']
						v_mntartan1exe = line['an1exe']
						print("mntpar",v_mntartan1)
						v_mntartan2 = line['an2']
						v_mntartan2exe = line['an2exe']
						print("mntpar",v_mntartan2)
						v_mntartprec = line['prec']
						v_mntartprecexe = line['precexe']
						print("mntpar",v_mntartprec)
						libart = line['lb_long']
						print("libelle",libart)



						#Boucle 4
						docparagraphe=[]
						self.env.cr.execute("""SELECT cd_titre, cd_section,cd_chapitre,cd_article,cd_paragraphe, lb_long, somparagraphe, an1, an1exe, an2, an2exe, prec, precexe 
						FROM vue_paragraphe WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and company_id = %s and x_exercice_id = %s""" %(budg_id,v_titre, v_section, v_chapitre, v_article, company_id, x_exercice_id))
						for line in self.env.cr.dictfetchall():

							v_paragraphe = line['cd_paragraphe']
							print("par",v_paragraphe)
							v_mntpar = int(line['somparagraphe'])
							print("mntpar",v_mntpar)
							v_mntparan1 = line['an1']
							v_mntparan1exe = line['an1exe']
							print("mntpar",v_mntparan1)
							v_mntparan2 = line['an2']
							v_mntparan2exe = line['an2exe']
							print("mntpar2",v_mntparan2)
							v_mntparprec = line['prec']
							v_mntparprecexe = line['precexe']
							print("mntparprec",v_mntparprec)
							libpar = line['lb_long']
							print("libelle",libpar)

							docrubrique=[]
							self.env.cr.execute("""SELECT cd_titre, cd_section,cd_chapitre,cd_article,cd_paragraphe,rubrique, somrubrique, lb_long, an1, an1exe, an2, an2exe, prec, precexe 
							FROM vue_rubrique WHERE budg_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and cd_paragraphe = '%s' and company_id = %s and x_exercice_id = %s """ %(budg_id, v_titre, v_section, v_chapitre, v_article, v_paragraphe,company_id, x_exercice_id))
							for rubs in self.env.cr.dictfetchall():


								v_rubrique =  rubs['rubrique']
								print("rubrique",v_rubrique)
								v_mntrub = int(rubs['somrubrique'])
								print("mntrub",v_mntrub)
								v_ruban1 = rubs['an1']
								v_ruban1exe = rubs['an1exe']
								print("ruban1",v_ruban1)
								v_ruban2 = rubs['an2']
								v_ruban2exe = rubs['an2exe']
								print("ruban2",v_ruban2)
								v_rubprec = rubs['prec']
								v_rubprecexe = rubs['precexe']
								print("rubprec",v_rubprec)
								librub = rubs['lb_long']
								print("libelle",librub)

								erubri= {v_rubrique : [v_ruban1,v_ruban1exe,v_ruban2,v_ruban2exe, v_rubprec, v_rubprecexe, v_mntrub, librub] }
								docrubrique.append(erubri)

							eparagraphe = {v_paragraphe : [v_mntparan1,v_mntparan1exe,v_mntparan2,v_mntparan2exe,v_mntparprec,v_mntparprecexe,v_mntpar, libpar],'rubrique':docrubrique}
							docparagraphe.append(eparagraphe)

						earticle={v_article : [v_mntartan1,v_mntartan1exe,v_mntartan2,v_mntartan2exe,v_mntartprec,v_mntartprecexe,v_mntart, libart], "paragraphe":docparagraphe}
						docarticle.append(earticle)

					echapitre = {v_chapitre : [v_mntchapan1,v_mntchapan1exe,v_mntchapan2,v_mntchapan2exe,v_mntchapprec,v_mntchapprecexe,v_mntchap, libchap], "article": docarticle}
					docchapitre.append(echapitre)

				esection = {v_section : [v_mntsecan1,v_mntsecan1exe,v_mntsecan2,v_mntsecan2exe,v_mntsecprec,v_mntsecprecexe,v_mntsec, libsec], "chapitre": docchapitre}
				docsection.append(esection)
				
			etitre = {v_titre: [v_mnttitan1, v_mnttitan1exe, v_mnttitan2, v_mnttitan2exe, v_mnttitprec, v_mnttitprecexe, v_mnttit, libtitre], "section": docsection}
			doctitre.append(etitre)
			
		return doctitre


class VueDepSection(models.Model):
	_name = "vue_dep_section"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
										default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
										string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	somsection = fields.Float('',readonly=True)

	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_dep_section')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_dep_section AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section, rs.lb_long, 
		coalesce(SUM(l.mnt_budgetise),0) as budgetise, coalesce(SUM(l.mnt_corrige),0) as corrige, 
		coalesce(SUM(l.mnt_engage),0) as engagement, coalesce(SUM(l.mnt_mandate),0) as mandat, 
		coalesce(SUM(l.taux),0) as taux, coalesce(SUM(l.reste_mandat),0) as reste 
		FROM budg_ligne_exe_dep l, budg_section bs, ref_section rs WHERE bs.id = l.cd_section_id and rs.id = bs.section 
		GROUP by company_id,x_exercice_id,rs.cd_section, rs.lb_long order by rs.cd_section)""")


class VueDepChapitre(models.Model):
	_name = "vue_dep_chapitre"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	somchapitre = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_dep_chapitre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_dep_chapitre AS 
		(select l.company_id,l.x_exercice_id, rs.cd_section,rc.cd_chapitre, rc.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_engage),0) as int) as engagement, cast(coalesce(SUM(l.mnt_mandate),0) as int) as mandat, cast(coalesce(SUM(l.taux),0) as float) as taux, cast(coalesce(SUM(l.reste_mandat),0) as int) as reste
		FROM budg_ligne_exe_dep l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre GROUP by company_id,x_exercice_id,rs.cd_section,rc.cd_chapitre, rc.lb_long
		order by rs.cd_section,rc.cd_chapitre)""")


class VueDepArticle(models.Model):
	_name = "vue_dep_article"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	somarticle = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_dep_article')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_dep_article AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_engage),0) as int) as engagement, cast(coalesce(SUM(l.mnt_mandate),0) as int) as mandat, cast(coalesce(SUM(l.taux),0) as float) as taux, cast(coalesce(SUM(l.reste_mandat),0) as int) as reste
		FROM budg_ligne_exe_dep l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article GROUP by company_id,x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article)""")


class VueDepParagraphe(models.Model):
	_name = "vue_dep_paragraphe"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	sompara = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_dep_paragraphe')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_dep_paragraphe AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_engage),0) as int) as engagement, cast(coalesce(SUM(l.mnt_mandate),0) as int) as mandat, cast(coalesce(SUM(l.taux),0) as float) as taux, cast(coalesce(SUM(l.reste_mandat),0) as int) as reste
		FROM budg_ligne_exe_dep l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe GROUP by company_id,x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe )""")


class VueDepRubrique(models.Model):
	_name = "vue_dep_rubrique"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one('budg_rubrique', string="Rubrique", readonly=True)
	somrub = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_dep_rubrique')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_dep_rubrique AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long,cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_engage),0) as int) as engagement, cast(coalesce(SUM(l.mnt_mandate),0) as int) as mandat, cast(coalesce(SUM(l.taux),0) as float) as taux, cast(coalesce(SUM(l.reste_mandat),0) as int) as reste
		FROM budg_ligne_exe_dep l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp, budg_rubrique br 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe and br.id = l.cd_rubrique_id GROUP by l.company_id,
		l.x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique)""")





class VueRecSection(models.Model):
	_name = "vue_rec_section"
	_auto = False


	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
										default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
										string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	somsection = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_rec_section')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rec_section AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section, rs.lb_long, coalesce(SUM(l.mnt_budgetise),0) as budgetise, coalesce(SUM(l.mnt_corrige),0) as corrige, 
		coalesce(SUM(l.mnt_rec),0) as emis, coalesce(SUM(l.taux),0) as taux FROM budg_ligne_exe_rec l,  budg_section bs, ref_section rs 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section GROUP by company_id,x_exercice_id,rs.cd_section, rs.lb_long
		order by rs.cd_section)""")


class VueRecChapitre(models.Model):
	_name = "vue_rec_chapitre"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	somchapitre = fields.Float('',readonly=True)



	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_rec_chapitre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rec_chapitre AS 
		(select l.company_id,l.x_exercice_id, rs.cd_section,rc.cd_chapitre, rc.lb_long, SUM(l.mnt_budgetise) as budgetise, SUM(l.mnt_corrige) as corrige, 
		cast(coalesce(SUM(l.mnt_rec),0) as int) as emis, cast(coalesce(SUM(l.taux),0) as int) as taux
		FROM budg_ligne_exe_rec l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre GROUP by company_id,x_exercice_id,rs.cd_section,rc.cd_chapitre, rc.lb_long
		order by rs.cd_section,rc.cd_chapitre)""")


class VueRecArticle(models.Model):
	_name = "vue_rec_article"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	somarticle = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_rec_article')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rec_article AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_rec),0) as int) as emis, cast(coalesce(SUM(l.taux),0) as float) as taux
		FROM budg_ligne_exe_rec l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article GROUP by company_id,x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article, ra.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article)""")


class VueRecParagraphe(models.Model):
	_name = "vue_rec_paragraphe"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	sompara = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_rec_paragraphe')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rec_paragraphe AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_rec),0) as int) as emis, cast(coalesce(SUM(l.taux),0) as float) as taux
		FROM budg_ligne_exe_rec l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe GROUP by company_id,x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe )""")


class VueRecRubrique(models.Model):
	_name = "vue_rec_rubrique"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
									string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one('budg_rubrique', string="Rubrique", readonly=True)
	somrub = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_rec_rubrique')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_rec_rubrique AS 
		(select l.company_id,l.x_exercice_id,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long, cast(coalesce(SUM(l.mnt_budgetise),0) as int) as budgetise, cast(coalesce(SUM(l.mnt_corrige),0) as int) as corrige, 
		cast(coalesce(SUM(l.mnt_rec),0) as int) as emis, cast(coalesce(SUM(l.taux),0) as float) as taux
		FROM budg_ligne_exe_rec l, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra,budg_paragraphe bp, ref_paragraphe rp, budg_rubrique br 
		WHERE bs.id = l.cd_section_id and rs.id = bs.section and 
		bc.id = l.cd_chapitre_id and rc.id = bc.chapitre and ba.id = l.cd_art_id and ra.id = ba.article and
		bp.id = l.cd_paragraphe_id and rp.id = bp.paragraphe and br.id = l.cd_rubrique_id GROUP by l.company_id,
		l.x_exercice_id, rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long
		order by rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique)""")


class BudgEditionSituationDep(models.TransientModel):
	_name = "budg_edition_situation_dep"

	name = fields.Char("Situation exécutoire des dépenses", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,required=True, string="Structure")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=False, required=True)

	def get_report_values(self):

		company_id = int(self.company_id)
		print("struct", company_id)
		x_exercice_id = int(self.x_exercice_id)
		print("exercice", x_exercice_id)


		# Boucle 1
		docsection = []
		self.env.cr.execute("""SELECT cd_section, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(engagement,0) as engagement,
		coalesce(mandat,0) as mandat, taux, coalesce(reste,0) as reste FROM vue_dep_section WHERE company_id = %s and x_exercice_id = %s""" ,(company_id, x_exercice_id))

		for sec in self.env.cr.dictfetchall():
			v_section = sec['cd_section']

			budgetisesec = int(sec['budgetise'])

			corrigesec = int(sec['corrige'])

			engagementsec = int(sec['engagement'])

			mandatsec = int(sec['mandat'])

			restesec = int(sec['reste'])

			tauxsec = round(sec['taux'],2)

			libsec = sec['lb_long']


			# Boucle 2

			docchapitre = []
			self.env.cr.execute("""SELECT cd_section,cd_chapitre, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(engagement,0) as engagement, coalesce(mandat,0) as mandat,
			taux, coalesce(reste,0) as reste FROM vue_dep_chapitre WHERE cd_section = '%s' and company_id = %s and x_exercice_id = %s""" % (v_section, company_id, x_exercice_id))

			for chap in self.env.cr.dictfetchall():
				v_chapitre = chap['cd_chapitre']
				print("chap", v_chapitre)
				budgetisechap = int(chap['budgetise'])
				print("budgetise", budgetisechap)
				corrigechap = int(chap['corrige'])
				print("corrige", corrigechap)
				engagementchap = int(chap['engagement'])
				print("engagement", engagementchap)
				mandatchap = int(chap['mandat'])
				print("mandat", mandatchap)
				restechap = int(chap['reste'])
				print("reste", restechap)
				tauxchap = round(chap['taux'],2)
				print("taux", tauxchap)
				libchap = chap['lb_long']
				print("libelle", libchap)

				# Boucle 3
				docarticle = []
				self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(engagement,0) as engagement, 
				coalesce(mandat,0) as mandat, taux, coalesce(reste,0) as reste
				FROM vue_dep_article WHERE cd_section = '%s' and cd_chapitre = '%s' and company_id = %s and x_exercice_id = %s""" % (
				v_section, v_chapitre, company_id, x_exercice_id))

				for art in self.env.cr.dictfetchall():
					v_article = art['cd_article']
					print("art", v_article)
					budgetiseart = int(art['budgetise'])
					print("budgetise", budgetiseart)
					corrigeart = int(art['corrige'])
					print("corrige", corrigeart)
					engagementart = int(art['engagement'])
					print("engagement", engagementart)
					mandatart = int(art['mandat'])
					print("mandat", mandatart)
					resteart = int(art['reste'])
					print("reste", resteart)
					tauxart = round(art['taux'],2)
					print("taux", tauxart)
					libart = art['lb_long']
					print("libelle", libart)

					# Boucle 4
					docparagraphe = []
					self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article,cd_paragraphe, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(engagement,0) as engagement, 
					coalesce(mandat,0) as mandat, taux, coalesce(reste,0) as reste
					FROM vue_dep_paragraphe WHERE cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and company_id = %s and x_exercice_id = %s""" % (
					v_section, v_chapitre, v_article, company_id, x_exercice_id))

					for para in self.env.cr.dictfetchall():
						v_paragraphe = para['cd_paragraphe']
						print("par", v_paragraphe)
						budgetisepar = int(para['budgetise'])
						print("budgetise", budgetisepar)
						corrigepar = int(para['corrige'])
						print("corrige", corrigepar)
						engagementpar = int(para['engagement'])
						print("engagement", engagementpar)
						mandatpar = int(para['mandat'])
						print("mandat", mandatpar)
						restepar = int(para['reste'])
						print("reste", restepar)
						tauxpar = round(para['taux'],2)
						print("taux", tauxpar)
						libpar = para['lb_long']
						print("libelle", libpar)

						#Boucle 5
						docrubrique = []
						self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article,cd_paragraphe,rubrique, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(engagement,0) as engagement,
						coalesce(mandat,0) as mandat, taux, coalesce(reste,0) as reste FROM vue_dep_rubrique WHERE cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and cd_paragraphe = '%s' and company_id = %s and x_exercice_id = %s """% (
						v_section, v_chapitre, v_article, v_paragraphe, company_id, x_exercice_id))

						for rubs in self.env.cr.dictfetchall():
							v_rubrique = rubs['rubrique']
							print("rubrique", v_rubrique)
							budgetiserub = int(rubs['budgetise'])
							print("budgetise", budgetiserub)
							corrigerub = int(rubs['corrige'])
							print("corrige", corrigerub)
							engagementrub = int(rubs['engagement'])
							print("engagement", engagementrub)
							mandatrub = int(rubs['mandat'])
							print("mandat", mandatrub)
							resterub = int(rubs['reste'])
							print("reste", resterub)
							tauxrub = round(rubs['taux'],2)
							print("taux", tauxrub)
							librub = rubs['lb_long']
							print("libelle", librub)

							erubris = {v_rubrique: [librub, budgetiserub, corrigerub, engagementrub, mandatrub, tauxrub, resterub]}
							erubri = OrderedDict(sorted(erubris.items(), key=lambda t: t[0]))
							docrubrique.append(erubri)

						eparagraphes = {v_paragraphe: [libpar, budgetisepar, corrigepar, engagementpar, mandatpar, tauxpar, restepar], 'rubrique': docrubrique}
						eparagraphe = OrderedDict(sorted(eparagraphes.items(), key=lambda t: t[0]))
						docparagraphe.append(eparagraphe)

					earticles = {v_article: [libart, budgetiseart, corrigeart, engagementart, mandatart, tauxart, resteart], "paragraphe": docparagraphe}
					earticle = OrderedDict(sorted(earticles.items(), key=lambda t: t[0]))
					docarticle.append(earticle)

				echapitres = {v_chapitre: [libchap, budgetisechap, corrigechap, engagementchap, mandatchap, tauxchap, restechap], "article": docarticle}
				echapitre = OrderedDict(sorted(echapitres.items(), key=lambda t: t[0]))
				docchapitre.append(echapitre)

			esections = {v_section: [libsec, budgetisesec, corrigesec, engagementsec, mandatsec, tauxsec, restesec],"chapitre": docchapitre}
			esection = OrderedDict(sorted(esections.items(), key=lambda t: t[0]))
			docsection.append(esection)
			print("result", docsection)

		return docsection
	



class BudgEditionSituationRec(models.TransientModel):
	_name = "budg_edition_situation_rec"

	name = fields.Char("Situation exécutoire des recettes", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,required=True, string="Structure")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=False, required=True)

	def get_report_values(self):

		company_id = int(self.company_id)
		print("struct", company_id)
		x_exercice_id = int(self.x_exercice_id)
		print("exercice", x_exercice_id)


		# Boucle 1
		docsection = []
		self.env.cr.execute("""SELECT cd_section, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(emis,0) as emis, coalesce(taux,0) as taux
		FROM vue_rec_section WHERE company_id = %s and x_exercice_id = %s""" % (company_id, x_exercice_id))

		for sec in self.env.cr.dictfetchall():
			v_section = sec['cd_section']
			print("sect", v_section)
			budgetisesec = int(sec['budgetise'])
			print("budgetise", budgetisesec)
			corrigesec = int(sec['corrige'])
			print("corrige", corrigesec)
			emissec = int(sec['emis'])
			print("emis", emissec)			
			tauxsec = round(sec['taux'],2)
			print("taux", tauxsec)
			libsec = sec['lb_long']
			print("libelle", libsec)

			# Boucle 2
			docchapitre = []
			self.env.cr.execute("""SELECT cd_section,cd_chapitre, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(emis,0) as emis, coalesce(taux,0) as taux
			FROM vue_rec_chapitre WHERE cd_section = '%s' and company_id = %s and x_exercice_id = %s""" % (v_section, company_id, x_exercice_id))

			for chap in self.env.cr.dictfetchall():
				v_chapitre = chap['cd_chapitre']
				print("chap", v_chapitre)
				budgetisechap = int(chap['budgetise'])
				print("budgetise", budgetisechap)
				corrigechap = int(chap['corrige'])
				print("corrige", corrigechap)
				emischap = int(chap['emis'])
				print("emis", emischap)
				tauxchap = round(chap['taux'],2)
				print("taux", tauxchap)
				libchap = chap['lb_long']
				print("libelle", libchap)

				# Boucle 3
				docarticle = []
				self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(emis,0) as emis, coalesce(taux,0) as taux 
				FROM vue_rec_article WHERE cd_section = '%s' and cd_chapitre = '%s' and company_id = %s and x_exercice_id = %s""" % (
				v_section, v_chapitre, company_id, x_exercice_id))

				for art in self.env.cr.dictfetchall():
					v_article = art['cd_article']
					print("art", v_article)
					budgetiseart = int(art['budgetise'])
					print("budgetise", budgetiseart)
					corrigeart = int(art['corrige'])
					print("corrige", corrigeart)
					emisart = int(art['emis'])
					print("emis", emisart)		
					tauxart = round(art['taux'],2)
					print("taux", tauxart)
					libart = art['lb_long']
					print("libelle", libart)

					# Boucle 4
					docparagraphe = []
					self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article,cd_paragraphe, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(emis,0) as emis, coalesce(taux,0) as taux
					FROM vue_rec_paragraphe WHERE cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and company_id = %s and x_exercice_id = %s""" % (
					v_section, v_chapitre, v_article, company_id, x_exercice_id))

					for para in self.env.cr.dictfetchall():
						v_paragraphe = para['cd_paragraphe']
						print("par", v_paragraphe)
						budgetisepar = int(para['budgetise'])
						print("budgetise", budgetisepar)
						corrigepar = int(para['corrige'])
						print("corrige", corrigepar)
						emispar = int(para['emis'])
						print("emis", emispar)
						tauxpar = round(para['taux'],2)
						print("taux", tauxpar)
						libpar = para['lb_long']
						print("libelle", libpar)

						#Boucle 5
						docrubrique = []
						self.env.cr.execute("""SELECT cd_section,cd_chapitre,cd_article,cd_paragraphe,rubrique, lb_long, coalesce(budgetise,0) as budgetise, coalesce(corrige,0) as corrige, coalesce(emis,0) as emis, coalesce(taux,0) as taux
						FROM vue_rec_rubrique WHERE cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and cd_paragraphe = '%s' and company_id = %s and x_exercice_id = %s """ % (
						v_section, v_chapitre, v_article, v_paragraphe, company_id, x_exercice_id))

						for rubs in self.env.cr.dictfetchall():
							v_rubrique = rubs['rubrique']
							print("rubrique", v_rubrique)
							budgetiserub = int(rubs['budgetise'])
							print("budgetise", budgetiserub)
							corrigerub = int(rubs['corrige'])
							print("corrige", corrigerub)
							emisrub = int(rubs['emis'])
							print("emis", emisrub)
							tauxrub = round(rubs['taux'],2)
							print("taux", tauxrub)
							librub = rubs['lb_long']
							print("libelle", librub)

							erubris = {v_rubrique: [librub, budgetiserub, corrigerub, emisrub, tauxrub]}
							erubri = OrderedDict(sorted(erubris.items(), key=lambda t: t[0]))
							docrubrique.append(erubri)

						eparagraphes = {v_paragraphe: [libpar, budgetisepar, corrigepar, emispar, tauxpar], 'rubrique': docrubrique}
						eparagraphe = OrderedDict(sorted(eparagraphes.items(), key=lambda t: t[0]))
						docparagraphe.append(eparagraphe)

					earticles = {v_article: [libart, budgetiseart, corrigeart, emisart, tauxart], "paragraphe": docparagraphe}
					earticle = OrderedDict(sorted(earticles.items(), key=lambda t: t[0]))
					docarticle.append(earticle)

				echapitres = {v_chapitre: [libchap, budgetisechap, corrigechap, emischap, tauxchap], "article": docarticle}
				echapitre = OrderedDict(sorted(echapitres.items(), key=lambda t: t[0]))
				docchapitre.append(echapitre)

			esections = {v_section: [libsec, budgetisesec, corrigesec, emissec, tauxsec], "chapitre": docchapitre}
			esection = OrderedDict(sorted(esections.items(), key=lambda t: t[0]))
			docsection.append(esection)
			print("result", docsection)

		return docsection


class BudgConsulEng(models.Model):
	_name = "budg_consul_eng"

	name = fields.Char("Name", default="Liste des engagements")
	dte_deb = fields.Date("Date debut")
	dte_fin = fields.Date("Date fin")
	procedure_id = fields.Many2one("budg_typeprocedure", "Type de procédure")
	etat = fields.Selection([
		('N', 'Confirmé'),
		('V', 'Approuvé'),
		('A','Annulé'),
		('W', 'Visé'),
		('R','Réjeté'),
		('LC','Liquidation en cours'),
		('L','Liquidé'),
		('T','Tous'),
	], string = "Etat")
	x_exercice_id = fields.Many2one("ref_exercice",
									default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_line = fields.One2many("budg_consul_engagement_lines", "eng_id", readonly=True)

	def afficher(self):

		dte_deb = self.dte_deb
		dte_fin = self.dte_fin
		v_etat = self.etat
		v_proc = int(self.procedure_id)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)


		for vals in self:
			vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
			e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
			where e.company_id = %d and e.x_exercice_id = %d order by e.no_eng """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.engagement_line.unlink()
			for line in rows:
				result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
									  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
			self.engagement_line = result

		if dte_deb and dte_fin:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.dt_etat between '%s' and '%s' order by e.no_eng """ % (val_struct, val_ex, dte_deb, dte_fin))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result

		elif dte_deb and dte_fin and v_etat:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.state = '%s' e.dt_etat between '%s' and '%s' order by e.no_eng """ % (val_struct, val_ex, v_etat, dte_deb, dte_fin))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result

		elif dte_deb and dte_fin and v_etat and v_proc:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.state = '%s' e.dt_etat between '%s' and '%s' and type_procedure = %s order by e.no_eng """ % (val_struct, val_ex, v_etat, dte_deb, dte_fin, v_proc))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result

		elif v_etat:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.state = '%s' order by e.no_eng """ % (val_struct, val_ex, v_etat))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result

		elif v_etat and v_proc:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.state = '%s' and type_procedure = %s order by e.no_eng """ % (val_struct, val_ex, v_etat, v_proc))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result

		elif dte_deb and dte_fin and v_proc:
			for vals in self:
				vals.env.cr.execute("""select e.dt_etat as dte, e.no_eng as eng, e.cd_rubrique_id as rub,
				e.no_beneficiaire as benef, e.lb_obj as obj, e.mnt_eng as mnt from budg_engagement e 
				where e.company_id = %s and e.x_exercice_id = %s and e.dt_etat between '%s' and '%s' and type_procedure = %s order by e.no_eng """ % (val_struct, val_ex, dte_deb, dte_fin, v_proc))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.engagement_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_eng': line['eng'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
				self.engagement_line = result





class BudgConsulEngLine(models.Model):
	_name = "budg_consul_engagement_lines"


	eng_id = fields.Many2one("budg_consul_eng", ondelete='cascade')
	dte = fields.Date("Date")
	no_eng = fields.Char("N° Eng")
	objet = fields.Text("Objet")
	rubrique_id = fields.Many2one("budg_rubrique","Rubrique")
	montant = fields.Integer("Montant")
	beneficiaire_id = fields.Many2one("ref_beneficiaire","Bénéficiaire")



class BudgConsulLiq(models.Model):
	_name = "budg_consul_liq"

	name = fields.Char("Name", default="Liste des liquidations")
	dte_deb = fields.Date("Date debut")
	dte_fin = fields.Date("Date fin")
	etat = fields.Selection([
		('N', 'Confirmé'),
		('L','Certifié'),
		('A','Annulé'),
		('T','Tous'),
	], string = "Etat")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	liquidation_line = fields.One2many("budg_consul_liquidation_lines", "liq_id", readonly=True)


	def afficher(self):

		dte_deb = self.dte_deb
		dte_fin = self.dte_fin
		v_etat = self.etat
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select l.dt_etat as dte, l.no_lo as liq, l.cd_rubrique_id as rub,
			l.no_beneficiaire as benef, l.lb_obj as obj, l.mnt_eng as mnt from budg_liqord l
			where l.company_id = %d and l.x_exercice_id = %d order by l.no_lo """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.liquidation_line.unlink()
			for line in rows:
				result.append((0, 0, {'dte': line['dte'], 'no_liq': line['liq'], 'rubrique_id': line['rub'],
									  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
			self.liquidation_line = result

		if dte_deb and dte_fin:
			for vals in self:
				vals.env.cr.execute("""select l.dt_etat as dte, l.no_lo as liq, l.cd_rubrique_id as rub,
				l.no_beneficiaire as benef, l.lb_obj as obj, l.mnt_paye as mnt from budg_liqord l 
				where l.company_id = %s and l.x_exercice_id = %s and l.dt_etat between '%s' and '%s' order by l.no_lo """ % (
				val_struct, val_ex, dte_deb, dte_fin))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.liquidation_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_liq': line['liq'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'],
										  'montant': line['mnt']}))
				self.liquidation_line = result

			if v_etat:
				for vals in self:
					vals.env.cr.execute("""select l.dt_etat as dte, l.no_lo as liq, l.cd_rubrique_id as rub,
					l.no_beneficiaire as benef, l.lb_obj as obj, l.mnt_paye as mnt from budg_liqord l
					where l.company_id = %s and l.x_exercice_id = %s and l.state = '%s' and l.dt_etat between '%s' and '%s' order by l.no_lo """ % (
					val_struct, val_ex, v_etat, dte_deb, dte_fin))

					rows = vals.env.cr.dictfetchall()
					result = []

					vals.liquidation_line.unlink()
					for line in rows:
						result.append((0, 0, {'dte': line['dte'], 'no_liq': line['liq'], 'rubrique_id': line['rub'],
											  'beneficiaire_id': line['benef'], 'objet': line['obj'],
											  'montant': line['mnt']}))
					self.liquidation_line = result

		elif v_etat:
			for vals in self:
				vals.env.cr.execute("""select l.dt_etat as dte, l.no_lo as liq, l.cd_rubrique_id as rub,
				l.no_beneficiaire as benef, l.lb_obj as obj, l.mnt_paye as mnt from budg_liqord l
				where l.company_id = %s and l.x_exercice_id = %s and l.state = '%s' order by l.no_lo """ % (
				val_struct, val_ex, v_etat))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.liquidation_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_liq': line['liq'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'],
										  'montant': line['mnt']}))
				self.liquidation_line = result


class BudgConsulLiqLine(models.Model):
	_name = "budg_consul_liquidation_lines"

	liq_id = fields.Many2one("budg_consul_liq", ondelete='cascade')
	dte = fields.Date("Date")
	no_liq = fields.Char("N° Liq")
	objet = fields.Text("Objet")
	rubrique_id = fields.Many2one("budg_rubrique","Rubrique")
	montant = fields.Integer("Montant")
	beneficiaire_id = fields.Char("Bénéficiaire")



class BudgConsulMdt(models.Model):
	_name = "budg_consul_mdt"

	name = fields.Char("Name", default="Liste des mandats")
	dte_deb = fields.Date("Date debut")
	dte_fin = fields.Date("Date fin")
	etat = fields.Selection([
		('N', 'Confirmé'),
		('O','Ordonnancé'),
		('E','Pris en charge'),
		('T','Tous'),
	], string = "Etat")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	mandat_line = fields.One2many("budg_consul_mandat_lines", "mdt_id", readonly=True)


	def afficher(self):

		dte_deb = self.dte_deb
		dte_fin = self.dte_fin
		v_etat = self.etat
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select m.dt_etat as dte, m.no_mandat as mdt, m.cd_rubrique_id as rub,
			m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m
			where m.company_id = %d and m.x_exercice_id = %d order by m.no_mandat """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_line.unlink()
			for line in rows:
				result.append((0, 0, {'dte': line['dte'], 'no_mdt': line['mdt'], 'rubrique_id': line['rub'],
									  'beneficiaire_id': line['benef'], 'objet': line['obj'], 'montant': line['mnt']}))
			self.mandat_line = result

		if dte_deb and dte_fin:
			for vals in self:
				vals.env.cr.execute("""select m.dt_etat as dte, m.no_mandat as mdt, m.cd_rubrique_id as rub,
				m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m 
				where m.company_id = %s and m.x_exercice_id = %s and m.dt_etat between '%s' and '%s' order by m.no_mandat """ % (
				val_struct, val_ex, dte_deb, dte_fin))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_mandat': line['mdt'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'],
										  'montant': line['mnt']}))
				self.mandat_line = result

		elif v_etat:
			for vals in self:
				vals.env.cr.execute("""select m.dt_etat as dte, m.no_mandat as mdt, m.cd_rubrique_id as rub,
				m.no_beneficiaire as benef, m.obj as obj, m.mnt_ord as mnt from budg_mandat m
				where m.company_id = %s and m.x_exercice_id = %s and m.state = '%s' order by m.no_lo """ % (
				val_struct, val_ex, v_etat))

				rows = vals.env.cr.dictfetchall()
				result = []

				vals.mandat_line.unlink()
				for line in rows:
					result.append((0, 0, {'dte': line['dte'], 'no_mdt': line['mdt'], 'rubrique_id': line['rub'],
										  'beneficiaire_id': line['benef'], 'objet': line['obj'],
										  'montant': line['mnt']}))
				self.mandat_line = result


class BudgConsulMdtLine(models.Model):
	_name = "budg_consul_mandat_lines"

	mdt_id = fields.Many2one("budg_consul_mdt", ondelete='cascade')
	dte = fields.Date("Date")
	no_mdt = fields.Char("N° Mdt")
	objet = fields.Text("Objet")
	rubrique_id = fields.Many2one("budg_rubrique","Rubrique")
	montant = fields.Integer("Montant")
	beneficiaire_id = fields.Char("Bénéficiaire")



class BudgEditionExeDep(models.Model):
	_name = "budg_execution_depense"

	name = fields.Char("titre", default="Compte administratif des dépenses")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	depense_line = fields.One2many("budg_execution_depense_lines","depense_id", readonly=True)

	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select * from budg_ligne_exe_dep l where l.company_id = %d and l.x_exercice_id = %d
			 order by l.cd_titre_id, l.cd_section_id, l.cd_chapitre_id, l.cd_art_id, l.cd_paragraphe_id, l.cd_rubrique_id
			  """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.depense_line.unlink()
			for line in rows:
				result.append((0, 0, {'titre': line['cd_titre_id'], 'section': line['cd_section_id'],
									  'chapitre': line['cd_chapitre_id'], 'article': line['cd_art_id'],
									  'paragraphe': line['cd_paragraphe_id'], 'rubrique': line['cd_rubrique_id'],
									  'initiale': line['mnt_budgetise'], 'corrige': line['mnt_corrige'],
									  'engagement': line['mnt_engage'], 'dispo': line['mnt_disponible'], 'mandat': line['mnt_mandate'], 'taux': line['taux'], 'reste': line['reste_mandat']}))
			self.depense_line = result



class BudgEditionExeDepLine(models.Model):
	_name = "budg_execution_depense_lines"

	depense_id = fields.Many2one("budg_execution_depense", ondelete='cascade')
	titre = fields.Many2one("budg_titre", "Titre")
	section = fields.Many2one("budg_section", "Section")
	chapitre = fields.Many2one("budg_chapitre", "Chapitre")
	article = fields.Many2one("budg_param_article", "Article")
	paragraphe = fields.Many2one("budg_paragraphe", "Paragraphe")
	rubrique = fields.Many2one("budg_rubrique", "Rubrique")
	initiale = fields.Float("Dotation initiale")
	corrige = fields.Float("Dotation corrigée")
	engagement = fields.Float("Engagement")
	dispo = fields.Float("Crédit Disponible")
	mandat = fields.Float("Mandatement")
	taux = fields.Float("Taux de réalisation(%)",digits = (15,2))
	reste = fields.Float("Reste à mandater")



class BudgEditionExeRec(models.Model):
	_name = "budg_execution_recette"

	name = fields.Char("titre", default="Compte administratif des recettes")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	recette_line = fields.One2many("budg_execution_rec_lines","recette_id", readonly=True)

	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select * from budg_ligne_exe_rec l where l.company_id = %d and l.x_exercice_id = %d
			 order by l.cd_titre_id, l.cd_section_id, l.cd_chapitre_id, l.cd_art_id, l.cd_paragraphe_id, l.cd_rubrique_id
			  """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.recette_line.unlink()
			for line in rows:
				result.append((0, 0, {'titre': line['cd_titre_id'], 'section': line['cd_section_id'],
									  'chapitre': line['cd_chapitre_id'], 'article': line['cd_art_id'],
									  'paragraphe': line['cd_paragraphe_id'], 'rubrique': line['cd_rubrique_id'],
									  'initiale': line['mnt_budgetise'], 'corrige': line['mnt_corrige'],
									  'emis': line['mnt_rec'], 'taux': line['taux'], 'reste': line['reste_emettre']}))
			self.recette_line = result



class BudgEditionExeRecLine(models.Model):
	_name = "budg_execution_rec_lines"

	recette_id = fields.Many2one("budg_execution_recette", ondelete='cascade')
	titre = fields.Many2one("budg_titre", "Titre")
	section = fields.Many2one("budg_section", "Section")
	chapitre = fields.Many2one("budg_chapitre", "Chapitre")
	article = fields.Many2one("budg_param_article", "Article")
	paragraphe = fields.Many2one("budg_paragraphe", "Paragraphe")
	rubrique = fields.Many2one("budg_rubrique", "Rubrique")
	initiale = fields.Float("Dotation initiale")
	corrige = fields.Float("Dotation corrigée")
	emis = fields.Float("Titre émis")
	taux = fields.Float("Taux de réalisation(%)",digits = (15,2))
	reste = fields.Float("Reste à recouvrer")


class Budg_CompteurBordEngRejet(models.Model):
	_name = "budg_compteur_bord_eng_rejet"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)

# Mise en bordereau des engagements rejetés
class BudgBordEngRejeteCtrl(models.Model):
	_name = "budg_bordereau_engagement_rejet_controle"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de Rejet d'Engagement de Contrôle",
								 readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='CG', readonly=True)
	date_emis = fields.Date("Date émision", readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur")
	# x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	engagement_ids = fields.One2many("budg_liste_engagment_rejet", "bord_id", string="Liste des engagements")
	state = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Bordereau envoyé à DFC'),
		('R', 'Réceptionné bordereau par DFC'),
	], 'Etat', default='N', required=True)
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.id as eng, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.type_procedure as proc, b.type_beneficiaire_id as typeb,
			b.no_beneficiaire as benef, b.lb_obj as obj, b.mnt_eng as mnt from budg_engagement b 
			where b.company_id = %d and x_exercice_id = %d and b.state = 'R' """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.engagement_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_eng': line['eng'], 'cd_titre_id': line['titre'],
									  'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
									  'cd_article_id': line['art'],
									  'cd_paragraphe_id': line['par'], 'cd_rubrique_id': line['rub'],
									  'type_procedure': line['proc'], 'type_beneficiaire_id': line['typeb'],
									  'no_beneficiaire': line['benef'], 'lb_obj': line['obj'],
									  'mnt_eng': line['mnt']}))
			self.engagement_ids = result

	def envoyer(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)
		for val in self.engagement_ids:
			if val.motif_rejet == " ":
				raise ValidationError(_("Veuillez choisir un motif de rejet"))
			else:
				pass

		self.date_emis = date.today()
		self.env.cr.execute("select bordeng from budg_compteur_bord_eng_rejet where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_eng_rejet(x_exercice_id,company_id,bordeng) VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
			self.write({'state': 'E'})
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_eng_rejet SET bordeng = %d WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))
			self.write({'state': 'E'})




	def action_receptionner(self):
		self.write({'state': 'E'})
		self.date_recus = date.today


class BudgListeEngagementRejet(models.Model):
	_name = 'budg_liste_engagment_rejet'

	bord_id = fields.Many2one('budg_bordereau_engagement_rejet_controle', ondelete='cascade')
	dt_etat = fields.Date(default=fields.Date.context_today, string="Date", readonly=True)
	no_eng = fields.Many2one("budg_engagement", string="N° engagement", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre', readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	type_procedure = fields.Many2one("budg_typeprocedure", string="Type de procédure", v=True)
	type_beneficiaire_id = fields.Many2one("ref_categoriebeneficiaire", readonly=True, string="Catégorie")
	no_beneficiaire = fields.Many2one("ref_beneficiaire", readonly=True, string="Bénéficiaire")
	lb_obj = fields.Text(string="Objet", readonly=True)
	mnt_eng = fields.Float(string="Montant", readonly=True)
	dt_visa_cf = fields.Date(string="Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
	commentaire = fields.Text("Commentaires")
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('R', 'Rejeté'),
	], default='R', string='Etat', index=True, readonly=True, track_visibility='always')
	envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')
	observation = fields.Text("Observations")
	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


# Reception bordereau de rejet DCMEF /CG
class BudgBordEngRecepRejetCtrl(models.Model):
	_name = "budg_bordereau_engagement_recep_rejet_controle"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Réception bordereau de rejet d'engagement", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_engagement_rejet_controle", "Bord. reçu", required=True,
								domain=[('state', '=', 'E')])
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	cd_acteur_accuse = fields.Char(string="Acteur")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	rejet_ids = fields.One2many("budg_engagement_rejeter", "rejet_id", string="Liste des engagements",
								ondelete="restrict")
	state = fields.Selection([
		('E', 'Envoyé par CG'),
		('R', 'Réceptionné'),
	], 'Etat', default='E', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select * from budg_liste_engagment_rejet b
			where b.bord_id = %d and b.company_id = %d and b.x_exercice_id = %d and b.state = 'R' """ % (
			id_bord, val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.rejet_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dt_etat'], 'eng_id': line['no_eng'],
									  'beneficiciare': line['no_beneficiaire'], 'objet': line['lb_obj'], 'montant': line['mnt_eng'], 'motif_rejet': line['motif_rejet']}))
			self.rejet_ids = result

	def receptionner(self):

		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.date_recus = date.today()


		self.env.cr.execute("""UPDATE budg_bordereau_engagement_rejet_controle SET state ='R', date_recus = %s WHERE id = %s and x_exercice_id = %s and
		company_id = %s""", (self.date_recus, bord, val_ex, val_struct))

		self.env.cr.execute(
			"select bordeng from budg_compteur_bord_eng_recep_rejet_ctrl where x_exercice_id = %d and company_id = %d" % (
			val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"""INSERT INTO budg_compteur_bord_eng_recep_rejet_ctrl(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
				val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"UPDATE budg_compteur_bord_eng_recep_rejet_ctrl SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
				vals, val_ex, val_struct))

		self.afficher()

		self.write({'state': 'R'})


class BudgEngRejeter(models.Model):
	_name = "budg_engagement_rejeter"

	rejet_id = fields.Many2one("budg_bordereau_engagement_recep_rejet_controle", ondelte='cascade')
	dt_etat = fields.Date("Date", readonly=True)
	eng_id = fields.Many2one("budg_engagement", "N° Engagement", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiciare = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	montant = fields.Float("Montant", readonly=True)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
	state = fields.Selection([
		('N', 'Nouveau'),
		('R', 'Rejeté')], string="Etat", default="R", readonly=True)


class Budg_Compteur_bordRecepEngCf(models.Model):
	_name = "budg_compteur_bord_eng_recep_rejet_ctrl"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class BudgCorrectionEngagementRejet(models.Model):
	_name = "budg_correction_engagement_rejet"
	_rec_name = "eng_id"

	eng_id = fields.Many2one("budg_engagement", "N° Engagement", required=True, domain=[('state', '=', 'R')])
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Paragraphe", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	anc_objet = fields.Text("Objet", readonly=True)
	objet = fields.Text("Objet", readonly=False)
	anc_beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
	cpte_benef = fields.Char('compte')
	imput_benef = fields.Char('imput')
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('R', 'Rejeté'), ('C', 'Corrigé')], default='R', string="Etat", required=True)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	piece_ids = fields.One2many("budg_piecejustificativecorrectmandat", "mdt_id")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	# Récuperer les elements de l'engagement choisi
	@api.onchange("eng_id")
	def Valeur(self):
		for vals in self:
			if vals.eng_id:
				self.titre_id = self.eng_id.cd_titre_id
				self.section_id = self.eng_id.cd_section_id
				self.chapitre_id = self.eng_id.cd_chapitre_id
				self.article_id = self.eng_id.cd_article_id
				self.para_id = self.eng_id.cd_paragraphe_id
				self.rub_id = self.eng_id.cd_rubrique_id
				self.mnt = self.eng_id.mnt_eng
				self.anc_beneficiaire = self.eng_id.no_beneficiaire
				self.anc_objet = self.eng_id.lb_obj
				self.motif_rejet = self.eng_id.motif_rejet


	@api.onchange('beneficiaire')
	def cpte(self):
		self.cpte_benef = self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
		self.imput_benef = self.beneficiaire.cpte_fournisseur.souscpte.id

	# Correction de l'engagement
	def corriger(self):
		eng = int(self.eng_id)
		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		for val in self:

			if val.motif_rejet == '1':
				raise ValidationError(_("Correction impossible pour ce motif. Veuillez annuler cet engagement et reprendre un nouveau."))

			elif val.motif_rejet == '2':
				raise ValidationError(_("Correction impossible pour ce motif. Veuillez annuler cet engagement et reprendre un nouveau."))
			elif val.motif_rejet == '3':

				benef = int(val.beneficiaire)
				cpte = self.cpte_benef
				imput = self.imput_benef
				val.env.cr.execute(
					"""UPDATE budg_engagement SET state='V' WHERE id = %s and x_exercice_id = %s and company_id = %s""",( eng, no_ex, struct))
				val.write({'state': 'C'})
				val.env.cr.execute("""select * from budg_piecejustificativecorrecteng where mdt_id = %s""")
				for vals in val.env.cr.dictfetchall():
					pj = vals['piecejust_id']
					ref = vals['reference']
					dte = vals['datepj']
					obl = vals['active']
					mnt = vals['montant']
					nbre = vals['nombre']

					self.env.cr.execute("""INSERT INTO budg_piece_eng(lb_long, ref, dte, oblige, montant, nombre, eng_id) 
									VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre, eng))


			elif val.motif_rejet == '4':
				benef = int(val.beneficiaire)
				cpte = self.cpte_benef
				imput = self.imput_benef
				val.env.cr.execute("""UPDATE budg_engagement SET state='V', no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""" ,(benef, cpte, imput, eng, no_ex, struct))
				val.write({'state': 'C'})

			elif val.motif_rejet == '5':
				obj = str(val.objet)
				val.env.cr.execute("""UPDATE budg_engagement SET lb_obj = %s, state='V' WHERE id = %s and x_exercice_id = %s and company_id = %s""",(obj, eng, no_ex, struct))
				val.write({'state': 'C'})
			else:
				raise ValidationError(_("Pas de données à corriger."))



class Budg_PieceJustiCorrecEng(models.Model):
	_name = "budg_piecejustificativecorrecteng"

	piecejust_id = fields.Many2one('ref_piece_justificatives', string="Intitulé")
	reference = fields.Char("Références", size=35)
	datepj = fields.Date('Date')
	active = fields.Boolean("Obligé ?", default=True)
	montant = fields.Integer('Montant', size=15)
	nombre = fields.Integer("Nbre copies(s)")
	eng_id = fields.Many2one("budg_correction_engagement_rejet",ondelete='cascade')


class BudgBordMdtControleRejet(models.Model):
	_name = "budg_bordereau_mandatement_controle_rejet"
	_rec_name = "no_bord_en"
	_order = " id desc"

	name = fields.Char()
	no_bord_en = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de rejet de mandats", readonly=True)
	cd_acteur = fields.Char(string="Acteur", readonly=True)
	date_emis = fields.Date(string="Date d'émission",readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_detail_bord_mandat_rejets", "bord_id",string="Liste des mandats")
	state = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Envoyé à DAF/DFC '),
		('R', 'Réceptionné par DAF/DFC '),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.id as mdt, b.cd_titre_id as titre, b.motif_rejet as motif_rejet, b.cd_section_id as sec, b.cd_chapitre_id as chap, b.commentaire as commentaire,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub,
			b.no_beneficiaire as benef, b.obj as obj, b.mnt_ord as mnt from budg_mandat b 
			where b.company_id = %d and x_exercice_id = %d and b.state = 'R' """ % (val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_mdt': line['mdt'], 'cd_titre_id': line['titre'],
									  'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
									  'cd_article_id': line['art'],'cd_paragraphe_id': line['par'],
									  'cd_rubrique_id': line['rub'],'no_beneficiaire': line['benef'],
									  'lb_obj': line['obj'],'mnt_ord': line['mnt'],'motif_rejet': line['motif_rejet'],'commentaire': line['commentaire']}))
			self.mandat_ids = result


	def envoyer(self):


		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.date_emis = date.today()

		self.env.cr.execute("select bordeng from budg_compteur_bord_mandat_rejet where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_mandat_rejet(x_exercice_id,company_id,bordeng) VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_mandat_rejet SET bordeng = %d WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))


		self.write({'state': 'E'})


class BudgListeMandatRejet(models.Model):
	_name = 'budg_detail_bord_mandat_rejets'

	bord_id = fields.Many2one('budg_bordereau_mandatement_controle_rejet', ondelete='cascade')
	dt_etat = fields.Date(string="Date", readonly=True)
	no_mdt = fields.Many2one("budg_mandat", string="N° Mandat", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre', readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	no_beneficiaire = fields.Char(string="Bénéficiaire",readonly=True)
	lb_obj = fields.Text(string="Objet", readonly=True)
	mnt_ord = fields.Float(string="Montant", readonly=True)
	dt_visa_cf = fields.Date(string="Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
	commentaire = fields.Text("Commentaire")
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('R', 'Rejeté'),
	], default='R', string='Etat', index=True, readonly=True, track_visibility='always')
	envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


class Budg_Compteur_bordMdtCf(models.Model):
	_name = "budg_compteur_bord_mandat_rejet"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class Budg_Compteur_bordMdtCAc(models.Model):
	_name = "budg_compteur_bord_mandat_rejet_ac"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


# Reception bordereau de rejet DCMEF /CG
class BudgBordMdtRecepRejetCtrl(models.Model):
	_name = "budg_bordereau_mandat_recep_rejet_controle"
	_rec_name = "no_bord_en"
	_order = " id desc"

	no_bord_en = fields.Char(string='Bord. N°', readonly=True)
	type_bord_trsm = fields.Char("Type de bordereau", default="Réception bordereau de rejet de mandat", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_mandatement_controle_rejet", "Bord. reçu", required=True,
								domain=[('state', '=', 'E')])
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										  readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	cd_acteur_accuse = fields.Char(string="Acteur")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	rejet_ids = fields.One2many("budg_mandat_rejeter", "rejet_id", string="Liste des engagements",
								ondelete="restrict")
	state = fields.Selection([
		('E', 'Envoyé par CG'),
		('R', 'Réceptionné'),
	], 'Etat', default='E', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select * from budg_mandat b
			where b.company_id = %s and b.x_exercice_id = %s and b.state = 'R' """ ,(val_struct, val_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.rejet_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dt_etat'], 'mdt_id': line['id'],
									  'beneficiciare': line['no_beneficiaire'], 'objet': line['lb_obj'], 'commentaire': line['commentaire'], 'montant': line['mnt_ord'], 'motif_rejet': line['motif_rejet']}))
			self.rejet_ids = result

	def receptionner(self):

		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.date_recus = date.today()


		self.env.cr.execute("""UPDATE budg_bordereau_mandatement_controle_rejet SET state ='R', date_recus = %s WHERE id = %s and x_exercice_id = %s and
		company_id = %s""", (self.date_recus, bord, val_ex, val_struct))

		self.env.cr.execute(
			"select bordeng from budg_compteur_bord_mdt_recep_rejet_ctrl where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"""INSERT INTO budg_compteur_bord_mdt_recep_rejet_ctrl(x_exercice_id,company_id,bordeng)  VALUES(%d, %d, %d)""" % (
				val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute(
				"UPDATE budg_compteur_bord_mdt_recep_rejet_ctrl SET bordeng = %d  WHERE x_exercice_id = %d and company_id = %d" % (
				vals, val_ex, val_struct))

		self.afficher()

		self.write({'state': 'R'})


class BudgMdtRejeter(models.Model):
	_name = "budg_mandat_rejeter"

	rejet_id = fields.Many2one("budg_bordereau_mandat_recep_rejet_controle", ondelte='cascade')
	dt_etat = fields.Date("Date", readonly=True)
	mdt_id = fields.Many2one("budg_mandat", "N° Mandat", readonly=True)
	objet = fields.Text("Objet", readonly=True)
	beneficiciare = fields.Char("Bénéficiaire", readonly=True)
	montant = fields.Float("Montant", readonly=True)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
	commentaire = fields.Text("Commentaire", readonly=True)
	state = fields.Selection([
		('N', 'Nouveau'),
		('R', 'Rejeté')], string="Etat", default="R", readonly=True)


class Budg_Compteur_bordRecepMdtCf(models.Model):
	_name = "budg_compteur_bord_mdt_recep_rejet_ctrl"

	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	bordeng = fields.Integer(default=0)


class BudgCorrectionMandat(models.Model):
	_name = "budg_correction_mandat"
	_rec_name = "mandat_id"

	mandat_id = fields.Many2one("budg_mandat",domain=['|',('state', '=', 'R'),('state', '=', 'J')], required=True, string ="N° Ordonnance")
	titre_id = fields.Many2one("budg_titre", "Titre", readonly=True)
	section_id = fields.Many2one("budg_section", "Section", readonly=True)
	chapitre_id = fields.Many2one("budg_chapitre", "Chapitre", readonly=True)
	article_id = fields.Many2one("budg_param_article", "Article", readonly=True)
	para_id = fields.Many2one("budg_paragraphe", "Paragraphe", readonly=True)
	rub_id = fields.Many2one("budg_rubrique", "Rubrique", readonly=True)
	mnt = fields.Float("Montant", readonly=True)
	anc_objet = fields.Text("Objet", readonly=True)
	objet = fields.Text("Objet", readonly=False)
	anc_beneficiaires = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=True)
	anc_beneficiaire = fields.Char("Id Bénéficiaire", readonly=True)
	beneficiaire = fields.Many2one("ref_beneficiaire", "Bénéficiaire", readonly=False)
	cpte_benef = fields.Char('compte')
	imput_benef = fields.Char('imput')
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	state = fields.Selection([('R', 'A corriger'), ('C', 'Corrigé')], default='R', string="Etat", required=True)
	etat = fields.Selection([('1', 'A mettre en bord. pour AC'), ('2', 'A mettre en bord. pour CG')], default='1', string="Destinataire", required=False)
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
	commentaire = fields.Text("Commentaire", readonly=True)
	commentaire_daf = fields.Text("Commentaire/DAF", readonly=False)

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	piece_ids = fields.One2many("budg_piecejustificativecorrectmandat","mdt_id")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	# Récuperer les elements du mandat rejeté choisi
	@api.onchange("mandat_id")
	def Valeur(self):
		for vals in self:
			if vals.mandat_id:
				self.titre_id = self.mandat_id.cd_titre_id
				self.section_id = self.mandat_id.cd_section_id
				self.chapitre_id = self.mandat_id.cd_chapitre_id
				self.article_id = self.mandat_id.cd_article_id
				self.para_id = self.mandat_id.cd_paragraphe_id
				self.rub_id = self.mandat_id.cd_rubrique_id
				self.mnt = self.mandat_id.mnt_ord
				self.anc_beneficiaire = self.mandat_id.no_beneficiaire
				self.anc_beneficiaires = self.mandat_id.no_beneficiaires
				self.anc_objet = self.mandat_id.obj
				self.motif_rejet = self.mandat_id.motif_rejet
				self.commentaire = self.mandat_id.commentaire

	@api.onchange('beneficiaire')
	def cpte(self):
		self.cpte_benef = self.beneficiaire.cpte_fournisseur.souscpte.concate_souscpte
		self.imput_benef = self.beneficiaire.cpte_fournisseur.souscpte.id

	# Correction du mandat
	def corriger(self):
		mdt = int(self.mandat_id)
		no_ex = int(self.x_exercice_id)
		struct = int(self.company_id)
		for val in self:

			if val.motif_rejet == '1':
				raise ValidationError(
					_("Correction impossible pour ce motif. Veuillez annuler ce mandat et son engagement lié et reprendre à nouveau le dossier."))

			elif val.motif_rejet == '2':
				raise ValidationError(
					_("Correction impossible pour ce motif. Veuillez annuler ce mandat et son engagement lié et reprendre à nouveau le dossier."))

			elif val.motif_rejet == '3':
				mdt_id = int(self.mandat_id)
				m_id = int(self.id)
				liq = int(self.mandat_id.no_lo)
				no_eng = int(self.mandat_id.no_lo.no_eng)

				val.env.cr.execute("""select * from budg_piecejustificativecorrectmandat where mdt_id = %d""" %(m_id))
				for vals in val.env.cr.dictfetchall():
					pj = vals['piecejust_id']
					ref = vals['reference']
					dte = vals['datepj']
					obl = vals['active']
					mnt = vals['montant']
					nbre = vals['nombre']

					self.env.cr.execute("""INSERT INTO budg_piece_ord(lb_long, ref, dte, oblige, montant, nombre, mandat_id) 
					VALUES (%s, %s, %s, %s, %s, %s, %s) """,(pj, ref, dte, obl, mnt, nbre, mdt_id))

					self.env.cr.execute("""INSERT INTO budg_piece_liq(lb_long, ref, dte, oblige, montant, nombre,liq_id) 
					VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre,liq))
					
					self.env.cr.execute("""INSERT INTO budg_piece_engagement(lb_long, ref, dte, oblige, montant, nombre,eng_id) 
					VALUES (%s, %s, %s, %s, %s, %s, %s) """, (pj, ref, dte, obl, mnt, nbre,no_eng))
				

				val.env.cr.execute("""UPDATE budg_mandat SET state='O' WHERE id = %s and x_exercice_id = %s and company_id = %s""",(mdt, no_ex, struct))

				val.write({'state': 'C'})

			elif val.motif_rejet == '4':
				eng = val.mandat_id.no_eng
				liq = int(val.mandat_id.no_lo)
				benef = int(val.beneficiaire)
				benefs = val.beneficiaire.nm
				cpte = self.cpte_benef
				imput = self.imput_benef
				
				
				val.env.cr.execute("""UPDATE budg_engagement SET no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""",
				(benef, cpte, imput, eng, no_ex, struct))
				

				val.env.cr.execute("""UPDATE budg_liqord SET no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
				(benef, cpte, imput, liq, no_ex, struct))
				

				val.env.cr.execute("""UPDATE budg_mandat SET state='O', no_beneficiaire = %s, cpte_benef = %s, imput_benef = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",
				(benef, cpte, imput, mdt, no_ex, struct))

				
				val.write({'state': 'C'})

			elif val.motif_rejet == '5':
				eng = val.mandat_id.no_eng
				liq = int(val.mandat_id.no_lo)
				obj = str(val.objet)

				val.env.cr.execute("""UPDATE budg_engagement SET lb_obj = %s WHERE no_eng = %s and x_exercice_id = %s and company_id = %s""", (obj, eng, no_ex, struct))


				val.env.cr.execute("""UPDATE budg_liqord SET lb_obj = %s WHERE id = %s and x_exercice_id = %s and company_id = %s""",(obj, liq, no_ex, struct))
				

				val.env.cr.execute("""UPDATE budg_mandat SET obj = %s, state='O' WHERE id = %s and x_exercice_id = %s and company_id = %s""",(obj, mdt, no_ex, struct))
				
				val.write({'state': 'C'})
			else:
				raise ValidationError(_("Pas de données à corriger."))


class Budg_PieceJustiCorrec(models.Model):
	_name = "budg_piecejustificativecorrectmandat"

	piecejust_id = fields.Many2one('ref_piece_justificatives', string="Intitulé")
	reference = fields.Char("Références", size=35)
	datepj = fields.Date('Date')
	active = fields.Boolean("Obligé ?", default=True)
	montant = fields.Integer('Montant', size=15)
	nombre = fields.Integer("Nbre copies(s)")
	mdt_id = fields.Many2one("budg_correction_mandat",ondelete='cascade')


class BudgImprimer(models.Model):
	_name = "budg_imprimer"

	name = fields.Char(default="Etat d'exécution des dépenses")
	dte_debut = fields.Date("Du", required=True)
	dte_fin = fields.Date("Au", required=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	imprimer_ids = fields.One2many("budg_imprimer_line","imprimer_id", readonly=True)

	def afficher(self):

		no_ex = int(self.x_exercice_id)
		cd_struct = int(self.company_id)

		self.env.cr.execute("DELETE FROM budg_imprimer_line")

		for vals in self:
			vals.env.cr.execute("select * from budg_ligne_exe_dep where company_id = %d and x_exercice_id = %d order by cd_titre_id, cd_section_id, cd_chapitre_id, cd_art_id, cd_paragraphe_id,cd_rubrique_id " % (cd_struct, no_ex))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.imprimer_ids.unlink()
			for line in rows:
				result.append((0, 0, {'titre': line['cd_titre_id'], 'section': line['cd_section_id'], 'chapitre': line['cd_chapitre_id'],
									'article': line['cd_art_id'], 'paragraphe': line['cd_paragraphe_id'],'rubrique': line['cd_rubrique_id'],
									  'initiale': line['mnt_budgetise'],'corrige': line['mnt_corrige']}))
			self.imprimer_ids = result

		self.CalculEngagement()
		self.CalculLiquidation()
		self.CalculMandat()

	def CalculEngagement(self):

		no_ex = int(self.x_exercice_id)
		cd_struct = int(self.company_id)
		deb = self.dte_debut
		fin = self.dte_fin

		self.env.cr.execute("""select sum(mnt_eng) as mnt,cd_titre_id, cd_section_id,
			 cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id from budg_engagement where dt_etat between %s and %s and company_id = %s and
			 x_exercice_id = %s and state not in ('draft','A','N') group by cd_titre_id, cd_section_id, cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id """ ,(deb, fin, cd_struct, no_ex))

		for val in self.env.cr.dictfetchall():
			eng = val['mnt']
			tit = val['cd_titre_id']
			sec = val['cd_section_id']
			chap = val['cd_chapitre_id']
			art = val['cd_article_id']
			par = val['cd_paragraphe_id']
			rub = val['cd_rubrique_id']

			self.env.cr.execute("""UPDATE budg_imprimer_line SET engagement = %s where titre = %s and section = %s and
			chapitre = %s and article = %s and paragraphe = %s and rubrique = %s and company_id = %s and 
			x_exercice_id = %s""" ,(eng, tit, sec, chap, art, par, rub, cd_struct, no_ex))

	def CalculLiquidation(self):

		no_ex = int(self.x_exercice_id)
		cd_struct = int(self.company_id)
		deb = self.dte_debut
		fin = self.dte_fin

		self.env.cr.execute("""select sum(mnt_paye) as mnt,cd_titre_id, cd_section_id,
			 cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id from budg_liqord where dt_etat between %s and %s and company_id = %s and
			 x_exercice_id = %s and state not in ('draft','A','N') group by cd_titre_id, cd_section_id, cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id """ ,(deb, fin, cd_struct, no_ex))

		for val in self.env.cr.dictfetchall():
			liq = val['mnt']
			tit = val['cd_titre_id']
			sec = val['cd_section_id']
			chap = val['cd_chapitre_id']
			art = val['cd_article_id']
			par = val['cd_paragraphe_id']
			rub = val['cd_rubrique_id']

			self.env.cr.execute("""UPDATE budg_imprimer_line SET liquide = %s where titre = %s and section = %s and
			chapitre = %s and article = %s and paragraphe = %s and rubrique = %s and company_id = %s and 
			x_exercice_id = %s""" ,(liq, tit, sec, chap, art, par, rub, cd_struct, no_ex))


	def CalculMandat(self):

		no_ex = int(self.x_exercice_id)
		cd_struct = int(self.company_id)
		deb = self.dte_debut
		fin = self.dte_fin

		self.env.cr.execute("""select sum(mnt_ord) as mnt,cd_titre_id, cd_section_id,
			 cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id from budg_mandat where dt_etat between %s and %s and company_id = %s and
			 x_exercice_id = %s and state not in ('draft','A','R','N') group by cd_titre_id, cd_section_id, cd_chapitre_id, cd_article_id, cd_paragraphe_id, cd_rubrique_id """ ,(deb, fin, cd_struct, no_ex))

		for val in self.env.cr.dictfetchall():
			mdt = val['mnt']
			tit = val['cd_titre_id']
			sec = val['cd_section_id']
			chap = val['cd_chapitre_id']
			art = val['cd_article_id']
			par = val['cd_paragraphe_id']
			rub = val['cd_rubrique_id']

			self.env.cr.execute("""UPDATE budg_imprimer_line SET mandat = %s, taux = (%s/ corrige)*100 where titre = %s and section = %s and
			chapitre = %s and article = %s and paragraphe = %s and rubrique = %s and company_id = %s and 
			x_exercice_id = %s""" ,(mdt,mdt, tit, sec, chap, art, par, rub, cd_struct, no_ex))

	def get_report_values(self):

		company_id = int(self.company_id)
		x_exercice_id = int(self.x_exercice_id)

		doctitre = []
		self.env.cr.execute("SELECT cd_titre, coalesce(initi,0) as initi, lb_long, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_titre WHERE company_id = %d and x_exercice_id = %d" % (company_id, x_exercice_id))
		for line in self.env.cr.dictfetchall():

			v_titre = line['cd_titre']
			v_t_lib = line['lb_long']
			v_t_init = int(line['initi'])
			v_t_corr = line['corr']
			v_t_eng = line['eng']
			v_t_liq= line['liq']
			v_t_mdt = line['mdt']
			v_t_taux = round(line['taux'],2)

			# Boucle 2
			docsection = []
			self.env.cr.execute(
				"SELECT cd_titre, cd_section, coalesce(initi,0) as initi, lb_long, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_section WHERE company_id = %s and x_exercice_id = %s and cd_titre = '%s' " %(company_id, x_exercice_id,v_titre))
			for line in self.env.cr.dictfetchall():

				v_section = line['cd_section']
				v_s_lib = line['lb_long']
				v_s_init = int(line['initi'])
				v_s_corr = line['corr']
				v_s_eng = line['eng']
				v_s_liq = line['liq']
				v_s_mdt = line['mdt']
				v_s_taux = round(line['taux'],2)

				# Boucle 3
				docchapitre = []
				self.env.cr.execute(
					"SELECT cd_titre, cd_section, cd_chapitre, lb_long, coalesce(initi,0) as initi, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_chapitre WHERE company_id = %s and x_exercice_id = %s and cd_titre = '%s' and cd_section = '%s' " %(company_id, x_exercice_id, v_titre, v_section))

				for line in self.env.cr.dictfetchall():

					v_chapitre = line['cd_chapitre']
					v_c_lib = line['lb_long']
					v_c_init = int(line['initi'])
					v_c_corr = line['corr']
					v_c_eng = line['eng']
					v_c_liq = line['liq']
					v_c_mdt = line['mdt']
					v_c_taux = round(line['taux'],2)

					# Boucle 4
					docarticle = []
					self.env.cr.execute(
						"SELECT cd_titre, cd_section, cd_chapitre, cd_article, lb_long, coalesce(initi,0) as initi, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_article WHERE company_id = %s and x_exercice_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' " %(company_id, x_exercice_id, v_titre, v_section, v_chapitre))
					for line in self.env.cr.dictfetchall():

						v_article = line['cd_article']
						v_a_lib = line['lb_long']
						v_a_init = int(line['initi'])
						v_a_corr = line['corr']
						v_a_eng = line['eng']
						v_a_liq = line['liq']
						v_a_mdt = line['mdt']
						v_a_taux = round(line['taux'],2)

						# Boucle 4
						docparagraphe = []
						self.env.cr.execute(
							"SELECT cd_titre, cd_section, cd_chapitre, cd_article, cd_paragraphe, lb_long, coalesce(initi,0) as initi, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_paragraphe WHERE company_id = %s and x_exercice_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' " %(company_id, x_exercice_id, v_titre, v_section, v_chapitre, v_article))
						for line in self.env.cr.dictfetchall():

							v_paragraphe = line['cd_paragraphe']
							v_p_lib = line['lb_long']
							v_p_init = int(line['initi'])
							v_p_corr = line['corr']
							v_p_eng = line['eng']
							v_p_liq = line['liq']
							v_p_mdt = line['mdt']
							v_p_taux = round(line['taux'],2)

							docrubrique = []
							self.env.cr.execute(
								"SELECT cd_titre, cd_section, cd_chapitre, cd_article, cd_paragraphe, rubrique, lb_long, coalesce(initi,0) as initi, coalesce(corr,0) as corr, coalesce(eng,0) as eng, coalesce(liq,0) as liq, coalesce(mdt,0) as mdt, taux as taux FROM vue_sit_rubrique WHERE company_id = %s and x_exercice_id = %s and cd_titre = '%s' and cd_section = '%s' and cd_chapitre = '%s' and cd_article = '%s' and cd_paragraphe = '%s' " %(company_id, x_exercice_id, v_titre, v_section, v_chapitre, v_article,v_paragraphe))

							for line in self.env.cr.dictfetchall():
								v_rubrique = line['rubrique']
								v_r_lib = line['lb_long']
								v_r_init = int(line['initi'])
								v_r_corr = line['corr']
								v_r_eng = line['eng']
								v_r_liq = line['liq']
								v_r_mdt = line['mdt']
								v_r_taux = round(line['taux'],2)

								erubriq = {v_rubrique: [v_r_lib, v_r_init, v_r_corr, v_r_eng, v_r_liq, v_r_mdt, v_r_taux]}
								erubri = OrderedDict(sorted(erubriq.items(), key=lambda t: t[0]))
								docrubrique.append(erubri)

							eparagraphes = {v_paragraphe: [v_p_lib, v_p_init, v_p_corr, v_p_eng, v_p_liq, v_p_mdt, v_p_taux],'rubrique': docrubrique}
							eparagraphe = OrderedDict(sorted(eparagraphes.items(), key=lambda t: t[0]))
							docparagraphe.append(eparagraphe)

						earticles = {v_article: [v_a_lib, v_a_init, v_a_corr, v_a_eng, v_a_liq, v_a_mdt, v_a_taux],"paragraphe": docparagraphe}
						earticle = OrderedDict(sorted(earticles.items(), key=lambda t: t[0]))
						docarticle.append(earticle)

					echapitres = {v_chapitre: [v_c_lib, v_c_init, v_c_corr, v_c_eng, v_c_liq, v_c_mdt, v_c_taux], "article": docarticle}
					echapitre = OrderedDict(sorted(echapitres.items(), key=lambda t: t[0]))
					docchapitre.append(echapitre)

				esections = {v_section: [v_s_lib, v_s_init, v_s_corr, v_s_eng, v_s_liq, v_s_mdt, v_s_taux], "chapitre": docchapitre}
				esection = OrderedDict(sorted(esections.items(), key=lambda t: t[0]))
				docsection.append(esection)

			etitres = {v_titre: [v_t_lib, v_t_init, v_t_corr, v_t_eng, v_t_liq, v_t_mdt, v_t_taux], "section": docsection}
			etitre = OrderedDict(sorted(etitres.items(), key=lambda t: t[0]))
			doctitre.append(etitre)
			print("result", doctitre)

		return doctitre


class BudgImprimerLines(models.Model):
	_name = "budg_imprimer_line"

	imprimer_id = fields.Many2one("budg_imprimer", ondelete='cascade')
	titre = fields.Many2one("budg_titre", "Titre")
	section = fields.Many2one("budg_section", "Section")
	chapitre = fields.Many2one("budg_chapitre", "Chapitre")
	article = fields.Many2one("budg_param_article", "Article")
	paragraphe = fields.Many2one("budg_paragraphe", "Paragraphe")
	rubrique = fields.Many2one("budg_rubrique", "Rubrique")
	initiale = fields.Float("Dotation initiale")
	corrige = fields.Float("Dotation corrigée")
	engagement = fields.Float("Dépenses engagées")
	liquide = fields.Float("Dépenses liquidées")
	mandat = fields.Float("Dépenses mandatées")
	taux = fields.Float("Taux d'exécution")
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)


class BudgSitTitre(models.Model):
	_name="vue_sit_titre"
	_auto=False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id,readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id = fields.Many2one('budg_titre',string="Titre", readonly=True)
	somtitre = fields.Float('',readonly=True)

	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_sit_titre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_titre AS (select l.company_id,l.x_exercice_id,rt.cd_titre, rt.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt WHERE bt.id = l.titre and rt.id = bt.titre and l.corrige > 0 GROUP by l.company_id, l.x_exercice_id, l.titre, rt.cd_titre, rt.lb_long
		order by rt.cd_titre)""")


class BudgSitSection(models.Model):
	_name = "vue_sit_section"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	somsection = fields.Float('',readonly=True)

	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_sit_section')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_section AS (select l.company_id,l.x_exercice_id,rt.cd_titre,rs.cd_section, rs.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs WHERE bt.id = l.titre and rt.id = bt.titre and bs.id = l.section and rs.id = bs.section and l.corrige > 0 
		GROUP by l.company_id, l.x_exercice_id, l.section, rt.cd_titre, rs.cd_section, rs.lb_long
		order by rt.cd_titre,rs.cd_section)""")


class BudgSitChapitre(models.Model):
	_name = "vue_sit_chapitre"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	somchapitre = fields.Float('',readonly=True)

	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_sit_chapitre')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_chapitre AS (select l.company_id,l.x_exercice_id,rt.cd_titre,rs.cd_section, rc.cd_chapitre, rc.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc WHERE bt.id = l.titre and rt.id = bt.titre and bs.id = l.section and rs.id = bs.section and l.corrige > 0 
		and bc.id = l.chapitre and rc.id = bc.chapitre GROUP by l.company_id, l.x_exercice_id, l.section, rt.cd_titre, rs.cd_section, rc.cd_chapitre, rc.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre)""")


class BudgViewSitArticle(models.Model):
	_name = "vue_sit_article"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	somarticle = fields.Float('', readonly=True)


	@api.model
	def init(self):

		tools.drop_view_if_exists(self.env.cr, 'vue_sit_article')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_article AS (select l.company_id,l.x_exercice_id,rt.cd_titre,rs.cd_section, rc.cd_chapitre,ra.cd_article, ra.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra
		WHERE bt.id = l.titre and rt.id = bt.titre and bs.id = l.section and rs.id = bs.section and l.corrige > 0 and bc.id = l.chapitre and rc.id = bc.chapitre and ba.id = l.article and ra.id = ba.article
		GROUP by l.company_id, l.x_exercice_id, l.section, rt.cd_titre, rs.cd_section, rc.cd_chapitre, ra.cd_article, ra.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article)""")


class BudgVueSitPar(models.Model):
	_name = "vue_sit_paragraphe"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	sompara = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_sit_paragraphe')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_paragraphe AS (select l.company_id,l.x_exercice_id,rt.cd_titre,rs.cd_section, rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe, rp.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra, budg_paragraphe bp, ref_paragraphe rp 
		WHERE bt.id = l.titre and rt.id = bt.titre and bs.id = l.section and rs.id = bs.section and l.corrige > 0 and bc.id = l.chapitre and rc.id = bc.chapitre and ba.id = l.article and ra.id = ba.article and bp.id = l.paragraphe and rp.id = bp.paragraphe
		GROUP by l.company_id, l.x_exercice_id, l.section, rt.cd_titre, rs.cd_section, rc.cd_chapitre, ra.cd_article, rp.cd_paragraphe, rp.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe)""")


class BudgViewSitRubrique(models.Model):
	_name = "vue_sit_rubrique"
	_auto = False

	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice",default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),string="Exercice", readonly=True)
	cd_titre_id =fields.Many2one('budg_titre',string="Titre", readonly=True)
	cd_section_id = fields.Many2one('budg_section', string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one('budg_chapitre', string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one('budg_param_article', string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one('budg_paragraphe', string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one('budg_rubrique', string="Rubrique", readonly=True)
	somrub = fields.Float('',readonly=True)



	@api.model
	def init(self):
		tools.drop_view_if_exists(self.env.cr, 'vue_sit_rubrique')

		self.env.cr.execute("""CREATE OR REPLACE VIEW vue_sit_rubrique AS (select l.company_id,l.x_exercice_id,rt.cd_titre,rs.cd_section, rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique, br.lb_long,coalesce(SUM(l.initiale),0) as initi, coalesce(SUM(l.corrige),0) as corr, coalesce(SUM(l.engagement),0) as eng ,coalesce(SUM(l.liquide),0) as liq ,
		coalesce(SUM(l.mandat),0) as mdt, (coalesce(SUM(l.engagement),0)/ coalesce(SUM(l.corrige),0))*100 as taux FROM budg_imprimer_line l,budg_titre bt, ref_titre rt, budg_section bs, ref_section rs, budg_chapitre bc, ref_chapitre rc,budg_param_article ba, ref_article ra, budg_paragraphe bp, ref_paragraphe rp , budg_rubrique br 
		WHERE bt.id = l.titre and rt.id = bt.titre and bs.id = l.section and rs.id = bs.section and l.corrige > 0 and bc.id = l.chapitre and rc.id = bc.chapitre and ba.id = l.article and ra.id = ba.article and bp.id = l.paragraphe and rp.id = bp.paragraphe and br.id = l.rubrique
		GROUP by l.company_id, l.x_exercice_id, l.section, rt.cd_titre, rs.cd_section, rc.cd_chapitre, ra.cd_article, rp.cd_paragraphe,br.rubrique, br.lb_long
		order by rt.cd_titre,rs.cd_section,rc.cd_chapitre,ra.cd_article,rp.cd_paragraphe,br.rubrique)""")


class BudgBordMdtControleRejetAc(models.Model):
	_name = "budg_bordereau_mandatement_rejet_ac"
	_rec_name = "no_bord_en"
	_order = " id desc"

	name = fields.Char()
	no_bord_en = fields.Char("Bord. N°", readonly=True)
	type_bord_trsm = fields.Char('Type de bordereau', default="Bordereau de rejet d'ordonnances", readonly=True)
	cd_acteur = fields.Char(string="Acteur", readonly=True)
	date_emis = fields.Date(string="Date d'émission", readonly=True)
	date_recus = fields.Date("Date de reception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	cd_acteur_accuse = fields.Char(string="Acteur", readonly=True)
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	mandat_ids = fields.One2many("budg_detail_bord_mandat_rejet_ac", "bord_id", string="Liste des mandats")
	state = fields.Selection([
		('N', 'Nouveau'),
		('E', 'Envoyé à DAF/DFC '),
		('R', 'Réceptionné par DAF/DFC '),
	], 'Etat', default='N', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	signataire_4 = fields.Many2one("budg_signataire", default=lambda self: self.env['budg_signataire'].search([('code', '=', '4')]))

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))


	def MntPre(self):

		for val in self:

			val_id = int(val.id)
			val_ex = int(val.x_exercice_id)
			val_struct = int(val.company_id)

			val.env.cr.execute("""SELECT sum(mnt_ord) FROM budg_detail_bord_mandat_rejet_ac e,budg_bordereau_mandatement_rejet_ac m
			WHERE e.envoyer_daf = 'Y' AND m.company_id = %d AND e.bord_id = %d AND e.bord_id = m.id""" % (val_struct, val_id))
			res = val.env.cr.fetchone()
			resu = res and res[0] or 0
			val.totaux = resu


	@api.depends('totaux')
	def amount_to_words(self):
		self.text_amount = num2words(self.totaux, lang='fr')


	def afficher(self):

		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select b.dt_etat as dte, b.id as mdt, b.cd_titre_id as titre, b.cd_section_id as sec, b.cd_chapitre_id as chap,
			b.cd_article_id as art, b.cd_paragraphe_id as par, b.cd_rubrique_id as rub, b.motif_rejet as motif_rejet, b.commentaire as commentaire,
			b.no_beneficiaire as benef, b.obj as obj, b.mnt_ord as mnt from budg_liste_mandatement_pc b 
			where b.company_id = %d and b.state = 'J' and etat = 'MR' """ % (val_struct))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.mandat_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dte'], 'no_mdt': line['mdt'], 'cd_titre_id': line['titre'],
									  'cd_section_id': line['sec'], 'cd_chapitre_id': line['chap'],
									  'cd_article_id': line['art'],'cd_paragraphe_id': line['par'],
									  'cd_rubrique_id': line['rub'],'no_beneficiaire': line['benef'],
									  'lb_obj': line['obj'],'mnt_ord': line['mnt'],'motif_rejet': line['motif_rejet'],'commentaire': line['commentaire']}))
			self.mandat_ids = result


	def envoyer(self):


		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.date_emis = date.today()

		self.env.cr.execute("select bordeng from budg_compteur_bord_mandat_rejet_ac where x_exercice_id = %d and company_id = %d" % (val_ex, val_struct))
		bordeng = self.env.cr.fetchone()
		no_bord_en = bordeng and bordeng[0] or 0
		c1 = int(no_bord_en) + 1
		c = str(no_bord_en)
		if c == "0":
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("""INSERT INTO budg_compteur_bord_mandat_rejet_ac(x_exercice_id,company_id,bordeng) VALUES(%d, %d, %d)""" % (val_ex, val_struct, vals))
		else:
			c1 = int(no_bord_en) + 1
			c = str(no_bord_en)
			ok = str(c1).zfill(4)
			self.no_bord_en = ok
			vals = c1
			self.env.cr.execute("UPDATE budg_compteur_bord_mandat_rejet_ac SET bordeng = %d WHERE x_exercice_id = %d and company_id = %d" % (vals, val_ex, val_struct))

		self.majOrdonnance()

		self.write({'state': 'E'})


	def receptionner(self):
		self.write({'state': 'R'})


	#changer l'etat des ordonnances pour qu'elles s'affichent plus quand on veut mettre dans un bord de rejet
	def majOrdonnance(self):

		v_struct = int(self.company_id)
		print('struct', v_struct)

		self.env.cr.execute("""select * from budg_liste_mandatement_pc where etat = 'MR' and company_id = %d""" %(v_struct))
		for val in self.env.cr.dictfetchall():
			etat = val['etat']
			print('ecr', etat)
			no_mdt = val['no_mandat']
			print('lecr', no_mdt)
			self.env.cr.execute("""update budg_liste_mandatement_pc set etat ='R' where no_mandat = %d and company_id = %d""" %(no_mdt, v_struct))


class BudgListeMandatRejetAc(models.Model):
	_name = 'budg_detail_bord_mandat_rejet_ac'

	bord_id = fields.Many2one('budg_bordereau_mandatement_rejet_ac', ondelete='cascade')
	dt_etat = fields.Date(string="Date", readonly=True)
	no_mdt = fields.Many2one("budg_mandat", string="N° Mandat", readonly=True)
	cd_titre_id = fields.Many2one("budg_titre", 'Titre', readonly=True)
	cd_section_id = fields.Many2one("budg_section", string="Section", readonly=True)
	cd_chapitre_id = fields.Many2one("budg_chapitre", string="Chapitre", readonly=True)
	cd_article_id = fields.Many2one("budg_param_article", string="Article", readonly=True)
	cd_paragraphe_id = fields.Many2one("budg_paragraphe", string="Paragraphe", readonly=True)
	cd_rubrique_id = fields.Many2one("budg_rubrique", string="Rubrique", readonly=True)
	no_beneficiaire = fields.Many2one("ref_beneficiaire",string="Bénéficiaire",readonly=True)
	lb_obj = fields.Text(string="Objet", readonly=True)
	mnt_ord = fields.Float(string="Montant", readonly=True)
	dt_visa_cf = fields.Date(string="Date Visa")
	motif_rejet = fields.Selection([('1', 'Erreur Imputation'),
									('2', 'Erreur Montant'), ('3', 'Erreur Pièce'), ('4', 'Erreur Bénéficiaire'),
									('5', 'Erreur Objet')], string="Motif du rejet", readonly=False)
	
	commentaire = fields.Text("Commentaire")
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, string="Structure")
	state = fields.Selection([
		('R', 'Rejeté'),
	], default='R', string='Etat', index=True, readonly=True, track_visibility='always')
	envoyer_daf = fields.Selection([('Y', 'Oui'), ('N', 'Non')], string='Envoyé ?', default='Y')

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)


# Reception bordereau de rejet DCMEF /CG
class BudgBordEngRecepRejetAc(models.Model):
	_name = "budg_bordereau_mandat_recep_rejet_ac"
	_rec_name = "type_bord_trsm"
	_order = " id desc"

	type_bord_trsm = fields.Char("Type de bordereau", default="Bordereau de rejet d'ordonnance AC", readonly=True)
	cd_acteur = fields.Char(string="Acteur", default='DAF/DFC', readonly=True)
	bord_recu = fields.Many2one("budg_bordereau_mandatement_rejet_ac", "Bord. reçu", required=True,
								domain=[('state', '=', 'E')])
	date_emis = fields.Date("Date émision", default=fields.Date.context_today, readonly=True)
	date_recus = fields.Date("Date de réception", readonly=True)
	num_accuse = fields.Char()
	totaux = fields.Integer()
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
										readonly=True)
	text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words")
	cd_acteur_accuse = fields.Char(string="Acteur", default='DAF/DFC')
	company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
	rejet_ids = fields.One2many("budg_mandat_rejeter_ac", "rejet_id", string="Liste des engagements",
								ondelete="restrict")
	state = fields.Selection([
		('E', 'Envoyé par AC'),
		('R', 'Réceptionné'),
	], 'Etat', default='E', required=True)
	total_prec = fields.Integer()

	current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
	x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

	# Récupérer l'exercice de l'utilisateur poour effectuer les traitements sur ça
	@api.onchange('current_users')
	def User(self):
		if self.current_users:
			self.x_exercice_id = self.current_users.x_exercice_id

	# Controler l'exercice pour voir si ce n'est pas un exercice clos
	@api.constrains('x_exercice_id')
	def _ControleExercice(self):
		no_ex = int(self.x_exercice_id)
		v_ex = int(self.x_exercice_id.no_ex)
		for record in self:
			record.env.cr.execute("select count(id) from ref_exercice where etat = '1' and id = %d" % (no_ex))
			res = self.env.cr.fetchone()
			val = res and res[0] or 0
			if val == 0:
				raise ValidationError(_("Exercice" + " " + str(v_ex) + " " + "est clôs. Traitement impossible"))

	def afficher(self):

		id_bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		for vals in self:
			vals.env.cr.execute("""select * from budg_detail_bord_mandat_rejet_ac b
			where b.company_id = %s and b.bord_id = %s and b.state = 'R' """ ,(val_struct, id_bord))

			rows = vals.env.cr.dictfetchall()
			result = []

			vals.rejet_ids.unlink()
			for line in rows:
				result.append((0, 0, {'dt_etat': line['dt_etat'], 'mdt_id': line['no_mdt'], 'beneficiciare': line['no_beneficiaire'], 'objet': line['lb_obj'], 'commentaire': line['commentaire'], 'montant': line['mnt_ord'], 'motif_rejet': line['motif_rejet']}))
			self.rejet_ids = result

	def receptionner(self):

		bord = int(self.bord_recu)
		val_ex = int(self.x_exercice_id)
		val_struct = int(self.company_id)

		self.afficher()
		self.date_recus = date.today()

		self.env.cr.execute("""UPDATE budg_bordereau_mandatement_rejet_ac SET state ='R', date_recus = %s 
		WHERE id = %s and x_exercice_id = %s and company_id = %s""", (self.date_recus, bord, val_ex, val_struct))
		self.write({'state': 'R'})


class BudgMdtRejete(models.Model):
    _name = "budg_mandat_rejeter_ac"
    rejet_id = fields.Many2one("budg_bordereau_mandat_recep_rejet_ac", ondelte='cascade')
    dt_etat = fields.Date("Date", readonly=True)
    mdt_id = fields.Many2one("budg_mandat", "N° Ordonnance", readonly=True)
    objet = fields.Text("Objet", readonly=True)
    beneficiciare = fields.Many2one("ref_beneficiaire","Bénéficiaire", readonly=True)
    montant = fields.Float("Montant", readonly=True)
    motif_rejet = fields.Selection([('1', 'Erreur Imputation'), ('2', 'Erreur Montant'), ('3', 'Erreur Pièce'),
                                ('4', 'Erreur Bénéficiaire'), ('5', 'Erreur Objet')], string="Motif du rejet", readonly=True)
    commentaire = fields.Text("Commentaire", readonly=True)
    state = fields.Selection([('N', 'Nouveau'), ('R', 'Rejeté')], string="Etat", default="R", readonly=True)
