{
    'name': 'First Eponge Custom Product',
    'version': '17.0.0.1',
    'description': '',
    'summary': '',
    'author': 'Line of Code',
    'website': 'lineofcode.org',
    'license': 'LGPL-3',
    'category': 'industry',
    'depends': [
        'base',
        'sale',
    ],
    "data": [
        "views/fe_confection_line_views.xml",
        "views/fe_confection_type_views.xml",
        "views/product_template_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
        'security/security.xml',
        "security/ir.model.access.csv",
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': True,
    'assets': {
        
    }
}