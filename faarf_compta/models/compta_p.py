from odoo import api, models, fields, _
from odoo.exceptions import ValidationError



class Compta_PCP(models.Model):
    _name = 'compta_prise_charge_p'
    _rec_name = 'date_pc'

    etat_mandat = fields.Selection([
        ('T', 'Tout'),
        ('W', 'Mandat Visé')
    ], 'Etat mandat', default='T')
    trier_par = fields.Selection([
        ('1', 'N° Ordre'),
        ('d', 'Date'),
    ], 'Trier par')
    numero_mandat = fields.Many2one("budg_mandat_b", "N° Mandat", domain=[('state', '=', 'I')])
    type_ecriture = fields.Many2one("compta_type_ecriture", 'Type ecriture',
                                    default=lambda self: self.env['compta_type_ecriture'].search(
                                        [('type_ecriture', '=', 'P')]))
    prise_charge_lines = fields.One2many("compta_prise_charge_line_p", "prise_charge_id",
                                         states={'P': [('readonly', True)]})
    type_operation = fields.Many2one("compta_type1_op_cpta", "Catégorie d'opération")
    type2_op = fields.Many2one("compta_reg_op_guichet_unique", "Nature d'opération")
    type1 = fields.Many2one("compta_operation_guichet", string="Catégorie d'opération", required=False)
    type2 = fields.Many2one("compta_type_op_cpta", string="Nature d'opération", domain="[('typebase_id','=',type1)]",
                            required=False)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")
    no_ecr = fields.Integer("N° Ecriture", readonly=True)
    date_pc = fields.Date("Date", default=fields.Date.context_today, readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Validé'),
        ('P', 'Provisoire'),
    ], 'Trier par')
    mnt_total = fields.Integer('Total')
    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

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

    def valider_pc(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        id_pc = self.id
        val_mandat = str(self.numero_mandat.no_mandat)

        self.env.cr.execute(
            "select count(etat) from compta_prise_charge_line_p where prise_charge_id = %d and etat = True" % (id_pc))
        et = self.env.cr.fetchone()
        etat = et and et[0] or 0

        if etat >= 1:

            self.env.cr.execute("""SELECT sum(montant)
            FROM compta_prise_charge_line_p WHERE company_id = %d AND prise_charge_id = %d and etat = True """ % (
            val_struct, id_pc))
            res = self.env.cr.fetchone()
            self.mnt_total = res and res[0] or 0
            val_mnt = self.mnt_total

            self.write({'state': 'V'})
        else:
            raise ValidationError(_("Aucune écriture à générer. Veuillez cocher au moins une ligne."))

    def remplir_prise(self):

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        val_mandat = str(self.numero_mandat.id)

        if self.numero_mandat and self.etat_mandat == 'W':
            for vals in self:
                vals.env.cr.execute("""SELECT m.no_eng as eng, m.no_mandat as mandat, l.no_lo as liq, 
                m.dt_etat as dt, m.mnt_ord as mnt, e.cpte_rub as debit, 
                r.souscpte as id_imput_debit, e.cpte_benef as credit, e.imput_benef as id_imput_credit
                from budg_mandat_p m, budg_engagement_p e,budg_param_rub_p br, budg_liqord_p l, compta_plan_lines r
                where m.no_eng = e.id and m.id = %s and r.id = br.cpte_id and 
                br.id = e.rubrique_id and m.no_lo = l.id and m.state = 'I' and m.company_id = %s and m.x_exercice_id = %s""",
                                    (val_mandat, val_struct, val_ex))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.prise_charge_lines.unlink()
                for line in rows:
                    result.append((0, 0, {'num_eng': line['eng'], 'num_liq': line['liq'], 'num_mandat': line['mandat'],
                                          'date_mandat': line['dt'], 'montant': line['mnt'], 'imp_deb': line['debit'],
                                          'id_imp_deb': line['id_imput_debit'], 'id_imp_cred': line['id_imput_credit'],
                                          'imp_cred': line['credit']}))
                self.prise_charge_lines = result
        elif self.etat_mandat == 'T':
            for vals in self:
                vals.env.cr.execute(""" SELECT distinct m.no_eng as eng, m.no_mandat as mandat, l.no_lo as liq, 
                m.dt_etat as dt, m.mnt_ord as mnt, e.cpte_rub as debit, 
                r.souscpte as id_imput_debit, e.cpte_benef as credit, e.imput_benef as id_imput_credit
                from budg_mandat_b m, budg_engagement_p e,budg_param_rub_p br, budg_liqord_p l, compta_plan_lines r
                where m.no_eng = e.no_eng and r.id = br.cpte_id and
                br.id = e.rubrique_id and m.no_lo = l.id and m.state = 'I' and m.company_id = %s and m.x_exercice_id = %s""",
                                    (val_struct, val_ex))
                rows = vals.env.cr.dictfetchall()
                result = []

                vals.prise_charge_lines.unlink()
                for line in rows:
                    result.append((0, 0, {'num_eng': line['eng'], 'num_liq': line['liq'], 'num_mandat': line['mandat'],
                                          'date_mandat': line['dt'], 'montant': line['mnt'], 'imp_deb': line['debit'],
                                          'id_imp_deb': line['id_imput_debit'], 'id_imp_cred': line['id_imput_credit'],
                                          'imp_cred': line['credit']}))
                self.prise_charge_lines = result

        self.write({'state': 'draft'})

    # Fonction compteur et génération des numéros des ecritures et des lignes d'ecritures

    def generer_ecriture_pc(self):

        self.write({'state': 'P'})

        val_ex = int(self.x_exercice_id)
        val_struct = int(self.company_id)
        id_pc = self.id
        val_date = str(self.date_pc)
        var_etat = 'P'
        var_sens = 'D'
        # val_mandat = str(self.numero_mandat.no_mandat)
        v_type = int(self.type_ecriture)

        # Attribution des numero et lignes d'ecritures pour l'enregistrement des cheques emis

        self.env.cr.execute(
            "select no_ecr,no_lecr from compta_compteur_ecr where x_exercice_id = %d and company_id = %d" % (
            val_ex, val_struct))
        noecr = self.env.cr.dictfetchall()
        no_ecrs = noecr and noecr[0]['no_ecr']
        no_ecrs1 = noecr and noecr[0]['no_lecr']
        no_ecr = no_ecrs

        if not (no_ecr):
            no_ecr = 1
            self.no_ecr = no_ecr
            no_ecrs1 = 1
            lecr = no_ecrs1
            self.env.cr.execute(
                "INSERT INTO compta_ecriture(no_ecr,dt_ecriture, type_ecriture, type_op ,x_exercice_id, company_id, state) VALUES (%s, %s, %s,'ID', %s, %s, 'P')",
                (no_ecr, val_date, v_type, val_ex, val_struct))

            self.env.cr.execute(
                """INSERT INTO compta_compteur_ecr(x_exercice_id,company_id,no_ecr,no_lecr) VALUES(%d, %d, %d,0)""" % (
                val_ex, val_struct, no_ecr))

            self.env.cr.execute(
                "select * from compta_prise_charge_line_p where company_id = %d and prise_charge_id = %d " % (
                val_struct, id_pc))

            for val in self.env.cr.dictfetchall():
                v_cred = val['id_imp_cred']
                var_cptesdebs = val['id_imp_deb']
                v_mnt = val['montant']
                # v_ex = val['x_exercice_id']
                v_str = val['company_id']
                etat = val['etat']
                v_etat = val['fg_etat']
                v_sens = val['fg_sens']
                val_mandat = val['num_mandat']

                self.env.cr.execute(
                    "select no_ecr,no_lecr from compta_compteur_ecr where x_exercice_id = %d and company_id = %d" % (
                    val_ex, v_str))
                noecr = self.env.cr.dictfetchall()
                no_ecrs = noecr and noecr[0]['no_ecr']
                no_ecrs1 = noecr and noecr[0]['no_lecr']

                no_ecr = no_ecrs
                no_ecrs1 = int(no_ecrs1)
                no_lecr = no_ecrs1 + 1

                if etat == True:
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture(no_ecr, no_lecr, no_souscptes, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens, fg_etat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                    no_ecr, no_lecr, var_cptesdebs, v_mnt, val_ex, v_str, val_date, var_sens, v_etat))

                    no_lecrs = no_lecr + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture(no_ecr, no_lecr, no_souscptes, mt_lecr, fg_sens, x_exercice_id, company_id, dt_ligne,fg_etat) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'P')""",
                                        (no_ecr, no_lecrs, v_cred, v_mnt, v_sens, val_ex, v_str, val_date))

                    self.env.cr.execute(
                        "UPDATE compta_compteur_ecr SET no_ecr = %d, no_lecr = %d WHERE no_ecr = %d and x_exercice_id = %d and company_id = %d" % (
                        no_ecr, no_lecrs, no_ecr, val_ex, v_str))

                    self.env.cr.execute(
                        "UPDATE budg_mandat SET state = 'E' WHERE no_mandat = %s and x_exercice_id = %s and company_id = %s",
                        (val_mandat, val_ex, v_str))

        else:
            no_ecr = no_ecr + 1
            self.no_ecr = no_ecr
            # no_ecrs1 = no_ecrs1 + 1
            # lecr = no_ecrs1

            self.env.cr.execute(
                "INSERT INTO compta_ecriture(no_ecr,dt_ecriture, type_ecriture, type_op ,x_exercice_id, company_id, state) VALUES (%s, %s, %s,'ID', %s, %s, 'P')",
                (no_ecr, val_date, v_type, val_ex, val_struct))

            self.env.cr.execute(
                "UPDATE compta_compteur_ecr SET no_ecr = %d WHERE x_exercice_id = %d and company_id = %d" % (
                no_ecr, val_ex, val_struct))

            self.env.cr.execute(
                "select * from compta_prise_charge_line where company_id = %d and prise_charge_id = %d " % (
                val_struct, id_pc))

            for val in self.env.cr.dictfetchall():
                v_cred = val['id_imp_cred']
                var_cptesdebs = val['id_imp_deb']
                v_mnt = val['montant']
                # v_ex = val['x_exercice_id']
                v_str = val['company_id']
                etat = val['etat']
                v_etat = val['fg_etat']
                v_sens = val['fg_sens']
                val_mandat = val['num_mandat']

                self.env.cr.execute(
                    "select no_ecr,no_lecr from compta_compteur_ecr where x_exercice_id = %d and company_id = %d" % (
                    val_ex, v_str))
                noecr = self.env.cr.dictfetchall()
                no_ecrs = noecr and noecr[0]['no_ecr']
                no_ecrs1 = noecr and noecr[0]['no_lecr']
                no_ecr = no_ecrs

                no_lecr = no_ecrs1 + 1

                if etat == True:
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture(no_ecr, no_lecr, no_souscptes, mt_lecr, x_exercice_id, company_id, dt_ligne, fg_sens, fg_etat) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                    no_ecr, no_lecr, var_cptesdebs, v_mnt, val_ex, v_str, val_date, var_sens, v_etat))

                    no_lecrs = no_lecr + 1
                    self.env.cr.execute("""INSERT INTO compta_ligne_ecriture(no_ecr, no_lecr, no_souscptes, mt_lecr, fg_sens, x_exercice_id, company_id, dt_ligne,fg_etat) 
                     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'P')""",
                                        (no_ecr, no_lecrs, v_cred, v_mnt, v_sens, val_ex, v_str, val_date))

                    self.env.cr.execute(
                        "UPDATE compta_compteur_ecr SET no_ecr = %d, no_lecr = %d WHERE no_ecr = %d and x_exercice_id = %d and company_id = %d" % (
                        no_ecr, no_lecrs, no_ecr, val_ex, v_str))

                    self.env.cr.execute(
                        "UPDATE budg_mandat SET state = 'E' WHERE no_mandat = %s and x_exercice_id = %s and company_id = %s",
                        (val_mandat, val_ex, v_str))


class Compta_PcLineP(models.Model):
    _name = "compta_prise_charge_line_p"

    no_ecr = fields.Integer()
    no_lecr = fields.Integer("N° Ligne", readonly=True)
    prise_charge_id = fields.Many2one("compta_prise_charge_p", ondelete='cascade')
    num_eng = fields.Char("N° Eng", readonly=True)
    num_liq = fields.Char("N° Liq", readonly=True)
    num_mandat = fields.Char("N° Mdt", readonly=True)
    imputation = fields.Char("Imputation", readonly=True)
    date_mandat = fields.Date("Date", readonly=True)
    montant = fields.Integer("Montant", readonly=True)
    imp_deb = fields.Char("Imput.Débit", readonly=True)
    id_imp_deb = fields.Integer("id Imput.Débit", readonly=True)
    imp_cred = fields.Char("Imput.Crédit", readonly=True)
    id_imp_cred = fields.Integer("id Imput.crédit", readonly=True)
    fg_sens = fields.Char(default='C')
    fg_etat = fields.Char(default='P')
    etat = fields.Boolean("OK", default=False)
    # active = fields.Boolean(string="Ok ?", default=False)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    # x_exercice_id = fields.Many2one("ref_exercice", default=lambda self: self.env['ref_exercice'].search([('etat','=', 1)]), string="Exercice")

    current_users = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    x_exercice_id = fields.Many2one("ref_exercice", string="Exercice")

    @api.onchange('current_users')
    def User(self):
        if self.current_users:
            self.x_exercice_id = self.current_users.x_exercice_id

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
