# See LICENSE file for full copyright and licensing details.

{
    'name': 'Gestion des conventions et partenariats',
    'version': '1.0',
    'author': 'Telia Informatique',
    'category': 'Gestion des conventions et partenariats',
    'Summary': 'Module de gestion des conventions et partenariats',
    'description': 'Gestion des conventions et partenariats',
    'depends': ['base', 'Referentiel_Global'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'views/partenaire.xml',
             'views/convention.xml',
             'reports/formation.xml',
             ],
    'installable': True,
    'auto_install': False,
}
