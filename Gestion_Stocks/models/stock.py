from odoo import fields,api,models,_
from odoo.exceptions import ValidationError
from _datetime import date, datetime


#Definition des Classes pour gerer le stock


#Classe pour gerer les groupes d'articles   
"""
class StockGroupeArticle(models.Model):
    
    _name = "stock_groupearticle"
    #_rec_name = "concat_fields"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of groupe article.", default=10)
    #x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    #company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    concat_fields = fields.Char(compute = "_concat")
    name = fields.Char(string = "Libéllé long", required=True)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_groupe = fields.Char(string = "Code",size = 10)
    
    _sql_constraints = [('code_groupe_unique', 'unique(code_groupe)', 
                     'Ce code d identification du groupe existe dejà, svp entrer un autre code')]



    #fonction de concatenation
    @api.depends('code_groupe','name')
    def _concat(self):
      for tests in self:
        tests.concat_fields = (tests.code_groupe or '')+' '+(tests.name or '')

    
#Classe pour gerer les familles d'articles   

class StockFamilleArticle(models.Model):
    
    _name = "stock_famillearticle"
    #_rec_name = "concat_fields_famille"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of famille article.", default=10)
    #x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    #company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    x_groupearticle_id = fields.Many2one('stock_groupearticle', string = 'Groupe', required=True)
    concat_fields_famille = fields.Char(compute = "_concat_famille")

    name = fields.Char(string = "Libéllé long", required = True)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_famille = fields.Char(string = "Code Famille",required = True,size = 10)
    
    _sql_constraints = [('code_famille_unique', 'unique(code_famille)', 
                     'Ce code d identification de famille existe dejà, svp entrer un autre code')]
    
 
    
    #fonction de concatenation de famille article
    @api.depends('code_famille','name')
    def _concat_famille(self):
      for tests in self:
        tests.concat_fields_famille = (tests.code_famille or '')+' '+(tests.name or '')""" 

    
#Classe pour gerer les sous familles d'articles   
class StockSousFamilleArticle(models.Model):
    
    _name = "stock_sousfamille_article"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of type article.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    x_famillearticle_id = fields.Many2one('stock_famillearticle', string = 'Famille')

    name = fields.Char(string = "Libéllé long", required = True,size = 65)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_sous_f_article = fields.Char(string = "Code",required = True,size = 10)
    
    _sql_constraints = [('code_type_unique', 'unique(code_type_article)', 
                     'Ce code d identification de type article existe dejà, svp entrer un autre code')]
    
    
    
    
#Classe pour gerer les types de mouvement de stock
class StockMouvementArticle(models.Model):
    
    _name = "stock_mouvementstock"
    _rec_name = "concat_fields_mouvement"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of mouvement article.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    concat_fields_mouvement = fields.Char(compute = "_concat_mvt")
    name = fields.Char(string = "Libéllé long", required = True,size = 65)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_mvt = fields.Char(string = "Code mouvement",required = True,size = 10)
    x_type = fields.Selection([
        ('1','Entrée'), ('2','Sortie'),   
        ], string="Type")
    
    _sql_constraints = [('code_mvt_unique', 'unique(code_mvt)', 
                     'Ce code d identification du mouvement existe dejà, svp entrer un autre code')]

    #fonction de concatenation
    @api.depends('code_mvt','name')
    def _concat_mvt(self):
      for tests in self:
        tests.concat_fields_mouvement = (tests.code_mvt or '')+' '+(tests.name or '')
        
        
#Classe pour gerer les unités de stockage
class StockUniteStockage(models.Model):
    
    _name = "stock_unitestockage"
    #_rec_name = "concat_fields_unite"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of mouvement article.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    #
    #concat_fields_unite = fields.Char(compute = "_concat_unite")
    name = fields.Char(string = "Libéllé long", required = True,size = 65)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_unite = fields.Char(string = "Code Unité",required = True,size = 10)
    
    _sql_constraints = [('code_unite_unique', 'unique(code_unite)', 
                     'Ce code d identification unité de stockage existe dejà, svp entrer un autre code')]


#Classe pour gerer les magasins de stockage
class StockMagasinStockage(models.Model):
    
    _name = "stock_magasinstockage"
    _rec_name = "concat_fields_mag"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of magasin.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    concat_fields_mag = fields.Char(compute = "_concat_mag")
    name = fields.Char(string = "Libéllé long", required = True,size = 65)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_mag = fields.Char(string = "Code Magasin",required = True,size = 10)
    responsable = fields.Many2one('res.users',string = "Responsable")

    _sql_constraints = [('code_mag_unique', 'unique(code_mag)', 
                     'Ce code d identification de magasin de stockage existe dejà, svp entrer un autre code')]

    #fonction de concatenation du champ libellé long et du code
    @api.depends('code_mag','name')
    def _concat_mag(self):
      for tests in self:
        tests.concat_fields_mag = (tests.code_mag or '')+' '+(tests.name or '')
        
        
#Classe pour gerer les qualifications
class StockQualification(models.Model):
    
    _name = "stock_qualifications"
    _rec_name = 'lib_long'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of qualification.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    lib_long = fields.Char(string = "Libéllé long", required = True,size = 65)
    libcourt = fields.Char(string = "Libéllé court",size = 35)
    code_qualification = fields.Char(string = "Code Qualification",required = True,size = 10)

    _sql_constraints = [('code_qual_unique', 'unique(code_qualification)', 
                     'Ce code d identification de qualification existe dejà, svp entrer un autre code')]


#Classe pour gerer les articles
class StockArticle(models.Model):
    
    _name = "stock_article"
    #_inherit = "product.template"
    #_rec_name = "concat_fields_article"
    #x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    concat_fields_article = fields.Char(compute = "_concat_art")
    name = fields.Char(string = "Libéllé long", required = True)
    libcourt = fields.Char(string = "Libéllé court",size = 65)
    code_article = fields.Char(string = "Code Article",required = True,size = 20)
    seuil_article = fields.Integer(string = "Seuil",required = False)
    qte_article_en_stock = fields.Integer(default = 0)
    
    
    x_groupearticle_id = fields.Many2one('stock_groupearticle',string = "Groupe", required=False)
    x_famillearticle_id = fields.Many2one('stock_famillearticle',string = "Famille", required=False)
    sous_f_article_id = fields.Many2one('stock_sousfamille_article',string = "Sous Famille")
    magasin_id = fields.Many2one('stock_magasinstockage',string = "Magasin")
    unite_stock_id = fields.Many2one('stock_unitestockage',string = "Unité")
    unite_livraison_id = fields.Many2one('stock_unitestockage',string = "Unité de livraison")


    _sql_constraints = [('code_article_unique', 'unique(code_article)', 
                     'Ce code d identification d article existe dejà, svp entrer un autre code')]

    #fonction de concatenation du champ libellé long et du code de qualification
    @api.depends('code_article','name')
    def _concat_art(self):
      for tests in self:
        tests.concat_fields_article = (tests.code_article or '')+' '+(tests.name or '')
                             
        
#Classe pour gerer les entrées d'articles(stock)   
class StockEntreeStock(models.Model):
    
    _name = "stock_livraisonfourniture"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of livraison article.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string = "Livraison N°", required = True)
    numordre = fields.Char(string = "N° Ordre", readonly = True)
    numcmde = fields.Char("N°Bon de commande", required=True)
    date_livraison = fields.Date(string = "Date livraison",default=date.today(), required = True)
    date_op = fields.Datetime('Date Opération',default=datetime.today(), readonly =True)
    fournisseur_id = fields.Many2one('ref_beneficiaire',string = "Fournisseur", required=True)
    objet_livraison = fields.Text(string = 'Observations')
    x_line_ids = fields.One2many('stock_livraisonfourniture_line','x_stock_id', string = 'Ajout Des Articles ')
    active = fields.Boolean(string = "Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Fait'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
    magasin_id = fields.Many2one('stock_magasinstockage',string = "Magasin", required = True)
    etat_entree = fields.Char(default = 'Entrée')

    #Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})
    
    #fonction permettant de mettre à jour la quantité des produits
    
    def miseajourstock(self):
        v_id = int(self.id)
        v_struct = int(self.company_id)
        self.env.cr.execute("""select count(l.id) from stock_livraisonfourniture_line l,stock_livraisonfourniture s 
        where s.id = l.x_stock_id and l.x_stock_id = %d and s.company_id = %d""" %(v_id, v_struct))
        lo = self.env.cr.fetchone()
        res = lo and lo[0] or 0
        if res <= 0:
            raise ValidationError(_('Veuillez saisir au moins un article!'))

        for record in self.x_line_ids:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            val_id = int(record.x_article_id)
            print('val id',val_id)
            val_qte = int(record.qte_livre)
            print('val qté',val_qte)
            record.env.cr.execute("""UPDATE stock_article set qte_article_en_stock = qte_article_en_stock + %d  WHERE id in (%d)""" %(val_qte,val_id))
        
            if record.qte_livre <= 0:
                raise ValidationError(_('Veuillez saisir une quantitée supérieure ou égale à 1'))
            
            self.env.cr.execute("select no_code from hr_cpte_entree_stock where company_id = %d" %(x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.numordre = 'ES' + '/' + ok
                vals = c1
                self.env.cr.execute("""INSERT INTO hr_cpte_entree_stock(company_id,no_code)  VALUES(%d , %d)""" %(x_struct_id,vals))    
            else:
                
                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                self.numordre = 'ES' + '/' + ok
                vals = c1
                self.env.cr.execute("UPDATE hr_cpte_entree_stock SET no_code = %d  WHERE company_id = %d" %(vals,x_struct_id))

        self.write({'state': 'V'})


#Classe pour gerer le compteur pour l'entrée en stock
class Compteur_Entree_Stock(models.Model):
    _name = "hr_cpte_entree_stock"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


#ligne pour l'entrée en stock
class StockEntreeStockLine(models.Model):
    
    _name = "stock_livraisonfourniture_line"
    x_stock_id = fields.Many2one('stock_livraisonfourniture', ondelete='cascade')
    x_article_id = fields.Many2one('stock_article', string = 'Articles', required = True)
    qte_actuelle = fields.Integer(string = 'Quantité actuelle', readonly = True)
    qte_livre = fields.Integer(string = 'Quantité')
    prix_unitaire_article = fields.Float(string = 'Prix Unitaire', required = True)
    montant_total_article = fields.Float(string = 'Montant', readonly = True)
    
    #fonction pour emplir les champs de l'employé a noter
    @api.onchange('x_article_id')
    def remplir_champ(self):
        for x in self:
            x.qte_actuelle = x.x_article_id.qte_article_en_stock
    
    #Fonction permettant de calculer le montant total de l'article en fonction de sa quantité
    @api.onchange('qte_livre','prix_unitaire_article')
    def calcul_mnt(self):
        if self.qte_livre or self.prix_unitaire_article:
            for vals in self:
                vals.montant_total_article = vals.qte_livre * vals.prix_unitaire_article
                
    # fonction pour remplir la qté livrée de l'article selectionné
    # @api.onchange('x_article_id')
    # def remplir_qte(self):
    #     self.qte_disponible = self.x_article_id.qte_article_en_stock

                
#Class pour gerer les besoins annuels de chaque service de chaque EPE                
class StockBesoinsAnnuels(models.Model):
    
    _name = "stock_besoinannuel"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice',string = "Année", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string = "Code",size = 50)
    #annee_besoin = fields.Char(string = "Année")
    date_besoin = fields.Datetime(string = 'Date/Heure', default=datetime.today())
    beneficiaire = fields.Many2one('hr_service',string = "Adressé à", readonly = True,default=lambda self: self.env['hr_service'].search([('est_stock','=', 1)]))
    service_demandeur = fields.Char(string = 'Service demandeur')
    objet_besoin = fields.Text(string = 'Objet')
    x_line_ids = fields.One2many('stock_besoinannuel_line','x_besoin_id')
    active = fields.Boolean(string = "Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('R', 'Receptionner'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user)
    
    #Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})
    
    #fonction de recuperation du service de l'utilisateur connecté et changement d'etat
    def action_valider(self):
        self.write({'state': 'V'})
        for record in self.x_line_ids:
            if record.qtes <= 0:
                raise ValidationError(_('Veuillez saisir une quantitée supérieure ou égale à 1'))

        x_struct_id = int(self.company_id)
        x_user_id = int(self.current_user)
        self.env.cr.execute("""select (R.name) AS service, (R.code) AS code From hr_service R, hr_employee E, res_users U where R.id = E.hr_service and u.id = E.user_id and U.id = %s and U.company_id = %s""",(x_user_id,x_struct_id))
        rows = self.env.cr.dictfetchall()
        self.service_demandeur = rows and rows[0]['service']

        cd_serv = rows and rows[0]['code']
        self.env.cr.execute("select no_code from hr_compteur_besoin where company_id = %d" %(x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = str(cd_serv) + '/' + ok
            vals = c1
            self.env.cr.execute("""INSERT INTO hr_compteur_besoin(company_id,no_code)  VALUES(%d , %d)""" %(x_struct_id,vals))    
        else:
            
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.name = str(cd_serv) + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE hr_compteur_besoin SET no_code = %d  WHERE company_id = %d" %(vals,x_struct_id))

    def action_eng_recep(self):
        self.write({'state': 'R'})
    
    #fonction de recuperation de l'année en cours
    @api.onchange('beneficiaire')
    def _annee_en_cours(self):
        vals = datetime.now()
        vals1 = vals.year
        #print('Value', vals1)
        # self.annee_besoin = vals1

class StockBesoinsAnnuelsLine(models.Model):
    _name = "stock_besoinannuel_line"

    x_besoin_id = fields.Many2one('stock_besoinannuel', ondelete='cascade')
    x_article_id = fields.Many2one('stock_article', string = 'Articles', required=True)
    unite_id = fields.Many2one("stock_unitestockage","Unité")
    qte_demandee = fields.Integer(string = 'Qté arbitrée')
    montant = fields.Integer(string='P.U')
    mnt_total = fields.Integer(string='Total', readonly=True)
    qtes = fields.Integer(string='Qté demandée')
    qte_read = fields.Integer(string='Qté affectée', readonly=True)
    
    #fonction pour controler ramener l'unité
    @api.onchange('x_article_id')
    def controler_qte_demande(self):
        for x in self:
            if x.x_article_id:
                x.unite_id = x.x_article_id.unite_stock_id

    @api.onchange('qte_demandee')
    def qte(self):
        for x in self:
            if x.qte_demandee:
                x.qte_read = x.qte_demandee

    @api.onchange('qtes', 'montant')
    def qte(self):
        for x in self:
            x.mnt_total = x.montant * x.qtes

class StockParamService(models.Model):
    _name = "stock_param_service"

    name = fields.Many2one('hr_service', string="Adressé à", required=True)
    state = fields.Boolean(default=False, string="Etat")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

 
#Classe pour gerer le compteur pour les besoins annuels
class Compteur_besoin(models.Model):
    _name = "hr_compteur_besoin"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()
       

#Class pour gerer la centralisation des besoins annuels de chaque service de chaque EPE                
class StockCentralisationBesoinsAnnuels(models.Model):
    
    _name = "central_besoinannuel"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]),string = 'Année', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Char(string="Code", size=50, readonly=True)
    annee_en_cours = fields.Many2one('ref_exercice', string='Année', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    x_line_ids = fields.One2many('central_besoinannuel_line', 'x_besoin_central_id',
                                 string='Liste Des Articles demandées')
    active = fields.Boolean(string="Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),('F', 'Fait'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')
    current_user = fields.Many2one('res.users','Utilisateur', default=lambda self: self.env.user)
    date_centralisation = fields.Date(string = "Date", default=date.today())
    service_traiteur = fields.Many2one('hr_service',string = "Adressé à", readonly = True,default=lambda self: self.env['hr_service'].search([('est_stock','=', 1)]))

    def action_eng_draft(self):
        self.write({'state': 'draft'})

    #fonction de remplissage du tableau
    def centraliser(self):
        if self.annee_en_cours:
            annee = int(self.x_exercice_id)
            x_struct_id = int(self.company_id)
            for vals in self:
                vals.env.cr.execute("""select (P.id) AS article, SUM(L.qtes) AS quantite from stock_article P, stock_besoinannuel S, stock_besoinannuel_line L where P.id = L.x_article_id and S.id = L.x_besoin_id and S.x_exercice_id = %s and S.state = 'R' and S.company_id = %s GROUP BY article""",(annee,x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []
                
                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'article': line['article'], 'qte_demandee':line['quantite']}))
                self.x_line_ids = result

            self.env.cr.execute("select no_code from stock_cpte_central_besoin where company_id = %d" %(x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'CTRL' + '/' + ok
                vals = c1
                self.env.cr.execute("""INSERT INTO stock_cpte_central_besoin(company_id,no_code)  VALUES(%d , %d)""" %(x_struct_id,vals))    
            else:
                
                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                self.name = 'CTRL' + '/' + ok
                vals = c1
                self.env.cr.execute("UPDATE stock_cpte_central_besoin SET no_code = %d  WHERE company_id = %d" %(vals,x_struct_id))
            
        self.write({'state': 'F'})
                

#class pour gerer les lignes de centralisation des besoins annuels   
class StockCentralisationBesoinsAnnuelsLine(models.Model):
    
    _name = "central_besoinannuel_line"
    x_besoin_central_id = fields.Many2one('central_besoinannuel', ondelete='cascade')
    article = fields.Many2one("stock_article",string = 'Article')
    qte_demandee = fields.Integer(string = 'Quantité demandée',readonly=True)
    qte = fields.Integer(string='Quantité arbitrée ')
    
    
#Classe pour gerer le compteur pour la centralisation des besoins annuels
class Compteur_Central_besoin(models.Model):
    _name = "stock_cpte_central_besoin"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


#Class pour gerer les demandes d'approvisionnement  de chaque service de chaque EPE                
class StockBesoinsApprovisionnement(models.Model):
    
    _name = "stock_besoinapprov"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    x_exercice_id = fields.Many2one('ref_exercice', default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]))
    company_id = fields.Many2one('res.company',string = "Structure", default=lambda self: self.env.user.company_id.id)
    
    name = fields.Char(string = "Numéro", size = 50, readonly = True)
    date_demande_approv = fields.Date(string = "Date Demande",default=date.today())
    beneficiaire = fields.Many2one('hr_service',string = "De", default=lambda self: self.env['hr_service'].search([('est_stock','=', '1')]))
     
    dotation = fields.Selection([
        ('ordinaire',"Dotation ordinaire"),
        ('urgence',"Dotation d'\'urgence"),   
        ], required = True,string = "Dotation")
    service_benef = fields.Many2one("hr.department",string = "Vers", readonly = True)
    
    responsable = fields.Char(string = "Responsable Stock", readonly = True)
    objet_approv = fields.Text(string = 'Observations')
    
    etat_besoin = fields.Selection([
        ('1', 'initial'), ('2', 'Recep'),
        ], string="Etat besoin")
    x_line_ids = fields.One2many('stock_besoinapprov_line', 'x_besoin_approv_id',
                                 string='Ajout Des Articles ', states = {'E': [('readonly', True)], 'A': [('readonly', True)]})
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    etat_sortie = fields.Char(default='Sortie')
    observation_reception = fields.Text()
    active = fields.Boolean(string="Etat", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('A', 'Rejeter'),
        ('E', 'Envoyer'),
        ('R', 'Receptionner'),
        ('D', 'Vérifier la disponibilité'),
        ('T', 'Traiter'),
        ('Re', 'Rejeter'),
        ('En', 'Fait'),
        ('S', 'Servi'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    #fonction pour remplir le responsable
    @api.onchange('dotation') 
    def remplir_champ(self):
        self.responsable = self.beneficiaire.responsable.name

    #fonction pour remplir le service à qui c'est adressé
    @api.onchange('dotation') 
    def remplir_champ1(self):
        x_struct_id = int(self.company_id)
        x_user_id = int(self.current_user)
        self.env.cr.execute("""select (R.id) AS service, (R.code) AS code From hr_department R, res_users U where R.id = U.direction_id and U.id = %d and U.company_id = %d""" %(x_user_id,x_struct_id))
        rows = self.env.cr.dictfetchall()
        self.service_benef = rows and rows[0]['service']
   
    #Les fonctions permettant de changer d'etat
    def action_eng_draft(self):
        self.write({'state': 'draft'})
    
    #fonction de recuperation du service de l'utilisateur connecté et changement d'etat
    def action_valider(self):
        x_struct_id = int(self.company_id)
        x_user_id = int(self.current_user)
        # self.env.cr.execute("""select (R.id) AS service, (R.code) AS code From hr_department R, res_users U where R.id = U.direction_id and U.id = %s and U.company_id = %s""",(x_user_id,x_struct_id))
        # rows = self.env.cr.dictfetchall()
        # self.service_traiteur = rows and rows[0]['service']
                        
        self.env.cr.execute("select no_code from stock_cpte_central_besoin where company_id = %d" %(x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'CTRL' + '/' + ok
            vals = c1
            self.env.cr.execute("""INSERT INTO stock_cpte_central_besoin(company_id,no_code)  VALUES(%d , %d)""" %(x_struct_id,vals))    
        else:
            
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.name = 'CTRL' + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE stock_cpte_central_besoin SET no_code = %d  WHERE company_id = %d" %(vals,x_struct_id))
        for record in self.x_line_ids:
            if record.qte_demandee <= 0:
                raise ValidationError(_('Veuillez saisir une quantitée supérieure ou égale à 1'))
        
        self.write({'state': 'V'})
    
    def action_rejet(self):
        self.write({'state': 'A'})

    def action_envoie(self):
        self.write({'state': 'E'})
    
    def action_recep(self):
        self.write({'state': 'R'})
    
    def action_verifier(self):
        for record in self.x_line_ids:
            val_id = int(record.x_article_id)
            record.env.cr.execute("""SELECT id,qte_article_en_stock from stock_article where id = %d""" %(val_id))
            for line in record.env.cr.dictfetchall():
                v_id = int(line['id'])
                qte = int(line['qte_article_en_stock'])
                self.env.cr.execute("""UPDATE stock_besoinapprov_line set qte_actuelle = %d WHERE x_article_id = %d""" %(qte,v_id))

        self.write({'state': 'D'})

    def action_traiter(self):
        for record in self.x_line_ids:
            val_id = int(record.x_article_id)
            val_qte = int(record.qte_octroye)
            record.env.cr.execute("""UPDATE stock_article set qte_article_en_stock = qte_article_en_stock - %d WHERE id in (%d)""" %(val_qte,val_id))
            if record.qte_octroye <= 0:
                raise ValidationError(_('Veuillez saisir une quantitée supérieure ou égale à 1'))
            if record.qte_octroye > record.qte_actuelle:
                raise ValidationError(_('Veuillez saisir une quantitée inférieure ou égale à la quantité disponible en stock svp'))
        
        self.write({'state': 'T'})

    def action_rejeter(self):
        self.write({'state': 'Re'})
    
    def action_boncommande(self):
        self.write({'state': 'En'})
 
 
class StockBesoinsApprovisionnementLine(models.Model):
    
    _name = "stock_besoinapprov_line"
    x_besoin_approv_id = fields.Many2one('stock_besoinapprov', ondelete='cascade')
    x_article_id = fields.Many2one('stock_article', string = 'Articles demandés', required=True)
    x_unite_id = fields.Many2one('stock_unitestockage', string = 'Unité', readonly=True)
    qte_demandee = fields.Integer(string = 'Quantité demandée', required=True)
    qte_actuelle = fields.Integer(string = 'Quantité disponible', readonly=True)
    qte_octroye = fields.Integer(string = 'Quantité accordée')
    observation_dde = fields.Text('Observations')
    id_stock = fields.Many2one("stock_cloture")

    @api.onchange("x_article_id")
    def Unite(self):
        for x in self:
            if x.x_article_id:
                x.x_unite_id = x.x_article_id.unite_stock_id


#classe mère de l'inventaire
class Stock_Inventaires(models.Model):
    
    _name = "stock_inventaires"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    name = fields.Char(string = 'Nom', required = True)
    x_date_debut = fields.Date(string='Date début', required=True)
    x_date_fin = fields.Date(string='Date fin', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('stock_inventaires_line', 'x_stock_inv_id', string="Articles et quantité en stock")
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_inv = fields.Date(string="Date", default=date.today())
    x_magasin_id = fields.Many2one('stock_magasinstockage', string='Magasin', required=True)

    # fonction de remplissage du tableau
    def valider(self):
        if self.x_date_debut and self.x_date_fin:
            ddbut = str(self.x_date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.x_date_fin.strftime("%Y-%m-%d"))
            x_struct_id = int(self.company_id)
            x_empl_id = int(self.x_magasin_id)
            for vals in self:
                vals.env.cr.execute(
                    """select (Ar.name) AS article, Ar.qte_article_en_stock AS quantite, (L.name) AS magasin   From stock_article Ar, stock_magasinstockage L where Ar.magasin_id = L.id  and L.id = %s and Ar.company_id = %s""",
                    (x_empl_id, x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'x_article': line['article'], 'x_qte': line['quantite']}))
                self.x_line_ids = result


class Stock_InventaireLine(models.Model):
    _name = "stock_inventaires_line"
    x_stock_inv_id = fields.Many2one('stock_inventaires')
    x_article = fields.Char(string='Article')
    x_qte = fields.Float(string='Quantité')


# classe mère de la preparation l'inventaire
class Stock_Preparation_Inventaires(models.Model):
    _name = "stock_inventairepreps"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    name = fields.Char(string='Numéro')
    date_inv = fields.Date(string="Date", default=date.today())
    x_periode = fields.Char(string='Période', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('stock_inventairepreps_line', 'x_stockprep_inv_id',
                                 string="Articles et quantité en stock", states={'Ap': [('readonly', True)]})
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    objet_inv = fields.Text(string='Objet')
    x_magasin_id = fields.Many2one('stock_magasinstockage', string='Magasin', required=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Valider'),
        ('Ap', 'Approuver'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # fonction de recuperation du service de l'utilisateur connecté et changement d'etat
    def action_valider(self):
        x_struct_id = int(self.company_id)

        self.env.cr.execute("select no_code from stock_cpte_fiche where company_id = %d" % (x_struct_id))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(4)
            self.name = 'FICH' + '/' + ok
            vals = c1
            self.env.cr.execute(
                """INSERT INTO stock_cpte_fiche(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
        else:
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(4)
            self.name = 'CTRL' + '/' + ok
            vals = c1
            self.env.cr.execute("UPDATE stock_cpte_fiche SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'V'})

    def action_ap(self):
        self.write({'state': 'Ap'})


class Stock_InventairesLine(models.Model):
    _name = "stock_inventairepreps_line"
    x_stockprep_inv_id = fields.Many2one('stock_inventairepreps')
    x_employe_id = fields.Many2one('stock_membre', string='Membre', required=True)
    x_service_id = fields.Char(string='Direction/Service', readonly=True)
    x_qualification = fields.Many2one('stock_qualifications', string='Qualification', required=True)

    # fonction pour remplir le service de l'employé selectionné
    @api.onchange('x_employe_id')
    def remplir_champ(self):
        self.x_service_id = self.x_employe_id.service


# Classe pour gerer le compteur pour la fiche d'inventaire
class Compteur_Fiche_Inventaire(models.Model):
    _name = "stock_cpte_fiche"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# classe mère du controle fiche inventaire
class Stock_Controle_Fiche_Inventaire(models.Model):
    _name = "stock_ficheinventaire"
    _order = 'sequence, id'
    _rec_name = 'x_magasin_id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of besoins annuels.", default=10)
    name = fields.Char(string='Numéro')
    date_fiche_invs = fields.Date(string="Date", default=date.today())
    # x_periode = fields.Char(string = 'Période', readonly = True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('stock_ficheinventaire_line', 'x_stockfiche_inv_id',
                                 string="Articles et quantité en stock")
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    # objet_fiche_inv = fields.Text(string = 'Objet', readonly = True)
    x_magasin_id = fields.Many2one('stock_magasinstockage', string='Magasin', required=True)

    x_line_p_ids = fields.One2many('stock_pointageinventaire_line', 'x_stockpoint_inv_id',string="Articles et quantité en stock")

    # fonction de remplissage du tableau
    def action_valider(self):
        x_mag_id = int(self.x_magasin_id)

        for vals in self:
            vals.env.cr.execute("""select DISTINCT(L.x_article_id) AS article, A.qte_article_en_stock AS quantite FROM stock_article A, stock_livraisonfourniture S, stock_livraisonfourniture_line L, stock_magasinstockage M 
                WHERE S.id = L.x_stock_id AND S.magasin_id = M.id AND A.id = L.x_article_id AND M.id = %d""" % (
                x_mag_id))
            rows = vals.env.cr.dictfetchall()
            result = []

            # delete old payslip lines
            vals.x_line_ids.unlink()
            for line in rows:
                result.append((0, 0, {'x_article_id': line['article'], 'qte_the': line['quantite']}))
            self.x_line_ids = result

    # fonction de remplissage du tableau
    def action_confront(self):
        x_mag_id = int(self.x_magasin_id)
        for vals in self:
            vals.env.cr.execute(
                """select DISTINCT(L.x_article_id) AS article, A.qte_article_en_stock AS quantite FROM stock_article A, stock_livraisonfourniture S, stock_livraisonfourniture_line L, stock_magasinstockage M 
                WHERE S.id = L.x_stock_id AND S.magasin_id = M.id AND A.id = L.x_article_id AND M.id = %d""" % (
                    x_mag_id))
            rows = vals.env.cr.dictfetchall()
            result = []

            # delete old payslip lines
            vals.x_line_p_ids.unlink()
            for line in rows:
                result.append((0, 0, {'x_article_id': line['article'], 'qte_the': line['quantite']}))
            self.x_line_p_ids = result

    # fonction de mise à niveau du stock
    def action_niveau(self):
        for record in self.x_line_p_ids:
            val_id = int(record.x_article_id)
            val_qte_ec = int(record.qte_phys)
            self.env.cr.execute("""UPDATE stock_article set qte_article_en_stock = %s WHERE id = %s""",(val_qte_ec, val_id))


# class controle et validation inventaire ligne pour le controle
class Stock_Controle_Fiche_InventaireLine(models.Model):
    _name = "stock_ficheinventaire_line"
    x_stockfiche_inv_id = fields.Many2one('stock_ficheinventaire')
    x_article_id = fields.Many2one('stock_article',string='Article', readonly=True)
    qte_the = fields.Integer(string='Quantité théorique', readonly=True)


# class controle et validation inventaire ligne pour le pointage
class Stock_Pointage_Fiche_InventaireLine(models.Model):
    _name = "stock_pointageinventaire_line"
    x_stockpoint_inv_id = fields.Many2one('stock_ficheinventaire')
    x_article_id = fields.Many2one('stock_article',string='Article', readonly=True)
    qte_the = fields.Integer(string='Quantité théorique', readonly=True)
    qte_phys = fields.Integer(string='Quantité physique')
    ecart_qte = fields.Integer(string='Ecart', readonly=True)
    observations = fields.Text(string='Observations')

    @api.onchange('qte_phys')
    def val_ecart(self):
        if self.qte_phys:
            self.ecart_qte = self.qte_phys - self.qte_the


# classe de mise en place de la commission
class MiseEnPlaceComission(models.Model):
    _name = 'stock_commission'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of preparation.", default=10)
    name = fields.Char('Code commission', readonly=True)
    date_mise_place = fields.Date('Date ', default=date.today())
    x_line_ids = fields.One2many('stock_commission_line', 'stock_com_id', string="Membres de la commission",
                                 states={'D': [('readonly', True)]})
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    obje_com = fields.Text('Objet', required=True)
    x_line_p_ids = fields.One2many('stock_destruction_line', 'stock_des_id', string="Articles à detruire",
                                   states={'D': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('D', 'Destruction effectuée'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # fonction de mise à niveau du stock quand on va actionner le bouton de destruction
    def action_valider(self):
        for record in self.x_line_p_ids:
            val_id = int(record.x_article_id)
            val_qte_destr = int(record.qte_des)
            record.env.cr.execute(
                """UPDATE stock_article set qte_article_en_stock = qte_article_en_stock - %d WHERE id = %d""" % (
                val_qte_destr, val_id))

            x_struct_id = int(self.company_id)
            self.env.cr.execute("select no_code from stock_cpte_com where company_id = %d" % (x_struct_id))
            lo = self.env.cr.fetchone()
            no_lo = lo and lo[0] or 0
            c1 = int(no_lo) + 1
            c = str(no_lo)
            if c == "0":
                ok = str(c1).zfill(4)
                self.name = 'COMM' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    """INSERT INTO stock_cpte_com(company_id,no_code)  VALUES(%d , %d)""" % (x_struct_id, vals))
            else:

                c1 = int(no_lo) + 1
                c = str(no_lo)
                ok = str(c1).zfill(4)
                self.name = 'COMM' + '/' + ok
                vals = c1
                self.env.cr.execute(
                    "UPDATE stock_cpte_com SET no_code = %d  WHERE company_id = %d" % (vals, x_struct_id))

        self.write({'state': 'D'})


# classe de mise en place de la commission line
class MiseEnPlaceComissionLine(models.Model):
    _name = 'stock_commission_line'
    stock_com_id = fields.Many2one('stock_commission')
    matricule = fields.Char('Matricule')
    nomprenom = fields.Many2one('stock_membre', string='Nom/Prénom(s)')
    tel = fields.Char('Email/Téléphone')
    email = fields.Char('Email')
    qualif = fields.Many2one('stock_qualifications', string='Qualification')
    service = fields.Char('Service')

    # fonction pour remplir le matricule,telephone,email,service de l'employé selectionné
    @api.onchange('nomprenom')
    def remplir_champ(self):
        self.service = self.nomprenom.service
        self.matricule = self.nomprenom.matricule
        self.tel = self.nomprenom.mail_tel



# Classe pour gerer le compteur pour la fiche d'inventaire
class Compteur_Commission_Destruction(models.Model):
    _name = "stock_cpte_com"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()


# class des articles à détruire
class ComissionDestructionLine(models.Model):
    _name = "stock_destruction_line"
    stock_des_id = fields.Many2one('stock_commission')
    x_article_id = fields.Many2one('stock_article', string='Article')
    qte_disponible = fields.Integer(string='Quantité disponible', readonly=True)
    qte_des = fields.Integer(string='Quantité à détruire')
    observations = fields.Text(string='Observations')

    # fonction pour remplir la qté disponible de l'article selectionné
    @api.onchange('x_article_id')
    def remplir_qte(self):
        self.qte_disponible = self.x_article_id.qte_article_en_stock


# classe mère du seuil de l'inventaire
class Stock_Seuil_Inventaire(models.Model):
    _name = "stock_seuil"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of seuil inventaire.", default=10)
    _rec_name = 'x_recherche'
    name = fields.Char(string='Numéro')
    x_recherche = fields.Selection([
        ('1', 'Globale'),
        ('2', "Groupe"),
        ('3', "Famille"),
        ('4', "En dessous du seuil"),
        ('5', "Magasin"),
    ], string="Rechercher par", default='1', required=True)
    x_groupe_id = fields.Many2one('stock_groupearticle', string='Groupe')
    x_famille_id = fields.Many2one('stock_famillearticle', string='Famille')
    x_sous_f_id = fields.Many2one('stock_sousfamille_article', string='Sous-Famille')
    x_magasin_id = fields.Many2one('stock_magasinstockage', string='Magasin')

    x_line_ids = fields.One2many('stock_seuil_line', 'x_stock_seuil_id', string="Articles")
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    """state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Recherche effectuée'),
        ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')"""

    # Les fonctions permettant de changer d'etat
    
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    # fonction de rechecrche
    def action_rech(self):
        if self.x_recherche:
            x_struct_id = int(self.company_id)
            x_grp_id = int(self.x_groupe_id)
            x_fa_id = int(self.x_famille_id)
            x_sf_id = int(self.x_sous_f_id)
            x_mag_id = int(self.x_magasin_id)
            for vals in self:
                if x_grp_id:
                    vals.env.cr.execute(
                        """select DISTINCT(Ar.name) AS article,(Ar.code_article) AS code, (Ar.qte_article_en_stock) AS quantite, (Ar.seuil_article) AS seuil From stock_article Ar, stock_groupearticle G where Ar.x_groupearticle_id = G.id  and G.id = %s and Ar.company_id = %s""",
                        (x_grp_id, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0,
                                       {'code': line['code'], 'designation': line['article'], 'seuil': line['seuil'],
                                        'qte': line['quantite']}))
                    self.x_line_ids = result
                    self.x_groupe_id = False
                elif x_fa_id:
                    vals.env.cr.execute(
                        """select DISTINCT(Ar.name) AS article,(Ar.code_article) AS code, (Ar.qte_article_en_stock) AS quantite, (Ar.seuil_article) AS seuil From stock_article Ar, stock_famillearticle F where Ar.x_famillearticle_id = F.id  and F.id = %s and Ar.company_id = %s""",
                        (x_fa_id, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0,
                                       {'code': line['code'], 'designation': line['article'], 'seuil': line['seuil'],
                                        'qte': line['quantite']}))
                    self.x_line_ids = result
                    self.x_famille_id = False


                elif x_mag_id:
                    vals.env.cr.execute(
                        """select DISTINCT(Ar.name) AS article,(Ar.code_article) AS code, (Ar.qte_article_en_stock) AS quantite, (Ar.seuil_article) AS seuil From stock_article Ar, stock_magasinstockage M where Ar.magasin_id = M.id  and M.id = %s and Ar.company_id = %s""",
                        (x_mag_id, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0,
                                       {'code': line['code'], 'designation': line['article'], 'seuil': line['seuil'],
                                        'qte': line['quantite']}))
                    self.x_line_ids = result
                    self.x_magasin_id = False
                elif self.x_recherche == '4':
                    vals.env.cr.execute( """select DISTINCT(Ar.name) AS article,(Ar.code_article) AS code, (Ar.qte_article_en_stock) AS quantite, (Ar.seuil_article) AS seuil 
                    From stock_article Ar where Ar.company_id = %s and Ar.qte_article_en_stock <= Ar.seuil_article order by code""" %(x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0,
                                       {'code': line['code'], 'designation': line['article'], 'seuil': line['seuil'],
                                        'qte': line['quantite']}))
                    self.x_line_ids = result

                else:
                    vals.env.cr.execute("""select DISTINCT(Ar.name) AS article,(Ar.code_article) AS code, (Ar.qte_article_en_stock) AS quantite, (Ar.seuil_article) AS seuil From stock_article Ar where Ar.company_id = %s""" % (x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()
                    for line in rows:
                        result.append((0, 0,
                                       {'code': line['code'], 'designation': line['article'], 'seuil': line['seuil'],
                                        'qte': line['quantite']}))
                    self.x_line_ids = result
            self.test()

    def test(self):
        v_id = int(self.id)
        v_struct = int(self.company_id)
        self.env.cr.execute("select code, qte, seuil from stock_seuil_line l, stock_seuil s where s.id = l.x_stock_seuil_id and l.x_stock_seuil_id = %d" %(v_id))
        for val in self.env.cr.dictfetchall():
            seuil = val['seuil']
            qte = val['qte']
            code = val['code']

            if qte <= seuil:
                self.env.cr.execute("update stock_seuil_line set state = '1' where code = %s and company_id = %s" ,(code, v_struct))
            else:
                self.env.cr.execute("update stock_seuil_line set state = '2' where code = %s and company_id = %s",(code, v_struct))
        # self.write({'state': 'R'})


class Stock_Seuil_Inventaireine(models.Model):
    _name = "stock_seuil_line"
    x_stock_seuil_id = fields.Many2one('stock_seuil', ondelete='cascade')
    code = fields.Char(string='Code')
    designation = fields.Char(string='Désignation')
    seuil = fields.Integer(string="Seuil d'\'arlerte")
    qte = fields.Integer('Quantité en stock')
    state = fields.Selection([('1','1'),('2','2')],string='etat')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    @api.onchange('seuil')
    def remplir_champ(self):
        for x in self:
            if x.qte <= x.seuil:
                x.state == '1'
            else:
                x.state == '2'


# classe mère de la fiche de stock
class Stock_Fiche(models.Model):
    _name = "stock_fiche"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of seuil inventaire.", default=10)
    _rec_name = 'x_recherche'
    name = fields.Char(string='Numéro')
    x_recherche = fields.Selection([
        ('1', 'Globale'),
        ('2', 'Article'),
        ('3', "Groupe"),
        ('4', "Famille"),
        ('6', "Magasin"),
    ], string="Rechercher par", default='1', required=True)
    x_article_id = fields.Many2one('stock_article', string='Article')
    x_groupe_id = fields.Many2one('stock_groupearticle', string='Groupe')
    x_famille_id = fields.Many2one('stock_famillearticle', string='Famille')
    x_sous_f_id = fields.Many2one('stock_sousfamille_article', string='Sous-Famille')
    x_magasin_id = fields.Many2one('stock_magasinstockage', string='Magasin')

    x_date_debut = fields.Date(string='Date début', required=True)
    x_date_fin = fields.Date(string='Date fin', required=True)

    x_line_ids = fields.One2many('stock_fiche_line', 'x_stock_fiche_id', string="Articles", readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)

    # Les fonctions permettant de changer d'etat

    # fonction de rechecrche
    def action_rech(self):
        if self.x_recherche:
            x_struct_id = int(self.company_id)
            x_grp_id = int(self.x_groupe_id)
            x_art_id = int(self.x_article_id)
            x_fa_id = int(self.x_famille_id)
            x_sf_id = int(self.x_sous_f_id)
            x_mag_id = int(self.x_magasin_id)
            ddbut = str(self.x_date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.x_date_fin.strftime("%Y-%m-%d"))
            for vals in self:
                if x_grp_id:
                    vals.env.cr.execute(
                        """SELECT L.* , (S.name) as article,(S.seuil_article) AS seuil,(S.code_article) AS code, (S.qte_article_en_stock) AS quantite, date(B.write_date) as date, (B.etat_sortie) as etat,(B.service_benef) as service_bene,(SE.name) as bene FROM stock_besoinapprov_line L, stock_besoinapprov B, stock_article S,hr_service SE, stock_groupearticle G WHERE L.x_besoin_approv_id = B.id  AND S.id = L.x_article_id  AND SE.id = B.beneficiaire AND S.x_groupearticle_id = G.id  and G.id = %s AND  date(B.write_date) BETWEEN %s AND %s AND B.company_id = %s AND B.state = 'En'""",
                        (x_grp_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()

                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_en_stock': line['quantite'],
                                              'qte_dispo': line['qte_actuelle'], 'qte_traite': line['qte_octroye'],
                                              'de_service': line['bene'], 'vers_service': line['service_bene'],
                                              'observation': line['observation_dde']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """SELECT L.*, (A.name) as article, (A.code_article) as code,(A.seuil_article) AS seuil, (F.fournisseur_id) as fournisseur, (F.etat_entree) as etat,(F.objet_livraison) as obs, date(F.write_date) as date FROM stock_livraisonfourniture_line L, stock_livraisonfourniture F, stock_article A, stock_groupearticle G WHERE L.x_stock_id = F.id AND A.id = L.x_article_id AND A.x_groupearticle_id = G.id  AND G.id = %s AND  date(F.write_date) BETWEEN %s AND %s AND F.company_id = %s AND F.state = 'V'""",
                        (x_grp_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []
                    # delete old payslip lines
                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_traite': line['qte_livre'],
                                              'fournisseur': line['fournisseur'], 'observation': line['obs']}))
                    self.x_line_ids = result

                    self.x_groupe_id = False

                elif x_fa_id:

                    vals.env.cr.execute(
                        """SELECT L.* , (S.name) as article,(S.seuil_article) AS seuil,(S.code_article) AS code, (S.qte_article_en_stock) AS quantite, date(B.write_date) as date, (B.etat_sortie) as etat,(B.service_benef) as service_bene,(SE.name) as bene FROM stock_besoinapprov_line L, stock_besoinapprov B, stock_article S,hr_service SE, stock_famillearticle F WHERE L.x_besoin_approv_id = B.id  AND S.id = L.x_article_id  AND SE.id = B.beneficiaire AND S.x_famillearticle_id = F.id AND F.id = %s AND  date(B.write_date) BETWEEN %s AND %s AND B.company_id = %s AND B.state = 'En'""",
                        (x_fa_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()

                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_en_stock': line['quantite'],
                                              'qte_dispo': line['qte_actuelle'], 'qte_traite': line['qte_octroye'],
                                              'de_service': line['bene'], 'vers_service': line['service_bene'],
                                              'observation': line['observation_dde']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """SELECT L.*, (A.name) as article, (A.code_article) as code,(A.seuil_article) AS seuil, (F.fournisseur_id) as fournisseur, (F.etat_entree) as etat,(F.objet_livraison) as obs, date(F.write_date) as date FROM stock_livraisonfourniture_line L, stock_livraisonfourniture F, stock_article A, stock_famillearticle FA WHERE L.x_stock_id = F.id AND A.id = L.x_article_id AND A.x_famillearticle_id = FA.id  and FA.id = %s AND  date(F.write_date) BETWEEN %s AND %s AND F.company_id = %s AND F.state = 'V'""",
                        (x_fa_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []
                    # delete old payslip lines
                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_traite': line['qte_livre'],
                                              'fournisseur': line['fournisseur'], 'observation': line['obs']}))
                    self.x_line_ids = result

                    self.x_famille_id = False


                elif x_mag_id:

                    vals.env.cr.execute(
                        """SELECT L.* , (S.name) as article,(S.seuil_article) AS seuil,(S.code_article) AS code, (S.qte_article_en_stock) AS quantite, date(B.write_date) as date, (B.etat_sortie) as etat,(B.service_benef) as service_bene,(SE.name) as bene FROM stock_besoinapprov_line L, stock_besoinapprov B, stock_article S,hr_service SE, stock_magasinstockage M WHERE L.x_besoin_approv_id = B.id  AND S.id = L.x_article_id  AND SE.id = B.beneficiaire AND S.magasin_id = M.id  and M.id = %s AND  date(B.write_date) BETWEEN %s AND %s AND B.company_id = %s AND B.state = 'En'""",
                        (x_mag_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()

                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_en_stock': line['quantite'],
                                              'qte_dispo': line['qte_actuelle'], 'qte_traite': line['qte_octroye'],
                                              'de_service': line['bene'], 'vers_service': line['service_bene'],
                                              'observation': line['observation_dde']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """SELECT L.*, (A.name) as article, (A.code_article) as code,(A.seuil_article) AS seuil, (F.fournisseur_id) as fournisseur, (F.etat_entree) as etat,(F.objet_livraison) as obs, date(F.write_date) as date FROM stock_livraisonfourniture_line L, stock_livraisonfourniture F, stock_article A, stock_magasinstockage M WHERE L.x_stock_id = F.id AND A.id = L.x_article_id AND A.magasin_id = M.id  and M.id = %s AND  date(F.write_date) BETWEEN %s AND %s AND F.company_id = %s AND F.state = 'V'""",
                        (x_mag_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []
                    # delete old payslip lines
                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_traite': line['qte_livre'],
                                              'fournisseur': line['fournisseur'], 'observation': line['obs']}))
                    self.x_line_ids = result

                    self.x_magasin_id = False

                elif x_art_id:

                    vals.env.cr.execute(
                        """SELECT L.* , (S.name) as article,(S.seuil_article) AS seuil,(S.code_article) AS code, (S.qte_article_en_stock) AS quantite, date(B.write_date) as date, (B.etat_sortie) as etat,(B.service_benef) as service_bene,(SE.name) as bene FROM stock_besoinapprov_line L, stock_besoinapprov B, stock_article S,hr_service SE WHERE L.x_besoin_approv_id = B.id  AND S.id = L.x_article_id  AND SE.id = B.beneficiaire AND S.id = %s AND  date(B.write_date) BETWEEN %s AND %s AND B.company_id = %s AND B.state = 'En'""",
                        (x_art_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()

                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_en_stock': line['quantite'],
                                              'qte_dispo': line['qte_actuelle'], 'qte_traite': line['qte_octroye'],
                                              'de_service': line['bene'], 'vers_service': line['service_bene'],
                                              'observation': line['observation_dde']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """SELECT L.*, (A.name) as article, (A.code_article) as code,(A.seuil_article) AS seuil, (F.fournisseur_id) as fournisseur, (F.etat_entree) as etat,(F.objet_livraison) as obs, date(F.write_date) as date FROM stock_livraisonfourniture_line L, stock_livraisonfourniture F, stock_article A, stock_famillearticle FA WHERE L.x_stock_id = F.id AND A.id = L.x_article_id AND A.id = %s AND  date(F.write_date) BETWEEN %s AND %s AND F.company_id = %s AND F.state = 'V'""",
                        (x_art_id, ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []
                    # delete old payslip lines
                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_traite': line['qte_livre'],
                                              'fournisseur': line['fournisseur'], 'observation': line['obs']}))
                    self.x_line_ids = result

                    self.x_article_id = False

                else:

                    vals.env.cr.execute(
                        """SELECT L.* , (S.name) as article,(S.seuil_article) AS seuil,(S.code_article) AS code, (S.qte_article_en_stock) AS quantite, date(B.write_date) as date, (B.etat_sortie) as etat,(B.service_benef) as service_bene,(SE.name) as bene FROM stock_besoinapprov_line L, stock_besoinapprov B, stock_article S,hr_service SE WHERE L.x_besoin_approv_id = B.id  AND S.id = L.x_article_id  AND SE.id = B.beneficiaire  AND  date(B.write_date) BETWEEN %s AND %s AND B.company_id = %s AND B.state = 'En'""",
                        (ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []

                    # delete old payslip lines
                    vals.x_line_ids.unlink()

                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_en_stock': line['quantite'],
                                              'qte_dispo': line['qte_actuelle'], 'qte_traite': line['qte_octroye'],
                                              'de_service': line['bene'], 'vers_service': line['service_bene'],
                                              'observation': line['observation_dde']}))
                    self.x_line_ids = result

                    vals.env.cr.execute(
                        """SELECT L.*, (A.name) as article, (A.code_article) as code,(A.seuil_article) AS seuil, (F.fournisseur_id) as fournisseur, (F.etat_entree) as etat,(F.objet_livraison) as obs, date(F.write_date) as date FROM stock_livraisonfourniture_line L, stock_livraisonfourniture F, stock_article A WHERE L.x_stock_id = F.id AND A.id = L.x_article_id  AND  date(F.write_date) BETWEEN %s AND %s AND F.company_id = %s AND F.state = 'V'""",
                        (ddbut, ddfin, x_struct_id))
                    rows = vals.env.cr.dictfetchall()
                    result = []
                    # delete old payslip lines
                    for line in rows:
                        result.append((0, 0, {'date_traitement': line['date'], 'code': line['code'],
                                              'designation': line['article'], 'seuil': line['seuil'],
                                              'etat': line['etat'], 'qte_traite': line['qte_livre'],
                                              'fournisseur': line['fournisseur'], 'observation': line['obs']}))
                    self.x_line_ids = result


class Stock_Fiche_Line(models.Model):
    _name = "stock_fiche_line"
    x_stock_fiche_id = fields.Many2one('stock_fiche')
    date_traitement = fields.Date('Date')
    code = fields.Char(string='Code')
    designation = fields.Char(string='Désignation')
    seuil = fields.Char(string="Seuil d'\'arlerte")
    etat = fields.Char('Etat')
    qte_en_stock = fields.Char('Quantité en stock')
    qte_dispo = fields.Char('Stock dispo')
    qte_traite = fields.Integer('Qté traitée')
    de_service = fields.Char('De')
    vers_service = fields.Char('Vers')
    fournisseur = fields.Many2one('ref_beneficiaire')
    observation = fields.Char('Observations')


class StockCloture(models.Model):
    _name = "stock_cloture"

    name = fields.Many2one("stock_besoinapprov", "Bon de sortie à clôturer", required=True, domain=([('state','=','En')]))
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('T', 'Traité'),('S', 'Servi'),], 'Etat', default='T', index=True, required=True, readonly=True)
    cloture_ids = fields.One2many("stock_besoinapprov_line","id_stock", readonly=True)
    dte = fields.Date(string="Date de clôture", default=date.today())

    @api.onchange('name')
    def Remplissage(self):
        if self.name:
            self.cloture_ids = self.name.x_line_ids


    def cloture(self):
        v_struct = int(self.company_id)
        v_id = int(self.name)

        self.env.cr.execute("""UPDATE stock_besoinapprov SET state = 'S' WHERE company_id = %d and id = %d""" %(v_struct, v_id))
        self.write({'state': 'S'})



class StockMembre(models.Model):
    _name = 'stock_membre'

    name = fields.Char("Nom & Prénom",required=True)
    service = fields.Char("Service",required=True)
    matricule = fields.Char("Matricule", required=False)
    mail_tel = fields.Char("Mail/Téléphone",required=True)
    active = fields.Boolean("Actif", default=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)


class StockFicheEntree(models.Model):
    _name = "stock_fiche_entree"

    name = fields.Char(string="Fiche initiale N°", required=True)
    x_date = fields.Date(string='Date ', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('draft', 'Nouveau'),('V', 'Validé'),], 'Etat', default='draft', index=True, required=True, readonly=True)
    fiche_ids = fields.One2many("stock_fiche_entree_line","fiche_id")

    def valider(self):

        v_id = int(self.id)
        v_struct = int(self.company_id)

        self.env.cr.execute("select * from stock_fiche_entree_line where company_id = %d and fiche_id = %d " % (v_struct, v_id))

        for val in self.env.cr.dictfetchall():
            v_art = val['name']
            v_str = val['company_id']
            v_qte = val['qte_article_en_stock']

            self.env.cr.execute("""update stock_article set qte_article_en_stock = qte_article_en_stock + %s where id = %s and company_id = %s""",(v_qte, v_art, v_str))

            self.write({'state': 'V'})

class StockFicheEntreeLine(models.Model):
    _name = "stock_fiche_entree_line"

    fiche_id = fields.Many2one("stock_fiche_entree", ondelete='cascade')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    name = fields.Many2one("stock_article",string="Article ", required=True)
    qte_article_en_stock = fields.Integer("Qté en stock", required=True)
    unite_stock_id = fields.Many2one('stock_unitestockage', string="Unité", readonly=True)

    @api.onchange("name")
    def unite(self):
        for x in self:
            if x.name:
                x.unite_stock_id = x.name.unite_stock_id
