{
    "name": "Gestion de Stock et Approvisionnement",
    "version": "1.0",
    "author": "TELIA INFORMATIQUE",
    "depends": ["base", "Referentiel_Global"],
    'images': ['static/description/stock.jpg'],
    "data":[
        "security/security.xml",
        "views/stock.xml",
        "Report/report_fiche_inventaire.xml",
        "Report/report_fiche_inventaire_qte.xml",
        "Report/report_fiche_pointage.xml",
        "Report/report_centralisation.xml",
        "Report/report_liste_participant.xml",
        "Report/report_besoin.xml",
        "Report/report_bon_sorties.xml",
        "Report/report_fiche.xml",
        "security/ir.model.access.csv"],
    "category": "EPE",
    "Summary": "Gestion de Stock et Approvisionnement des EPE",
    "installable": True,
    "auto_install": False,

}
