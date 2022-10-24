{
    "name": "Gestion des Ressources Humaines",
    "version": "1.0",
    "author": "TELIA INFORMATIQUE",
    "depends":["Referentiel_Global","hr","hr_contract","payroll"],
    "data":[
        'security/security.xml',
        'security/restricted_company_rule.xml',
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/hr_employee.xml",
        "views/hr_employee_registre.xml",
        "views/hr_employee_indemnite.xml",
        "views/hr_contract.xml",
        "views/stage.xml",
        "views/conge.xml",
        "views/actes_administrative.xml",
        "views/menus.xml",
        "report/report_conge.xml",
        "report/report_abs.xml",
        "report/report_decret.xml",
        "report/report_planning.xml",
        "report/report_demande_conge.xml",
        "report/report_demande_autorisation_absence.xml",
        "report/report_actes_administratif.xml",
        "report/hr_employee_registre.xml",
        "data/data.xml",
    ],
    "category": "EPE",
    "Summary": "Gestion des Ressources Humaines",
    "installable": True,
    "auto_install": False,
    "application": True,
}