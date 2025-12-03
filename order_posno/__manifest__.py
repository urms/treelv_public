{
    'name': 'Positionsnr.',
    'version': '18.0.1.0.1',
    'category': 'TreElv',
    'summary': 'Fügt eindeutige Positionsnummer zu Verkaufsaufträgen hinzu',
    'description': """
Positionsnummer für Verkaufsaufträge
=====================================
Dieses Modul fügt ein Feld 'positionno' zu sale.order.line hinzu,
um immer eine eindeutige numerische Positionsnummer zu haben.
    """,
    'author': 'TreeLV',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/renumber_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/icon.svg'],

}
