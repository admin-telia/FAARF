{
    "name": "Gestion de paie",
    "version": "1.0",
    "author": "TELIA INFORMATIQUE",
    "depends":["payroll"],
    "data":[
        'security/security.xml',
        'security/restricted_company_rule.xml',
        "security/ir.model.access.csv",
        "views/hr_paie.xml",
        "views/rappel_precompte.xml",
        "views/hr_avance_salaire.xml",
        "views/hr_etat_paie.xml",
        "views/etat_nominatif_paie.xml",
        "views/hr_etat_cotisation.xml",
        "views/vue_report_bulletin.xml",
        "report/report_etat_nominatif.xml",
        "report/report_bordereau_paie.xml",
        "views/menus.xml",
        "data/data.xml",
    ],
    "application": True,
    "category": "EPE",
    "Summary": "Gestion de paie",
    "installable": True,
    "auto_install": False,
}
