# See LICENSE file for full copyright and licensing details.

{
    'name': 'Gestion des formations',
    'version': '1.0',
    'author': 'Telia Informatique',
    'category': 'Gestion des formations',
    'Summary': 'Module de gestion des formations',
    'description': 'Gestion des formations',
    'images': ['static/description/formation.jpg'],
    'depends': ['base', 'Referentiel_Global', 'faarf_credit'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'views/donnee.xml',
             'views/formation.xml',
             'reports/formation.xml',
             ],
    'installable': True,
    'auto_install': False,
}
